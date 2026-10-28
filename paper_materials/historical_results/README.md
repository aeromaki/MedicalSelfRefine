# Historical Self-Refinement results

These are the 13 historical runs used in the original analysis, not new revision experiments. Each model JSON contains 300 question/answer instances and the stored initial and two refinement-stage results. The filenames use the saved model aliases; the separate `deepseek-r1` and `deepseek-r1-distill-70b` files must not be merged or treated as the same model.

Start with [accuracy_summary.csv](accuracy_summary.csv) for 39 model/stage summaries and [case_results.csv](case_results.csv) for 11,700 model/question/stage rows. Full responses and configuration are in the model JSONs. [file_manifest.json](file_manifest.json) maps each public file to its original `Result.zip/Result/SelfRefine/` member and records both hashes.

Eleven files are byte-identical to their original files. In HuatuoGPT-o1-70B (17 cases) and Meditron3-8B (9 cases), internal traceback strings were replaced with a short context-length failure description. Only `generations[index].output.error` changed; all other JSON values are equal. [transformations.csv](transformations.csv) lists the 26 changes. The generic message in the supplied public copy does not recover any unknown historical server setting. Source-text attribution is described in [DATA_SOURCES.md](../DATA_SOURCES.md).

## Reading case_results.csv

The key is `(model, question_index_0based, answer_stage)`. Stage 0 is the initial response; stages 1 and 2 are successive refinement positions. `stored_result` copies the original Boolean result array. `stored_prediction` may be empty because extraction failed or no output was available; it is not a new interpretation of the response.

| execution_status | Meaning |
|---|---|
| initial_response_saved | Initial response text is present |
| refiner_response_saved | New Refiner text is present at that stage |
| retained_at_stop_no_refiner_call | A Critic response triggered the original STOP rule; the answer was retained without Refiner output |
| carried_forward_after_previous_stop | Later Critic is absent and the stored answer was carried forward |
| generation_failed | The whole generation record contains an error instead of the normal output structure |

Stopped/carry-forward positions are not independent generated answers. For the 26 failed generation records, the original result arrays are false at all three stages; the CSV preserves those stored values and explicitly marks failure. The supplied accuracy_summary uses the original 300-question denominator and includes those stored failures; it is not a failure-excluded estimate. `new_answer_text_saved` and `critic_response_observed` distinguish actual generated text from retained state.
