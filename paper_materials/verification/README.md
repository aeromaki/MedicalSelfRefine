# Offline verification

From the repository root:

```text
python -B paper_materials/verification/verify_materials.py
python -B -m unittest discover -s paper_materials/error_taxonomy/code -p "test_recompute_agreement.py"
```

Python 3.10+ and its standard library are sufficient. No credentials, API calls or new model generation are involved. The verifier prints its findings and does not rewrite files by default. `--output NEW_PATH.json` writes a new report only; an existing file is refused.

Checks include all 300 questions/answers in each of 13 historical result files, 11,700 case/stage rows, 39 accuracy rows, 26 failure records, all seven STOP count columns and rate denominators, 171 review response strings/hashes, prompt counts 8/2/2/5, the 13-model catalog, and all 30 taxonomy comparisons. If `SHA256SUMS.txt` is present, every listed file hash is checked. [Recorded results](verification_results.json) describe the arithmetic/file checks; they are not a clinical validation of the responses.

[source_manifest.json](source_manifest.json) identifies supplied archives. The [historical file manifest](../historical_results/file_manifest.json) maps public files to the original archive members and reports source/public SHA-256. The [26-case transformation table](../historical_results/transformations.csv) records removal of internal error tracebacks. No other historical JSON values were changed.

Source artifact hashes cannot prove the contents of an unavailable source; the local collection additionally checked the supplied archives before publication. The later remote dataset comparison is preserved as provenance, not repeated by this offline verifier. Likewise, taxonomy candidate-code records cannot substitute for re-extracting codes from omitted classifier prose.

The publication directory is marked `-text` in repository `.gitattributes` to preserve CSV/JSON bytes across operating systems. The taxonomy prompt outside this directory is identified by its original Git blob hash; a Windows checkout may change its line endings without changing the experiment's stored prompt.
