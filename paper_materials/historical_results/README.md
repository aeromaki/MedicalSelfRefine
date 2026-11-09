# Historical Self-Refinement results

These are the 13 historical runs used in the original analysis, not new revision experiments. Each model JSON contains 300 question/answer instances and the saved initial and two refinement-stage results. The filenames use the saved model aliases; `deepseek-r1` and `deepseek-r1-distill-70b` are separate models.

Start with [accuracy_summary.csv](accuracy_summary.csv) for 39 model/stage summaries and [case_results.csv](case_results.csv) for 11,700 model/question/answer-stage rows. The model JSON files preserve the original responses, predictions, correctness arrays, and execution records. [file_manifest.json](file_manifest.json) maps each public JSON file to its original `Result.zip/Result/SelfRefine/` archive member and records the source/public hashes.

**Scoring update (7 November 2026):** `accuracy_summary.csv` and `case_results.csv` reflect a corrected answer-extraction pass for **Qwen2.5-7B**. No model was rerun. The original Qwen JSON, including its saved predictions and `result`/`final_score` arrays, was **not changed**. For all other 12 models, the CSV prediction and scoring fields are unchanged from the archived records. See [Qwen2.5-7B correction](#qwen25-7b-answer-extraction-correction) below.

Eleven model JSON files are byte-identical to the supplied historical files. For HuatuoGPT-o1-70B (17 cases) and Meditron3-8B (9 cases), internal traceback strings were replaced with a short context-length failure description. Only `generations[index].output.error` changed; all other JSON values were preserved. [transformations.csv](transformations.csv) lists these 26 replacements. The generic descriptions do not recover unknown historical server settings. Source-text attribution is described in [DATA_SOURCES.md](../DATA_SOURCES.md).

## Reading case_results.csv

The key is `(model, question_index_0based, answer_stage)`. Stage 0 is the initial response; stages 1 and 2 are subsequent answer positions after the first and second Critic--Refiner opportunities. This yields 13 x 300 x 3 = **11,700 rows**, not 11,700 independent generated responses.

The column names `stored_prediction` and `stored_result` were retained for compatibility with the original CSV schema. **For Qwen2.5-7B only, the entries at stages 1 and 2 can differ from the predictions and correctness values stored in the unmodified model JSON, because these CSV entries reflect corrected answer extraction.** For all other models and for Qwen2.5-7B stage 0, they retain their archived values. `stored_result` is a Boolean correctness indicator based on the relevant CSV prediction and the reference answer; a missing or invalid prediction is scored incorrect.

| execution_status | Meaning |
|---|---|
| initial_response_saved | Initial Solver text is present |
| refiner_response_saved | New Refiner text is present at that stage |
| retained_at_stop_no_refiner_call | A Critic response triggered the original STOP rule; no subsequent Refiner output was generated |
| carried_forward_after_previous_stop | The later Critic was not run and the previous answer was retained |
| generation_failed | The generation record contains an error in place of normal output |

Stopped/carry-forward positions are retained answer states, not independent generated answers. The 26 failed generation records remain incorrect at all three positions, are labeled `generation_failed`, and are **not** excluded from the 300-item accuracy denominator. `new_answer_text_saved` and `critic_response_observed` distinguish actual generation from retained states. STOP detection/format analysis is provided separately in [stopping_analysis](../stopping_analysis/README.md).

## Qwen2.5-7B answer-extraction correction

The archived Qwen2.5-7B result file contains Refiner outputs with an unambiguous answer written **solely as a single triple-backticked A--E letter**, such as `` ```C``` ``, for which the original extraction stored no prediction. The correction recovered that single letter *from the already saved response text*, without consulting the answer key. When an early STOP left no new Refiner output, the latest corrected prediction was carried forward to the retained answer state where applicable.

- **209** missing predictions were recovered from exact single-choice fenced Refiner responses; **one** further prediction was carried forward after STOP.
- **210** Qwen2.5-7B CSV answer-position predictions changed, of which **106** changed the recorded correctness status.
- The other models, all initial Solver answers, the execution/STOP statuses, and all original model JSON files were unchanged.

| Qwen2.5-7B answer position | Archived JSON correct / 300 | Rescored CSV correct / 300 |
|---|---:|---:|
| Initial (stage 0) | 167 | 167 |
| After first refinement (stage 1) | 116 | 167 |
| Final (stage 2) | 111 | 166 |

`accuracy_summary.csv` uses the same `stored_correct_count` and `stored_accuracy` column names for backward compatibility; its Qwen2.5-7B rows at stages 1 and 2 now represent **rescored** accuracy rather than the unmodified `final_score` stored in the raw JSON. These are scoring corrections, not additional model generations or retrospective answer selection based on the gold labels.

To verify the revised tables, use the updated [offline verification script](../verification/verify_materials.py). For Qwen2.5-7B, the verifier independently reconstructs these corrections from the saved response strings; for all other models it requires the original stored predictions and correctness arrays to match the CSVs.
