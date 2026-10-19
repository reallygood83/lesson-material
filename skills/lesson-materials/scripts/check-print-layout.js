/* Evaluate this expression in the browser displaying your own print HTML.
   Read-only geometry check. This does not replace inspecting every rendered PDF page. */
(async () => {
  await document.fonts.ready;
  const minGapPx = 2 * 96 / 25.4;
  const draft = '※ 초안입니다. 수업 전 반드시 검토하세요.';
  const unloadedFonts = Array.from(document.fonts)
    .filter(font => font.status !== 'loaded' && font.status !== 'unloaded')
    .map(font => ({ family: font.family, status: font.status }));
  const sheets = Array.from(document.querySelectorAll('.sheet'));
  const pages = sheets.map((sheet, index) => {
    const errors = [];
    const rect = sheet.getBoundingClientRect();
    const contents = sheet.querySelectorAll(':scope > .content');
    const footers = sheet.querySelectorAll(':scope > .footer');
    if (contents.length !== 1) errors.push('Need exactly one direct .content child.');
    if (footers.length !== 1) errors.push('Need exactly one direct .footer child.');
    const content = contents[0];
    const footer = footers[0];
    let contentBottom = content?.getBoundingClientRect().bottom ?? rect.top;
    let left = content?.getBoundingClientRect().left ?? rect.left;
    let right = content?.getBoundingClientRect().right ?? rect.right;
    if (content) {
      for (const child of content.querySelectorAll('*')) {
        const style = getComputedStyle(child);
        if (style.display === 'none' || style.visibility === 'hidden') continue;
        const childRect = child.getBoundingClientRect();
        if (!childRect.width || !childRect.height) continue;
        contentBottom = Math.max(contentBottom, childRect.bottom);
        left = Math.min(left, childRect.left);
        right = Math.max(right, childRect.right);
      }
      // Text can overflow an otherwise correctly sized box, including nowrap formulas.
      const walker = document.createTreeWalker(content, NodeFilter.SHOW_TEXT);
      while (walker.nextNode()) {
        const node = walker.currentNode;
        if (!node.textContent.trim()) continue;
        const element = node.parentElement;
        if (!element || getComputedStyle(element).visibility === 'hidden') continue;
        const range = document.createRange();
        range.selectNodeContents(node);
        for (const textRect of range.getClientRects()) {
          if (!textRect.width || !textRect.height) continue;
          contentBottom = Math.max(contentBottom, textRect.bottom);
          left = Math.min(left, textRect.left);
          right = Math.max(right, textRect.right);
        }
      }
    }
    const footerRect = footer?.getBoundingClientRect();
    const gap = footerRect ? footerRect.top - contentBottom : null;
    if (gap !== null && gap < minGapPx) errors.push('Less than 2mm between content and footer.');
    if (sheet.scrollHeight > sheet.clientHeight + 1) errors.push('Vertical page overflow.');
    if (sheet.scrollWidth > sheet.clientWidth + 1 || left < rect.left - 1 || right > rect.right + 1) errors.push('Horizontal content overflow.');
    if (footerRect && (footerRect.bottom > rect.bottom + 1 || footerRect.left < rect.left - 1 || footerRect.right > rect.right + 1)) errors.push('Footer outside page.');
    if (!footer || !footer.textContent.includes(draft)) errors.push('Missing draft notice in footer.');
    const ratio = rect.width / rect.height;
    if (Math.abs(ratio - 210 / 297) > 0.01) errors.push('Sheet is not A4 portrait ratio.');
    return {
      page: index + 1,
      gapMm: gap === null ? null : Math.round(gap * 25.4 / 96 * 10) / 10,
      overflowY: Math.max(0, sheet.scrollHeight - sheet.clientHeight),
      errors,
      ok: errors.length === 0,
    };
  });
  return {
    ok: sheets.length > 0 && unloadedFonts.length === 0 && pages.every(page => page.ok),
    pageCount: sheets.length,
    fontErrors: unloadedFonts,
    errors: sheets.length ? [] : ['No .sheet pages found.'],
    pages,
    reminder: 'Render the PDF and visually inspect every page; geometry alone cannot establish readability.',
  };
})()
