# Self-Refinement (SR) Medical QA Experiment

This project is a codebase for experimenting with Self-Refinement methods in medical question-answering (QA) tasks.

## Paper materials

The initial publication materials include the full role prompts, 300 evaluated MedQA items, historical results, STOP reanalysis, and GPT/Claude/DeepSeek error-taxonomy comparisons.

[English guide](paper_materials/README.md) | [Korean guide](paper_materials/README_KO.md) | [Summary workbook](paper_materials/summary_tables.xlsx)

Historical experiment outputs, their reanalysis, and taxonomy reclassification are documented separately. Supplementary reproducibility results are reported in revised-manuscript Supplementary Tables 10 and 11 (12 models under greedy/temperature-zero decoding and 11 models with three temperature-0.7 runs). Their run-level records are not part of the initial October 2026 GitHub materials release.

## Project Overview

- **Purpose**: Comparative experiments of Self-Refinement, Multi-Critic Self-Refinement, and GenRM methods in medical QA
- **Datasets**: MedQA, MedMCQA, PubMedQA, DDXPlus
- **Models**: Various LLM models (GPT-4o, Llama, Qwen, HuatuoGPT, etc.)

## Project Structure

```text
implementations/
|-- main.py                 # Main execution script
|-- main_critic.py          # Critic-only execution script
|-- config_sr.py            # Self-Refinement configuration
|-- config_mcsr.py          # Multi-Critic Self-Refinement configuration
|-- config_genrm.py         # GenRM configuration
|-- models.json             # Local model configuration (gitignored)
|-- queue.example.json      # Tracked example experiment queue
|-- requirements.txt        # Python dependencies
|-- results/                # Experiment results storage (gitignored)
|-- runbox/                 # Core library
|   |-- agents/             # Agent implementations
|   |-- benchmarks/         # Benchmark datasets
|   `-- prompts/            # Prompt templates
`-- utils.py                # Utility functions
```

## Quick Start

### 1. Environment Setup

```bash
# Python 3.12+ required
python --version

# From the repository root, switch to the directory containing requirements.txt/main.py
cd implementations

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file and add the following content:

```env
HF_CACHE_DIR="path/to/huggingface/cache"
OPENAI_API_KEY="your_openai_api_key"
```

### 3. Model Configuration

From `implementations/`, copy the public template using `cp ../paper_materials/model_information/models.template.json models.json`, then update the example endpoints and model IDs for your authorized local or API servers. The placeholder for DeepSeek-R1 is deliberately not a valid live model ID. `models.json` is gitignored and may contain private connection details. Example of the required configuration shape:

```json
{
  "gpt-4o": {
    "model": "gpt-4o"
  },
  "huatuogpt-o1-70b": {
    "model": "FreedomIntelligence/HuatuoGPT-o1-70B",
    "base_url": "http://127.0.0.1:8025/v1/"
  }
}
```

### 4. Run Experiments

```bash
# Intrinsic Self-Refinement example; update models.json before running.
# This example uses 300 MedQA items and can incur API/GPU costs.
python main.py -q queue.example.json -n 1 -r results

# Other execution arms in this general-purpose codebase were not run in the paper.
```

## Experiment Methods

### Self-Refinement (SR)
- **Initial Response** -> **Critique** -> **Refinement** -> **Repeat**
- Repeat improvement process `n_iter` times

### Multi-Critic Self-Refinement (MCSR)
- Multiple critics evaluate simultaneously
- Improvement from diverse perspectives

### GenRM
- Generative critique model
- More natural feedback

## Command Options

```bash
python main.py [OPTIONS]

Options:
  -q, --queue_path      Experiment configuration file path
  -n, --n_process       Number of parallel processing processes
  -r, --result_dir_path Result storage directory
  --buffer_path         Buffer file path (default: .cache/buffer)
```

## Result Analysis

Experiment results are saved in JSON format in the `results/` folder:

```json
{
  "config": {},
  "final_score": [0.87, 0.88, 0.89],
  "total_cost": 7.29,
  "generations": []
}
```

## Historical study vs. general-purpose code

The manuscript evaluates **intrinsic self-refinement only**. The codebase also supports other methods, providers, and benchmarks; that support does not mean those arms or endpoints were used in the manuscript. According to the researcher's account, the historical open-weight models were served locally with vLLM 0.9.2/BF16. The preserved Together AI endpoints are archival configuration evidence, not independently verified final serving logs. See [model provenance](paper_materials/model_information/README.md).

## Model Serving

### Local Server (vLLM)
```bash
# Example server command (adjust model ID, checkpoint, GPU resources and port)
vllm serve FreedomIntelligence/HuatuoGPT-o1-70B --port 8025
```

### Cloud APIs
- Together AI
- OpenAI
- Other compatible APIs

## Development Tools

- **Type Checking**: [pyre](https://pyre-check.org)
- **Code Formatting**: black, isort
- **Linting**: flake8

## Requirements

- Python >= 3.12
- CUDA-compatible GPU (when using local server)
- Sufficient memory (when using 70B models)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is developed for research purposes.

## Contact

If you have any questions about the project, please create an issue.
