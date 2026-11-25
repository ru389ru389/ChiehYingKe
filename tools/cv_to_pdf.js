// 將 tools/cv.html 轉成 assets/cv/Chieh-Ying_Ke_CV.pdf（需要 Playwright）
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

(async () => {
  const root = path.resolve(__dirname, '..');
  const out = path.join(root, 'assets', 'cv', 'Chieh-Ying_Ke_CV.pdf');
  fs.mkdirSync(path.dirname(out), { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.join(root, 'tools', 'cv.html'));
  await page.pdf({
    path: out, format: 'A4', printBackground: true, preferCSSPageSize: true,
    displayHeaderFooter: true, headerTemplate: '<span></span>',
    footerTemplate: '<div style="font-size:8px;color:#8a96a3;width:100%;text-align:center;font-family:Arial">Chieh-Ying Ke — CV · <span class="pageNumber"></span> / <span class="totalPages"></span></div>',
  });
  await browser.close();
  console.log('wrote', out);
})();
