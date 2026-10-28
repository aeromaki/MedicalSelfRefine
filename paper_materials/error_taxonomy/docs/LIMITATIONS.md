# Interpretation and limitations

These results measure consistency between saved error-type classifications. They do not establish classification accuracy, rank the models by clinical correctness, or identify an adjudicated human reference standard. The included analysis contains no human-workbook merge.

## Inputs and classification criteria

The reruns intentionally reused the archived inputs and prompt. The existing input audit found 526 instances with `prediction=None` and 32 nonempty predictions outside A–E. In 105 instances, the entire student response was a single fenced choice matching the supplied correct answer while `prediction` was missing. These are mechanical comparisons with the supplied answer, not fresh clinical adjudications.

An upstream extraction defect was reproduced: a compiled regular expression passed `re.DOTALL` as the second argument to `findall`, where it is interpreted as a starting position, while the compiled expression itself lacked the flag needed to match newlines inside a code block. The workflow also had an LLM fallback. Consequently, the reproduced defect does not by itself prove the cause of every historical missing prediction. Some archived responses also departed from the question's scenario; selected examples establish their presence but not their prevalence.

The prompt assumes the student's answer is incorrect and provides no explicit no-error, insufficient-evidence, or absent-reasoning category. Its first example also describes a diagnostic issue while assigning primary category 1, basic medical knowledge. Boundaries between knowledge, diagnostic, and overlapping subtype errors can admit different interpretations. Neither these inputs nor the examples were corrected for this experiment. Model variability, input quality, and criterion ambiguity therefore cannot be separated causally by the observed agreement rates.

## Models and sampling

The two new GPT runs returned the same dated model identifier and used identical reconstructed inputs and request settings. Temperature and seed were unspecified, however, and matching identifiers do not establish identical backend execution. The historical GPT snapshot and sampling conditions are unknown. Cross-model comparisons also differ in provider, reasoning settings, and output budget; they are not a controlled test in which model identity is the only changed implementation condition.

Recorded model names describe the saved request/response metadata. The package does not independently verify their release histories, relative capabilities, or continued endpoint availability. DeepSeek rate-limit recovery changed concurrency and elapsed execution time. Saved complete instances were reused during recovery, and the final manifest's concurrency of 1 does not describe every earlier request.

## Missing labels and metric choice

Invalid codes, no-error outputs, and non-normal completions are not interchangeable outcomes. They are excluded from the relevant agreement denominator and remain separately documented. In particular, DeepSeek's 78 missing taxonomy labels were normally completed responses, not unresolved API failures. All 78 had a final student-answer choice matching the supplied answer when a choice letter followed by option text was allowed; this string-based finding is not proof that every associated explanation was medically sound.

The common-case analysis excludes every instance invalid in any of the five label sets. Its 2,908 instances are therefore a selected subset. Pairwise-valid comparisons retain more instances but have different denominators. Both are reported, together with the raw-saved-label sensitivity analysis, so that exclusion and parser-recovery choices remain visible.

Complete subtype-set agreement is strict: adding or removing a single subtype creates disagreement. Primary agreement, subtype agreement, both-axes agreement, and Jaccard similarity answer different questions. High primary agreement must not be presented as full taxonomy reproducibility. Cohen's κ also reflects the marginal category distributions; it is not an accuracy score.

The same question appears across answer-generating models and refinement stages. The instances are not independent observations. No independence-based confidence intervals, significance tests, or causal effect estimates are supplied.

## Evidence and access

Source-key matching, equality of saved input objects, prompt-byte equality, journal/result correspondence, and unchanged baseline hashes were checked. These checks address file provenance and mechanical correspondence; they are not a full human review of the semantic appropriateness of every response. Reconstructed message arrays were compared, but actual HTTP request bodies were not separately captured.

The shared taxonomy parser was improved after the initial Claude run. Execution-time source versions and historical dependency locks are not fully recoverable from the available records. This subfolder can reproduce its agreement tables from included labels but does not include raw classifier response prose or duplicate benchmark material and the six prompt examples. Readers cannot independently reparse the original grading prose or perform an end-to-end classification rerun from these files alone. The existing repository taxonomy prompt source is linked in METHODS.md and identified by its experimental hash.

These findings support reporting the observed instability and its methodological context. They do not quantify how much disagreement each limitation caused.
