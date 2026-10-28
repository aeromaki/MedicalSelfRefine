# Model identities and execution evidence

Start with [the readable model table](models.md), then use [model_catalog.csv](model_catalog.csv) for the full fields. The table covers the **13 answer-generating models in the historical self-refinement results**. It does not describe the later GPT/Claude/DeepSeek taxonomy graders; those settings are in the separate error-taxonomy materials.

## How to interpret the evidence

| Evidence type | Meaning |
|---|---|
| Archived configuration | A preserved alias-to-model or endpoint mapping; not a captured HTTP request or proof of the final server deployment |
| Reconstructed client request | Source and a pinned dependency's default request construction, conditional on no unrecorded changes or overrides |
| Researcher statement | A condition confirmed by the researcher, distinguished from a recovered historical runtime log |
| Reported revision condition | A setting or experimental condition described for revision work; not proof that the corresponding run is complete |
| UNKNOWN / PENDING | The supplied evidence does not establish the value; it is not zero or a guessed server default |

The result JSON records the model alias for each role. The separate preserved configuration supplies request-model strings. In particular, an API identifier ending in `Instruct-Turbo` is not automatically the exact Hugging Face repository used by a later local server. The final served repository and weight commit remain unverified where marked unknown.

The researcher confirmed vLLM **0.9.2** and **BF16** for historical and revision open-model execution. These fields are explicitly tagged as researcher statements. Archived Together AI endpoint mappings describe preserved configuration; they do not override the researcher's account of final vLLM execution. The statement does not cover GPT API internals. BF16 and the recollection that no extra quantization was applied do not establish whether a model's native weight configuration used quantization.

## Identity boundaries

**DeepSeek-R1-Distill-Llama-70B and the separate DeepSeek-R1 result are distinct entries.** The preserved `deepseek-r1` mapping names `deepseek-ai/DeepSeek-R1`, but the latest handoff leaves the actual historical deployment identity unresolved. The catalog therefore retains the mapping as evidence without resolving the uncertainty by substituting the Distill model.

Meditron retains the archived `OpenMeditron/Meditron3-*` identifiers. The researcher-reported namespace relationship with EPFLiGHT does not prove historical and current weight revisions are identical. Base/instruction-tuned status and model-specific citations must be established from appropriate model evidence, not from the absence of `Instruct` in a name. Two additional aliases in an older local manifest, BioMistral-7B and DeepSeek-R1-Distill-8B, are not part of these 13 historical result files and are excluded.

## Historical versus revision settings

[historical_settings.json](historical_settings.json) records the reconstructed solver/critic/refiner request temperature of **0.7** and omitted `top_p`, `seed`, and `max_tokens`. The auxiliary answer extractor has temperature **0**. [decoding_evidence.md](decoding_evidence.md) records the inspected dependency source and conditional conclusion. These facts do not reconstruct backend defaults or prove how the server executed each request.

[revision_settings.json](revision_settings.json) records reported revision conditions without presenting them as completed results: a greedy/temperature-zero condition and three independent repeats under historical request settings. The supplied package has no final run inventory or dispersion analysis. It is not a live status report of remote experiments. Retries and checkpoint resumes must not count as independent repeats. A GPT API temperature-zero condition is not described as a verified strict greedy implementation.

`max_model_len` limits combined input and output context. The 8192/4096 values under revision review are not historical limits and are not the output-token parameter `max_tokens`. Final output budgets remain pending run manifests. No STOP/continue-balanced prompt experiment is claimed here.

## Configuration template

[models.template.json](models.template.json) shows the original alias-to-configuration shape and contains no credentials or internal endpoints. It is deliberately **not an executable historical configuration**: endpoints are reserved `.invalid` placeholders, final served IDs need confirmation, and the separate DeepSeek-R1 model is an explicit placeholder. The existing loader passes JSON values literally; it does not interpolate environment placeholders. Before use, supply a verified deployment ID and authorized endpoint and configure credentials through the appropriate client environment. No new model request is needed to read or verify these materials.

An executable reproduction configuration and complete model-paper citations remain open items. [references.md](references.md) explains the current source boundary. No unknown commit, citation, model identity or backend default has been filled by inference.
