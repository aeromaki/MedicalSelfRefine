# Model information and reproducibility evidence

Start with [the readable model table](models.md), then use [model_catalog.csv](model_catalog.csv) for the full fields. The table covers the **13 answer-generating models in the historical self-refinement results**. It does not describe the later GPT/Claude/DeepSeek taxonomy graders; those settings are in the separate error-taxonomy materials.

## Evidence categories

| Evidence category | Meaning |
|---|---|
| Archived configuration | A preserved alias-to-model or endpoint mapping; not a captured HTTP request or proof of the final server deployment |
| Researcher statement | A condition confirmed by the researcher, distinguished from a recovered historical runtime log |
| Reported revision condition | A setting or experimental condition described for revision work; not proof that the corresponding run is complete |
| UNKNOWN / PENDING | The supplied evidence does not establish the value; it is not zero or a guessed server default |

The result JSON records the model alias for each role. The separate preserved configuration supplies request-model strings. In particular, an API identifier ending in `Instruct-Turbo` is not automatically the exact Hugging Face repository used by a later local server. The final served repository and weight commit remain unverified where marked unknown.

The researcher confirmed vLLM **0.9.2** and **BF16** for historical and revision open-model execution. These fields are explicitly tagged as researcher statements. Archived Together AI endpoint mappings describe preserved configuration; they do not override the researcher's account of final vLLM execution. The statement does not cover GPT API internals. BF16 and the recollection that no extra quantization was applied do not establish whether a model's native weight configuration used quantization.

**DeepSeek-R1-Distill-Llama-70B and the separate DeepSeek-R1 result are distinct entries.** The preserved `deepseek-r1` mapping names `deepseek-ai/DeepSeek-R1`, but the latest handoff leaves the actual historical deployment identity unresolved. The catalog therefore retains the mapping as evidence without resolving the uncertainty by substituting the Distill model.

Meditron retains the archived `OpenMeditron/Meditron3-*` identifiers. The researcher-reported namespace relationship with EPFLiGHT does not prove historical and current weight revisions are identical. Base/instruction-tuned status and model-specific citations must be established from appropriate model evidence, not from the absence of `Instruct` in a name. Two additional aliases in an older local manifest, BioMistral-7B and DeepSeek-R1-Distill-8B, are not part of these 13 historical result files and are excluded from the historical result catalog; the July 2025 lookup lists them separately for configuration completeness.

## Historical versus revision settings

[historical_settings.json](historical_settings.json) records the reconstructed solver/critic/refiner request temperature of **0.7** and omitted `top_p`, `seed`, and `max_tokens`. The auxiliary answer extractor has temperature **0**. [decoding_evidence.md](decoding_evidence.md) records the inspected dependency source and conditional conclusion. These facts do not reconstruct backend defaults or prove how the server executed each request.

[revision_settings.json](revision_settings.json) now distinguishes the **completed supplementary experiments reported in the manuscript** from run-level records absent from this initial GitHub release. Supplementary Table 10 reports a single greedy-decoding run for ten open-weight models and temperature-zero API requests for two GPT models (12 models). Supplementary Table 11 reports mean and sample SD over three temperature-0.7 runs for 11 models. Complete per-run inventories and output files have not been deposited here. Retries and checkpoint resumes should not be counted as independent repetitions. A GPT API temperature-zero condition is not proof of an internally strict greedy algorithm.

`max_model_len` limits combined input and output context. On 24 November 2026, the researcher confirmed that historical open-weight models were configured with **max_model_len=8192**. This supersedes the earlier unresolved historical context entry and is tagged as a researcher statement, not a recovered runtime log. It does not describe GPT API limits or the output-token parameter `max_tokens`. The separate 8192/4096 revision conditions remain recorded in revision_settings.json. Final output budgets remain pending run manifests. No STOP/continue-balanced prompt experiment is claimed here.

## Using the configuration template

- Open-model entries use `http://localhost:8000/v1` as a **local vLLM example**, not the historical server address. Replace it with your own authorized endpoint when the client and server are on different machines. No researcher's computer IP is required in a public file.
- Reusing the example port does not automatically serve every listed model at once; set each entry to the endpoint serving that model, or use an appropriately configured router.
- The `model` string must match the ID exposed by your server. Archived `Instruct-Turbo` IDs are provider serving names and are not automatically Hugging Face download repository names. The separate DeepSeek-R1 placeholder also needs a verified deployment ID.
- GPT-4o and GPT-4o-mini omit `base_url` and use the client's default OpenAI endpoint unless your environment overrides it. Do not point these entries at a local vLLM server when reproducing the original API use.
- Supply credentials through the client environment. The existing loader does not expand environment-variable placeholders inside JSON. Configure model downloads/revisions and `max_model_len` on the server; the repository lookup table is provenance, not additional ChatOpenAI constructor arguments.

## Candidate revisions, model identity and limitations

The researcher reports downloading open models in **July 2025**. [revision_lookup.md](revision_lookup.md) lists full candidate commit hashes, dates, official source links and limitations. Downloadable versions are [CSV](model_revisions_july2025.csv) and [JSON](model_revisions_july2025.json). The lookup covers all 13 historical result models and separately labels BioMistral-7B and the empty DeepSeek-R1-Distill-8B configuration entry.

These are revisions reconstructed from repository history or metadata under the stated main-branch download assumptions. They are not claimed as recovered runtime hashes. Mistral has five possible July repository snapshots with identical non-README files; Llama candidates use public metadata because history is gated; Meditron historical hashes remain unavailable. GPT API models use model IDs/snapshots rather than public weight commits.

The Solver, Critic, and Refiner used langchain-openai version 0.2.4, with a sampling temperature of 0.7 inherited from the library defaults. The client did not explicitly specify top_p, seed, or max_tokens; their effective server-side values were not recorded. The maximum combined input-and-output context length for open-weight models was configured to 8,192 tokens. GPT-4o and GPT-4o-mini were accessed through the gpt-4o and gpt-4o-mini API aliases. The auxiliary GPT-4o-mini answer extractor used a temperature of 0.
