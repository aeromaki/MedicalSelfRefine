# Error-taxonomy reclassification

[한국어 안내](README_KO.md) · [Methods](docs/METHODS.md) · [Limitations](docs/LIMITATIONS.md) · [Data dictionary](docs/DATA_DICTIONARY.md)

This part of the initial paper-materials release compares five sets of error-type labels on **3,309 archived answer instances**: historical GPT-4o-mini, two GPT-4o-mini reruns, Claude, and DeepSeek. It is separate from the original Self-Refinement outcome analysis and from the pending repeated-generation/dispersion experiment for Comment 9.

The same question occurs across 13 answer-generating models and three stages. These are not 3,309 independent questions. The taxonomy reruns preserved the archived inputs and classification prompt, including the input-extraction and example-label limitations documented below. No human ratings are included.

## Read the results

| File | What it contains |
|---|---|
| [Agreement tables](results/agreement_tables.csv) | 30 rows: 10 pairwise-valid, 10 common-case, 10 raw-saved-code sensitivity comparisons |
| [Case labels](data/per_case_comparison.csv) | All 3,309 case keys and five canonical labels |
| [Label audit](data/record_audit.csv) | 16,545 case/rater records, raw saved codes, recovered codes, response metadata and hashes |
| [Input audit](data/input_audit.csv) | Input/question hashes and missing-prediction flag; no source prose |
| [DeepSeek unclassified cases](data/deepseek_unclassified.csv) | 78 cases with output form and mechanical string-match flags |
| [Full statistical summary](results/summary.json) | Metrics, denominators, category distributions, confusion matrices and provenance |
| [Run configurations](config/) | Four saved completed-run manifests; machine-specific source paths made relative |
| [English taxonomy](prompts/taxonomy.csv) | Original category names and definitions |

All five runs have valid labels for the same **2,908 cases**. For those cases:

| DeepSeek compared with | Primary agreement | Exact subtype set | Both axes exact | Primary Cohen kappa |
|---|---:|---:|---:|---:|
| Historical GPT | 37.52% | 14.20% | 9.35% | 0.1350 |
| GPT rerun 1 | 38.41% | 14.13% | 9.77% | 0.1473 |
| GPT rerun 2 | 38.41% | 14.41% | 9.53% | 0.1442 |
| Claude | 75.69% | 34.83% | 30.19% | 0.6516 |

Agreement is not accuracy. Missing codes are excluded rather than scored as disagreements. Exact subtype agreement requires the whole set to match; both-axes agreement additionally requires the same primary category. Code validity does not establish clinical correctness. See the methods and limitations before interpreting the table.

## Recompute offline

From this folder, with Python 3.10 or later:

```text
python code/recompute_agreement.py
python -m unittest discover -s code -p "test_recompute_agreement.py"
```

No API key, network access, or third-party package is needed. The program checks unique case keys, labels, recorded parser-recovery evidence, and all **30 comparison/cohort results** against the saved summary. Optional `--output recomputed_summary.json` writes a new file and refuses to overwrite an existing file.

The 19 synthetic tests cover label normalization, missingness, complete-set matching, duplicate identifiers, agreement/kappa, parser-recovery rules and reference mismatch handling. The included candidate ledger can validate the recorded recovery rules, but cannot substitute for re-extracting candidates from omitted response prose.

## Experimental identity and boundaries

Six historical GPT labels and 72 Claude labels were mechanically recovered from already saved responses. Original manifests retain their original counts; analysis labels and the raw-code sensitivity result document the change. DeepSeek completed all 3,309 requests; its 78 no-error-style outputs are unclassified under this error-only code format, not unfinished API requests.

Model strings in the manifests are observed metadata, not external release-date or performance-ranking claims. GPT reruns returned `gpt-4o-mini-2024-07-18`; the other recorded identifiers are `claude-sonnet-5-5` and `deepseek/deepseek-v4.1-flash-1017`. Temperature and seed were not explicitly set. The historical GPT deployment and historical dependency versions are not established.

[instructions_only.json](prompts/instructions_only.json) contains the exact system instruction and input template, explicitly marked as an incomplete excerpt. The six examples are not duplicated here. The existing repository [full taxonomy prompt source](../../vis/visbox/autolabel/prompt.json) is identified by experimental SHA-256 `203b97f8e025f7ecb13b25aade5510ed716c6ebd414bbaf92f8ed4d20ba84b7c`.

Raw classifier explanations, auxiliary reasoning, credentials, operational logs and the human workbook are excluded. The offline statistical analysis is self-contained; full request-level rerunning and independent original-response parsing are not. This collection does not assign a new license to upstream code or benchmark material.

[Source files](provenance/source_files.json) record transformations and hashes. Source artifact paths in statistical metadata are identifiers from the original workspace, not paths that must exist in this release. [Verification](provenance/verification.json) records fresh offline checks. No new model calls were made while preparing this release.
