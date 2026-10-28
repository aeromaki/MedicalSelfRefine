# The 300 evaluated MedQA items

[questions.csv](questions.csv) is the reading/table version; [questions.json](questions.json) preserves the same 300 records as structured data. Each record has `question_id` Q001–Q300, `index_zero_based` 0–299, `question`, `options`, `answer_key`, and the original `item_and_answer_sha256`.

The historical evaluation used the first 300 test-split items in their original order. This is a consecutive selection, not random sampling; there is no question-selection seed. A generation seed is a separate setting. The 300 questions, options, answers and order match all 13 historical result files and both supplied question-list formats.

[provenance.json](provenance.json) records the dataset source and the revision checked during revision work. That comparison establishes item/answer/order equality; it does not establish that the historical experiment downloaded that same commit. The historical dataset commit is not known. The dataset source is `bigbio/med_qa`, configuration `med_qa_en_source`, test split; upstream reference: https://huggingface.co/datasets/bigbio/med_qa .

Public benchmark exposure during model training cannot be excluded. Initial accuracy therefore should not be treated as pure reasoning ability or evidence of absence of contamination. Evaluation of the full test split is outside these historical 300-item results.

The data originate from MedQA and retain their source provenance. No new blanket license is granted to source questions or embedded third-party material by this release. Applicable upstream attribution and redistribution conditions remain relevant; see [data sources and attribution](../DATA_SOURCES.md).
