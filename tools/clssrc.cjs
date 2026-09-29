// Layout-shift sources + font status for a URL at two widths. Usage: node clssrc.cjs <url>
const { chromium } = require('playwright');
(async () => {
  const url = process.argv[2];
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  for (const [w, h] of [[1366, 900], [390, 844]]) {
    const ctx = await b.newContext({ viewport: { width: w, height: h } });
    const p = await ctx.newPage();
    await p.addInitScript(() => {
      window.__shifts = [];
      new PerformanceObserver(l => {
        for (const e of l.getEntries()) if (!e.hadRecentInput) window.__shifts.push({ v: +e.value.toFixed(3), t: Math.round(e.startTime), src: (e.sources || []).map(s => s.node && (s.node.tagName + '.' + (s.node.className || '').toString().split(' ')[0])).join('|') });
      }).observe({ type: 'layout-shift', buffered: true });
    });
    const errs = [];
    p.on('pageerror', e => errs.push(String(e.message).slice(0, 100)));
    await p.goto(url + (url.includes('?') ? '&' : '?') + 'c=' + Date.now(), { waitUntil: 'networkidle' });
    await p.waitForTimeout(1500);
    const r = await p.evaluate(() => ({
      cls: +window.__shifts.reduce((a, s) => a + s.v, 0).toFixed(3), shifts: window.__shifts.slice(0, 6),
      fonts: [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight),
      overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      sheets: document.querySelectorAll('.sheet').length,
    }));
    console.log(w + 'x' + h, JSON.stringify(r), 'errs', JSON.stringify(errs));
    await ctx.close();
  }
  await b.close();
})();
