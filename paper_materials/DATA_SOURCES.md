# Data sources and notices

The evaluated items originate from MedQA, distributed through the `bigbio/med_qa` English source configuration. We cite the original dataset authors and retain the source identifiers and selection provenance.

- [Original MedQA repository](https://github.com/jind11/MedQA) requests citation of the dataset paper and contains an [MIT LICENSE, Copyright (c) 2022 Di Jin](https://github.com/jind11/MedQA/blob/master/LICENSE). The [upstream notice is retained here](medqa_300/UPSTREAM_LICENSE_MedQA.txt) with its original wording.
- The [BigBio MedQA dataset card](https://huggingface.co/datasets/bigbio/med_qa) and its [README metadata](https://huggingface.co/datasets/bigbio/med_qa/raw/main/README.md) record the dataset license as unknown. The [BigBio loader](https://github.com/bigscience-workshop/biomedical/blob/master/bigbio/biodatasets/med_qa/med_qa.py) also records the dataset license as unknown; the loader's own software license is a separate matter.

These notices were checked against the current official sources on 28 October 2026. They do not establish the notices at the historical experiment date or at the separately checked dataset revision. The different source notices are reported separately; this release does not assign a new license to third-party exam content or represent every question as covered by the repository's MIT notice.

## Dataset citation

Jin D, Pan E, Oufattole N, Weng WH, Fang H, Szolovits P. *What Disease Does This Patient Have? A Large-Scale Open Domain Question Answering Dataset from Medical Exams.* Applied Sciences. 2021;11(14):6421. [Preprint](https://arxiv.org/abs/2009.13081).

```bibtex
@article{jin2021disease,
  title={What Disease Does This Patient Have? A Large-Scale Open Domain Question Answering Dataset from Medical Exams},
  author={Jin, Di and Pan, Eileen and Oufattole, Nassim and Weng, Wei-Hung and Fang, Hanyi and Szolovits, Peter},
  journal={Applied Sciences},
  volume={11},
  number={14},
  pages={6421},
  year={2021},
  publisher={MDPI}
}
```

## Selection and provenance

The historical inputs match the first 300 test items, zero-based positions 0–299. The later dataset comparison used `bigbio/med_qa`, configuration `med_qa_en_source`, revision `484a6c066fe8e75c83edea0c88b5169316714fcd`. Question content, supplied correct answers and order match. This establishes the later comparison, not that this revision was used historically. Details are retained in [dataset provenance](medqa_300/provenance.json).

Historical model outputs, prompt templates/examples and STOP review annotations were supplied by the research team. Model-output text can repeat source question content. Their presence does not certify the medical accuracy of the text. Public benchmark exposure during model training cannot be excluded, so initial accuracy should not be interpreted as pure reasoning ability.

The existing repository does not establish a general software/data license by describing research use alone. This materials commit preserves attribution and documents known source notices without assigning a blanket new license. Model-specific citations and historical revision gaps are listed with their evidence status in [model information](model_information/README.md).
