# Historical STOP analysis

This is a reanalysis of preserved historical Critic responses. It is not a new experiment with changed examples or a measure of model confidence. Read [stop_counts.csv](stop_counts.csv) for all 26 model/Critic-stage rows, [stop_examples.md](stop_examples.md) for marker distinctions, and the [171-case viewer](review_171.html) after downloading it locally for detailed screening evidence.

| Measure | Numerator | Denominator | Rate |
|---|---:|---:|---:|
| Original detector | 1,579 | 6,559 | 24.07% |
| Exact terminal marker | 1,408 | 6,559 | 21.47% |
| Terminal marker allowing whitespace and case differences | 1,416 | 6,559 | 21.59% |
| Original detector only | 171 | 6,559 | 2.61% |
| Whitespace/case-tolerant terminal marker only | 8 | 6,559 | 0.12% |

The denominator is Critic responses whose contents were saved and can be inspected at that stage. It is not all scheduled calls, all 300 questions, or the subset entering a stage with a correct answer. Consequently these format/detection rates are different from appropriate-stopping rates conditional on a correct entering answer.

CSV count columns are `observed`, `legacy`, `strict`, `relaxed`, `both`, `legacy_only`, and `relaxed_only`. `both` means original detection and relaxed terminal detection. Every `_rate` divides its corresponding numerator by that row's `observed` count, not by 300. Missing later Critic calls after stopping and failed generations do not enter `observed`. [counts_verification.json](counts_verification.json) records independent recalculation of every count column and the 171 response hashes.

## Review of the 171 original-detector-only records

The saved exploratory screening identified three strong feedback/STOP conflict candidates, one minor correction candidate, and 167 cases without an explicit decision reversal identified by that screen. No case was confirmed as a pure quotation/negation false stop. This does **not** establish zero errors or a 0% semantic false-positive rate. The screen was not independent blinded clinical adjudication. The unexecuted Refiner responses and their possible answer changes are unknown.

[review_171.csv](review_171.csv) provides keys, saved state, screening notes and text; [review_171.json](review_171.json) retains the full screening fields, including uncertainty and pending independent labels. The Korean notes are the original screening notes, not a new medical assessment. `index` is a zero-based question index. [review_summary.json](review_summary.json) preserves the original screening summary.
