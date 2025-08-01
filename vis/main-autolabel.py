from visbox import autolabel_all_multiprocessing, load_model_logs


logs = load_model_logs([
    'deepseek-r1',
    'deepseek-r1-distill-70b',
    #'deepseek-r1-distill-14b',
    #'gemma-2-9b',
    #'gemma-2-27b',
    'gpt-4o',
    'gpt-4o-mini',
    'huatuogpt-o1-8b',
    'huatuogpt-o1-70b',
    'llama-3.1-8b',
    'llama-3.1-70b',
    'meditron3-8b',
    'meditron3-70b',
    'mistral-7b',
    'qwen2.5-7b',
    'qwen2.5-72b'
    ])


if __name__ == "__main__":
    autolabel_all_multiprocessing(
        { "model": "gpt-4o-mini" },
        logs
        )
