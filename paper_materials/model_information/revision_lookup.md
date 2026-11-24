# Model repository revisions for July 2025 downloads

Updated 24 November 2026. The researcher reports an open-model download month of July 2025. The table distinguishes repository history from evidence of what was actually served. Reconstruction assumes a fresh download from the stated repository's main branch without an explicitly pinned older revision. All timestamps below are UTC.

`candidate_revisions` contains full 40-character repository commit hashes. A commit identifies a repository snapshot, including documentation, configuration and tokenizer files; it is not a per-weight-file checksum. The historical deployment revision field remains unknown unless execution/download evidence establishes it.

## All configured models

| Alias | Candidate repository / API source | Full candidate revision(s) | Evidence status |
|---|---|---|---|
| deepseek-r1-distill-70b | [deepseek-ai/DeepSeek-R1-Distill-Llama-70B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B/commits/main) | `b1c0b44b4369b597ad119a196caf79a9c40e141e` | history_verified_no_july_changes |
| deepseek-r1 | [deepseek-ai/DeepSeek-R1](https://huggingface.co/deepseek-ai/DeepSeek-R1/commits/main) | `56d4cbbb4d29f4355bab4b9a39ccb717a14ad5ad` | history_verified_no_july_changes |
| gpt-4o-mini | [gpt-4o-mini](https://developers.openai.com/api/docs/models/gpt-4o-mini) | Not applicable: API | api_not_applicable |
| gpt-4o | [gpt-4o](https://developers.openai.com/api/docs/models/gpt-4o) | Not applicable: API | api_not_applicable |
| huatuogpt-o1-70b | [FreedomIntelligence/HuatuoGPT-o1-70B](https://huggingface.co/FreedomIntelligence/HuatuoGPT-o1-70B/commits/main) | `a10f06ad04115c5205da2cf63b2e06b5e9d13ac9` | history_verified_no_july_changes |
| huatuogpt-o1-8b | [FreedomIntelligence/HuatuoGPT-o1-8B](https://huggingface.co/FreedomIntelligence/HuatuoGPT-o1-8B/commits/main) | `afc8b260e5b3dee9233863cf2de3080f3094442a` | history_verified_no_july_changes |
| llama-3.1-70b | [meta-llama/Llama-3.1-70B-Instruct](https://huggingface.co/api/models/meta-llama/Llama-3.1-70B-Instruct) | `1605565b47bb9346c5515c34102e054115b4f98b` | metadata_inference_history_gated |
| llama-3.1-8b | [meta-llama/Llama-3.1-8B-Instruct](https://huggingface.co/api/models/meta-llama/Llama-3.1-8B-Instruct) | `0e9e39f249a16976918f6564b8830bc894c89659` | metadata_inference_history_gated |
| meditron3-70b | [EPFLiGHT/Meditron3-70B](https://huggingface.co/api/models/OpenMeditron/Meditron3-70B) | Not recovered | history_gated |
| meditron3-8b | [EPFLiGHT/Meditron3-8B](https://huggingface.co/api/models/OpenMeditron/Meditron3-8B) | Not recovered | history_gated |
| mistral-7b | [mistralai/Mistral-7B-Instruct-v0.1](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1/commits/main) | `2dcff66eac0c01dc50e4c41eea959968232187fe`<br>`0f4876c9377f68fd4b6a971c77b96a84993754ae`<br>`48061930344d3406dd79b7825fe86e1f9bcc2d15`<br>`9db24f5cef284857f21081e53f57925196341ef9`<br>`ec5deb64f2c6e6fa90c1abf74a91d5c93a9669ca` | multiple_snapshots_same_model_files |
| qwen2.5-72b | [Qwen/Qwen2.5-72B-Instruct](https://huggingface.co/Qwen/Qwen2.5-72B-Instruct/commits/main) | `495f39366efef23836d0cfae4fbe635880d2be31` | history_verified_upstream_candidate |
| qwen2.5-7b | [Qwen/Qwen2.5-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct/commits/main) | `a09a35458c702b33eeacc393d103063234e8bc28` | history_verified_upstream_candidate |
| biomistral-7b | [BioMistral/BioMistral-7B](https://huggingface.co/BioMistral/BioMistral-7B/commits/main) | `9a11e1ffa817c211cbb52ee1fb312dc6b61b40a5` | extra_config_only_history_verified |
| deepseek-r1-distill-8b | Not specified | Not recovered | extra_empty_config_entry |

## Evidence levels and identity boundaries

- `history_verified_no_july_changes`: the inspected repository main history has no July 2025 commit. The historical download must still match that repository and the stated assumptions. DeepSeek-R1's historical deployment identity remains unresolved in the original catalog; it is separate from Distill-Llama-70B and is not replaced with R1-0528.
- `history_verified_upstream_candidate`: Qwen's upstream main history has no July changes. The archived *-Instruct-Turbo serving IDs do not prove the exact local download repository. See [Together's model table](https://docs.together.ai/docs/deprecations) and [Qwen 7B Turbo](https://www.together.ai/models/qwen2-5-7b-instruct-turbo).
- `metadata_inference_history_gated`: Llama's public metadata reports the listed SHA with lastModified in September/December 2024; these are July candidates inferred from metadata. Full history returned HTTP 401. The archived Turbo-to-upstream mapping remains unverified.
- `history_gated`: OpenMeditron URLs redirect to EPFLiGHT, but historical commit APIs returned HTTP 401. Current metadata revisions are dated June 2026 and were excluded from July 2025 candidates. A namespace redirect alone does not establish historical weight identity.
- `api_not_applicable`: GPT entries preserve the actual requested aliases. Current API documentation cannot establish the exact historical response snapshot. GPT-4o-mini's documented dated snapshot is gpt-4o-mini-2024-07-18; it is not presented here as a recovered historical response ID.
- `extra_config_only_history_verified` / `extra_empty_config_entry`: BioMistral and the empty Distill-8B entry are not among the 13 historical result files. BioMistral's repository has no July changes. The empty entry has no model ID, so no repository is invented.

## Mistral snapshot timeline

Five repository snapshots could have been downloaded during July 2025:

| Main commit begins (UTC) | Full revision |
|---|---|
| 2024-08-22T11:33:25.000Z | `2dcff66eac0c01dc50e4c41eea959968232187fe` |
| 2025-07-23T12:13:26.000Z | `0f4876c9377f68fd4b6a971c77b96a84993754ae` |
| 2025-07-24T16:39:09.000Z | `48061930344d3406dd79b7825fe86e1f9bcc2d15` |
| 2025-07-24T16:39:59.000Z | `9db24f5cef284857f21081e53f57925196341ef9` |
| 2025-07-24T16:44:46.000Z | `ec5deb64f2c6e6fa90c1abf74a91d5c93a9669ca` |

Each row applies until the next listed commit; the first was already current at the start of July. The four July commits changed README.md only. Public tree metadata for all five snapshots showed the same 15 paths and identical Git object IDs for all 14 non-README files, including weights, tokenizer and model/generation configuration. Thus the exact repository snapshot needs the download date/time, while the model files are equivalent across these five main snapshots. No model weights were downloaded for this comparison.

## Audit data

The [JSON](model_revisions_july2025.json) and [CSV](model_revisions_july2025.csv) preserve full hashes, dates, source URLs, assumptions and per-model notes. [revision_evidence.json](revision_evidence.json) contains the inspected commit lists/metadata and the Mistral tree comparison. The [13-model catalog](model_catalog.csv) keeps these candidates in separate columns from verified historical deployment fields.
