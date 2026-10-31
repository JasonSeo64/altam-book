# SOA Exam ALTAM 장기보험수리 — 보충자료

『SOA Exam ALTAM 장기보험수리』(서재영 지음)의 보충자료 저장소입니다.
출제범위는 SOA Exam ALTAM 실라버스 2026년 10월판을 기준으로 합니다.

## 받는 법

- **한 번에 받기:** 오른쪽 **Releases**에서 책의 판에 맞는 버전(초판은 `v1.0`)의 ZIP 파일을 내려받습니다.
- **최신 파일 받기:** 초록색 **Code** 버튼 → **Download ZIP**.

## 들어 있는 것

| 폴더·파일 | 내용 |
|---|---|
| `figures_code/` | 본문 그림을 만드는 파이썬 코드. 장별 `figs_chNN.py`, 공통 스타일 `fig_style.py` |
| `errata.md` | 정오표 |

### 그림 코드 실행

```bash
pip install -r requirements.txt
python figures_code/figs_ch05.py     # → figures/ch05_fig1.png … 가 만들어집니다
```

다중상태모형의 전이력, 연생 생존확률, 보증옵션의 가치 등 모수를 바꿔 실행해 보면 결과가 어떻게 달라지는지 직접 확인할 수 있습니다.
SOA가 제공하는 워크북·공식집·기출문제는 SOA 홈페이지에서 받으세요.

## 정오표·문의

오류를 발견하시면 이 저장소의 **Issues**에 장·쪽·내용을 적어 주세요. 확인된 오류는 `errata.md`에 반영합니다.

## 라이선스

- 코드(`*.py`): MIT License — `LICENSE` 참고
- 그 밖의 자료: © 2026 서재영. 책 본문·문제·해설은 이 저장소에 포함되지 않으며, 무단 전재와 복제를 금합니다.
