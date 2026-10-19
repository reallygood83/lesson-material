#!/usr/bin/env python3
"""SKILL.md 프런트매터와 필수 문구를 검사한다. PyYAML이 있으면 파싱도 한다."""
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / 'skills' / 'lesson-materials'
SKILL = SKILL_DIR / 'SKILL.md'
REQUIRED_FILES = (
    'references/output-formats.md',
    'references/curriculum-check.md',
    'references/pdf-layout.md',
    'scripts/build_pptx.py',
    'scripts/build_pdf.py',
    'scripts/platform_paths.py',
    'scripts/check-print-layout.js',
    'assets/a4.css',
    'assets/exam-print.css',
    'agents/openai.yaml',
    'custom-instructions.txt',
)
PHRASES = (
    '1차시 도입',
    '[확인 필요]',
    '교육과정 외 내용입니다',
    '오개념',
    '※ 초안입니다. 수업 전 반드시 검토하세요.',
    '공유 설정은 바꾸지 않는다',
    '개인정보',
)


def fail(message):
    print(f'FAIL {message}')
    return 1


def unquote(value):
    text = value.strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in '"\'':
        return text[1:-1]
    return text


def main():
    errors = 0
    if not SKILL.is_file():
        return fail(f'없음: {SKILL}')
    raw = SKILL.read_text(encoding='utf-8')
    if raw.startswith('\ufeff'):
        errors += fail('BOM이 있습니다')
    if '\r\n' in raw:
        errors += fail('줄바꿈은 LF여야 합니다')
    if not raw.startswith('---\n'):
        errors += fail('파일은 --- 로 시작해야 합니다')
        return errors
    end = raw.find('\n---\n', 4)
    if end < 0:
        errors += fail('프런트매터 닫는 --- 가 없습니다')
        return errors
    block = raw[4:end]
    lines = [line for line in block.split('\n') if line.strip()]
    keys = []
    fields = {}
    for line in lines:
        if ':' not in line:
            errors += fail(f'프런트매터 형식 오류: {line}')
            continue
        key, value = line.split(':', 1)
        keys.append(key.strip())
        fields[key.strip()] = value.strip()
    if keys != ['name', 'description']:
        errors += fail(f'프런트매터 키는 name, description만 허용: {keys}')
    name_line = fields.get('name', '')
    if name_line != '"lesson-materials"':
        errors += fail('name은 큰따옴표 문자열 "lesson-materials" 여야 합니다')
    description_line = fields.get('description', '')
    if not (description_line.startswith('"') and description_line.endswith('"')):
        errors += fail('description은 큰따옴표 문자열이어야 합니다')
    description = unquote(description_line)
    if not (1 <= len(description) <= 1024):
        errors += fail(f'description 길이는 1~1024자: {len(description)}')
    if SKILL_DIR.name != 'lesson-materials':
        errors += fail('스킬 폴더 이름은 lesson-materials 여야 합니다')
    for relative in REQUIRED_FILES:
        if not (SKILL_DIR / relative).is_file():
            errors += fail(f'필수 파일 없음: {relative}')
    body = raw[end + len('\n---\n'):]
    for phrase in PHRASES:
        if phrase not in body:
            errors += fail(f'SKILL.md에 없음: {phrase}')
    for marker in ('## 5. 도구별 경로', '### 5-A.', '### 5-B.', '### 5-C.'):
        if marker not in body:
            errors += fail(f'SKILL.md에 없음: {marker}')
    instructions_path = SKILL_DIR / 'custom-instructions.txt'
    if instructions_path.is_file():
        instructions = instructions_path.read_text(encoding='utf-8')
        for phrase in PHRASES:
            if phrase not in instructions:
                errors += fail(f'custom-instructions.txt에 없음: {phrase}')
    openai_path = SKILL_DIR / 'agents' / 'openai.yaml'
    if openai_path.is_file():
        openai = openai_path.read_text(encoding='utf-8')
        if 'display_name: "수업자료 만들기"' not in openai:
            errors += fail('agents/openai.yaml display_name이 예상과 다릅니다')

    try:
        import yaml
    except ImportError:
        yaml = None
    if yaml is None:
        message = 'PyYAML이 없어 파싱 검사는 건너뛰었습니다'
        if os.environ.get('REQUIRE_PYYAML') == '1':
            errors += fail(message)
        else:
            print('WARN ' + message)
    else:
        parsed = yaml.safe_load(block)
        if not isinstance(parsed, dict):
            errors += fail('프런트매터 YAML이 사전이 아닙니다')
        elif parsed.get('name') != 'lesson-materials':
            errors += fail(f'파싱된 name이 다릅니다: {parsed.get("name")!r}')
        elif parsed.get('description') != description:
            errors += fail('파싱된 description이 원문과 다릅니다')
        else:
            print(f'yaml_ok name={parsed["name"]} description_chars={len(parsed["description"])}')
    if errors:
        print(f'frontmatter_fail count={errors}')
        return 1
    print('frontmatter_ok')
    return 0


if __name__ == '__main__':
    sys.exit(main())
