# Chieh-Ying Ke — Personal Website

Personal academic website of Chieh-Ying Ke (柯緁盈), Postdoctoral Research Fellow,
Radar Laboratory, Department of Atmospheric Sciences, National Central University.

Live site: https://ru389ru389.github.io/ChiehYingKe/

## 網站架構

使用 GitHub Pages 內建的 Jekyll 自動產生，不需另外安裝或設定 Actions。
中文版在根目錄，英文版在 `/en/`，右上角按鈕一鍵切換。

| 檔案 | 內容 |
| --- | --- |
| `_includes/pages/*.html` | 各頁內容（中英文共用一份，以 `lang` 切換） |
| `*.html`、`en/*.html` | 中文／英文頁面入口（只有標題與網址設定） |
| `_data/publications.yml` | 著作；`topics` 決定列在哪個研究專長下 |
| `_data/conferences.yml` | 研討會；`text_en` 為英文版 |
| `_data/places.yml` | 研討會地點座標（世界地圖用）；研討會加 `place:` 代碼即可標在地圖上 |
| `_data/campaigns.yml` | 野外觀測（含 type 類型與 lat/lng 座標，會標在右側地圖） |
| `_data/campaign_types.yml` | 野外觀測類型的圖示、顏色與名稱 |
| `_data/research.yml` | 研究專長（中英文） |
| `_data/i18n.yml` | 介面文字（中英文） |
| `_layouts/default.html` | 共用的導覽列、語言切換、頁首與頁尾 |
| `_config.yml` | 網站名稱、Email、導覽列項目與顏色 |
| `assets/style.css` | 樣式與配色 |

## 如何更新

新增論文、研討會或觀測：編輯 `_data/` 裡對應的 `.yml` 檔，複製一筆修改即可；
有中文內容時，加上 `_en` 欄位提供英文版。推上 `main` 後約 1–2 分鐘網站自動更新。
