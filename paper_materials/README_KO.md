# MedicalSelfRefine 논문 공개 자료

[English](README.md) · [요약 Excel](summary_tables.xlsx) · [열·ID 설명](DATA_DICTIONARY.md)

2026-10-28에 정리한 첫 공개 자료입니다. **본실험 결과**, **본실험의 STOP 재분석**, **error taxonomy 재분류**를 구분했습니다. 기존 실행 코드와 원본 파일을 변경하거나 새 모델 호출을 수행하지 않았습니다.

| 찾는 자료 | 위치 |
|---|---|
| Solver·Critic·Refiner·보조 정답 추출기의 전체 프롬프트 | [prompts](prompts/README.md) |
| MedQA 첫 300문항·선택지·정답·선정 규칙 | [medqa_300](medqa_300/selection_and_source.md) |
| 13개 모델 본실험 결과, 정확도·단계별 상태 | [historical_results](historical_results/README.md) |
| STOP 검출 비교와 171건 탐색적 검토 | [stopping_analysis](stopping_analysis/README.md) |
| 원본 GPT·GPT 재실행 1/2·Claude·DeepSeek 분류와 일치도 | [error_taxonomy](error_taxonomy/README_KO.md) |
| 모델 ID·실행 설정·근거·미확인 정보 | [model_information](model_information/README.md) |
| 숫자·문항·파일 해시 검증 | [verification](verification/README.md) |

먼저 Excel이나 각 폴더의 설명을 읽고, 자세한 응답은 모델별 JSON에서 확인할 수 있습니다. 데이터 재사용 기준은 CSV/JSON이며 Excel은 같은 표를 읽기 쉽게 보여주는 사본입니다.

STOP 분석은 검사 가능한 Critic 응답 6,559건을 분모로 합니다. 기존 검출 1,579건, 정확한 종료 표식 1,408건, 공백·개행·대소문자 차이를 허용한 종료 표식 1,416건입니다. 171건의 탐색적 검토를 오탐률 0%나 독립 임상 판정으로 해석하지 않습니다.

본실험 13개 결과 중 11개는 원본과 바이트가 같고, 두 파일은 실패 26건의 내부 오류 기록만 공개용 문장으로 바뀌었습니다. 문항·답변·점수 등 나머지 값은 같습니다. [변경 내역](historical_results/transformations.csv)에 원본과 공개본의 관계를 기록했습니다.

Comment 9의 최종 반복 생성 실험·dispersion 자료는 포함하지 않았습니다. 이 자료의 부재로 현재 다른 환경에서 실행 중인 실험 상태를 판단할 수는 없습니다. 과거 설정, 연구자 확인 내용, revision 새 설정은 구분해 표기했습니다.

사람 평가 200건, 한글/영문 답변서 초안, API 키, 실제 환경설정 파일, 내부 운영 로그는 이번 공개 대상에 포함하지 않았습니다. 문항의 출처·라이선스 표기 차이와 모델 출처의 미확인 사항은 [공개 범위](PUBLICATION_STATUS.md)와 [출처 안내](DATA_SOURCES.md)를 참고하세요.
