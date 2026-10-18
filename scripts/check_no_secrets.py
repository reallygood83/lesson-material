#!/usr/bin/env python3
"""공개 저장소에 개인정보·비밀값이 없는지 텍스트 파일을 검사한다."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {'.git', '.venv', 'venv', '__pycache__', '.agents', '.claude'}
SKIP_SUFFIXES = {
    '.png', '.jpg', '.jpeg', '.gif', '.webp', '.pdf', '.pptx', '.ppt',
    '.pyc', '.ttf', '.otf', '.ttc', '.woff', '.woff2', '.zip',
}
PATTERNS = (
    (re.compile('/Users' + '/[A-Za-z0-9._-]+/'), '개인 홈 경로'),
    (re.compile(r'(?i)[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}'), '이메일 주소'),
    (re.compile('codex mcp ' + 'list'), '비밀값을 출력할 수 있는 명령'),
    (re.compile(r'(?i)(api[_-]?key|secret[_-]?key|access[_-]?token)\s*[:=]\s*\S+'), '자격 증명'),
    (re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----'), '개인 키'),
    (re.compile(r'\bsk-[A-Za-z0-9]{20,}'), 'API 키 형태'),
    (re.compile(r'\bgh[pousr]_[A-Za-z0-9]{20,}'), 'GitHub 토큰'),
    (re.compile(r'\bAKIA[0-9A-Z]{16}\b'), 'AWS 키'),
    (re.compile(r'\bxox[baprs]-[A-Za-z0-9-]{10,}'), '슬랙 토큰'),
)


def main():
    errors = 0
    for path in ROOT.rglob('*'):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in SKIP_SUFFIXES:
            continue
        data = path.read_bytes()
        if b'\0' in data:
            continue
        text = data.decode('utf-8', errors='replace')
        for pattern, label in PATTERNS:
            match = pattern.search(text)
            if match:
                relative = path.relative_to(ROOT)
                print(f'FAIL {relative}: {label}: {match.group(0)[:80]}')
                errors += 1
    if errors:
        print(f'secrets_fail count={errors}')
        return 1
    print('secrets_ok')
    return 0


if __name__ == '__main__':
    sys.exit(main())
