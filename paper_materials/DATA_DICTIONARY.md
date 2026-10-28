# Reading the files

CSV is UTF-8 (with a BOM where helpful for Excel); JSON is UTF-8. Each subsection has its own README. A missing answer, a skipped model call, an execution failure and an incorrect saved answer are different states.

## Shared question identity

The MedQA subset uses `index_zero_based` / `question_index_0based` 0–299 and reading IDs `Q001`–`Q300`, where the numeric ID is the index plus one. These identify positions in the retained subset, not a claim about a universal MedQA ID. Questions are selected consecutively; there was no random item-selection seed.

Each historical model has 300 generation records. Model aliases name saved result files; aliases do not by themselves resolve a model repository or weight revision. Consult the model catalog. In particular, `deepseek-r1` and `deepseek-r1-distill-70b` are separate saved model identities.

## Historical answers and scores

The key in `historical_results/case_results.csv` is `(model, question_index_0based, answer_stage)`. Stage 0 is initial, stages 1 and 2 are stored refinement positions. This produces 13 × 300 × 3 = 11,700 rows, not 11,700 independent model calls.

`stored_prediction` and `stored_result` preserve the archived extracted choice and correctness value. `execution_status`, `new_answer_text_saved` and `critic_response_observed` distinguish generation from answer retention after STOP and whole-record failure. The original 26 failed records retain their saved false results; no answer or counterfactual refinement is invented.

`accuracy_summary.csv` has 39 model/stage rows, with the original denominator of 300. Failure-excluded accuracy would be a different analysis. Model JSONs preserve the original configuration, scores and output structure; provenance records the 26 substitutions in the error-message strings.

## STOP counts

The key is `(model, critic_step)` with steps 1 and 2. `observed` is the number of inspectable saved Critic responses in that group. `legacy` means detected by the original rule, `strict` means the exact ending marker, and `relaxed` permits whitespace/case variation inside an ending marker. `both` is legacy and relaxed, `legacy_only` is legacy without relaxed, and `relaxed_only` is relaxed without legacy. Rate columns divide by `observed`.

These denominators differ from appropriate-stopping conditional on entering with a correct answer. Later unentered stages and unavailable failed outputs are not inspectable responses. Screening fields in the 171-case table express exploratory judgments and uncertainty; they are not independent clinical ground truth.

## Error taxonomy

The key is `(student_model, stage, source_id)`; this is a different table from the 11,700 historical positions. It contains the 3,309 archived answer instances selected for taxonomy classification. Use the composite key, not spreadsheet position. `student_model` generated the answer being assessed; the five classifier columns identify the graders.

Canonical codes contain one primary category 1–4 and a complete nonempty subtype set a–g. Empty classifier cells mean unavailable classification. The [taxonomy data dictionary](error_taxonomy/docs/DATA_DICTIONARY.md) explains raw-code recovery, missingness, response/input hashes, comparison flags and metrics. Agreement measures consistency, not accuracy.

## Model evidence

An explicit archival value, a reconstructed client default, a researcher statement, a revision plan and an unverified field are separate evidence categories. Unspecified request parameters are not numeric zero or known server defaults. Context and output limits remain distinct fields.

## Formats

Markdown explains the interpretation; CSV exposes tabular values; JSON retains structured source detail. `summary_tables.xlsx` is a reading copy of selected tables generated from the same sources. The HTML review viewer is for downloading and opening in a browser; GitHub's ordinary file view displays its source.
