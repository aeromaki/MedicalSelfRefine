# Self-Refinement (SR) Medical QA Experiment

This project is a codebase for experimenting with Self-Refinement methods in medical question-answering (QA) tasks.

## 📋 Project Overview

- **Purpose**: Comparative experiments of Self-Refinement, Multi-Critic Self-Refinement, and GenRM methods in medical QA
- **Datasets**: MedQA, MedMCQA, PubMedQA, DDXPlus
- **Models**: Various LLM models (GPT-4o, Llama, Qwen, HuatuoGPT, etc.)

## 🏗️ Project Structure

```
sr/implementations/
├── main.py                 # Main execution script
├── main_critic.py          # Critic-only execution script
├── config_sr.py           # Self-Refinement configuration
├── config_mcsr.py         # Multi-Critic Self-Refinement configuration
├── config_genrm.py        # GenRM configuration
├── models.json            # Model configuration file
├── requirements.txt       # Python dependencies
├── queues/               # Experiment queue configuration files
│   ├── huatuo70b.json
│   ├── gpt-4o.json
│   └── ...
├── results/              # Experiment results storage
├── runbox/               # Core library
│   ├── agents/           # Agent implementations
│   ├── benchmarks/       # Benchmark datasets
│   └── prompts/          # Prompt templates
└── utils.py              # Utility functions
```

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Python 3.12+ required
python --version

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

Configure the models to use in `models.json`:

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
# Self-Refinement experiment
python main.py -q queues/huatuo70b.json -n 4 -r results

# Critic-only experiment
python main_critic.py -q queues/huatuo70b.json -n 4 -r results
```

## 📊 Experiment Methods

### Self-Refinement (SR)
- **Initial Response** → **Critique** → **Refinement** → **Repeat**
- Repeat improvement process `n_iter` times

### Multi-Critic Self-Refinement (MCSR)
- Multiple critics evaluate simultaneously
- Improvement from diverse perspectives

### GenRM
- Generative critique model
- More natural feedback

## 🔧 Command Options

```bash
python main.py [OPTIONS]

Options:
  -q, --queue_path      Experiment configuration file path
  -n, --n_process       Number of parallel processing processes
  -r, --result_dir_path Result storage directory
  --buffer_path         Buffer file path (default: .cache/buffer)
```

## 📈 Result Analysis

Experiment results are saved in JSON format in the `results/` folder:

```json
{
  "config": {...},           // Experiment configuration
  "final_score": [0.87, 0.88, 0.89],  // Accuracy for each iteration
  "total_cost": 7.29,        // Total cost
  "generations": [...]       // Detailed results
}
```

## 🖥️ Model Serving

### Local Server (vLLM)
```bash
# Run on GPU server
vllm serve FreedomIntelligence/HuatuoGPT-o1-70B --port 8025
```

### Cloud APIs
- Together AI
- OpenAI
- Other compatible APIs

## 🛠️ Development Tools

- **Type Checking**: [pyre](https://pyre-check.org)
- **Code Formatting**: black, isort
- **Linting**: flake8

## 📝 Requirements

- Python >= 3.12
- CUDA-compatible GPU (when using local server)
- Sufficient memory (when using 70B models)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is developed for research purposes.

## 📞 Contact

If you have any questions about the project, please create an issue.