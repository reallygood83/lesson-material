#!/usr/bin/env bash
# 수업자료 스킬을 Codex, Gemini CLI, Claude Code가 읽는 폴더에 복사합니다.
# Aside는 계정마다 경로가 달라 복사하지 않고 안내만 출력합니다.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="${ROOT}/skills/lesson-materials"
NAME="lesson-materials"

if [[ ! -f "${SRC}/SKILL.md" ]]; then
  echo "스킬 원본을 찾지 못했습니다: ${SRC}/SKILL.md" >&2
  exit 1
fi

do_user=0
do_repo=0
do_codex=0
do_claude=0

usage() {
  cat <<'EOF'
사용법: ./install.sh [--user] [--repo] [--codex] [--claude]

--user    이 컴퓨터의 사용자 스킬 폴더에 설치합니다. 옵션을 생략하면 이 값이 기본입니다.
          Codex, Gemini CLI: ~/.agents/skills/lesson-materials
          Claude Code:       ~/.claude/skills/lesson-materials
--repo    이 저장소 안에 설치합니다.
          .agents/skills/lesson-materials
          .claude/skills/lesson-materials
--codex   Codex·Gemini CLI 경로만 설치합니다.
--claude  Claude Code 경로만 설치합니다.

--codex와 --claude를 모두 생략하면 두 경로를 모두 설치합니다.
같은 이름의 폴더가 있으면 이름 뒤에 .bak.날짜시간을 붙여 옮긴 뒤 새 폴더로 바꿉니다.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --user) do_user=1 ;;
    --repo) do_repo=1 ;;
    --codex) do_codex=1 ;;
    --claude) do_claude=1 ;;
    -h|--help) usage; exit 0 ;;
    *)
      echo "알 수 없는 옵션: $1" >&2
      usage
      exit 1
      ;;
  esac
  shift
done

if [[ "${do_user}" -eq 0 && "${do_repo}" -eq 0 ]]; then
  do_user=1
fi
if [[ "${do_codex}" -eq 0 && "${do_claude}" -eq 0 ]]; then
  do_codex=1
  do_claude=1
fi

install_one() {
  local dest="$1"
  local parent
  parent="$(dirname "${dest}")"
  mkdir -p "${parent}"
  if [[ -e "${dest}" || -L "${dest}" ]]; then
    local bak="${dest}.bak.$(date +%Y%m%d%H%M%S)"
    mv "${dest}" "${bak}"
    echo "기존 폴더를 백업했습니다: ${bak}"
  fi
  mkdir -p "${dest}"
  cp -a "${SRC}/." "${dest}/"
  echo "설치했습니다: ${dest}"
}

if [[ "${do_user}" -eq 1 && "${do_codex}" -eq 1 ]]; then
  install_one "${HOME}/.agents/skills/${NAME}"
fi
if [[ "${do_user}" -eq 1 && "${do_claude}" -eq 1 ]]; then
  install_one "${HOME}/.claude/skills/${NAME}"
fi
if [[ "${do_repo}" -eq 1 && "${do_codex}" -eq 1 ]]; then
  install_one "${ROOT}/.agents/skills/${NAME}"
fi
if [[ "${do_repo}" -eq 1 && "${do_claude}" -eq 1 ]]; then
  install_one "${ROOT}/.claude/skills/${NAME}"
fi

cat <<'EOF'

Aside는 복사하지 않습니다. 아래 중 하나로 등록하세요.
1. Aside 채팅의 내장 skill-creator에게 skills/lesson-materials/SKILL.md 와 references 두 파일을 주고, 이름이 lesson-materials 인 스킬을 만들게 합니다.
2. ~/.aside/u/<계정>/skills/user/lesson-materials/ 에 스킬 폴더를 넣은 뒤 설정 > Skills에 보이는지 확인합니다. 계정마다 경로가 다릅니다.
3. 스킬 없이 쓰려면 skills/lesson-materials/custom-instructions.txt 를 Project의 AGENTS.md에 붙입니다.

ChatGPT 프로젝트와 Gemini Gems는 custom-instructions.txt 전체를 지침란에 붙여 넣습니다.
Python으로 PDF·pptx를 만들 때는 저장소의 requirements.txt 를 설치하고, Google Chrome과 한글 글꼴이 필요합니다.
EOF
