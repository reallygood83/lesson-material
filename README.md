# 수업자료 스킬 (lesson-materials)

대한민국 초·중·고 교사가 학년·과목·단원을 말하면, 수업 자료를 같은 규칙으로 만드는 에이전트 스킬입니다. Aside, OpenAI Codex, Claude Code, Gemini CLI처럼 `SKILL.md`를 읽는 도구와, 스킬 폴더가 없는 ChatGPT 프로젝트·Gemini Gems에서 같은 지침으로 움직이게 저장소를 구성했습니다.

스킬의 기준 본문은 `skills/lesson-materials/` 한 폴더입니다. 도구마다 파일을 만드는 방법만 다릅니다.

## 무엇을 만드나요

학년·과목·단원이 있으면 바로 만듭니다. 학년이 없으면 학년만 물어봅니다. 차시 목표가 없으면 그 단원 1차시 도입용이라고 밝히고 만듭니다.

1. **구글 슬라이드.** 제목은 「슬라이드 N: 제목」. 발표자 노트에 구어체 대본. 도입 멘트, 정리 발문, 오개념 1장. 그림은 도형으로 그립니다.
2. **활동지 PDF.** A4. 학생용(문제만)과 교사용(정답·지도 메모).
3. **퀴즈 PDF 두 개.** 5문항 내외의 문제지와, 정답·해설. 점수·등급·서열은 만들지 않습니다.
4. **수업용 AI 프롬프트.** Gemini Gems와 NotebookLM에 붙여 넣는 문장.

2022 개정 성취기준은 코드와 원문을 [NCIC](https://www.ncic.re.kr) 등 공개 자료에서 확인합니다. 확인하지 못하면 `[확인 필요]`를 붙입니다. 교육과정 밖이면 「교육과정 외 내용입니다」라고 적습니다. 계산은 검산하고, 교과서 지문·기출 문항은 그대로 옮기지 않습니다. 학생 실명과 개인정보가 들어 있는 요청은 만들지 않습니다. 모든 결과 맨 아래에 다음 문장을 넣습니다.

> ※ 초안입니다. 수업 전 반드시 검토하세요.

파일 공유 설정은 바꾸지 않습니다. 로그인이 필요하면 교사가 직접 로그인합니다.

## 사용 예

도구에 이렇게 말합니다.

```text
5학년 수학 약분과 통분 수업자료 만들어 줘
```

학년·과목·단원이 있으므로 추가 질문 없이 1차시 도입(약분)으로 만들기 시작합니다. 통분은 다음 차시로 안내합니다. 같은 요청으로 만든 작은 샘플이 `examples/5학년_수학_약분/`에 있습니다. 슬라이드 7장, 활동지, 퀴즈 5문항, AI 프롬프트입니다.

## 어떤 도구에 어떻게 넣나요

공통 폴더는 `skills/lesson-materials/`입니다. `SKILL.md` 첫머리의 `name: "lesson-materials"`는 큰따옴표 문자열입니다. Aside 검증기가 이 표기를 요구합니다. 큰따옴표는 YAML 문법이므로 Codex, Claude Code, Gemini CLI가 읽는 이름은 `lesson-materials`와 같습니다.

| 도구 | 설치 |
| --- | --- |
| Codex | `~/.agents/skills/lesson-materials/` 에 폴더를 복사합니다. 이 저장소를 연 상태라면 `<저장소>/.agents/skills/lesson-materials/` 도 읽습니다. |
| Gemini CLI | 사용자 스킬로 `~/.agents/skills/` 또는 `~/.gemini/skills/`를 읽습니다. 이 저장소는 Codex와 같은 `~/.agents/skills/`에 넣습니다. 워크스페이스는 `.agents/skills/` 또는 `.gemini/skills/`입니다. |
| Claude Code | `~/.claude/skills/lesson-materials/SKILL.md` (이 컴퓨터의 모든 프로젝트). 저장소 공유는 `.claude/skills/lesson-materials/SKILL.md`. |
| Aside | 아래 Aside 절. 설치 스크립트는 복사하지 않습니다. |
| 그 밖의 SKILL.md 도구 | 그 도구 문서에 나온 스킬 폴더에 `lesson-materials` 폴더를 넣습니다. 형식은 [Agent Skills 규격](https://agentskills.io/specification)을 따릅니다. |
| ChatGPT 프로젝트, Gemini Gems | 스킬 폴더가 없습니다. `skills/lesson-materials/custom-instructions.txt` 전체를 프로젝트 지침 또는 Gem 지침에 붙여 넣습니다. |

호출 예: Codex는 `$lesson-materials` 또는 `/skills`, Claude Code는 `/lesson-materials`, Gemini CLI는 `/skills`에서 목록을 확인합니다. 설명과 맞는 수업 준비 요청이면 이름을 부르지 않아도 스킬이 켜질 수 있습니다.

### 설치 스크립트

macOS와 리눅스, Windows의 Git Bash에서 저장소 루트로 실행합니다.

```bash
chmod +x install.sh
./install.sh
```

기본 동작은 사용자 폴더 두 곳입니다.

- `~/.agents/skills/lesson-materials` (Codex, Gemini CLI)
- `~/.claude/skills/lesson-materials` (Claude Code)

이미 같은 폴더가 있으면 `lesson-materials.bak.날짜시간`으로 옮긴 뒤 바꿉니다.

```bash
./install.sh --repo          # 이 저장소의 .agents/skills 와 .claude/skills
./install.sh --codex         # Codex·Gemini CLI 경로만
./install.sh --claude        # Claude Code 경로만
./install.sh --help
```

Windows에서 bash가 없으면 WSL이나 Git Bash로 같은 명령을 실행합니다. 스크립트 없이 할 때는 `skills/lesson-materials` 폴더를 위 경로에 그대로 복사하면 됩니다.

### Aside

1. Aside 채팅의 내장 skill-creator에게 `SKILL.md`와 `references/` 두 파일을 주고 `lesson-materials` 스킬을 만들게 합니다. 스크립트와 `assets/`도 함께 넣으면 PDF·pptx 경로까지 스킬 안에 남습니다.
2. 사용자 스킬 위치는 `~/.aside/u/<계정>/skills/user/lesson-materials/` 입니다. `<계정>`은 사람마다 다릅니다. 넣은 뒤 설정 > Skills에 보이는지 확인합니다.
3. Project의 AGENTS.md에 `custom-instructions.txt`를 붙여 그 Project를 선택한 채팅에서만 쓸 수 있습니다.

자세한 순서는 [docs/aside-registration.md](docs/aside-registration.md)에 있습니다. Aside 경로 중 skill-creator로 만드는 방법을 우선으로 안내합니다. 폴더 위치는 앱에서 확인한 경로이며, Aside 공식 문서 URL은 이 저장소에 적지 않았습니다.

### ChatGPT 프로젝트와 Gemini Gems

`skills/lesson-materials/custom-instructions.txt`를 열고 전체를 복사해 지침란에 붙입니다. 파일을 직접 만들 수 없는 도구는 슬라이드 대본, 활동지, 문제지, 정답·해설, AI 프롬프트를 채팅에 나누어 적습니다. 구글 슬라이드와 문서를 직접 열 수 있으면 그 형식으로 파일을 만듭니다.

## 필요한 환경

브라우저만 쓰는 Aside, 지침만 붙이는 ChatGPT·Gems는 Python이 필요 없습니다.

코딩 도구에서 `.pptx`와 PDF를 만들 때:

```bash
python -m venv ~/.venvs/lesson-materials
~/.venvs/lesson-materials/bin/python -m pip install -r requirements.txt
```

`uv`를 쓰면 다음도 같습니다.

```bash
uv venv ~/.venvs/lesson-materials
uv pip install --python ~/.venvs/lesson-materials/bin/python python-pptx pypdfium2 pypdf
```

이 저장소에서 확인한 버전은 python-pptx 1.0.2, pypdf 6.21.1, pypdfium2 5.14.0입니다. `requirements.txt`는 그 버전 이상을 적습니다.

- **Google Chrome** 또는 Chromium. PDF 변환에 씁니다. macOS는 `/Applications/Google Chrome.app`, Windows는 `Program Files\Google\Chrome\Application\chrome.exe`와 사용자 AppData의 Chrome, 리눅스는 `google-chrome` 또는 `chromium`을 찾습니다. 다른 경로면 환경 변수 `LESSON_CHROME`에 실행 파일을 지정합니다.
- **한글 글꼴.** macOS의 Apple SD Gothic Neo, Windows의 맑은 고딕(Malgun Gothic), 리눅스의 나눔고딕이나 Noto Sans CJK. `.ttf` 또는 `.otf`를 찾으면 PDF에 넣습니다. 글꼴 파일을 직접 지정하려면 `LESSON_FONT_FILE`과 `LESSON_FONT_FAMILY`를 씁니다.

지금 쓰는 경로를 보려면:

```bash
python skills/lesson-materials/scripts/platform_paths.py
```

## 알려진 문제

- Codex의 workspace-write 샌드박스에서는 Chrome이 바로 종료되어 PDF가 안 만들어질 수 있습니다. 샌드박스 밖에서 실행 승인을 받은 뒤 다시 만듭니다.
- macOS Chrome은 한글을 Type3 글꼴로 PDF에 넣는 경우가 있습니다. 검사 결과의 `type3_inline`은 임베드된 것으로 보고, `missing=0`인지만 확인합니다.
- Google Drive 플러그인이 없으면 Codex는 `.pptx`만 줍니다. 드라이브에 올리면 구글 슬라이드로 열립니다. 플러그인의 가져오기 도구가 있으면 편집 가능한 구글 슬라이드로 가져오는 단계까지 합니다.
- 리눅스 컨테이너에서 Chrome이 샌드박스 없이 실행되어야 할 때가 있습니다. 스크립트는 그런 환경에서 한 번 더 시도하고, 성공하면 `chrome_mode`에 그 사실을 출력합니다.
- 글꼴이 없는 컴퓨터의 pptx에는 `Malgun Gothic`이라는 이름만 들어갑니다. 그 컴퓨터에 글꼴이 없으면 다른 글꼴로 보입니다.

## 폴더 구조

```text
skills/lesson-materials/          스킬 본문. 설치하면 이 폴더가 통째로 복사됩니다.
  SKILL.md                        규칙과 도구별 경로
  custom-instructions.txt         ChatGPT·Gems·Aside Project에 붙여 넣는 지침
  references/                     성취기준 확인, 결과물 형식
  scripts/                        pptx·PDF 생성, Chrome·글꼴 찾기
  assets/a4.css                   A4 조판
  agents/openai.yaml              Codex에 보이는 이름과 기본 문장
examples/5학년_수학_약분/         샘플 원본과 만들어진 pptx·PDF
docs/                             Codex에서 스킬을 만든 과정, Aside 등록
scripts/                          저장소용 검사 (프런트매터, 비밀값)
.github/workflows/skill-check.yml GitHub Actions 검사
install.sh
requirements.txt
LICENSE                           MIT, 저작권자 reallygood83
```

Codex에서 스킬을 만들고 고친 프롬프트 전문은 [docs/codex-skill-creation.md](docs/codex-skill-creation.md)에 있습니다.

## 라이선스

[MIT](LICENSE)입니다. 저작권자는 reallygood83입니다. 교과서 지문, 기출 문항 등 제삼자의 저작물은 이 저장소에 넣지 않습니다. 샘플 문항은 이 저장소를 위해 새로 썼습니다.

## 출처

설치 경로는 아래 문서에서 확인한 것만 적었습니다.

- Codex 스킬 위치(`~/.agents/skills`, 저장소 `.agents/skills`): https://developers.openai.com/codex/skills
- Claude Code 스킬 위치(`~/.claude/skills`, 저장소 `.claude/skills`): https://code.claude.com/docs/en/skills
- Gemini CLI 스킬 위치(`~/.gemini/skills`, `~/.agents/skills`, 워크스페이스 `.gemini/skills`, `.agents/skills`): https://geminicli.com/docs/cli/skills/
- SKILL.md 공통 형식: https://agentskills.io/specification
- Codex 플러그인: https://developers.openai.com/codex/plugins
- 성취기준: https://www.ncic.re.kr

※ 초안입니다. 수업 전 반드시 검토하세요.
