// 將 tools/cv.html 與 tools/cv_zh.html 轉成 assets/cv/ 內的 PDF（需要 Playwright）
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const JOBS = [
  { src: 'cv.html', out: 'Chieh-Ying_Ke_CV.pdf', footer: 'Chieh-Ying Ke — CV' },
  { src: 'cv_zh.html', out: 'Chieh-Ying_Ke_CV_zh.pdf', footer: '柯緁盈 — 履歷' },
];

(async () => {
  const root = path.resolve(__dirname, '..');
  fs.mkdirSync(path.join(root, 'assets', 'cv'), { recursive: true });
  const browser = await chromium.launch();
  for (const j of JOBS) {
    const page = await browser.newPage();
    await page.goto('file://' + path.join(root, 'tools', j.src));
    const out = path.join(root, 'assets', 'cv', j.out);
    await page.pdf({
      path: out, format: 'A4', printBackground: true, preferCSSPageSize: true,
      displayHeaderFooter: true, headerTemplate: '<span></span>',
      footerTemplate: `<div style="font-size:8px;color:#8a96a3;width:100%;text-align:center;font-family:Arial,'Noto Sans CJK TC'">${j.footer} · <span class="pageNumber"></span> / <span class="totalPages"></span></div>`,
    });
    await page.close();
    console.log('wrote', out);
  }
  await browser.close();
})();
