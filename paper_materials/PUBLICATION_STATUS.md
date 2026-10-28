# Scope of the initial materials release

This release contains the supplied historical results, full role prompts, the selected 300-question list, historical STOP reanalysis and completed five-run error-taxonomy label analysis. It is not the final response to every revision comment.

| Item | Status |
|---|---|
| Historical 13-model Self-Refinement outputs | Included; 26 traceback-string substitutions documented, other values preserved |
| Full Solver/Critic/Refiner/answer-extractor prompts | Included with 8/2/2/5 examples, respectively |
| MedQA selection, answers and later dataset comparison | Included; historical dataset commit remains unknown |
| STOP detector/format analysis and 171-case screen | Included as historical-output reanalysis; no independent semantic false-positive estimate |
| Completed GPT/Claude/DeepSeek taxonomy classifications | Included as derived codes, audit metadata and offline comparison code; full grading prose is omitted |
| Comment 9 final repeated-generation results and dispersion | Not included; not available in the supplied materials and not inferred from restart logs |
| Fully established model identity/weight revision/environment table | Partial evidence included; unknown entries explicitly marked |
| Runnable, credential-free model deployment configuration | Not claimed; templates illustrate structure, with remaining identity/serving requirements stated |
| Human A/B ratings | Not included in this initial release |
| Editor/reviewer response letters | Not included; old drafts are not presented as current final responses |
| API credentials, real environment files, internal logs | Excluded |

Recorded deployment identifiers are evidence of returned/requested strings, not proof of release histories or capability rankings. Researcher-confirmed vLLM 0.9.2/BF16 and revision plans are distinguished from settings recoverable from historical files. `max_model_len` is a context limit; it is not the output `max_tokens` setting.

Existing experiment code is outside the changes made for this materials release. New verification tools only read the released artifacts. See [source notices](DATA_SOURCES.md) for attribution and license-scope uncertainty rather than assuming one license covers every included component.
