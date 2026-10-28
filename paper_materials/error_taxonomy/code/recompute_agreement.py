"""Recompute saved-label agreement without API access or third-party packages.

From the package root::

    python code/recompute_agreement.py
    python code/recompute_agreement.py --output recomputed_summary.json

The two CSV files contain canonical labels and a response audit ledger, not
original clinical questions or raw model replies. The audit checks recorded
parser candidates and recovery rules; it cannot independently extract those
candidates from withheld response text or establish clinical correctness. An
output file is written only after reference validation and is never overwritten.
Python 3.10 or later is required.
"""

import argparse
from collections import Counter
import csv
from itertools import combinations
import json
import math
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent.parent
RATERS = ("deepseek", "original_gpt", "claude", "gpt_repeat1", "gpt_repeat2")
LABEL_PATTERN = re.compile(r"([1-4])\s*-\s*([a-g](?:\s*,\s*[a-g])*)", re.I)
KEY_FIELDS = ("student_model", "stage", "source_id")
FLAG_FIELDS = tuple(
    f"deepseek_vs_{rater}_{metric}"
    for rater in RATERS[1:]
    for metric in ("paired", "primary", "subtype_exact", "both_axes")
)
REQUIRED_FIELDS = (*KEY_FIELDS, *RATERS, "common_all_five", *FLAG_FIELDS)
AUDIT_FIELDS = (
    *KEY_FIELDS, "rater", "raw_saved_label", "analysis_label",
    "recovered_from_response", "fenced_taxonomy_candidates", "finish_reason",
    "validation_issue", "response_model", "input_data_sha256", "explanation_sha256",
)


def parse_label(text):
    """Blank means missing; otherwise require one primary and a subtype set."""
    if not isinstance(text, str):
        raise ValueError("A label must be a CSV string")
    text = text.strip()
    if not text:
        return None
    match = LABEL_PATTERN.fullmatch(text)
    if match is None:
        raise ValueError(f"Invalid taxonomy label: {text!r}")
    subtypes = frozenset(re.split(r"\s*,\s*", match[2].lower()))
    return int(match[1]), subtypes


def check_flag(row, field, expected, location):
    actual = row[field]
    wanted = "" if expected is None else str(expected)
    if actual != wanted:
        raise ValueError(f"{location}: {field} is {actual!r}, expected {wanted!r}")


def case_key(row, location):
    if not row["student_model"].strip():
        raise ValueError(f"{location}: empty student_model")
    try:
        stage, source_id = int(row["stage"]), int(row["source_id"])
    except ValueError as exc:
        raise ValueError(f"{location}: stage/source_id must be integers") from exc
    if stage not in (0, 1, 2) or source_id < 0:
        raise ValueError(f"{location}: invalid stage/source_id")
    return row["student_model"].strip(), stage, source_id


def read_cases(path):
    """Validate composite identifiers and saved comparison flags, then parse."""
    cases = []
    seen = set()
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        fields = reader.fieldnames or []
        if len(fields) != len(set(fields)):
            raise ValueError("Duplicate CSV column names")
        missing = set(REQUIRED_FIELDS) - set(fields)
        if missing:
            raise ValueError(f"Missing CSV columns: {sorted(missing)}")
        for line, row in enumerate(reader, start=2):
            location = f"CSV line {line}"
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f"{location}: unexpected number of fields")
            key = case_key(row, location)
            if key in seen:
                raise ValueError(f"{location}: duplicate composite key {key}")
            seen.add(key)
            labels = {rater: parse_label(row[rater]) for rater in RATERS}
            common = all(label is not None for label in labels.values())
            check_flag(row, "common_all_five", common, location)
            left = labels["deepseek"]
            for rater in RATERS[1:]:
                right = labels[rater]
                paired = left is not None and right is not None
                prefix = f"deepseek_vs_{rater}_"
                check_flag(row, prefix + "paired", paired, location)
                expected = {
                    "primary": left[0] == right[0] if paired else None,
                    "subtype_exact": left[1] == right[1] if paired else None,
                    "both_axes": left == right if paired else None,
                }
                for metric, value in expected.items():
                    check_flag(row, prefix + metric, value, location)
            cases.append({**labels, "_key": key})
    if not cases:
        raise ValueError("No response instances in CSV")
    return cases


def recovered_label(rater, raw, candidates, finish_reason):
    """Apply only the historical GPT/Claude mechanical recovery rules."""
    if raw is not None:
        return raw
    allowed = rater == "original_gpt" or (rater == "claude" and finish_reason == "stop")
    return next(iter(candidates)) if allowed and len(candidates) == 1 else None


def read_audit(path, cases):
    """Match one record per case/rater and verify recorded recovery evidence."""
    main = {row["_key"]: row for row in cases}
    if len(main) != len(cases):
        raise ValueError("Duplicate composite keys in main cases")
    expected = {(key, rater) for key in main for rater in RATERS}
    seen = set()
    raw_cases = {key: {"_key": key} for key in main}
    recovered = {"original_gpt": 0, "claude": 0}
    input_hashes = {}
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        fields = reader.fieldnames or []
        if len(fields) != len(set(fields)):
            raise ValueError("Duplicate audit CSV column names")
        missing = set(AUDIT_FIELDS) - set(fields)
        if missing:
            raise ValueError(f"Missing audit CSV columns: {sorted(missing)}")
        for line, row in enumerate(reader, start=2):
            location = f"Audit CSV line {line}"
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f"{location}: unexpected number of fields")
            key, rater = case_key(row, location), row["rater"]
            identifier = key, rater
            if identifier not in expected:
                raise ValueError(f"{location}: unknown case/rater {identifier}")
            if identifier in seen:
                raise ValueError(f"{location}: duplicate case/rater {identifier}")
            seen.add(identifier)
            raw, analyzed = parse_label(row["raw_saved_label"]), parse_label(row["analysis_label"])
            candidate_text = row["fenced_taxonomy_candidates"].strip()
            candidates = {parse_label(value) for value in candidate_text.split(";")} if candidate_text else set()
            if None in candidates:
                raise ValueError(f"{location}: blank candidate in a nonempty candidate list")
            expected_label = recovered_label(rater, raw, candidates, row["finish_reason"])
            if analyzed != main[key][rater] or analyzed != expected_label:
                raise ValueError(f"{location}: analysis label conflicts with main CSV or recovery rule")
            was_recovered = raw is None and analyzed is not None
            check_flag(row, "recovered_from_response", was_recovered, location)
            if was_recovered:
                recovered[rater] += 1
            if rater != "original_gpt" and analyzed is not None and row["finish_reason"] != "stop":
                raise ValueError(f"{location}: valid modern label has a non-stop finish")
            for field in ("input_data_sha256", "explanation_sha256"):
                if re.fullmatch(r"[0-9a-f]{64}", row[field]) is None:
                    raise ValueError(f"{location}: invalid {field}")
            known_hash = input_hashes.setdefault(key, row["input_data_sha256"])
            if row["input_data_sha256"] != known_hash:
                raise ValueError(f"{location}: input hashes differ across raters")
            raw_cases[key][rater] = raw
    if seen != expected:
        raise ValueError(f"Audit CSV is missing {len(expected - seen)} case/rater records")
    return {
        "raw_cases": [raw_cases[row["_key"]] for row in cases],
        "recovered_labels": recovered,
        "record_count": len(seen),
    }


def distribution(labels):
    n = len(labels)
    primary = Counter(label[0] for label in labels)
    subtype = Counter(code for label in labels for code in label[1])
    return {
        "n": n,
        "primary_counts": {str(code): primary[code] for code in range(1, 5)},
        "primary_proportions": {
            str(code): primary[code] / n if n else None for code in range(1, 5)
        },
        "subtype_counts": {code: subtype[code] for code in "abcdefg"},
        "subtype_proportions": {
            code: subtype[code] / n if n else None for code in "abcdefg"
        },
    }


def agreement(left, right):
    """Nominal primary kappa and exact/overlap subtype statistics."""
    if len(left) != len(right):
        raise ValueError("Paired sequences have different lengths")
    n = len(left)
    matrix = [[0] * 4 for _ in range(4)]
    primary = subtype = joint = 0
    jaccards = []
    for first, second in zip(left, right):
        matrix[first[0] - 1][second[0] - 1] += 1
        primary += first[0] == second[0]
        subtype += first[1] == second[1]
        joint += first == second
        jaccards.append(len(first[1] & second[1]) / len(first[1] | second[1]))
    left_counts = Counter(label[0] for label in left)
    right_counts = Counter(label[0] for label in right)
    chance = sum(left_counts[code] * right_counts[code] for code in range(1, 5))
    denominator = n * n - chance
    kappa = (n * primary - chance) / denominator if denominator else None
    return {
        "n": n,
        "primary_match": primary,
        "primary_agreement": primary / n if n else None,
        "primary_kappa": kappa,
        "subtype_exact_match": subtype,
        "subtype_exact_agreement": subtype / n if n else None,
        "mean_subtype_jaccard": math.fsum(jaccards) / n if n else None,
        "both_axes_match": joint,
        "both_axes_agreement": joint / n if n else None,
        "confusion_rows_first_columns_second": matrix,
        "first_distribution": distribution(left),
        "second_distribution": distribution(right),
    }


def compare_pairs(cases):
    output = {}
    for first, second in combinations(RATERS, 2):
        paired = [row for row in cases if row[first] is not None and row[second] is not None]
        output[f"{first}_vs_{second}"] = agreement(
            [row[first] for row in paired], [row[second] for row in paired]
        )
    return output


def recompute(cases, audit=None):
    common = [row for row in cases if all(row[rater] is not None for rater in RATERS)]
    output = {
        "total": len(cases),
        "valid_counts": {
            rater: sum(row[rater] is not None for row in cases) for rater in RATERS
        },
        "pairwise_valid": compare_pairs(cases),
        "common_all_five_n": len(common),
        "common_all_five": compare_pairs(common),
        "common_all_five_distributions": {
            rater: distribution([row[rater] for row in common]) for rater in RATERS
        },
    }
    if audit is not None:
        output["raw_saved_labels_sensitivity"] = compare_pairs(audit["raw_cases"])
        output["previously_recovered_labels"] = audit["recovered_labels"]
    return output


def compare_value(actual, expected, location="summary", tolerance=1e-12):
    """Compare matching nested schemas; float comparisons use absolute tolerance."""
    if isinstance(actual, dict):
        if not isinstance(expected, dict) or actual.keys() != expected.keys():
            raise ValueError(f"{location}: different object keys")
        for key, value in actual.items():
            compare_value(value, expected[key], f"{location}.{key}", tolerance)
    elif isinstance(actual, list):
        if not isinstance(expected, list) or len(actual) != len(expected):
            raise ValueError(f"{location}: different array lengths")
        for index, (value, reference) in enumerate(zip(actual, expected)):
            compare_value(value, reference, f"{location}[{index}]", tolerance)
    elif isinstance(actual, float):
        if not isinstance(expected, (int, float)) or isinstance(expected, bool):
            raise ValueError(f"{location}: expected a number")
        if not math.isfinite(actual) or not math.isfinite(expected):
            raise ValueError(f"{location}: non-finite number")
        if not math.isclose(actual, expected, rel_tol=0.0, abs_tol=tolerance):
            raise ValueError(f"{location}: {actual!r} != {expected!r}")
    elif type(actual) is not type(expected) or actual != expected:
        raise ValueError(f"{location}: {actual!r} != {expected!r}")


def verify_against_reference(computed, reference):
    """Only CSV-reproducible summary fields are checked, not provenance claims."""
    for field, value in computed.items():
        if field not in reference:
            raise ValueError(f"Reference is missing {field}")
        compare_value(value, reference[field], field)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=ROOT / "data/per_case_comparison.csv")
    parser.add_argument("--audit", type=Path, default=ROOT / "data/record_audit.csv")
    parser.add_argument("--reference", type=Path, default=ROOT / "results/summary.json")
    parser.add_argument("--output", type=Path, help="New JSON path; existing files are refused")
    args = parser.parse_args(argv)
    try:
        if args.output and args.output.exists():
            raise FileExistsError(f"Output already exists: {args.output}")
        cases = read_cases(args.csv)
        audit = read_audit(args.audit, cases)
        computed = recompute(cases, audit)
        reference = json.loads(args.reference.read_text(encoding="utf-8"))
        verify_against_reference(computed, reference)
        if args.output:
            with args.output.open("x", encoding="utf-8", newline="\n") as stream:
                json.dump(computed, stream, ensure_ascii=False, indent=2, allow_nan=False)
                stream.write("\n")
    except (OSError, ValueError, KeyError) as exc:
        print(f"Verification failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({
        "status": "verified",
        "total": computed["total"],
        "valid_counts": computed["valid_counts"],
        "common_all_five_n": computed["common_all_five_n"],
        "pairwise_comparisons_verified": len(computed["pairwise_valid"]),
        "common_comparisons_verified": len(computed["common_all_five"]),
        "raw_saved_comparisons_verified": len(computed["raw_saved_labels_sensitivity"]),
        "audit_records_verified": audit["record_count"],
        "previously_recovered_labels": computed["previously_recovered_labels"],
        "absolute_float_tolerance": 1e-12,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
