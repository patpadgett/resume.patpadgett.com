// render.js - pagination measuring pass and final PDF/screenshot pass for resume.patpadgett.com
// usage: node render.js            -> reads flow index.html, writes .paginated.json + fit report
//        node render.js --final    -> checks overflow, writes Patrick_Padgett_Resume.pdf, og card, review screenshots
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const ROOT = __dirname;
const FINAL = process.argv.includes('--final');
const PDF = 'Patrick_Padgett_Resume.pdf';

(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 1100, height: 1300 }, deviceScaleFactor: 1 });
  page.on('pageerror', e => console.error('PAGE ERROR', e.message));
  page.on('console', m => { if (m.type() === 'error') console.error('CONSOLE', m.text()); });
  await page.goto('file://' + path.join(ROOT, 'index.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(150);

  if (!FINAL) {
    const result = await page.evaluate(() => {
      const sheet = document.querySelector('.sheet');
      const flow = sheet.querySelector('.flow');
      const foot = sheet.querySelector('.foot');
      const cs = getComputedStyle(sheet), fcs = getComputedStyle(foot);
      const avail = 11 * 96 - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom) - foot.offsetHeight - parseFloat(fcs.marginTop);
      sheet.classList.add('measure');
      const flowTop = flow.getBoundingClientRect().top;
      const atoms = [];
      for (const el of flow.children) {
        if (el.tagName === 'UL') {
          for (const li of el.children) atoms.push({ el: li, kind: 'li', ul: el });
        } else {
          const k = el.classList.contains('job') ? 'job' : el.classList.contains('proj') ? 'proj' : el.classList.contains('edu') ? 'edu' : el.tagName.toLowerCase();
          atoms.push({ el, kind: k });
        }
      }
      for (const a of atoms) {
        const r = a.el.getBoundingClientRect();
        const mt = parseFloat(getComputedStyle(a.kind === 'li' && a.el === a.ul.firstElementChild ? a.ul : a.el).marginTop) || 0;
        a.top = r.top - flowTop; a.bottom = r.bottom - flowTop; a.mt = mt;
      }
      // break algorithm with keep-with-next
      const pages = []; let cur = []; let origin = null;
      const keepsWithNext = a => a.kind === 'h2' || a.kind === 'job' || a.kind === 'proj' || (a.kind === 'li' && a.el === a.ul.firstElementChild && a.ul.classList.contains('exp'));
      for (let i = 0; i < atoms.length; i++) {
        const a = atoms[i];
        if (origin === null) origin = a.top - a.mt;
        const fill = a.bottom - origin;
        if (fill > avail && cur.length) {
          // pull back trailing atoms that must travel with the next one
          let moved = [];
          while (cur.length && keepsWithNext(cur[cur.length - 1])) moved.unshift(cur.pop());
          // a job header + exactly one bullet at the page foot: move both
          if (cur.length >= 2 && cur[cur.length - 1].kind === 'li' && cur[cur.length - 2].kind === 'job' && cur[cur.length - 1].el !== cur[cur.length - 1].ul.lastElementChild) { moved.unshift(cur.pop()); moved.unshift(cur.pop()); }
          pages.push(cur); cur = moved.concat([a]); origin = (moved[0] || a).top - (moved[0] || a).mt;
        } else cur.push(a);
      }
      if (cur.length) pages.push(cur);
      const fills = pages.map(p => p[p.length - 1].bottom - (p[0].top - p[0].mt));
      // serialise
      const html = pages.map(p => {
        let out = '', openUl = null;
        for (const a of p) {
          if (a.kind === 'li') {
            if (openUl !== a.ul) { if (openUl) out += '</ul>'; const cont = a.el !== a.ul.firstElementChild ? ' cont' : ''; out += `<ul class="${a.ul.className}${cont}">`; openUl = a.ul; }
            out += a.el.outerHTML;
          } else { if (openUl) { out += '</ul>'; openUl = null; } out += a.el.outerHTML; }
        }
        if (openUl) out += '</ul>';
        return out;
      });
      return { avail, fills, pages: html, total: atoms[atoms.length - 1].bottom - (atoms[0].top - atoms[0].mt) };
    });
    fs.writeFileSync(path.join(ROOT, '.paginated.json'), JSON.stringify(result.pages));
    const pct = result.fills.map(f => (100 * f / result.avail).toFixed(1) + '%');
    console.log(`avail/page ${result.avail.toFixed(0)}px; content ${result.total.toFixed(0)}px = ${(100 * result.total / (2 * result.avail)).toFixed(1)}% of two sheets; pages ${result.pages.length}; fills ${pct.join(', ')}`);
    if (result.pages.length !== 2) { console.error(`FIT: ${result.pages.length} pages (need 2) - adjust PROFILE in build.py`); process.exitCode = 2; }
  } else {
    const over = await page.evaluate(() => [...document.querySelectorAll('.sheet')].map(s => { const f = s.querySelector('.flow'); return { sheet: s.dataset.sheet, over: f.scrollHeight - f.clientHeight, free: f.clientHeight - f.scrollHeight }; }));
    console.log('overflow check:', JSON.stringify(over));
    // fonts-blocked gate: the metric-matched local fallbacks must hold both sheets when the woff2 files never arrive
    const fb = await browser.newPage({ viewport: { width: 1366, height: 900 } });
    await fb.route(/assets\/fonts\//, rt => rt.abort());
    await fb.goto('file://' + path.join(ROOT, 'index.html')); await fb.evaluate(() => document.fonts.ready); await fb.waitForTimeout(150);
    const overFb = await fb.evaluate(() => [...document.querySelectorAll('.sheet .flow')].map((f, i) => ({ sheet: i + 1, over: f.scrollHeight - f.clientHeight, family: getComputedStyle(document.querySelector('h1')).fontFamily.split(',')[0] })));
    const fbLast = await fb.evaluate(() => { const li = [...document.querySelectorAll('.sheet[data-sheet="2"] .flow li')]; const l = li[li.length - 1].getBoundingClientRect(); const f = document.querySelector('.sheet[data-sheet="2"] .flow').getBoundingClientRect(); return { lastBottom: Math.round(l.bottom), flowBottom: Math.round(f.bottom), fits: l.bottom <= f.bottom + 0.5 }; });
    console.log('fonts-blocked overflow check:', JSON.stringify(overFb), 'last item fits:', JSON.stringify(fbLast));
    if (overFb.some(o => o.over > 0) || !fbLast.fits) { console.error('FAIL: sheets overflow with fonts blocked'); process.exit(3); }
    await fb.close();
    if (over.some(o => o.over > 0)) { console.error('OVERFLOW on a sheet'); process.exitCode = 3; }
    // PDF
    await page.emulateMedia({ media: 'print' });
    await page.pdf({ path: path.join(ROOT, PDF), format: 'Letter', printBackground: true, preferCSSPageSize: true, tagged: true, outline: false, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
    await page.emulateMedia({ media: 'screen' });
    // review captures
    const rev = path.join(ROOT, '.impeccable', 'review'); fs.mkdirSync(rev, { recursive: true });
    await page.addStyleTag({ content: '.sheet{animation:none !important}' });
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.evaluate(() => window.scrollTo(0, 0)); await page.waitForTimeout(100);
    await page.screenshot({ path: path.join(rev, 'desktop.png'), fullPage: true });
    // sheet 1 at 2x for reading
    const s1 = await page.$('.sheet[data-sheet="1"]');
    await s1.screenshot({ path: path.join(rev, 'sheet1@2x.png'), scale: 'device' }).catch(() => {});
    const page2 = await browser.newPage({ viewport: { width: 1000, height: 1200 }, deviceScaleFactor: 2 });
    await page2.goto('file://' + path.join(ROOT, 'index.html')); await page2.evaluate(() => document.fonts.ready); await page2.waitForTimeout(150);
    await page2.addStyleTag({ content: '.sheet{animation:none !important}' });
    await (await page2.$('.sheet[data-sheet="1"]')).screenshot({ path: path.join(rev, 'sheet1@2x.png') });
    await (await page2.$('.sheet[data-sheet="2"]')).screenshot({ path: path.join(rev, 'sheet2@2x.png') });
    // og card 1200x630 from the composed .og.html at 1x
    const og = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
    await og.goto('file://' + path.join(ROOT, '.og.html')); await og.evaluate(() => document.fonts.ready); await og.waitForTimeout(200);
    await og.screenshot({ path: path.join(ROOT, 'assets', 'og-card.png'), clip: { x: 0, y: 0, width: 1200, height: 630 } });
    await og.close();
    await page2.close();
    // mobile
    await page.setViewportSize({ width: 390, height: 844 });
    await page.evaluate(() => window.scrollTo(0, 0)); await page.waitForTimeout(150);
    await page.screenshot({ path: path.join(rev, 'mobile.png'), fullPage: true });
    const hscroll = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    console.log('mobile horizontal overflow px:', hscroll);
    await page.setViewportSize({ width: 320, height: 700 });
    await page.waitForTimeout(100);
    const hscroll320 = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    console.log('320 horizontal overflow px:', hscroll320);
    console.log('wrote', PDF, 'and review captures');
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
