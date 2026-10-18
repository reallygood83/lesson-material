# 샘플: 5학년 수학 약분과 통분, 1차시 도입

차시 목표를 말하지 않은 요청 「5학년 수학 약분과 통분」에 맞춰, 약분을 처음 만나는 1차시 도입으로 만든 작은 예시입니다. 통분은 다음 차시로 안내합니다.

성취기준 문장 「[6수01-06] 크기가 같은 분수를 만드는 방법을 이해하고, 분수를 약분, 통분할 수 있다.」는 경기도교육청이 2026년 2월에 공개한 5~6학년 수업-평가 계획 PDF에서 확인했습니다.

https://www.goe.go.kr/resource/goe/na/bbs_2675/2026/02/116dc7a4-254a-44fe-9e77-3e908ecc5ff3.pdf

NCIC 교과 교육과정 원문 파일과 한 번 더 대조한 뒤 수업에 쓰세요. 문항은 이 저장소에서 새로 썼고, 교과서 지문이나 기출 문항을 옮기지 않았습니다.

## 파일

| 파일 | 내용 |
| --- | --- |
| `slides.json` | 슬라이드 7장 명세. 4·5장에 분수 막대 도형 |
| `수업자료.pptx` | `build_pptx.py`로 만든 16:9 덱 7장. 발표자 노트와 분수 막대 도형 포함 |
| `활동지.html`, `활동지.pdf` | 학생용 2쪽 다음 교사용 2쪽 |
| `퀴즈_문제지.html`, `퀴즈_문제지.pdf` | 5문항 1쪽. 점수·등급 없음 |
| `퀴즈_정답해설.html`, `퀴즈_정답해설.pdf` | 정답과 오답 보기 해설 2쪽 |
| `AI_프롬프트.txt` | Gems·NotebookLM용 프롬프트 |

## 검산해 둔 정답

- 2/4 = 1/2, 4/8 = 1/2. 두 분수는 같다.
- 6/9 = 2/3, 10/16 = 5/8, 12/15 = 4/5, 14/21 = 2/3, 8/12 = 2/3.
- 1/3과 3/5는 같지 않다. 1/2와 2/3도 같지 않고, 1/2 = 2/4이다.
- 15/25 = 3/5, 12/18 = 2/3. 7/9는 공약수가 1뿐이라 더 약분할 수 없다.
- 퀴즈 1번 정답은 ② 2/3, 3번 정답은 ② 2/4이다.

## 다시 만들기

저장소 루트에서, 패키지를 설치한 Python으로 실행합니다. PDF·pptx가 이미 있으면 스크립트가 덮어쓰지 않으므로 지운 뒤 실행합니다.

```bash
python skills/lesson-materials/scripts/build_pptx.py \
  "examples/5학년_수학_약분/slides.json" \
  "examples/5학년_수학_약분/수업자료.pptx"

python skills/lesson-materials/scripts/build_pdf.py \
  "examples/5학년_수학_약분/활동지.html" \
  "examples/5학년_수학_약분/활동지.pdf"

python skills/lesson-materials/scripts/build_pdf.py \
  "examples/5학년_수학_약분/퀴즈_문제지.html" \
  "examples/5학년_수학_약분/퀴즈_문제지.pdf"

python skills/lesson-materials/scripts/build_pdf.py \
  "examples/5학년_수학_약분/퀴즈_정답해설.html" \
  "examples/5학년_수학_약분/퀴즈_정답해설.pdf"
```

※ 초안입니다. 수업 전 반드시 검토하세요.
