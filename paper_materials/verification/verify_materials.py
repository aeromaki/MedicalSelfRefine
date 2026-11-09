"""Read-only checks of released data and Qwen scoring correction; no API calls."""
import argparse
from collections import Counter
import csv
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
COUNT_FIELDS = ("observed", "legacy", "strict", "relaxed", "both", "legacy_only", "relaxed_only")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def rows(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stop_flags(text):
    legacy = any(value in text.lower() for value in ("`stop`", "'stop'", '"stop"'))
    strict = bool(re.search(r"(?<!`)```STOP```\s*\Z", text))
    relaxed = bool(re.search(r"(?<!`)```\s*STOP\s*```\s*\Z", text, re.I))
    return dict(zip(COUNT_FIELDS, (1, int(legacy), int(strict), int(relaxed),
        int(legacy and relaxed), int(legacy and not relaxed), int(relaxed and not legacy))))


def unique(records, fields):
    result = {}
    for record in records:
        key = tuple(record[field] for field in fields)
        assert key not in result, ("duplicate key", fields, key)
        result[key] = record
    return result


def scored_predictions(model, generation):
    """Return rescored answers and correction counts without using answer keys.

    The original JSON predictions and results are validated independently in
    verify(). Qwen2.5-7B only: recover an exactly triple-fenced single answer
    when the original extractor recorded None; preserve old non-null answers.
    Carry forward a corrected response when a later Refiner was not invoked.
    """
    output = generation["output"]
    if "error" in output:
        return [None, None, None], Counter()
    predictions = [output["initial_prediction"]]
    correction_events = Counter()
    for iteration in output["iteration"]:
        raw = iteration["refiner_prediction"]
        corrected = raw
        if model == "qwen2.5-7b" and raw is None:
            response = iteration["refiner_response"]
            match = re.fullmatch(r"```([A-E])```", response) if isinstance(response, str) else None
            if match is not None:
                corrected = match.group(1)
                correction_events["recovered_exact_fenced_choice"] += 1
            elif response == "-" and len(predictions) > 1:
                corrected = predictions[-1]
                if corrected is not None:
                    correction_events["corrected_answer_carried_after_stop"] += 1
        predictions.append(corrected)
    assert len(predictions) == 3
    return predictions, correction_events


def verify():
    questions = read_json(ROOT / "medqa_300/questions.json")
    assert len(questions) == 300
    assert [q["index_zero_based"] for q in questions] == list(range(300))
    assert [q["question_id"] for q in questions] == [f"Q{i+1:03d}" for i in range(300)]
    question_csv = rows(ROOT / "medqa_300/questions.csv")
    assert len(question_csv) == 300
    for expected, actual in zip(questions, question_csv):
        for field in expected:
            value = actual[field]
            if field == "options":
                value = json.loads(value)
            elif field == "index_zero_based":
                value = int(value)
            assert value == expected[field], ("question CSV", expected["question_id"], field)

    manifest = read_json(ROOT / "historical_results/file_manifest.json")
    entries = manifest["files"]
    assert len(entries) == 13 and len({e["model"] for e in entries}) == 13
    tables = rows(ROOT / "historical_results/case_results.csv")
    cases = unique(tables, ("model", "question_index_0based", "answer_stage"))
    assert len(cases) == 11700
    scores = unique(rows(ROOT / "historical_results/accuracy_summary.csv"), ("model", "answer_stage"))
    assert len(scores) == 39
    counts, outputs, failed = {}, {}, Counter()
    correction_counts = Counter()
    changed_predictions = 0
    changed_correctness = 0
    for entry in entries:
        model = entry["model"]
        path = ROOT / "historical_results" / entry["public_file"]
        assert sha(path) == entry["public_sha256"], path.name
        data = read_json(path)
        generations = data["generations"]
        assert len(generations) == 300
        rescored_correct = [0, 0, 0]
        for step in (1, 2):
            counts[model, step] = Counter({field: 0 for field in COUNT_FIELDS})
        for index, generation in enumerate(generations):
            question = questions[index]
            assert generation["input"] == {"question": question["question"], "options": question["options"]}
            assert generation["label"] == question["answer_key"]
            output = generation["output"]
            failure = "error" in output
            failed[model] += int(failure)
            if failure:
                assert generation["result"] == [False, False, False]
                raw_predictions = [None, None, None]
            else:
                raw_predictions = [output["initial_prediction"]] + [v["refiner_prediction"] for v in output["iteration"]]
                assert len(raw_predictions) == 3
                assert [p == generation["label"] for p in raw_predictions] == generation["result"]
                stopped = False
                for step, iteration in enumerate(output["iteration"], 1):
                    critic = iteration["critic_response"]
                    if critic is None:
                        assert stopped
                        continue
                    assert not stopped
                    text = critic["response"]
                    flags = stop_flags(text)
                    counts[model, step].update(flags)
                    outputs[model, index, step] = text
                    stopped = bool(flags["legacy"])
                    assert (iteration["refiner_response"] == "-") == stopped
            predictions, changes = scored_predictions(model, generation)
            correction_counts.update(changes)
            rescored = [p == generation["label"] for p in predictions]
            for stage in range(3):
                rescored_correct[stage] += int(rescored[stage])
                changed_predictions += int(raw_predictions[stage] != predictions[stage])
                changed_correctness += int(generation["result"][stage] != rescored[stage])
                row = cases[model, str(index), str(stage)]
                assert row["question_id"] == question["question_id"] and row["gold_answer"] == generation["label"]
                assert row["stored_result"] == str(rescored[stage]), ("rescored result", model, index, stage)
                prediction, has_text, has_critic, detected = predictions[stage], False, False, False
                if failure:
                    status = "generation_failed"
                elif stage == 0:
                    has_text = bool(output["initial_response"])
                    status = "initial_response_saved" if has_text else "initial_response_missing"
                else:
                    iteration = output["iteration"][stage-1]
                    has_critic = iteration["critic_response"] is not None
                    detected = has_critic and bool(stop_flags(iteration["critic_response"]["response"])["legacy"])
                    has_text = iteration["refiner_response"] != "-"
                    status = "refiner_response_saved" if has_text else "retained_at_stop_no_refiner_call" if has_critic else "carried_forward_after_previous_stop"
                expected = {"stored_prediction": "" if prediction is None else str(prediction), "execution_status": status,
                    "new_answer_text_saved": str(has_text), "critic_response_observed": str(has_critic),
                    "legacy_stop_detected_at_this_step": str(detected), "source_file": model + ".json"}
                assert all(row[k] == v for k, v in expected.items()), ("case table", model, index, stage)
        for stage in range(3):
            original_correct = sum(g["result"][stage] for g in generations)
            assert math.isclose(original_correct / 300, data["final_score"][stage], abs_tol=1e-12)
            score = scores[model, str(stage)]
            assert int(score["scheduled_questions"]) == 300
            assert int(score["generation_failures"]) == failed[model]
            assert int(score["stored_correct_count"]) == rescored_correct[stage], ("score count", model, stage)
            assert math.isclose(float(score["stored_accuracy"]), rescored_correct[stage] / 300, abs_tol=1e-12)
            if model != "qwen2.5-7b":
                assert rescored_correct[stage] == original_correct
            else:
                assert rescored_correct[stage] == (167, 167, 166)[stage]
                assert original_correct == (167, 116, 111)[stage]
    assert sum(failed.values()) == 26
    assert changed_predictions == 210 and changed_correctness == 106, (changed_predictions, changed_correctness)
    assert correction_counts == Counter({"recovered_exact_fenced_choice": 209,
        "corrected_answer_carried_after_stop": 1}), correction_counts

    stop_table = unique(rows(ROOT / "stopping_analysis/stop_counts.csv"), ("model", "critic_step"))
    assert len(stop_table) == 26
    for (model, step), count in counts.items():
        row = stop_table[model, str(step)]
        for field in COUNT_FIELDS:
            assert int(row[field]) == count[field], ("STOP count", model, step, field)
            if field + "_rate" in row:
                assert math.isclose(float(row[field + "_rate"]), count[field] / count["observed"], abs_tol=1e-12)
    totals = {field: sum(c[field] for c in counts.values()) for field in COUNT_FIELDS}
    assert list(totals.values()) == [6559, 1579, 1408, 1416, 1408, 171, 8]
    reviews = read_json(ROOT / "stopping_analysis/review_171.json")
    review_keys = unique(reviews, ("model", "index", "critic_step"))
    expected_keys = {key for key, text in outputs.items() if stop_flags(text)["legacy_only"]}
    assert len(review_keys) == 171 and set(review_keys) == expected_keys
    for key, record in review_keys.items():
        assert record["text"] == outputs[key]
        assert hashlib.sha256(record["text"].encode("utf-8")).hexdigest() == record["text_sha256"]
    review_csv = rows(ROOT / "stopping_analysis/review_171.csv")
    assert len(unique(review_csv, ("model", "index", "critic_step"))) == 171
    for row in review_csv:
        record = review_keys[row["model"], int(row["index"]), int(row["critic_step"])]
        assert row["text"] == record["text"] and row["text_sha256"] == record["text_sha256"]

    prompts = read_json(ROOT / "prompts/full_prompts.json")
    prompt_counts = {role: len(value["examples"]) for role, value in prompts.items()}
    assert prompt_counts == {"solver": 8, "critic": 2, "refiner": 2, "extractor": 5}
    assert sha(ROOT / "prompts/full_prompts.json") == read_json(ROOT / "prompts/provenance.json")["source_sha256"]
    assert all(not stop_flags(example["output"])["legacy"] for example in prompts["critic"]["examples"])
    catalog = rows(ROOT / "model_information/model_catalog.csv")
    assert len(catalog) == 13 and {r["result_alias"] for r in catalog} == {e["model"] for e in entries}
    task = subprocess.run([sys.executable, "-I", "-B", str(ROOT / "error_taxonomy/code/recompute_agreement.py")],
        capture_output=True, text=True, encoding="utf-8")
    assert task.returncode == 0, task.stderr
    taxonomy = json.loads(task.stdout)
    checksums = ROOT / "verification/SHA256SUMS.txt"
    if checksums.exists():
        for line in checksums.read_text(encoding="utf-8").splitlines():
            expected, relative = line.split("  ", 1)
            target = (ROOT / relative).resolve()
            assert target.is_relative_to(ROOT.resolve()) and sha(target) == expected, relative
    return {"status": "verified", "historical_models": len(entries), "questions": len(questions),
        "historical_case_stage_rows": len(cases), "accuracy_rows": len(scores), "failed_generation_records": sum(failed.values()),
        "qwen2_5_7b_scoring_changes": {"predictions": changed_predictions, "correctness": changed_correctness,
            "recovered_from_fenced_responses": correction_counts["recovered_exact_fenced_choice"],
            "carried_forward_after_STOP": correction_counts["corrected_answer_carried_after_stop"]},
        "STOP_model_stage_rows": len(counts), "STOP_totals": totals, "review_records_matched_to_responses": len(reviews),
        "prompt_examples": prompt_counts, "model_catalog_rows": len(catalog), "taxonomy": taxonomy,
        "scope": "Offline file/table consistency, including Qwen answer-extraction correction; no model generation, remote dataset request, or clinical adjudication."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Optional new report file; existing files are refused")
    args = parser.parse_args()
    if args.output and args.output.exists():
        parser.error("Output already exists")
    result = verify()
    content = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        with args.output.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
    print(content, end="")


if __name__ == "__main__":
    main()
