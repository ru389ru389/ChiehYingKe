#!/usr/bin/env python3
"""產生英文版學術履歷 HTML（之後由 tools/cv_to_pdf.js 轉成 PDF）。

用法（在 repo 根目錄）：
    python3 tools/make_cv.py           # 產生 tools/cv.html
    node tools/cv_to_pdf.js            # 產生 assets/cv/Chieh-Ying_Ke_CV.pdf

資料來源：_data/publications.yml、conferences.yml、campaigns.yml，
個人資訊與學歷寫在本檔下方。更新論文或研討會後重新執行即可。
"""
import html
import os
import re
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(name):
    with open(os.path.join(ROOT, '_data', name), encoding='utf-8') as f:
        return yaml.safe_load(f)


def en(item, key):
    return item.get(key + '_en') or item.get(key) or ''


def clean(s):
    """保留 <b>/<em>，其餘移除。"""
    s = str(s)
    s = re.sub(r'<(?!/?(b|em)>)[^>]+>', '', s)
    return s


pubs = load('publications.yml')
confs = load('conferences.yml')
camps = load('campaigns.yml')

PROFILE = {
    'name': 'Chieh-Ying Ke',
    'name_zh': '柯緁盈',
    'title': 'Postdoctoral Research Fellow',
    'unit': 'Radar Laboratory, Department of Atmospheric Sciences, National Central University, Taoyuan, Taiwan',
    'email': 'cyke812@g.ncu.edu.tw',
    'web': 'ru389ru389.github.io/ChiehYingKe',
    'orcid': '0000-0001-8232-6407',
    'wos': 'AAA-3895-2021',
    'scholar': 'scholar.google.com/citations?user=pxloPuUAAAAJ',
}

INTERESTS = [
    'Weather radar observation and mobile-radar field campaigns (TEAM-R)',
    'Multiple-Doppler wind and thermodynamic retrieval; mesoscale severe weather analysis',
    'Radar data assimilation (EnKF, WRF-LETKF); impact of thermodynamic variables on cloud microphysics and QPF',
    'Ensemble simulation, ensemble sensitivity analysis (ESA) and unsupervised clustering',
    'Arctic atmosphere and vertical atmospheric coupling',
]

EDUCATION = [
    ('2022 – present', 'Postdoctoral Research Fellow', 'Radar Laboratory, National Central University', 'Thermodynamic retrieval; radar data assimilation'),
    ('2015 – 2022', 'Ph.D., Atmospheric Sciences, 2022', 'National Central University', 'Radar meteorology; radar data assimilation; EnKF'),
    ('2012 – 2014', 'M.S., Atmospheric Sciences', 'National Central University', 'Radar meteorology; wind retrieval; case analysis'),
    ('2008 – 2012', 'B.S., Atmospheric Sciences', 'National Central University', ''),
]

SKILLS = [
    ('Modeling & DA', 'WRF, EnKF, WRF-LETKF, ensemble simulation, OSSE'),
    ('Radar analysis', 'Multiple-Doppler wind retrieval, thermodynamic retrieval, mobile radar operation'),
    ('Programming', 'Fortran, Python, MATLAB, NCL, GrADS, Linux'),
    ('Methods', 'Ensemble sensitivity analysis, k-means clustering, unsupervised machine learning'),
    ('Languages', 'Mandarin (native), Taiwanese, English'),
]

AWARDS = []
for y in confs:
    for it in y['items']:
        if it.get('award'):
            AWARDS.append((y['year'], en(it, 'award'),
                           re.search(r'<em>(.*?)</em>', en(it, 'text')).group(1)))

e = html.escape


def section(title, body):
    return f'<section><h2>{title}</h2>{body}</section>'


def pub_rows(kind):
    rows = []
    for p in pubs:
        if p['type'] != kind:
            continue
        doi = f' <span class="doi">doi:{e(p["doi"])}</span>' if p.get('doi') else ''
        rows.append(
            f'<li><span class="yr">{e(str(en(p, "year")))}</span><div>'
            f'{clean(en(p, "authors"))}: {e(en(p, "title"))}. {clean(en(p, "venue"))}{doi}</div></li>')
    return '<ol class="list">' + ''.join(rows) + '</ol>'


parts = []
parts.append(section('Research Interests',
                      '<ul class="bul">' + ''.join(f'<li>{e(x)}</li>' for x in INTERESTS) + '</ul>'))
parts.append(section('Education &amp; Positions', '<ol class="list">' + ''.join(
    f'<li><span class="yr">{e(a)}</span><div><b>{e(b)}</b>, {e(c)}'
    + (f'<br><span class="muted">{e(d)}</span>' if d else '') + '</div></li>'
    for a, b, c, d in EDUCATION) + '</ol>'))
parts.append(section('Journal Publications', pub_rows('journal')))
parts.append(section('Book Chapter', pub_rows('book')))
parts.append(section('Preprint', pub_rows('preprint')))
parts.append(section('Thesis', pub_rows('thesis')))
if AWARDS:
    parts.append(section('Awards', '<ol class="list">' + ''.join(
        f'<li><span class="yr">{y}</span><div>{e(a)}, {e(v)}</div></li>' for y, a, v in AWARDS) + '</ol>'))

conf_rows = []
for y in confs:
    for it in y['items']:
        conf_rows.append(f'<li><span class="yr">{y["year"]}</span><div>{clean(en(it, "text"))}</div></li>')
parts.append(section(f'Conference Presentations ({len(conf_rows)})', '<ol class="list small">' + ''.join(conf_rows) + '</ol>'))

camp_rows = []
for c in camps:
    camp_rows.append(f'<li><span class="yr">{e(c["when"][:7].replace("—", "").strip())}</span>'
                     f'<div>{e(en(c, "title"))} <span class="muted">— {e(en(c, "where"))}</span></div></li>')
parts.append(section(f'Field Campaigns ({len(camp_rows)}, TEAM-R mobile radar)',
                     '<ol class="list small">' + ''.join(camp_rows) + '</ol>'))
parts.append(section('Skills', '<table class="skills">' + ''.join(
    f'<tr><th>{e(a)}</th><td>{e(b)}</td></tr>' for a, b in SKILLS) + '</table>'))

P = PROFILE
doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{P["name"]} — CV</title>
<style>
@page {{ size: A4; margin: 16mm 15mm 16mm 15mm; }}
* {{ box-sizing: border-box; }}
body {{ font-family: "Inter", "Noto Sans TC", "Noto Sans CJK TC", Arial, sans-serif; color: #1a2433; font-size: 9.6pt; line-height: 1.42; margin: 0; }}
header {{ border-bottom: 2.5px solid #0f9b8e; padding-bottom: 8px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: flex-end; gap: 16px; }}
h1 {{ font-size: 22pt; margin: 0; color: #0b2545; letter-spacing: .2px; }}
h1 small {{ font-size: 12pt; color: #5b6878; font-weight: 500; margin-left: 6px; }}
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
    <h1>{P["name"]}<small>{P["name_zh"]}</small></h1>
    <p class="role">{P["title"]}</p>
    <p class="unit">{P["unit"]}</p>
  </div>
  <div class="contact">
    <b>Email</b> {P["email"]}<br>
    <b>Web</b> {P["web"]}<br>
    <b>ORCID</b> {P["orcid"]}<br>
    <b>ResearcherID</b> {P["wos"]}<br>
    <b>Scholar</b> {P["scholar"]}
  </div>
</header>
{''.join(parts)}
</body></html>'''

out = os.path.join(ROOT, 'tools', 'cv.html')
with open(out, 'w', encoding='utf-8') as f:
    f.write(doc)
print('wrote', out)
