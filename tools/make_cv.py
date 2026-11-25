#!/usr/bin/env python3
"""產生學術履歷 HTML（英文版與中文版），之後由 tools/cv_to_pdf.js 轉成 PDF。

用法（在 repo 根目錄）：
    python3 tools/make_cv.py      # 產生 tools/cv.html（英文）與 tools/cv_zh.html（中文）
    node tools/cv_to_pdf.js       # 產生 assets/cv/Chieh-Ying_Ke_CV.pdf 與 Chieh-Ying_Ke_CV_zh.pdf

資料來源：_data/publications.yml、conferences.yml、campaigns.yml；
個人資訊、學歷、研究興趣與技能寫在本檔下方的 TEXT（中英各一份）。
更新論文、研討會或觀測後重新執行即可。
"""
import html
import os
import re
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(name):
    with open(os.path.join(ROOT, '_data', name), encoding='utf-8') as f:
        return yaml.safe_load(f)


def clean(s):
    """保留 <b>/<em>，其餘移除。"""
    return re.sub(r'<(?!/?(b|em)>)[^>]+>', '', str(s))


pubs = load('publications.yml')
confs = load('conferences.yml')
camps = load('campaigns.yml')

CONTACT = {
    'email': 'cyke812@g.ncu.edu.tw',
    'web': 'ru389ru389.github.io/ChiehYingKe',
    'orcid': '0000-0001-8232-6407',
    'wos': 'AAA-3895-2021',
    'scholar': 'scholar.google.com/citations?user=pxloPuUAAAAJ',
}

TEXT = {
    'en': {
        'html_lang': 'en',
        'name': 'Chieh-Ying Ke', 'name_sub': '柯緁盈',
        'title': 'Postdoctoral Research Fellow',
        'unit': 'Radar Laboratory, Department of Atmospheric Sciences, National Central University, Taoyuan, Taiwan',
        'labels': {'email': 'Email', 'web': 'Web', 'orcid': 'ORCID', 'wos': 'ResearcherID', 'scholar': 'Scholar'},
        'h': {'interests': 'Research Interests', 'edu': 'Education &amp; Positions', 'journal': 'Journal Publications',
              'book': 'Book Chapter', 'preprint': 'Preprint', 'thesis': 'Thesis', 'awards': 'Awards',
              'confs': 'Conference Presentations ({n})', 'camps': 'Field Campaigns ({n}, TEAM-R mobile radar)',
              'skills': 'Skills'},
        'interests': [
            'Weather radar observation and mobile-radar field campaigns (TEAM-R)',
            'Multiple-Doppler wind and thermodynamic retrieval; mesoscale severe weather analysis',
            'Radar data assimilation (EnKF, WRF-LETKF); impact of thermodynamic variables on cloud microphysics and QPF',
            'Ensemble simulation, ensemble sensitivity analysis (ESA) and unsupervised clustering',
            'Arctic atmosphere and vertical atmospheric coupling',
        ],
        'edu': [
            ('2022 – present', 'Postdoctoral Research Fellow', 'Radar Laboratory, National Central University', 'Thermodynamic retrieval; radar data assimilation'),
            ('2022', 'Ph.D., Atmospheric Sciences', 'National Central University', 'Radar meteorology; radar data assimilation; EnKF'),
            ('2014', 'M.S., Atmospheric Sciences', 'National Central University', 'Radar meteorology; wind retrieval; case analysis'),
            ('2012', 'B.S., Atmospheric Sciences', 'National Central University', ''),
        ],
        'skills': [
            ('Modeling & DA', 'WRF, EnKF, WRF-LETKF, ensemble simulation, OSSE'),
            ('Radar analysis', 'Multiple-Doppler wind retrieval, thermodynamic retrieval, mobile radar operation'),
            ('Programming', 'Fortran, Python, MATLAB, NCL, GrADS, Linux'),
            ('Methods', 'Ensemble sensitivity analysis, k-means clustering, unsupervised machine learning'),
            ('Languages', 'Mandarin (native), Taiwanese, English'),
        ],
        'sep': ', ', 'dash': ' — ',
    },
    'zh': {
        'html_lang': 'zh-Hant',
        'name': '柯緁盈', 'name_sub': 'Chieh-Ying Ke',
        'title': '博士後研究員',
        'unit': '國立中央大學 大氣科學學系 雷達實驗室（桃園市中壢區）',
        'labels': {'email': 'Email', 'web': '網站', 'orcid': 'ORCID', 'wos': 'ResearcherID', 'scholar': 'Scholar'},
        'h': {'interests': '研究專長', 'edu': '學歷與經歷', 'journal': '期刊論文',
              'book': '專書章節', 'preprint': '預印本', 'thesis': '學位論文', 'awards': '獲獎',
              'confs': '研討會發表（{n} 篇）', 'camps': '野外觀測（{n} 次，TEAM-R 移動式雷達）',
              'skills': '技術能力'},
        'interests': [
            '氣象雷達觀測與移動式雷達野外實驗（TEAM-R）',
            '多都卜勒雷達風場與熱動力反演；中尺度劇烈天氣分析',
            '雷達資料同化（EnKF、WRF-LETKF）；熱動力變數對雲微物理與定量降水預報之影響',
            '系集模擬、系集敏感度分析（ESA）與非監督式分群',
            '北極大氣與大氣垂直耦合',
        ],
        'edu': [
            ('2022 – 現在', '博士後研究員', '國立中央大學 大氣科學學系 雷達實驗室', '熱動力反演、雷達資料同化'),
            ('2022', '博士，大氣科學', '國立中央大學', '雷達氣象、雷達資料同化、系集卡爾曼濾波（EnKF）'),
            ('2014', '碩士，大氣科學', '國立中央大學', '雷達氣象、風場反演、個案分析'),
            ('2012', '學士，大氣科學', '國立中央大學', ''),
        ],
        'skills': [
            ('模式與資料同化', 'WRF、EnKF、WRF-LETKF、系集模擬、OSSE'),
            ('雷達分析', '多都卜勒風場反演、熱動力反演、移動式雷達觀測'),
            ('程式語言', 'Fortran、Python、MATLAB、NCL、GrADS、Linux'),
            ('分析方法', '系集敏感度分析（ESA）、k-means 分群、非監督式機器學習'),
            ('語言', '中文（母語）、台語、英文'),
        ],
        'sep': '，', 'dash': '｜',
    },
}

e = html.escape


def pick(item, key, lang):
    if lang == 'en':
        return item.get(key + '_en') or item.get(key) or ''
    return item.get(key) or item.get(key + '_en') or ''


def build(lang):
    T = TEXT[lang]
    H = T['h']

    def section(title, body):
        return f'<section><h2>{title}</h2>{body}</section>'

    def pub_rows(kind):
        rows = []
        for p in pubs:
            if p['type'] != kind:
                continue
            doi = f' <span class="doi">doi:{e(p["doi"])}</span>' if p.get('doi') else ''
            rows.append(
                f'<li><span class="yr">{e(str(pick(p, "year", lang)))}</span><div>'
                f'{clean(pick(p, "authors", lang))}: {e(pick(p, "title", lang))}. {clean(pick(p, "venue", lang))}{doi}</div></li>')
        return '<ol class="list">' + ''.join(rows) + '</ol>'

    awards = []
    for y in confs:
        for it in y['items']:
            if it.get('award'):
                venue = re.search(r'<em>(.*?)</em>', pick(it, 'text', lang)).group(1)
                awards.append((y['year'], pick(it, 'award', lang), venue))

    parts = [section(H['interests'], '<ul class="bul">' + ''.join(f'<li>{e(x)}</li>' for x in T['interests']) + '</ul>')]
    parts.append(section(H['edu'], '<ol class="list">' + ''.join(
        f'<li><span class="yr">{e(a)}</span><div><b>{e(b)}</b>{T["sep"]}{e(c)}'
        + (f'<br><span class="muted">{e(d)}</span>' if d else '') + '</div></li>'
        for a, b, c, d in T['edu']) + '</ol>'))
    for kind in ['journal', 'book', 'preprint', 'thesis']:
        parts.append(section(H[kind], pub_rows(kind)))
    if awards:
        parts.append(section(H['awards'], '<ol class="list">' + ''.join(
            f'<li><span class="yr">{y}</span><div>{e(a)}{T["sep"]}{e(v)}</div></li>' for y, a, v in awards) + '</ol>'))

    conf_rows = [f'<li><span class="yr">{y["year"]}</span><div>{clean(pick(it, "text", lang))}</div></li>'
                 for y in confs for it in y['items']]
    parts.append(section(H['confs'].format(n=len(conf_rows)), '<ol class="list small">' + ''.join(conf_rows) + '</ol>'))

    camp_rows = [f'<li><span class="yr">{e(c["when"][:7].strip())}</span>'
                 f'<div>{e(pick(c, "title", lang))} <span class="muted">{T["dash"]}{e(pick(c, "where", lang))}</span></div></li>'
                 for c in camps]
    parts.append(section(H['camps'].format(n=len(camp_rows)), '<ol class="list small">' + ''.join(camp_rows) + '</ol>'))
    parts.append(section(H['skills'], '<table class="skills">' + ''.join(
        f'<tr><th>{e(a)}</th><td>{e(b)}</td></tr>' for a, b in T['skills']) + '</table>'))

    lab = T['labels']
    contact = '<br>'.join(f'<b>{lab[k]}</b> {CONTACT[k]}' for k in ['email', 'web', 'orcid', 'wos', 'scholar'])
    fonts = '"Noto Sans TC", "Noto Sans CJK TC", "Inter", Arial, sans-serif' if lang == 'zh' else '"Inter", "Noto Sans TC", "Noto Sans CJK TC", Arial, sans-serif'
    return f'''<!doctype html><html lang="{T["html_lang"]}"><head><meta charset="utf-8"><title>{T["name"]} — CV</title>
<style>
@page {{ size: A4; margin: 16mm 15mm 16mm 15mm; }}
* {{ box-sizing: border-box; }}
body {{ font-family: {fonts}; color: #1a2433; font-size: 9.6pt; line-height: {1.45 if lang == 'zh' else 1.42}; margin: 0; }}
header {{ border-bottom: 2.5px solid #0f9b8e; padding-bottom: 8px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: flex-end; gap: 16px; }}
h1 {{ font-size: 22pt; margin: 0; color: #0b2545; letter-spacing: .2px; }}
h1 small {{ font-size: 12pt; color: #5b6878; font-weight: 500; margin-left: 8px; }}
.role {{ margin: 3px 0 0; font-weight: 600; color: #1f6fb2; }}
.unit {{ margin: 1px 0 0; color: #5b6878; }}
.contact {{ text-align: right; font-size: 8.6pt; color: #5b6878; line-height: 1.5; white-space: nowrap; }}
.contact b {{ color: #1a2433; font-weight: 600; }}
section {{ margin-top: 10px; }}
h2 {{ font-size: 10.5pt; text-transform: uppercase; letter-spacing: .8px; color: #0b2545; margin: 0 0 5px; padding-bottom: 2px; border-bottom: 1px solid #d9e1ea; }}
.list {{ list-style: none; padding: 0; margin: 0; }}
.list li {{ display: grid; grid-template-columns: 84px 1fr; gap: 8px; margin-bottom: 4px; break-inside: avoid; }}
.list.small li {{ font-size: 8.8pt; margin-bottom: 2.5px; }}
.yr {{ color: #0f9b8e; font-weight: 700; font-variant-numeric: tabular-nums; }}
.muted {{ color: #5b6878; }}
.doi {{ color: #5b6878; font-size: 8.4pt; }}
.bul {{ margin: 0; padding-left: 16px; }} .bul li {{ margin-bottom: 1.5px; }}
.skills {{ border-collapse: collapse; }} .skills th {{ text-align: left; padding: 1px 12px 1px 0; color: #0b2545; white-space: nowrap; vertical-align: top; }} .skills td {{ padding: 1px 0; }}
b {{ font-weight: 700; }}
</style></head><body>
<header>
  <div>
    <h1>{T["name"]}<small>{T["name_sub"]}</small></h1>
    <p class="role">{T["title"]}</p>
    <p class="unit">{T["unit"]}</p>
  </div>
  <div class="contact">{contact}</div>
</header>
{''.join(parts)}
</body></html>'''


for lang, fname in [('en', 'cv.html'), ('zh', 'cv_zh.html')]:
    out = os.path.join(ROOT, 'tools', fname)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(build(lang))
    print('wrote', out)
