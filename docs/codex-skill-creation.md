# Codex에서 수업자료 스킬을 만든 과정

2026-10-18에 Codex에서 `lesson-materials` 스킬을 만들고, 인식 확인과 수업자료 생성, 구글 슬라이드 가져오기 수정을 한 기록입니다. 프롬프트는 그때 사용한 전문입니다.

지금 저장소의 `skills/lesson-materials`는 그 Codex용 스킬과 Aside용 스킬을 한 폴더로 합친 것입니다. 브라우저로 구글 슬라이드·문서를 직접 만드는 경로와, 스크립트로 `.pptx`·PDF를 만든 뒤 드라이브로 가져오는 경로가 함께 들어 있습니다. 아래 프롬프트 ①은 당시 Aside 원본을 Codex 경로만 남기도록 바꾸는 요청이라, 그대로 다시 실행하면 브라우저 경로가 빠집니다. 교사 컴퓨터에는 이 저장소를 받아 `install.sh`로 설치하는 쪽을 권합니다.

개인 경로, 메일 주소, 세션 식별자, 토큰은 적지 않았습니다. 명령 예시의 `~`는 사용자 홈입니다.

## 0. 사전 준비

1. Codex CLI 또는 Codex 앱이 설치되어 있는지 `codex --version`으로 확인합니다.
2. Google Drive 플러그인을 연결합니다. 구글 슬라이드로 가져올 때 필요합니다.
   - CLI: `codex`를 실행하고 `/plugins`를 입력한 뒤 Google Drive를 설치합니다. 연결 안내가 나오면 구글 계정으로 직접 로그인하고, 새 세션을 엽니다.
   - 앱: Plugins 탭에서 Google Drive를 설치하고 연결합니다.
   - 확인: `codex plugin list`에 `google-drive`가 installed, enabled로 보이는지 봅니다.
   - 드라이브 계정이 여러 개면 업로드 전에 어느 계정인지 묻습니다. 그때 계정을 고릅니다.
3. Python 패키지는 한 번만 설치합니다.

```bash
uv venv ~/.venvs/lesson-materials
uv pip install --python ~/.venvs/lesson-materials/bin/python python-pptx pypdfium2 pypdf
```

4. Google Chrome을 설치합니다. macOS 기본 위치는 `/Applications/Google Chrome.app`입니다. HTML을 A4 PDF로 바꿀 때 씁니다.
5. 당시 원본은 Aside용 스킬 폴더 `~/Downloads/lesson-materials/`였습니다. `SKILL.md`와 `references/`가 들어 있었습니다.

플러그인 목록은 `codex plugin list`로 확인합니다. 토큰이나 연결 비밀을 출력하는 명령은 확인용으로 쓰지 않습니다.

## 1. 스킬 만들기

앱이나 대화형 CLI에서는 아래 프롬프트를 붙여 넣으면 됩니다. 비대화형으로 할 때는 프롬프트를 파일로 저장하고, 쓰기 범위를 스킬 폴더로 제한합니다.

```bash
mkdir -p ~/.agents/skills
cd ~/.agents/skills
codex exec -s workspace-write --skip-git-repo-check -C ~/.agents/skills --add-dir /tmp \
  - < 01_create_skill.txt
```

**프롬프트 ① 스킬 생성**

```text
$skill-creator 를 사용해서 Codex 사용자 범위 스킬 `lesson-materials`를 만들어 줘.

[저장 위치]
- ~/.agents/skills/lesson-materials/ (이 폴더 안에만 쓰기. 다른 스킬·설정 파일은 읽기만 하고 바꾸지 말 것)
- 같은 이름 폴더가 이미 있으면 덮어쓰지 말고 멈춘 뒤 알려 줘.

[원본]
- ~/Downloads/lesson-materials/SKILL.md, references/output-formats.md, references/curriculum-check.md 를 읽고 내용(규칙·형식)을 그대로 살려. 이 원본은 Aside 브라우저용이라 아래만 Codex에 맞게 바꿔.

[바꿀 점]
1. 프런트매터: name: lesson-materials, description은 한 줄. 무엇을 하는지와 호출 상황(초·중·고 교사의 수업자료, PPT/구글 슬라이드, 활동지, 형성평가 퀴즈, 성취기준, 차시)을 앞쪽에 넣어. 1024자 이내.
2. 본문 앞부분에 굵게: "계획이나 진행 안내에서도 항상 결과물 형식을 그대로 말한다: PPT는 구글 슬라이드(Google Drive 플러그인으로 생성, 안 되면 .pptx), 활동지는 조판한 A4 PDF(학생용·교사용), 퀴즈는 문제지 PDF와 정답·해설 PDF."
3. '브라우저 경로(Aside)' 장을 'Codex 생성 경로'로 바꿔:
   - PPT 기본 경로: Presentations 플러그인(@presentations)으로 덱을 만들고, Google Drive 플러그인(@google-drive)의 프레젠테이션 가져오기(upload_mode "native_google_slides")로 편집 가능한 구글 슬라이드로 만든다. 대본은 각 슬라이드 발표자 노트. 그림(분수 막대 등)은 도형으로. 만든 뒤 Google Slides 스킬로 장수·노트·글자 겹침을 확인하고 링크를 준다. 공유 설정은 바꾸지 않는다.
   - 대체 경로(플러그인이 없거나 연결 안 됨/실패): scripts/build_pptx.py 로 .pptx 생성(도형 그림, 발표자 노트). "구글 드라이브에 올리면 구글 슬라이드로 열립니다"라고 안내. 선택: 교사가 요청할 때만 `gog drive upload <파일.pptx> --convert-to slides` 로 업로드·변환(gog CLI가 있을 때).
   - 활동지·퀴즈 PDF: HTML+CSS(A4, @page, 한글 폰트 Noto Sans KR/Apple SD Gothic Neo)로 조판 → scripts/build_pdf.py 로 Chrome 헤드리스 PDF 변환 → 폰트 임베드 확인 → 페이지 PNG 렌더해서 눈으로(이미지 보기) 겹침·잘림·한글 깨짐 확인. 파일: 활동지.pdf(학생용 쪽 다음 교사용 쪽), 퀴즈_문제지.pdf, 퀴즈_정답해설.pdf.
   - 결과물은 현재 작업 폴더 아래 <학년>_<과목>_<단원>_<차시>/ 에 모은다.
   - 성취기준: 웹 검색이 되면 NCIC(ncic.re.kr) 원문 확인, 안 되면 [확인 필요].
   - Python은 ~/.venvs/lesson-materials/bin/python 이 있으면 그것(python-pptx, pypdfium2, pypdf 설치됨), 없으면 설치 방법을 안내: `uv venv ~/.venvs/lesson-materials && uv pip install --python ~/.venvs/lesson-materials/bin/python python-pptx pypdfium2 pypdf`.
4. scripts/ 에 짧고 일반적인 스크립트 2개:
   - build_pdf.py: 입력 HTML → PDF(Chrome 헤드리스: /Applications/Google Chrome.app 또는 PATH의 chrome/chromium, --print-to-pdf, --no-pdf-header-footer, 임시 user-data-dir), 이어서 pypdfium2로 페이지 PNG 렌더(옵션), pypdf로 쪽수·폰트 임베드 출력.
   - build_pptx.py: JSON 명세(slides: title, bullets, notes, 선택 shapes[분수 막대: 칸 수·색칠 칸 수]) → 16:9 .pptx. 한글 글꼴 지정, 제목 32pt 이상·본문 20pt 이상.
   - assets/a4.css: A4 조판 기본 스타일(여백 18mm, 본문 11.5pt, 문항 박스, 쪽 나눔 클래스, 맨 아래 초안 문구 스타일).
5. agents/openai.yaml: display_name "수업자료 만들기", short_description 한 줄, default_prompt "5학년 수학 약분과 통분 1차시 수업자료 만들어 줘".
6. 나머지 규칙(학년 없으면 질문, 차시 없으면 1차시 도입용, 오개념 슬라이드, 학생용/교사용, 퀴즈 분리·채점/등급/서열 없음, 검산, 복제 금지, 개인정보 거부, [확인 필요], 맨 아래 "※ 초안입니다. 수업 전 반드시 검토하세요.")은 그대로 유지.

[끝나면]
- skill-creator의 검증 스크립트가 있으면 돌려서 통과시키고, scripts 두 개를 작은 샘플로 실행해 동작을 확인해(샘플 산출물은 /tmp 아래에, 스킬 폴더에는 남기지 말 것).
- 만든 파일 목록과 검증 결과를 짧게 알려 줘.
```

이 저장소의 스킬은 위 1번의 `name`을 Aside에도 맞게 `name: "lesson-materials"`로 통일했습니다. 큰따옴표는 YAML 문자열이므로 Codex가 읽는 이름은 `lesson-materials`입니다.

## 2. 스킬이 인식되는지 확인

```bash
codex exec -s read-only --skip-git-repo-check --ephemeral "<아래 프롬프트>" < /dev/null
```

`codex exec`에 프롬프트를 인자로 줄 때는 `< /dev/null`을 붙입니다. 붙이지 않으면 표준 입력을 더 읽는 상태에서 멈출 수 있습니다.

**프롬프트 ② 확인**

```text
지금 쓸 수 있는 스킬 목록에 lesson-materials 가 있는지, 그 SKILL.md 경로와 description을 알려 줘. 파일은 만들거나 고치지 마.
```

정상이면 `~/.agents/skills/lesson-materials/SKILL.md` 경로와 description을 알려 줍니다.

## 3. 실제로 써 보기

수업자료를 저장할 폴더에서 실행합니다. 예: `~/Documents/수업자료`. PDF를 만들 때 Chrome을 실행하므로, 평소 쓰는 권한 그대로 실행합니다. `-s workspace-write` 샌드박스에서는 Chrome이 바로 종료될 수 있습니다.

```bash
mkdir -p ~/Documents/수업자료 && cd ~/Documents/수업자료
codex exec --skip-git-repo-check -C ~/Documents/수업자료 "<아래 프롬프트>" < /dev/null
```

**프롬프트 ③ 테스트**

```text
$lesson-materials 5학년 수학 약분과 통분 2차시(약분) 수업자료 만들어 줘.
```

앱·CLI 대화창에서는 `$lesson-materials`를 입력하거나 `/skills`로 고릅니다. `$`를 빼고 「수업자료 만들어 줘」라고만 해도 description이 맞으면 스킬이 호출됩니다.

당시 결과 폴더 `5학년_수학_약분과통분_2차시/`에는 다음이 만들어졌습니다.

- `수업자료.pptx`: 슬라이드마다 발표자 노트, 분수 막대는 도형
- `구글슬라이드_링크.txt`: Drive 플러그인으로 가져온 편집 가능 문서. 공유 설정은 바꾸지 않음
- `활동지.pdf`: 학생용 쪽 다음 교사용 쪽, A4
- `퀴즈_문제지.pdf`, `퀴즈_정답해설.pdf`
- `AI_프롬프트.txt`: Gems·NotebookLM 프롬프트

## 4. 고치기

첫 테스트에서 Presentations 전용 도구가 없다는 이유로 구글 슬라이드를 건너뛰고 `.pptx`만 나왔습니다. Google Drive 플러그인의 `google_drive_import_presentation` 도구는 있었기 때문에 아래 프롬프트로 고쳤습니다. 지금 저장소의 5-B 경로는 이 수정이 반영된 순서입니다.

```bash
cd ~/.agents/skills/lesson-materials
codex exec -s workspace-write --skip-git-repo-check -C ~/.agents/skills/lesson-materials - < 04_fix_google_slides.txt
```

**프롬프트 ④ 수정 (구글 슬라이드 경로)**

```text
$skill-creator 로 ~/.agents/skills/lesson-materials 스킬의 'PPT 기본 경로'를 고쳐 줘. 이 스킬 폴더 밖은 바꾸지 마.

문제: 테스트에서 Presentations 플러그인 전용 도구가 없다는 이유로 구글 슬라이드 생성을 통째로 건너뛰고 .pptx만 줬다. 하지만 Google Drive 플러그인은 연결돼 있고 `google_drive_import_presentation`(upload_mode: "native_google_slides") 도구가 있다.

고칠 내용(SKILL.md 5장 'PPT 기본 경로'를 아래 순서로 바꾸기):
1. 먼저 .pptx를 만든다. Presentations 플러그인 도구가 있으면 그것으로, 없으면 scripts/build_pptx.py 로(도형 그림, 발표자 노트에 대본).
2. Google Drive 플러그인의 프레젠테이션 가져오기 도구(이름에 `google_drive_import_presentation`이 들어간 도구)를 찾아 스키마를 읽고, upload_mode "native_google_slides"로 가져와 편집 가능한 구글 슬라이드를 만든다. Presentations 도구가 없어도 이 도구가 있으면 반드시 이 단계를 한다.
3. 가져온 뒤 Drive 플러그인의 프레젠테이션 읽기 도구(get_presentation / get_presentation_outline / get_presentation_text 등)로 장수·발표자 노트·마지막 장 초안 문구를 확인하고, 구글 슬라이드 링크를 결과 폴더의 `구글슬라이드_링크.txt`에도 적는다.
4. 공유 설정은 바꾸지 않는다(기본: 본인만). 위치는 교사가 정하지 않으면 플러그인 기본 위치.
5. Drive 도구가 없거나 로그인이 필요하면: 직접 인증하지 말고 .pptx를 결과로 주며 "Codex 앱 > 플러그인에서 Google Drive를 설치·연결하거나 CLI에서 /plugins 로 설치한 뒤 새 세션에서 다시 요청해 주세요"라고 안내한다. .pptx는 이때의 대체 결과물이다.
6. 본문 앞부분 굵은 문장을 "PPT는 구글 슬라이드(.pptx를 만든 뒤 Google Drive 플러그인으로 구글 슬라이드로 가져옴, 플러그인이 없으면 .pptx)"로 맞춘다.

끝나면 quick_validate.py 를 다시 돌리고 바뀐 부분만 짧게 알려 줘.
```

**프롬프트 ⑤ 수정 (일반 틀)**

```text
$skill-creator 로 ~/.agents/skills/lesson-materials 스킬을 고쳐 줘. 고칠 점: <예: 퀴즈 해설에서 보기 번호와 내용이 어긋나지 않게 확인 단계를 추가>. 이 스킬 폴더 밖은 바꾸지 말고, 고친 뒤 검증 스크립트를 다시 돌려 결과를 알려 줘.
```

업로드 계정을 묻다 멈춘 뒤에는 세션을 이어 갑니다. 실제 세션 식별자는 문서나 채팅 로그에 남기지 말고, Codex가 안내하는 이어가기 절차만 사용합니다. 이어갈 때 넣은 요청은 아래와 같습니다. 계정 이름은 본인 연결 이름으로 바꿉니다.

```text
계정은 "Google 드라이브 — <내 계정>" 연결을 써. 스킬의 PPT 기본 경로대로 수업자료.pptx를 구글 슬라이드로 가져오고(공유 설정 변경 금지), 장수·발표자 노트·마지막 장 초안 문구를 확인한 뒤 링크를 구글슬라이드_링크.txt에 적고 알려 줘.
```

## 5. 설치 위치

공식 문서 기준입니다. 출처는 이 글 맨 아래에 있습니다.

| 범위 | 경로 |
| --- | --- |
| Codex 사용자 | `~/.agents/skills/lesson-materials/` |
| Codex 저장소 | `<저장소>/.agents/skills/lesson-materials/` |
| 관리자 | `/etc/codex/skills` |
| 끄기 | `~/.codex/config.toml`의 `[[skills.config]]`에 해당 `SKILL.md` 경로와 `enabled = false` |

호출은 `$lesson-materials` 또는 `/skills`입니다. 변경은 자동으로 보이며, 안 보이면 Codex를 다시 시작합니다.

Gemini CLI도 사용자 스킬로 `~/.agents/skills/`를 읽습니다. 같은 폴더를 두면 Gemini CLI와 Codex가 함께 봅니다.

## 6. 문제 해결

| 증상 | 해결 |
| --- | --- |
| `codex exec`가 표준 입력을 더 읽는다는 문구에서 멈춤 | 명령 끝에 `< /dev/null`을 붙입니다. |
| 신뢰된 디렉터리 안에서만 실행된다는 안내 | `--skip-git-repo-check`를 추가합니다. |
| PDF 변환 중 Chrome이 바로 종료 | `-s workspace-write` 샌드박스에서 날 수 있습니다. 평소 권한으로 실행하거나 실행 승인을 받습니다. |
| 구글 슬라이드가 안 나오고 `.pptx`만 나옴 | `codex plugin list`에서 google-drive가 켜져 있는지 확인하고, `/plugins`로 연결한 뒤 새 세션에서 다시 요청합니다. |
| 연결 계정 선택에서 대기 | 드라이브 계정이 여러 개인 경우입니다. 쓸 계정을 답하면 이어서 진행합니다. |
| 폰트 확인 결과 `type3_inline` | macOS Chrome이 한글 글리프를 PDF 안에 직접 넣은 경우로, 임베드로 봅니다. `missing=0`인지만 확인합니다. |
| python-pptx 없음 | 0장의 `uv venv` 명령을 실행합니다. |

## 7. 출처

- Codex 스킬 형식, 위치, `$skill-creator`, `$`와 `/skills` 호출: https://developers.openai.com/codex/skills
- Codex 플러그인(Google Drive, CLI `/plugins`): https://developers.openai.com/codex/plugins
- 성취기준 확인처: NCIC 국가교육과정정보센터 https://www.ncic.re.kr
- 당시 약분 예시의 성취기준 문장은 경기도교육청 공개 PDF로 [6수01-06]을 확인했습니다.

※ 초안입니다. 수업 전 반드시 검토하세요.
