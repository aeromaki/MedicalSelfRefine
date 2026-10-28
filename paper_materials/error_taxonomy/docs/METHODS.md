# Error-taxonomy reclassification: methods

## Scope and unit of analysis

This package documents reclassification of 3,309 archived medical question-answering response instances. It compares five saved sets of labels: historical GPT-4o-mini, two new GPT-4o-mini runs, Claude, and DeepSeek. The instances span 13 answer-generating models and three stages (0: initial answer; 1 and 2: successive refinements). An answer-generating model is distinct from the model that grades its error type. The same question can occur across models and stages; 3,309 instances do not represent 3,309 independent questions.

The reruns reused the `data` objects in the archived `Result/ErrorTypeClassification/label_2i_*.json` files. Each instance is matched by `(student_model, stage, source_id)`, equivalent to the original `(filename, stage, id)` key. Input equality, key uniqueness, journal-to-result equality, and prompt equality were checked before analysis. No previous taxonomy label or human rating was added to the classification input. Human workbook data are outside this package's analysis.

## Prompt and taxonomy

Each request comprised 14 messages: one system message, six user/assistant example pairs, and the current instance. The input template includes the question, options, supplied correct answer, extracted student answer (`prediction`), and student response. The prompt was held unchanged across the reruns, including its existing limitations.

The taxonomy requires one primary category (1–4) and one or more subtypes (a–g). The primary categories are basic medical knowledge, diagnosis, treatment/test suggestion, and other. The prompt asks for the earliest error in the physician's reasoning sequence and permits multiple subtypes. The exact instruction text and input template are in [instructions_only.json](../prompts/instructions_only.json); the category names are in [taxonomy.csv](../prompts/taxonomy.csv). This instruction-only file is an excerpt, not the full experimental prompt. The six examples are not duplicated in this subfolder. The existing repository [taxonomy prompt source](../../../vis/visbox/autolabel/prompt.json) is separate from this excerpt; the exact experimental prompt is identified by the hash below.

The full experimental prompt SHA-256 is `203b97f8e025f7ecb13b25aade5510ed716c6ebd414bbaf92f8ed4d20ba84b7c`. The source archive SHA-256 is `b71008903e5b40a004a6111516aff5deaaf4016652501db8cbf915d80822a5a7`. These hashes identify the original artifacts; they do not substitute for access to them.

## Model requests and execution

The following model identifiers are recorded request or response metadata, not independently established release or capability claims. Sanitized manifests are provided in [config](../config/).

| Run | Requested model | Observed response model | Request conditions |
|---|---|---|---|
| Historical GPT | Historical GPT-4o-mini designation | Exact snapshot not established | Historical sampling settings not established |
| GPT repeat 1 | `gpt-4o-mini` | `gpt-4o-mini-2024-07-18` | OpenAI; `max_tokens=8192`; concurrency 4 |
| GPT repeat 2 | `gpt-4o-mini-2024-07-18` | `gpt-4o-mini-2024-07-18` | OpenAI; `max_tokens=8192`; concurrency 4 |
| Claude | `claude-sonnet-5-5` | `claude-sonnet-5-5` | Anthropic endpoint via OpenAI-compatible Chat Completions; `max_tokens=8192`; concurrency 4 |
| DeepSeek | `deepseek/deepseek-v4.1-flash-1017` | `deepseek/deepseek-v4.1-flash-1017` | OpenRouter, pinned to DeepInfra `deepinfra/fp8`; `max_tokens=65536`; reasoning effort `high` |

Temperature and seed were not explicitly set in these reruns. Claude thinking was left at provider defaults. DeepSeek's output budget includes reasoning; its routing settings were `allow_fallbacks=false`, `require_parameters=true`, and `data_collection=deny`, with `X-OpenRouter-Metadata=enabled`. Its concurrency was reduced from 4 to 1 during rate-limit recovery; the final manifest records 1. Checkpointed instances were retained across restarts rather than deliberately reclassified.

All four reruns completed 3,309 saved responses. Completion times in UTC were 2026-10-20 04:13:38 (Claude), 2026-10-21 07:29:56 (GPT repeat 1), 2026-10-21 15:30:45 (GPT repeat 2), and 2026-10-26 09:04:52 (DeepSeek).

## Label parsing and exclusions

A valid taxonomy code has one primary number 1–4 and a nonempty subtype set a–g. Whitespace and case are normalized; subtype order and duplicates do not affect equality. The current parser examines fenced blocks and accepts a single distinct valid code; it does not choose among conflicting valid codes. For new runs, successful termination (`finish_reason=stop`) and the stored validation state are also required.

The initial historical/Claude extraction could miss a taxonomy code when an earlier fenced block contained an answer letter. A later mechanical reparse recovered six historical GPT labels and 72 Claude labels from unchanged response text. This was code extraction, not a new model call or manual reassignment of a category. For Claude, recovery was restricted to normally terminated responses. The saved manifests and raw response records remain unchanged; analysis labels are separate.

| Run | Total | Valid before the documented recovery | Recovered | Analysis-valid | Analysis-missing |
|---|---:|---:|---:|---:|---:|
| Historical GPT | 3,309 | 3,168 | 6 | 3,174 | 135 |
| GPT repeat 1 | 3,309 | 3,165 | 0 | 3,165 | 144 |
| GPT repeat 2 | 3,309 | 3,184 | 0 | 3,184 | 125 |
| Claude | 3,309 | 3,213 | 72 | 3,285 | 24 |
| DeepSeek | 3,309 | 3,231 | 0 | 3,231 | 78 |

“Valid” denotes code-format validity, not a clinically correct assessment. Missing labels are excluded from the relevant comparison denominator, not scored as disagreements or mapped to `4-g`. DeepSeek's 78 missing labels all terminated normally and expressed no error: 52 `No error`, 22 `None`, three `0 - none`, and one empty code block accompanied by no-error prose.

## Agreement analysis

[per_case_comparison.csv](../data/per_case_comparison.csv) contains all instance keys and analysis labels. [record_audit.csv](../data/record_audit.csv) distinguishes canonical raw saved labels from analysis labels and records recovery and validation evidence. Raw response prose is not included.

The analysis reports the ten unordered pairs among five label sets twice: first using each pair's available valid instances, and then using the same 2,908 instances valid in all five sets. These are 20 pair/cohort results, not 20 independent experiments. A further sensitivity analysis uses raw saved labels before the historical/Claude recovery.

For each comparison, the analysis computes:

- **Primary agreement:** equal primary category numbers.
- **Subtype exact agreement:** equality of the complete subtype sets, independently of primary category.
- **Both-axes agreement:** primary category and complete subtype set both equal.
- **Mean subtype Jaccard:** mean intersection size divided by union size across valid pairs.
- **Primary Cohen's κ:** unweighted agreement for nominal primary categories, adjusted for the two observed marginal distributions.

For example, `2-b,c` and `2-c,b` agree on both axes; `2-b,c` and `2-b` agree only on the primary category. Counts, denominators, distributions, and confusion matrices accompany the aggregate statistics. No confidence intervals or independence-based significance tests were calculated.

## Reproduction boundary

[recompute_agreement.py](../code/recompute_agreement.py) recomputes the agreement results from the included label tables without credentials, network access, or model calls. [summary.json](../results/summary.json) preserves the reported aggregate results. [source_files.json](../provenance/source_files.json) records source provenance.

The included code is a new standalone offline recalculation tool. It is not an execution-time snapshot of the historical API runners; notably, the shared taxonomy parser was improved after the initial Claude extraction. Exact historical dependency versions were not established. Offline agreement calculation uses Python's standard library.

This subfolder is self-contained for agreement recalculation, not for an end-to-end model rerun. It does not duplicate benchmark inputs, raw classifier response text, or the complete six-example prompt. Source-input and response hashes preserve traceability, but the omitted original grading responses are needed to independently repeat the original prose-to-code parsing audit. The wider repository contains separate task prompts and benchmark materials; those must not be confused with this taxonomy classifier's input format.
