# Error taxonomy 재분류 자료

[English](README.md) · [방법](docs/METHODS.md) · [한계](docs/LIMITATIONS.md) · [열 설명](docs/DATA_DICTIONARY.md)

본실험에서 보존한 답변 3,309건에 대해 원본 GPT, GPT 재실행 1·2, Claude, DeepSeek의 오류 유형 분류를 비교한 자료입니다. 원래 Self-Refinement 결과나 Comment 9의 반복 생성·dispersion 실험과 구분합니다. 사람 평가 데이터는 포함하지 않았습니다.

- [사례별 분류](data/per_case_comparison.csv): 학생 모델·단계·원본 ID로 매칭한 다섯 결과.
- [일치도 표](results/agreement_tables.csv): 비교별 유효 표본, 공통 2,908건, 복구 전 코드 민감도 총 30행.
- [분류 근거 기록](data/record_audit.csv): 16,545개 사례·평가자 조합의 원 저장 코드와 복구 코드, 메타데이터와 해시.
- [실행 조건](config/): 모델명·API 경로·출력 한도·병렬 수 등 보존된 manifest.
- [분류 기준](prompts/taxonomy.csv): 원래 영어 대분류·소분류 이름과 정의.

이 폴더에서 다음 명령으로 API 호출 없이 재계산할 수 있습니다.

```text
python code/recompute_agreement.py
python -m unittest discover -s code -p "test_recompute_agreement.py"
```

원본 GPT 6건과 Claude 72건의 기계적 파서 복구를 기록했습니다. DeepSeek는 3,309건 모두 완료했으며, 오류가 없다는 형식의 78건은 오류 전용 분류 체계에서 미분류로 남겼습니다. 미분류는 불일치로 세지 않고 비교 분모에서 제외합니다.

일치도는 정확도가 아닙니다. 소분류 하나의 추가·삭제도 전체 집합 일치에서는 불일치이며, 전체 코드 일치는 대분류와 소분류 집합이 모두 같아야 합니다. 입력 추출 문제와 프롬프트 예시의 불일치는 이번 재실험에서도 유지됐습니다. 같은 문항이 모델·단계에 반복되므로 3,309건을 독립 문항 수로 해석하지 않습니다.

공개 데이터만으로 통계는 재현할 수 있습니다. 원 평가 응답 전문은 포함하지 않아 모든 원문 파싱을 독립적으로 다시 확인할 수는 없습니다. `instructions_only.json`은 예시 여섯 개를 제외한 발췌본이며 완전한 실험 프롬프트가 아닙니다. 기존 저장소의 전체 taxonomy 프롬프트는 영문 README에 연결하고 정확한 해시로 식별했습니다.
