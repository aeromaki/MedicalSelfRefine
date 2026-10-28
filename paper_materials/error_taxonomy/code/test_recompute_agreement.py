"""Synthetic tests: python -m unittest discover -s code -p 'test_*.py'."""

import csv
import io
import unittest
from unittest.mock import patch

from recompute_agreement import (
    AUDIT_FIELDS, RATERS, REQUIRED_FIELDS, agreement, compare_value, parse_label,
    read_audit, read_cases, recompute,
)


def csv_row(source_id=0, **overrides):
    row = {"student_model": "synthetic", "stage": "0", "source_id": str(source_id)}
    row.update({rater: "1 - a" for rater in RATERS})
    row.update(overrides)
    labels = {rater: parse_label(row[rater]) for rater in RATERS}
    row["common_all_five"] = str(all(value is not None for value in labels.values()))
    first = labels["deepseek"]
    for rater in RATERS[1:]:
        second = labels[rater]
        paired = first is not None and second is not None
        prefix = f"deepseek_vs_{rater}_"
        row[prefix + "paired"] = str(paired)
        row[prefix + "primary"] = str(first[0] == second[0]) if paired else ""
        row[prefix + "subtype_exact"] = str(first[1] == second[1]) if paired else ""
        row[prefix + "both_axes"] = str(first == second) if paired else ""
    return row


def audit_rows(cases):
    rows = []
    for case in cases:
        student, stage, source = case["_key"]
        for rater in RATERS:
            label = case[rater]
            text = f"{label[0]} - {', '.join(sorted(label[1]))}" if label is not None else ""
            rows.append({
                "student_model": student, "stage": str(stage), "source_id": str(source),
                "rater": rater, "raw_saved_label": text, "analysis_label": text,
                "recovered_from_response": "False", "fenced_taxonomy_candidates": text,
                "finish_reason": "not_recorded" if rater == "original_gpt" else "stop",
                "validation_issue": "", "response_model": "synthetic",
                "input_data_sha256": "a" * 64, "explanation_sha256": "b" * 64,
            })
    return rows


class AgreementTests(unittest.TestCase):
    def read_csv(self, rows, fields, reader):
        stream = io.StringIO(newline="")
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
        stream.seek(0)
        with patch("recompute_agreement.Path.open", return_value=stream):
            return reader("synthetic.csv")

    def read_rows(self, rows):
        return self.read_csv(rows, REQUIRED_FIELDS, read_cases)

    def read_audit_rows(self, rows, cases):
        return self.read_csv(rows, AUDIT_FIELDS, lambda path: read_audit(path, cases))

    def test_order_and_duplicates_are_sets(self):
        self.assertEqual(parse_label(" 2 - C, b, c "), parse_label("2-b,c"))
        self.assertIsNone(parse_label("  "))

    def test_malformed_labels_do_not_become_missing(self):
        for text in ("No error", "0-a", "1-h", "1-", "1-a; b", "1-a trailing", "1-a,"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_label(text)

    def test_overlap_is_not_exact_and_axes_are_independent(self):
        first = [parse_label("1-a,b"), parse_label("1-c")]
        second = [parse_label("1-a"), parse_label("2-c")]
        result = agreement(first, second)
        self.assertEqual(result["primary_match"], 1)
        self.assertEqual(result["subtype_exact_match"], 1)
        self.assertEqual(result["both_axes_match"], 0)
        self.assertEqual(result["mean_subtype_jaccard"], 0.75)
        self.assertEqual(result["primary_kappa"], 0.0)
        self.assertEqual(result["confusion_rows_first_columns_second"][0], [1, 1, 0, 0])

    def test_degenerate_kappa_is_null(self):
        labels = [parse_label("1-a")] * 2
        result = agreement(labels, labels)
        self.assertEqual(result["primary_agreement"], 1.0)
        self.assertIsNone(result["primary_kappa"])

    def test_zero_pairs_report_null_rates(self):
        result = agreement([], [])
        self.assertEqual(result["n"], 0)
        self.assertIsNone(result["primary_agreement"])
        self.assertIsNone(result["primary_kappa"])

    def test_duplicate_composite_key_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate composite key"):
            self.read_rows([csv_row(), csv_row()])

    def test_same_source_id_in_different_stage_is_valid(self):
        self.assertEqual(len(self.read_rows([csv_row(), csv_row(stage="1")])), 2)

    def test_missing_labels_change_pairwise_and_common_denominators(self):
        cases = self.read_rows([
            csv_row(0), csv_row(1, original_gpt=""), csv_row(2, deepseek=""),
        ])
        result = recompute(cases)
        self.assertEqual(result["total"], 3)
        self.assertEqual(result["valid_counts"]["deepseek"], 2)
        self.assertEqual(result["valid_counts"]["claude"], 3)
        self.assertEqual(result["pairwise_valid"]["deepseek_vs_original_gpt"]["n"], 1)
        self.assertEqual(result["pairwise_valid"]["deepseek_vs_claude"]["n"], 2)
        self.assertEqual(result["pairwise_valid"]["claude_vs_gpt_repeat1"]["n"], 3)
        self.assertEqual(result["common_all_five_n"], 1)
        self.assertTrue(all(value["n"] == 1 for value in result["common_all_five"].values()))

    def test_incorrect_saved_match_flag_is_rejected(self):
        row = csv_row()
        row["deepseek_vs_claude_both_axes"] = "False"
        with self.assertRaisesRegex(ValueError, "both_axes"):
            self.read_rows([row])

    def test_unpaired_metric_must_be_blank(self):
        row = csv_row(claude="")
        row["deepseek_vs_claude_primary"] = "False"
        with self.assertRaisesRegex(ValueError, "primary"):
            self.read_rows([row])

    def test_incorrect_common_flag_is_rejected(self):
        row = csv_row()
        row["common_all_five"] = "False"
        with self.assertRaisesRegex(ValueError, "common_all_five"):
            self.read_rows([row])

    def test_recursive_reference_check_rejects_changed_counts_and_float_drift(self):
        compare_value({"rates": [0.2], "n": 1}, {"rates": [0.2 + 1e-13], "n": 1})
        with self.assertRaises(ValueError):
            compare_value({"rates": [0.2]}, {"rates": [0.2 + 1e-8]})
        with self.assertRaises(ValueError):
            compare_value({"n": 1}, {"n": 2})
        with self.assertRaises(ValueError):
            compare_value(0.2, float("nan"))

    def test_audit_recovery_and_raw_sensitivity_are_separate(self):
        cases = self.read_rows([csv_row()])
        rows = audit_rows(cases)
        for row in rows:
            if row["rater"] in ("original_gpt", "claude"):
                row["raw_saved_label"] = ""
                row["recovered_from_response"] = "True"
        audit = self.read_audit_rows(rows, cases)
        self.assertEqual(audit["record_count"], 5)
        self.assertEqual(audit["recovered_labels"], {"original_gpt": 1, "claude": 1})
        result = recompute(cases, audit)
        self.assertEqual(result["pairwise_valid"]["deepseek_vs_original_gpt"]["n"], 1)
        self.assertEqual(result["raw_saved_labels_sensitivity"]["deepseek_vs_original_gpt"]["n"], 0)
        self.assertEqual(result["raw_saved_labels_sensitivity"]["deepseek_vs_gpt_repeat1"]["n"], 1)

    def test_claude_nonstop_candidate_is_not_recovered(self):
        cases = self.read_rows([csv_row(claude="")])
        rows = audit_rows(cases)
        row = next(row for row in rows if row["rater"] == "claude")
        row["finish_reason"] = "content_filter"
        row["fenced_taxonomy_candidates"] = "1 - a"
        audit = self.read_audit_rows(rows, cases)
        self.assertEqual(audit["recovered_labels"]["claude"], 0)

    def test_conflicting_candidates_do_not_recover_blank_raw_label(self):
        cases = self.read_rows([csv_row(original_gpt="")])
        rows = audit_rows(cases)
        row = next(row for row in rows if row["rater"] == "original_gpt")
        row["fenced_taxonomy_candidates"] = "1 - a;2 - b"
        audit = self.read_audit_rows(rows, cases)
        self.assertEqual(audit["recovered_labels"]["original_gpt"], 0)

    def test_existing_raw_label_is_preserved_despite_conflicting_candidates(self):
        cases = self.read_rows([csv_row()])
        rows = audit_rows(cases)
        row = next(row for row in rows if row["rater"] == "original_gpt")
        row["fenced_taxonomy_candidates"] = "1 - a;2 - b"
        audit = self.read_audit_rows(rows, cases)
        self.assertEqual(audit["raw_cases"][0]["original_gpt"], parse_label("1 - a"))

    def test_duplicate_and_missing_audit_rows_are_rejected(self):
        cases = self.read_rows([csv_row()])
        rows = audit_rows(cases)
        with self.assertRaisesRegex(ValueError, "duplicate case/rater"):
            self.read_audit_rows([*rows, rows[0]], cases)
        with self.assertRaisesRegex(ValueError, "missing 1 case/rater"):
            self.read_audit_rows(rows[:-1], cases)

    def test_inconsistent_audit_label_and_recovery_flag_are_rejected(self):
        cases = self.read_rows([csv_row()])
        rows = audit_rows(cases)
        rows[0]["analysis_label"] = "2 - b"
        with self.assertRaisesRegex(ValueError, "analysis label conflicts"):
            self.read_audit_rows(rows, cases)
        rows = audit_rows(cases)
        rows[0]["recovered_from_response"] = "True"
        with self.assertRaisesRegex(ValueError, "recovered_from_response"):
            self.read_audit_rows(rows, cases)

    def test_audit_input_hashes_must_agree_across_raters(self):
        cases = self.read_rows([csv_row()])
        rows = audit_rows(cases)
        rows[-1]["input_data_sha256"] = "c" * 64
        with self.assertRaisesRegex(ValueError, "input hashes differ"):
            self.read_audit_rows(rows, cases)


if __name__ == "__main__":
    unittest.main()
