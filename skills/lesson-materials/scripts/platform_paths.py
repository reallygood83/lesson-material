#!/usr/bin/env python3
"""Find Chrome/Chromium and a Korean font on macOS, Linux, and Windows."""
import os
from pathlib import Path
import shutil
import subprocess

# Family names teachers' computers already have. Earlier entries win.
FONT_PREFERENCE = (
    'Apple SD Gothic Neo',
    'Malgun Gothic',
    '맑은 고딕',
    'Noto Sans CJK KR',
    'Noto Sans KR',
    'Noto Sans CJK',
    'NanumGothic',
    '나눔고딕',
    'NanumBarunGothic',
    '나눔바른고딕',
    'NanumMyeongjo',
    '나눔명조',
    'WenQuanYi Micro Hei',
)

# Used when no Korean font is installed. PowerPoint/구글 슬라이드가 있는 글꼴로 바꿉니다.
FALLBACK_FAMILY = 'Malgun Gothic'


class KoreanFont:
    def __init__(self, family, path=None):
        self.family = family
        self.path = Path(path) if path else None

    def __repr__(self):
        return f'KoreanFont(family={self.family!r}, path={self.path!r})'


def find_chrome():
    """Return a Chrome or Chromium executable path, or None."""
    override = os.environ.get('LESSON_CHROME', '').strip()
    if override:
        path = Path(override).expanduser()
        if path.is_file():
            return str(path)
        found = shutil.which(override)
        if found:
            return found

    candidates = []
    home = Path.home()
    local = os.environ.get('LOCALAPPDATA', '')
    program_dirs = [
        os.environ.get('PROGRAMFILES', r'C:\Program Files'),
        os.environ.get('PROGRAMFILES(X86)', r'C:\Program Files (x86)'),
    ]
    mac_apps = (
        'Google Chrome',
        'Chromium',
        'Google Chrome Beta',
        'Google Chrome Canary',
    )
    for base in (Path('/Applications'), home / 'Applications'):
        for app in mac_apps:
            exe = app
            candidates.append(base / f'{app}.app' / 'Contents' / 'MacOS' / exe)
    for folder in program_dirs:
        if not folder:
            continue
        root = Path(folder)
        candidates.append(root / 'Google' / 'Chrome' / 'Application' / 'chrome.exe')
        candidates.append(root / 'Google' / 'Chrome Beta' / 'Application' / 'chrome.exe')
        candidates.append(root / 'Chromium' / 'Application' / 'chrome.exe')
    if local:
        candidates.append(Path(local) / 'Google' / 'Chrome' / 'Application' / 'chrome.exe')
    linux_names = (
        'google-chrome-stable',
        'google-chrome',
        'chromium',
        'chromium-browser',
        'google-chrome-beta',
        'chrome',
    )
    for name in linux_names:
        found = shutil.which(name)
        if found:
            candidates.append(Path(found))
    for path in (
        Path('/usr/bin/google-chrome-stable'),
        Path('/usr/bin/google-chrome'),
        Path('/usr/bin/chromium'),
        Path('/usr/bin/chromium-browser'),
        Path('/snap/bin/chromium'),
    ):
        candidates.append(path)

    seen = set()
    for candidate in candidates:
        try:
            resolved = candidate.resolve()
        except OSError:
            continue
        key = str(resolved)
        if key in seen:
            continue
        seen.add(key)
        if candidate.is_file():
            return str(candidate)
    return None


def _known_font_files():
    windir = Path(os.environ.get('WINDIR', r'C:\Windows'))
    pairs = (
        ('/System/Library/Fonts/AppleSDGothicNeo.ttc', 'Apple SD Gothic Neo'),
        ('/System/Library/Fonts/Supplemental/AppleSDGothicNeo.ttc', 'Apple SD Gothic Neo'),
        ('/Library/Fonts/AppleSDGothicNeo.ttc', 'Apple SD Gothic Neo'),
        (str(windir / 'Fonts' / 'malgun.ttf'), 'Malgun Gothic'),
        ('/usr/share/fonts/truetype/nanum/NanumGothic.ttf', 'NanumGothic'),
        ('/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf', 'NanumBarunGothic'),
        ('/usr/share/fonts/opentype/noto/NotoSansCJKkr-Regular.otf', 'Noto Sans CJK KR'),
        ('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 'Noto Sans CJK KR'),
        ('/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc', 'Noto Sans CJK KR'),
        (str(Path.home() / '.local/share/fonts/NotoSansKR-Regular.otf'), 'Noto Sans KR'),
        (str(Path.home() / 'Library/Fonts/NotoSansKR-Regular.otf'), 'Noto Sans KR'),
    )
    found = []
    for raw, family in pairs:
        path = Path(raw)
        if path.is_file():
            found.append((path, family, 'Regular'))
    return found


def _from_fontconfig():
    if not shutil.which('fc-list'):
        return []
    try:
        proc = subprocess.run(
            ['fc-list', ':lang=ko', '--format', '%{file}\t%{family}\t%{style}\n'],
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (OSError, subprocess.TimeoutExpired):
        return []
    if proc.returncode != 0:
        return []
    found = []
    for line in proc.stdout.splitlines():
        parts = line.split('\t')
        if len(parts) < 2 or not parts[0].strip():
            continue
        path = Path(parts[0].strip())
        family = parts[1].strip()
        style = parts[2].strip() if len(parts) > 2 else ''
        if path.is_file() and family:
            found.append((path, family, style))
    return found


def _rank(path, family, style):
    names = [part.strip().lower() for part in family.split(',') if part.strip()]
    preference = len(FONT_PREFERENCE)
    for index, wanted in enumerate(FONT_PREFERENCE):
        if wanted.lower() in names:
            preference = index
            break
    style_key = style.lower()
    regular = 0 if style_key in ('', 'regular', 'normal', 'book', 'roman') else 1
    suffix = path.suffix.lower()
    embeddable = 0 if suffix in ('.ttf', '.otf') else 1
    return (preference, regular, embeddable, str(path))


def _primary_family(family):
    for part in family.split(','):
        name = part.strip()
        if name and all(ord(ch) < 128 for ch in name):
            return name
    return family.split(',')[0].strip()


def find_korean_font():
    """Return the best installed Korean font. Family is always set."""
    file_override = os.environ.get('LESSON_FONT_FILE', '').strip()
    family_override = os.environ.get('LESSON_FONT_FAMILY', '').strip()
    if file_override or family_override:
        path = Path(file_override).expanduser() if file_override else None
        if path and not path.is_file():
            path = None
        return KoreanFont(family_override or FALLBACK_FAMILY, path)

    rows = _from_fontconfig()
    seen = set()
    for path, _family, _style in rows:
        try:
            seen.add(path.resolve())
        except OSError:
            continue
    for item in _known_font_files():
        try:
            key = item[0].resolve()
        except OSError:
            continue
        if key not in seen:
            rows.append(item)
            seen.add(key)
    if not rows:
        return KoreanFont(FALLBACK_FAMILY, None)
    path, family, _style = min(rows, key=lambda item: _rank(*item))
    return KoreanFont(_primary_family(family), path)


if __name__ == '__main__':
    chrome = find_chrome()
    font = find_korean_font()
    print(f'chrome={chrome or "NOT_FOUND"}')
    print(f'font_family={font.family}')
    print(f'font_file={font.path or "NOT_FOUND"}')
