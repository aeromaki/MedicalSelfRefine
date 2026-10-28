# Selection, source and CSV format

The evaluation uses test-split indices 0–299 in order, corresponding to Q001–Q300. See [README.md](README.md) for the selection rule and interpretation, and [provenance.json](provenance.json) for the source revision checked during revision work. That checked revision does not establish the historical download commit.

In [questions.csv](questions.csv), the `options` cell is JSON-encoded. Read the CSV first and then use a JSON parser on that cell. The current source stores each option list as a multiline string, so decoding the cell returns the exact original string, including line breaks. This preserves the source value and avoids an implementation-specific object representation. [questions.json](questions.json) retains the original structured record values without this CSV encoding layer.

The other CSV fields are `question_id`, `index_zero_based`, `question`, `answer_key`, and `item_and_answer_sha256`. The file uses UTF-8 with BOM for Excel compatibility. All 300 JSON-encoded option cells were round-trip checked against the unchanged JSON source.
