How `.env` file should be set:
```
HF_CACHE_DIR="..."
OPENAI_API_KEY="..."
```

### Paper reproducibility entry point (documentation update, November 2026)

From the repository root:

```bash
cd implementations
pip install -r requirements.txt
cp ../paper_materials/model_information/models.template.json models.json
```

Edit `models.json` so each model ID and `base_url` matches the model **actually served** by your GPU/API host. The example `localhost` endpoint and historical `-Turbo` aliases are not verified live deployments. Replace `REPLACE_WITH_CONFIRMED_HISTORICAL_ID` with a real model ID if you run DeepSeek-R1. Keep local addresses and API credentials out of the public repository.

For an example intrinsic self-refinement queue, use the tracked `queue.example.json` in this directory, after verifying that `models.json` contains valid entries. To run the full 300-item example (incurs GPU/API costs):

```bash
python main.py -q queue.example.json -n 1 -r results
```

This codebase contains optional non-paper approaches. The paper **did not** execute an oracle-critic or plain re-ask arm. Historical deployment hashes and original API snapshots are not recreated by this sample configuration.

Set `models.json` before execution!

python >= 3.12 required!

Using [pyre](https://pyre-check.org) for type checking
