# Data dictionary

All CSV files use UTF-8 with BOM for spreadsheet compatibility. Empty classifier cells mean unavailable/invalid classification, not category 0 or an agreement outcome. Files contain derived labels and metadata, not clinical case prose.

## Case identity

`student_model`, `stage`, `source_id` together identify an answer instance. The student model generated the answer being graded; it is distinct from the classifier/rater. Stage 0 is the initial answer, stages 1 and 2 are subsequent refinement stages. `source_id` is the ID stored in the archived result, not a guaranteed globally stable dataset identifier. Never join by spreadsheet row number or source ID alone.

`file` in the DeepSeek missingness table is the equivalent original filename `label_2i_{student_model}.json`. Question hashes can identify repeated question strings; they are not patient identifiers.

## `per_case_comparison.csv`

| Columns | Meaning |
|---|---|
| `deepseek`, `original_gpt`, `claude`, `gpt_repeat1`, `gpt_repeat2` | Analysis label such as `2 - a, d`, or empty |
| `common_all_five` | True only when all five labels are valid |
| `deepseek_issue` | Saved DeepSeek validation issue; empty when none |
| `deepseek_vs_*_paired` | Both labels valid in this comparison |
| `*_primary` | Same category 1–4; empty if not paired |
| `*_subtype_exact` | Same entire a–g set, independently of primary category |
| `*_both_axes` | Both primary and subtype set match |

Subtype order and duplicate letters do not change a label. `1 - b, c` and `1 - c, b` match; `1 - b` and `1 - b, c` do not exactly match. Original category names remain in English in `prompts/taxonomy.csv`.

## `record_audit.csv`

One row per case and rater, 16,545 total. `raw_saved_label` is the canonical form of the originally saved valid code, blank otherwise. It is not the complete raw response string. `analysis_label` is the final code used in the comparison. `recovered_from_response=True` identifies six historical GPT codes and 72 Claude codes mechanically recovered from saved prose.

`fenced_taxonomy_candidates` lists distinct valid code candidates found in fenced blocks, separated by semicolons. It contains only category codes, not arbitrary fenced text. This is an extracted audit representation, not the original response.

`finish_reason`, `validation_issue`, and `response_model` are saved metadata. `not_recorded` explicitly marks absent historical metadata. A recovered Claude record can retain its original `invalid_category` issue while having a valid analysis label; the issue field describes the original run.

`input_data_sha256` hashes UTF-8 JSON of the original complete `data` object with sorted keys, `ensure_ascii=False`, and separators `(',', ':')`. `explanation_sha256` hashes the UTF-8 explanation string without normalization. The full input and explanation are omitted.

## `input_audit.csv` and `deepseek_unclassified.csv`

Input audit has one row per case, `input_data_sha256`, `question_sha256` (UTF-8 question string, no normalization), and `prediction_is_none`. These flags preserve the input-quality issue without redistributing source prose.

The DeepSeek table has 78 rows. `raw_block_form` is a normalized missing-classification form (`no error`, `none`, `0 - none`, or `(empty)`). The final two flags test whether the last original answer block matches the supplied gold choice, first as a single letter and then allowing `A. option text`. They are mechanical string comparisons, not clinical judgments. A correct choice does not prove the accompanying reasoning is correct.

## Aggregate results

Agreement columns are proportions in [0,1], not percentages. `primary_kappa` is unweighted Cohen kappa on nominal categories 1–4. `mean_subtype_jaccard` averages intersection/union of the subtype sets. Confusion matrices have the first named classifier on rows, second on columns, category order 1,2,3,4.

`pairwise_valid` uses all available cases for each pair. `common_all_five` restricts every comparison to the same 2,908 cases. `raw_saved_labels_sensitivity` omits the 6+72 recovered labels by using original valid saved codes. These three cohorts generate 30 comparison rows in `agreement_tables.csv`.

Four `config` files preserve original manifest counts. Claude's original 3,213 valid codes become 3,285 in the analysis after recovery. This is documented processing, not an inconsistency or an edit to the source manifest.
