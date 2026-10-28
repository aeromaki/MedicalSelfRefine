# MedicalSelfRefine: paper materials

[한국어 안내](README_KO.md) · [Summary workbook](summary_tables.xlsx) · [Data dictionary](DATA_DICTIONARY.md) · [Sources and notices](DATA_SOURCES.md)

This initial materials release, assembled on **28 October 2026**, separates the historical Self-Refinement experiment, reanalysis of its saved outputs, and subsequent error-taxonomy reclassification. It accompanies the existing code without changing that code or launching new model requests.

## Start here

| Question | Read | Download / reuse |
|---|---|---|
| What instructions and examples did each role receive? | [Full prompts and message assembly](prompts/README.md) | [Prompt JSON](prompts/full_prompts.json) |
| Which MedQA questions were evaluated? | [Selection and source](medqa_300/selection_and_source.md) | [300 questions and answers](medqa_300/questions.csv), [JSON](medqa_300/questions.json) |
| What did the original 13-model experiment produce? | [Historical results](historical_results/README.md) | [Accuracy by model/stage](historical_results/accuracy_summary.csv), [case results](historical_results/case_results.csv), model JSONs |
| How did the saved STOP markers compare with the original detector? | [STOP analysis](stopping_analysis/README.md) | [26 model/stage counts](stopping_analysis/stop_counts.csv), [171-case review](stopping_analysis/review_171.csv) |
| How reproducible were error-type labels? | [Error taxonomy](error_taxonomy/README.md) | [3,309 case labels](error_taxonomy/data/per_case_comparison.csv), [30 agreement comparisons](error_taxonomy/results/agreement_tables.csv) |
| Which model settings are established or still unknown? | [Model information](model_information/README.md) | [Model catalog](model_information/model_catalog.csv) |
| How can the supplied tables be checked? | [Verification guide](verification/README.md) | [Offline verifier](verification/verify_materials.py), [verification results](verification/verification_results.json) |

The workbook is a convenient reading copy of selected tables. CSV/JSON files are the calculation and provenance sources. Model output files contain long text, so start with the summaries and use the case identifiers to locate individual examples.

## Three different kinds of evidence

1. **Historical experiment:** 13 model files, each with 300 questions and initial/two refinement-position outcomes. Stopped positions may retain an earlier answer; they are not all newly generated responses.
2. **Historical-output reanalysis:** STOP format/detector counts and exploratory screening of 171 cases. The prompt and execution have not been rerun for this analysis.
3. **Error-taxonomy reclassification:** saved historical GPT labels plus two GPT-4o-mini reruns, Claude and DeepSeek labels on 3,309 archived answer instances. This is distinct from the repeated answer-generation experiment requested in Comment 9.

The historical source is `Result.zip/Result/SelfRefine/`. The two supplied public-material archives are not treated as separate experiments. Eleven released model files are byte-identical to this source. In two files, 26 internal error tracebacks were replaced with the supplied public failure description; all other JSON values match. [File provenance](historical_results/file_manifest.json) and [the change list](historical_results/transformations.csv) record that distinction.

## Revision comment map

| Comment | Available evidence | Boundary |
|---|---|---|
| 1: prompts and stopping | Solver 8, Critic 2, Refiner 2 and answer-extractor 5 examples; 6,559 inspected Critic responses | The two Critic examples both continue refinement. STOP counts do not establish confidence or a semantic false-positive rate. |
| 9: repeatability / dispersion | Historical request-setting reconstruction and documented revision plans | Final greedy/repeated-generation results and dispersion are **not included**. This release does not establish the live status of experiments elsewhere. |
| 10: model identity / environment | Saved request IDs, configuration evidence, separate researcher-reported settings, explicit unknown fields | Historical weight commits/context and some identities remain unverified. Configuration endpoints and researcher recollections are distinct evidence. |
| 11: item selection / contamination | MedQA test positions 0–299, matching questions/answers/order and a separately checked dataset revision | The later match does not prove the historical dataset commit. Public-benchmark training exposure cannot be excluded. |

## Reproduce the checks

From the repository root, using Python 3.10 or later:

```text
python -B paper_materials/verification/verify_materials.py
python -B -m unittest discover -s paper_materials/error_taxonomy/code -p "test_recompute_agreement.py"
```

These commands use the standard library and do not call an API. They check question identity/order, saved scores, generated table correspondence, STOP counts and review keys, all 30 taxonomy comparisons, and file integrity. They do not perform independent clinical adjudication or regenerate model responses.

Human ratings, reviewer-response drafts, credentials, environment files, internal operational logs, and incomplete Comment 9 results are outside this initial release. Model identifiers are recorded metadata rather than independently verified release-date or capability claims. See [publication status](PUBLICATION_STATUS.md) and [source notices](DATA_SOURCES.md) for remaining boundaries.
