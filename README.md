# Chieh-Ying Ke — Personal Website

Personal academic website of Chieh-Ying Ke (柯緁盈), Postdoctoral Research Fellow,
Radar Laboratory, Department of Atmospheric Sciences, National Central University.

Live site: https://ru389ru389.github.io/ChiehYingKe/

## 網站架構

使用 GitHub Pages 內建的 Jekyll 自動產生，不需另外安裝或設定 Actions。

| 檔案 | 內容 |
| --- | --- |
| `index.html` | 首頁（照片、數據、各分頁入口按鈕） |
| `about.html` | 關於我：簡介、學歷、技術工具 |
| `research.html` | 研究專長 |
| `publications.html` | 著作發表（資料來自 `_data/publications.yml`） |
| `conferences.html` | 研討會（資料來自 `_data/conferences.yml`） |
| `campaigns.html` | 外場觀測（資料來自 `_data/campaigns.yml`） |
| `_layouts/default.html` | 共用的導覽列、頁首與頁尾 |
| `_config.yml` | 網站名稱、Email、導覽列項目與顏色 |
| `assets/style.css` | 樣式與配色 |

## 如何更新

新增論文、研討會或觀測：只要編輯 `_data/` 裡對應的 `.yml` 檔，複製一筆修改即可，
推上 `main` 後約 1–2 分鐘網站自動更新。
