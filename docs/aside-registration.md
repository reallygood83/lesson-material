# Aside에 수업자료 스킬 등록하기

Aside에서 이 스킬을 쓰는 방법입니다. 설치 스크립트는 Aside 폴더를 복사하지 않습니다. 계정마다 경로가 다르고, 앱 안에서 만들어 확인하는 쪽이 안전합니다.

아래 경로는 Aside에서 사용자 스킬이 놓이는 위치로 확인한 것입니다. Aside 공식 문서에서 같은 경로를 따로 확인하지는 못했습니다.

## 1. 채팅의 skill-creator로 만들기

이 방법이 우선입니다.

1. 이 저장소의 `skills/lesson-materials/SKILL.md`를 엽니다.
2. `references/` 전체와 `assets/`, `scripts/`도 함께 준비합니다. 정밀 조판에는 `references/pdf-layout.md`, `assets/exam-print.css`, `scripts/check-print-layout.js`가 필요합니다.
3. Aside에서 새 채팅을 열고, 내장 skill-creator에게 `skills/lesson-materials/` 폴더 전체를 제공하거나 이 저장소 링크로 설치를 요청합니다.
4. 이렇게 요청합니다.

```text
이 내용으로 lesson-materials 라는 커스텀 스킬을 만들어 줘.
SKILL.md의 프런트매터 name은 큰따옴표 문자열 name: "lesson-materials" 로 유지해 줘.
references 전체와 scripts, assets, agents/openai.yaml, custom-instructions.txt 도 같은 폴더에 함께 넣어 줘.
특히 references/pdf-layout.md, assets/exam-print.css, scripts/check-print-layout.js 를 빠뜨리지 말아 줘.
```

5. 설정 > Skills에서 `lesson-materials`가 보이는지 확인합니다.
6. 입력창에서 `/`로 스킬을 고르거나, 아래 문장으로 동작만 확인합니다.

```text
5학년 수학 약분과 통분 수업자료 만들어 줘
```

학년·과목·단원이 있으면 질문 없이 만들기 시작하고, 차시를 말하지 않았으므로 1차시 도입용이라고 알려야 합니다. 결과물은 구글 슬라이드, 활동지 PDF, 퀴즈 문제지 PDF, 정답·해설 PDF, 수업용 AI 프롬프트입니다.

## 2. 사용자 스킬 폴더에 넣기

앱이 사용자 스킬을 읽는 위치는 다음과 같습니다.

```text
~/.aside/u/<계정>/skills/user/lesson-materials/
```

`<계정>`은 Aside에 로그인한 계정마다 다릅니다. 저장소의 `skills/lesson-materials` 폴더 내용을 그 위치에 넣습니다. `SKILL.md`가 `.../lesson-materials/SKILL.md`에 있어야 합니다. 넣은 뒤에는 설정 > Skills에 보이는지 확인합니다. 보이지 않으면 1번의 skill-creator 경로를 사용합니다.

## 3. Project 지침으로 쓰기

스킬 목록에 올리지 않고 프로젝트에만 붙일 수 있습니다.

1. Aside에서 새 Project를 만듭니다. 예: 「수업자료」.
2. Project의 AGENTS.md 지침에 `skills/lesson-materials/custom-instructions.txt` 내용 전체를 붙여 넣습니다.
3. 작업을 시작할 때 그 Project를 선택합니다.

이 경로는 스킬의 스크립트·CSS 자원을 자동으로 가져오지 않습니다. 정밀 조판 자원도 쓰려면 1번 또는 2번으로 스킬 폴더 전체를 설치합니다. Aside는 구글 슬라이드를 직접 만들고, 인쇄물은 HTML 정밀 조판을 브라우저에서 PDF로 출력하거나 필요한 경우 구글 문서로 만듭니다.

## 확인하면 좋은 것

- 프런트매터 첫 키가 `name: "lesson-materials"`인지. Aside 검증기는 이름을 큰따옴표 문자열로 요구합니다.
- 만든 슬라이드 발표자 노트에 구어체 대본이 있는지.
- 활동지·퀴즈가 A4 PDF인지, 퀴즈 정답이 문제지와 다른 파일인지.
- 문제지의 수능형 조판과 풀이 공간이 학년에 맞는지, 모든 PDF 쪽을 이미지로 검수했는지.
- 공유 설정을 에이전트가 바꾸지 않았는지.
- 마지막에 「※ 초안입니다. 수업 전 반드시 검토하세요.」가 있는지.

※ 초안입니다. 수업 전 반드시 검토하세요.
