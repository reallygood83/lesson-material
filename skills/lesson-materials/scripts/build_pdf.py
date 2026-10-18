#!/usr/bin/env python3
"""Typeset local HTML with Chrome; inspect PDF fonts and optionally render PNGs."""
import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

from pypdf import PdfReader

sys.path.insert(0, str(Path(__file__).resolve().parent))
from platform_paths import find_chrome, find_korean_font


def font_report(resources, seen, stats):
    """Count fonts; Type3 fonts (Chrome on macOS) carry their glyphs inside the PDF."""
    resources = resources.get_object() if hasattr(resources, 'get_object') else resources
    fonts = resources['/Font'] if '/Font' in resources else {}
    for name, ref in fonts.items():
        font = ref.get_object()
        if font.get('/Subtype') == '/Type3':
            stats['type3'] += 1
            continue
        ok = False
        for child in font.get('/DescendantFonts', [font]):
            desc = child.get_object().get('/FontDescriptor')
            desc = desc.get_object() if desc else {}
            ok = ok or any(k in desc for k in ('/FontFile', '/FontFile2', '/FontFile3'))
        stats['embedded' if ok else 'missing'] += 1
        if not ok:
            print(f"font NOT embedded: {font.get('/BaseFont', name)}")
    objects = resources['/XObject'] if '/XObject' in resources else {}
    for ref in objects.values():
        obj = ref.get_object()
        if id(obj) not in seen and obj.get('/Resources'):
            seen.add(id(obj))
            font_report(obj['/Resources'], seen, stats)


def _inline_stylesheets(html, source):
    def replace(match):
        tag = match.group(0)
        href_match = re.search(r'href=["\']([^"\']+)["\']', tag, re.I)
        if not href_match:
            return tag
        href = href_match.group(1)
        if href.startswith(('http://', 'https://', 'data:')):
            return tag
        css_path = (source.parent / href).resolve()
        if not css_path.is_file():
            return tag
        return '<style>\n' + css_path.read_text(encoding='utf-8') + '\n</style>'

    return re.sub(r'<link\b[^>]*>', replace, html, flags=re.I)


def prepare_html(source, font):
    """Copy HTML to a temp folder and attach a Korean font Chrome can embed."""
    directory = Path(tempfile.mkdtemp(prefix='lesson-html-'))
    text = _inline_stylesheets(source.read_text(encoding='utf-8'), source)
    blocks = []
    if font.path and font.path.suffix.lower() in ('.ttf', '.otf'):
        suffix = font.path.suffix.lower()
        shutil.copy(font.path, directory / f'lesson-hangul{suffix}')
        css_format = 'opentype' if suffix == '.otf' else 'truetype'
        blocks.append(
            '<style>\n'
            '@font-face {\n'
            '  font-family: "LessonHangul";\n'
            f'  src: url("lesson-hangul{suffix}") format("{css_format}");\n'
            '  font-weight: normal;\n'
            '  font-style: normal;\n'
            '}\n'
            f'body {{ font-family: "LessonHangul", "{font.family}", sans-serif; }}\n'
            '</style>'
        )
    else:
        blocks.append(f'<style>body {{ font-family: "{font.family}", sans-serif; }}</style>')
    injection = '\n'.join(blocks)
    if re.search(r'<head\b', text, re.I):
        text = re.sub(r'(<head\b[^>]*>)', r'\1\n' + injection, text, count=1, flags=re.I)
    else:
        text = injection + '\n' + text
    target = directory / 'index.html'
    target.write_text(text, encoding='utf-8')
    return directory, target


def _sandbox_failure(returncode, stderr):
    if returncode in {133, 134, 139, -5, -6, -11}:
        return True
    text = (stderr or '').lower()
    needles = (
        'no usable sandbox',
        'namespace',
        'zygote',
        'seccomp',
        'sigabrt',
        'aborted',
        'no-sandbox',
        'running as root',
    )
    return any(needle in text for needle in needles)


def _in_container():
    if hasattr(os, 'geteuid') and os.geteuid() == 0:
        return True
    return Path('/.dockerenv').is_file() or Path('/run/.containerenv').is_file()


def chrome_to_pdf(chrome, html, pdf):
    def run(extra):
        with tempfile.TemporaryDirectory(prefix='lesson-chrome-') as profile:
            command = [
                chrome, '--headless=new', '--disable-gpu', '--no-pdf-header-footer',
                '--no-first-run', '--no-default-browser-check',
                '--disable-dev-shm-usage', '--virtual-time-budget=15000',
                f'--user-data-dir={profile}', f'--print-to-pdf={pdf}',
                *extra, html.as_uri(),
            ]
            return subprocess.run(
                command, check=False, capture_output=True, text=True, timeout=120,
            )

    first_extra = ['--no-sandbox'] if _in_container() else []
    try:
        result = run(first_extra)
    except subprocess.TimeoutExpired:
        return False, 'Chrome PDF conversion timed out after 120 seconds.'
    if pdf.is_file() and pdf.stat().st_size and result.returncode == 0:
        mode = 'no-sandbox' if first_extra else 'sandbox'
        return True, mode
    stderr = (result.stderr or '') + (result.stdout or '')
    if not first_extra and _sandbox_failure(result.returncode, stderr):
        if pdf.exists():
            pdf.unlink()
        try:
            retried = run(['--no-sandbox'])
        except subprocess.TimeoutExpired:
            return False, 'Chrome PDF conversion timed out after 120 seconds.'
        if pdf.is_file() and pdf.stat().st_size and retried.returncode == 0:
            return True, 'retried_without_sandbox'
        stderr = (retried.stderr or '') + (retried.stdout or '')
        result = retried
    detail = ' '.join(stderr.split())[:1500] or 'No browser diagnostics.'
    return False, (
        f'Chrome PDF conversion failed (exit {result.returncode}). {detail} '
        'Codex workspace-write 샌드박스에서는 Chrome이 끝날 수 있습니다. '
        '샌드박스 밖에서 다시 실행해 주세요.'
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('html', type=Path)
    parser.add_argument('pdf', type=Path)
    parser.add_argument('--render-dir', type=Path)
    args = parser.parse_args()
    source, target = args.html.resolve(), args.pdf.resolve()
    if not source.is_file():
        parser.error(f'HTML not found: {source}')
    if target.exists():
        parser.error(f'Output already exists: {target}')
    chrome = find_chrome()
    if not chrome:
        parser.error('Install Google Chrome or Chromium, or set LESSON_CHROME to the executable.')
    font = find_korean_font()
    target.parent.mkdir(parents=True, exist_ok=True)
    html_dir, html_path = prepare_html(source, font)
    try:
        ok, detail = chrome_to_pdf(chrome, html_path, target)
    finally:
        shutil.rmtree(html_dir, ignore_errors=True)
    if not ok:
        parser.exit(1, detail + '\n')
    if not target.is_file() or not target.stat().st_size:
        raise RuntimeError('Chrome did not create a PDF.')
    reader = PdfReader(target)
    print(f'pdf={target} pages={len(reader.pages)} chrome={chrome} chrome_mode={detail}')
    print(f'font_family={font.family} font_file={font.path or "NOT_FOUND"}')
    stats = {'embedded': 0, 'type3': 0, 'missing': 0}
    for page in reader.pages:
        font_report(page.get('/Resources', {}), set(), stats)
    print(f"fonts embedded={stats['embedded']} type3_inline={stats['type3']} missing={stats['missing']}")
    if args.render_dir:
        import pypdfium2 as pdfium
        args.render_dir.mkdir(parents=True, exist_ok=True)
        with pdfium.PdfDocument(str(target)) as document:
            for index in range(len(document)):
                page = document[index]
                bitmap = page.render(scale=1.5)
                try:
                    path = args.render_dir / f'page-{index + 1:03}.png'
                    bitmap.to_pil().save(path)
                    print(f'png={path.resolve()}')
                finally:
                    bitmap.close()
                    page.close()


if __name__ == '__main__':
    main()
