# Historical model catalog

This table identifies archived configuration strings and their evidential limits. The full CSV contains separate fields for source type, dtype, context limits and missing provenance.

| Result alias | Archived request model ID | Variant evidence | Remaining identity/revision issue |
|---|---|---|---|
| deepseek-r1-distill-70b | `deepseek-ai/DeepSeek-R1-Distill-Llama-70B` | Distill-Llama variant explicitly named; detailed training/weight revision unverified | historical output token limit; historical context limit; final model citation; exact served repository and weight commit; model-native quantization configuration |
| deepseek-r1 | `deepseek-ai/DeepSeek-R1` | Historical identity unresolved; do not replace with the separately listed Distill model | historical model identity; historical output token limit; historical context limit; final model citation; exact served repository and weight commit; model-native quantization configuration |
| gpt-4o-mini | `gpt-4o-mini` | Proprietary API model; base/instruction-tuned checkpoint classification not established here | historical output token limit; historical context limit; final model citation; historical API snapshot |
| gpt-4o | `gpt-4o` | Proprietary API model; base/instruction-tuned checkpoint classification not established here | historical output token limit; historical context limit; final model citation; historical API snapshot |
| huatuogpt-o1-70b | `FreedomIntelligence/HuatuoGPT-o1-70B` | Base/instruction/post-training status not established by supplied execution evidence | historical output token limit; historical context limit; final model citation; exact served repository and weight commit; model-native quantization configuration |
| huatuogpt-o1-8b | `FreedomIntelligence/HuatuoGPT-o1-8B` | Base/instruction/post-training status not established by supplied execution evidence | historical output token limit; historical context limit; final model citation; exact served repository and weight commit; model-native quantization configuration |
| llama-3.1-70b | `meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo` | Instruct explicitly named in archived ID; exact final local weights unverified | historical output token limit; historical context limit; final model citation; exact served repository and weight commit; model-native quantization configuration |
| llama-3.1-8b | `meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo` | Instruct explicitly named in archived ID; exact final local weights unverified | historical output token limit; historical context limit; final model citation; exact served repository and weight commit; model-native quantization configuration |
| meditron3-70b | `OpenMeditron/Meditron3-70B` | Base/instruction/post-training status not established by supplied execution evidence | historical output token limit; historical context limit; final model citation; exact served repository and weight commit; model-native quantization configuration |
| meditron3-8b | `OpenMeditron/Meditron3-8B` | Base/instruction/post-training status not established by supplied execution evidence | historical output token limit; historical context limit; final model citation; exact served repository and weight commit; model-native quantization configuration |
| mistral-7b | `mistralai/Mistral-7B-Instruct-v0.1` | Instruct explicitly named in archived ID; exact final local weights unverified | historical output token limit; historical context limit; final model citation; exact served repository and weight commit; model-native quantization configuration |
| qwen2.5-72b | `Qwen/Qwen2.5-72B-Instruct-Turbo` | Instruct explicitly named in archived ID; exact final local weights unverified | historical output token limit; historical context limit; final model citation; exact served repository and weight commit; model-native quantization configuration |
| qwen2.5-7b | `Qwen/Qwen2.5-7B-Instruct-Turbo` | Instruct explicitly named in archived ID; exact final local weights unverified | historical output token limit; historical context limit; final model citation; exact served repository and weight commit; model-native quantization configuration |

Open-source serving with vLLM 0.9.2 and BF16 is recorded as a researcher statement. GPT API models are outside that environment claim. Archived Together endpoint mappings do not establish the final historical serving provider.

See [model_catalog.csv](model_catalog.csv), [evidence definitions](README.md), and [historical request settings](historical_settings.json).
