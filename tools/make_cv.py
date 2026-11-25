#!/usr/bin/env python3
"""產生學術履歷 HTML（英文版與中文版），之後由 tools/cv_to_pdf.js 轉成 PDF。

用法（在 repo 根目錄）：
    python3 tools/make_cv.py      # 產生 tools/cv.html（英文）與 tools/cv_zh.html（中文）
    node tools/cv_to_pdf.js       # 產生 assets/cv/Chieh-Ying_Ke_CV.pdf 與 Chieh-Ying_Ke_CV_zh.pdf

資料來源：_data/publications.yml、conferences.yml、campaigns.yml、places.yml、countries.yml；
個人資訊、學歷、研究興趣與技能寫在本檔下方的 TEXT（中英各一份）。
所有數字（論文數、研討會數、國家數、觀測次數）都由資料自動計算。
照片：tools/cv_photo.jpg（SHOW_PHOTO = False 可隱藏，例如投遞不收照片的歐美職缺）。
"""
import html
import os
import re
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOW_PHOTO = True


def load(name):
    with open(os.path.join(ROOT, '_data', name), encoding='utf-8') as f:
        return yaml.safe_load(f)


def clean(s):
    """保留 <b>/<em>，其餘移除。"""
    return re.sub(r'<(?!/?(b|em)>)[^>]+>', '', str(s))


pubs = load('publications.yml')
confs = load('conferences.yml')
camps = load('campaigns.yml')
places = load('places.yml')
countries = load('countries.yml')

# ---------- 由資料計算的數字 ----------
journals = [p for p in pubs if p['type'] == 'journal']
under_review = [p for p in journals if 'under review' in (p.get('venue_en') or '')]
published = [p for p in journals if p not in under_review]
first_author = [p for p in published if str(p['authors']).startswith('<b>')]
conf_items = [(y['year'], it) for y in confs for it in y['items']]
intl = [c for c in conf_items if c[1].get('intl')]
domestic = [c for c in conf_items if not c[1].get('intl')]
abroad = sorted({places[it['place']]['country'] for _, it in conf_items
                 if it.get('place') and places.get(it['place'], {}).get('country') not in (None, 'TW')})
ams_radar = [c for c in conf_items if re.search(r'\d+(st|nd|rd|th) (AMS |International )?Conference on Radar Meteorology', c[1].get('text_en') or c[1]['text'])]
camp_years = sorted({int(c['when'][:4]) for c in camps})

STATS = {
    'journal': len(journals), 'published': len(published), 'review': len(under_review),
    'first': len(first_author), 'conf': len(conf_items), 'intl': len(intl), 'dom': len(domestic),
    'countries': len(abroad), 'ams': len(ams_radar), 'camps': len(camps),
    'camp_from': camp_years[0], 'camp_to': camp_years[-1],
}

# ---------- 野外觀測：依計畫分組 ----------
GROUPS = [
    ('TAHOPE', 'TAHOPE', 'TAHOPE — Taiwan-Area Heavy Rain Observation and Prediction Experiment', 'TAHOPE 臺灣區域豪雨觀測與預報實驗'),
    ('YESRain', 'YESRain', 'YESRain — Yilan Experiment of Severe Rainfall', 'YESRain 宜蘭豪雨觀測實驗'),
    ('TASSE', 'TASSE', 'TASSE — Taipei Summer Storm Experiment', 'TASSE 雙北都會區夏季對流暴雨觀測實驗'),
    ('ICE-POP', 'ICE-POP', 'ICE-POP — PyeongChang 2018 Winter Olympics RDP (Korea)', 'ICE-POP 2018 平昌冬奧觀測實驗（韓國）'),
    ('FAOSE', 'FAOSE', 'FAOSE 2025 — Chiayi Full-Atmosphere Observation and Simulation Experiment', 'FAOSE 2025 嘉義全大氣觀測與模擬實驗'),
    ('CITEWARM', 'CITEWARM', 'CITEWARM 2026 — Convection Initiation Thermodynamics Experiment (mini-radiosondes)', 'CITEWARM 2026 嘉南平原對流肇始熱動力實驗（微型探空）'),
    ('monsoon', 'Southwest Monsoon', 'Southwest Monsoon Joint Observation Experiments', '西南氣流聯合觀測實驗'),
    ('typhoon', 'Typhoon', 'Typhoon observations (Chan-hom, Soudelor)', '颱風觀測（昌鴻、蘇迪勒）'),
    ('support', 'Support', 'Operational radar station support (Wufenshan, Hualien; CWB)', '氣象局雷達站支援觀測（五分山、花蓮）'),
    ('marine', None, 'Marine & coastal experiments (drifting buoys; Ørsted offshore wind)', '海洋與海岸觀測（漂流浮標、Ørsted 離岸風場）'),
]


def group_campaigns():
    out = []
    used = set()
    for key, needle, en_name, zh_name in GROUPS:
        items = []
        for i, c in enumerate(camps):
            if i in used:
                continue
            t = c.get('title_en', '')
            if (needle and needle in t) or (key == 'marine' and c['type'] == 'marine') or (key == 'typhoon' and c['type'] == 'typhoon'):
                items.append(c)
                used.add(i)
        if items:
            ys = sorted({int(c['when'][:4]) for c in items})
            yr = str(ys[0]) if len(ys) == 1 else (f'{ys[0]}–{ys[-1]}' if ys == list(range(ys[0], ys[-1] + 1)) else str(ys[0]) + ''.join('/' + str(y)[2:] for y in ys[1:]))
            out.append((yr, en_name, zh_name, len(items)))
    rest = [c for i, c in enumerate(camps) if i not in used]
    return out, rest


GROUPED, OTHER = group_campaigns()

CONTACT = {
    'email': 'cyke812@g.ncu.edu.tw',
    'web': 'ru389ru389.github.io/ChiehYingKe',
    'orcid': '0000-0001-8232-6407',
    'wos': 'AAA-3895-2021',
    'scholar': 'scholar.google.com/citations?user=pxloPuUAAAAJ',
}

S = STATS
TEXT = {
    'en': {
        'html_lang': 'en',
        'name': 'Chieh-Ying Ke', 'name_sub': '柯緁盈',
        'title': 'Postdoctoral Research Fellow · Radar Meteorology',
        'unit': 'Radar Laboratory, Department of Atmospheric Sciences, National Central University, Taoyuan, Taiwan',
        'labels': {'email': 'Email', 'web': 'Web', 'orcid': 'ORCID', 'wos': 'ResearcherID', 'scholar': 'Scholar'},
        'metrics': [
            (S['published'], 'Journal papers', f"{S['first']} first-author · {S['review']} in review"),
            (S['conf'], 'Presentations', f"{S['intl']} international"),
            (S['countries'], 'Countries', 'conferences abroad'),
            (S['ams'], 'AMS Radar Conf.', '2015 – 2025'),
            (S['camps'], 'Field deployments', f"{S['camp_from']} – {S['camp_to']}"),
        ],
        'summary': (
            'Radar meteorologist bridging observations and numerical models. Over a decade of hands-on '
            f"field work with the TEAM-R mobile radar ({S['camps']} deployments, including TAHOPE, YESRain, TASSE and the "
            'ICE-POP 2018 Olympic campaign in Korea), combined with multiple-Doppler wind and thermodynamic retrieval, '
            'radar data assimilation (EnKF / WRF-LETKF) and ensemble analysis to understand and better predict '
            f"heavy rainfall. Author of {S['published']} peer-reviewed journal papers ({S['first']} first-author, mainly in "
            f"<em>Monthly Weather Review</em>; {S['review']} more under review) and {S['conf']} conference presentations in {S['countries'] + 1} countries."
        ),
        'h': {'summary': 'Profile', 'interests': 'Research Interests', 'edu': 'Education &amp; Positions',
              'field': 'Field Research Experience', 'journal': 'Journal Publications', 'book': 'Book Chapter',
              'preprint': 'Preprint', 'thesis': 'Thesis', 'awards': 'Awards', 'confs': 'Conference Presentations',
              'intl': 'International ({n})', 'dom': 'Domestic ({n})', 'camps_all': 'All field deployments ({n})',
              'skills': 'Skills'},
        'field_role': 'Role: member of the TEAM-R mobile dual-polarization Doppler radar team — site survey, system setup, radar operation and data analysis.',
        'deploy': '{n} deployment(s)',
        'pub_note': 'Bold = C.-Y. Ke.',
        'interests': [
            'Weather radar observation and mobile-radar field campaigns (TEAM-R)',
            'Multiple-Doppler wind and thermodynamic retrieval; mesoscale severe weather',
            'Radar data assimilation (EnKF, WRF-LETKF); thermodynamics and cloud microphysics',
            'Ensemble simulation, ensemble sensitivity analysis (ESA) and k-means clustering',
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
        'title': '博士後研究員 · 雷達氣象',
        'unit': '國立中央大學 大氣科學學系 雷達實驗室（桃園市中壢區）',
        'labels': {'email': 'Email', 'web': '網站', 'orcid': 'ORCID', 'wos': 'ResearcherID', 'scholar': 'Scholar'},
        'metrics': [
            (S['published'], '期刊論文', f"第一作者 {S['first']} 篇 · 審查中 {S['review']} 篇"),
            (S['conf'], '研討會發表', f"國際 {S['intl']} 篇"),
            (S['countries'], '國外發表國家', '海外研討會'),
            (S['ams'], 'AMS 雷達氣象研討會', '2015 – 2025'),
            (S['camps'], '野外觀測', f"{S['camp_from']} – {S['camp_to']}"),
        ],
        'summary': (
            '專長雷達氣象，連結觀測與數值模式。十餘年來參與 TEAM-R 移動式雷達野外觀測'
            f"（共 {S['camps']} 次，包含 TAHOPE、YESRain、TASSE 與韓國平昌冬奧 ICE-POP 國際實驗），"
            '並結合多都卜勒風場與熱動力反演、雷達資料同化（EnKF / WRF-LETKF）及系集分析，'
            f"研究並改善豪雨預報。已發表期刊論文 {S['published']} 篇（第一作者 {S['first']} 篇，主要刊登於 "
            f"<em>Monthly Weather Review</em>；另 {S['review']} 篇審查中），研討會發表 {S['conf']} 篇，足跡遍及 {S['countries'] + 1} 個國家。"
        ),
        'h': {'summary': '簡介', 'interests': '研究專長', 'edu': '學歷與經歷', 'field': '野外觀測經驗',
              'journal': '期刊論文', 'book': '專書章節', 'preprint': '預印本', 'thesis': '學位論文', 'awards': '獲獎',
              'confs': '研討會發表', 'intl': '國際研討會（{n} 篇）', 'dom': '國內研討會（{n} 篇）',
              'camps_all': '野外觀測完整列表（{n} 次）', 'skills': '技術能力'},
        'field_role': '工作內容：TEAM-R 移動式雙偏極化都卜勒雷達團隊成員，負責場址勘查、系統架設、雷達操作與資料分析。',
        'deploy': '{n} 次',
        'pub_note': '粗體為本人。',
        'interests': [
            '氣象雷達觀測與移動式雷達野外實驗（TEAM-R）',
            '多都卜勒雷達風場與熱動力反演；中尺度劇烈天氣',
            '雷達資料同化（EnKF、WRF-LETKF）；熱動力與雲微物理',
            '系集模擬、系集敏感度分析（ESA）與 k-means 分群',
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

ICONS = {
    'summary': '<circle cx="12" cy="8" r="4"/><path d="M4 21c1-4 4-6 8-6s7 2 8 6"/>',
    'interests': '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4.5"/><path d="M12 12 L19 6"/>',
    'edu': '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c3 2 9 2 12 0v-5"/>',
    'field': '<path d="M3 20l6-11 4 7 3-4 5 8z"/><circle cx="17" cy="6" r="2"/>',
    'journal': '<path d="M6 3h9l4 4v14H6z"/><path d="M14 3v5h5M9 13h7M9 17h7"/>',
    'book': '<path d="M4 4h7a3 3 0 0 1 3 3v13a2 2 0 0 0-2-2H4z"/><path d="M20 4h-7a3 3 0 0 0-3 3"/>',
    'preprint': '<path d="M6 3h9l4 4v14H6z"/><path d="M9 13h7"/>',
    'thesis': '<path d="M2 9l10-5 10 5-10 5z"/>',
    'awards': '<circle cx="12" cy="9" r="5"/><path d="M8.5 13l-1.5 8 5-3 5 3-1.5-8"/>',
    'confs': '<rect x="3" y="4" width="18" height="12" rx="1.5"/><path d="M12 16v4M8 20h8"/>',
    'skills': '<path d="M14 7l3-3 3 3-3 3M4 20l9-9"/><path d="M7 4l3 3-3 3-3-3z"/>',
}

e = html.escape


def pick(item, key, lang):
    if lang == 'en':
        return item.get(key + '_en') or item.get(key) or ''
    return item.get(key) or item.get(key + '_en') or ''


def build(lang):
    T = TEXT[lang]
    H = T['h']

    def section(key, title, body, cls=''):
        icon = f'<svg viewBox="0 0 24 24">{ICONS[key]}</svg>' if key in ICONS else ''
        return f'<section class="{cls}"><h2>{icon}{title}</h2>{body}</section>'

    def pub_rows(kind, prefix):
        rows = []
        n = 0
        for p in pubs:
            if p['type'] != kind:
                continue
            n += 1
            doi = f' <span class="doi">doi:{e(p["doi"])}</span>' if p.get('doi') else ''
            first = ' first' if str(p['authors']).startswith('<b>') else ''
            rows.append(
                f'<li class="pub{first}"><span class="tag">{prefix}{n}</span><span class="yr">{e(str(p["year"])) if str(p["year"]).isdigit() else "—"}</span><div>'
                f'{clean(pick(p, "authors", lang))}: <span class="ptitle">{e(pick(p, "title", lang))}</span>. {clean(pick(p, "venue", lang))}{doi}</div></li>')
        return '<ol class="list pubs">' + ''.join(rows) + '</ol>'

    awards = []
    for y, it in conf_items:
        if it.get('award'):
            venue = re.search(r'<em>(.*?)</em>', pick(it, 'text', lang)).group(1)
            awards.append((y, pick(it, 'award', lang), venue))

    # header
    lab = T['labels']
    contact = ''.join(f'<div><b>{lab[k]}</b><span>{CONTACT[k]}</span></div>' for k in ['email', 'web', 'orcid', 'wos', 'scholar'])
    photo = '<img class="photo" src="cv_photo.jpg" alt="">' if SHOW_PHOTO else ''
    metrics = ''.join(f'<div class="m"><b>{n}</b><span>{e(a)}</span><small>{e(b)}</small></div>' for n, a, b in T['metrics'])

    parts = []
    parts.append(section('summary', H['summary'], f'<p class="summary">{T["summary"]}</p>'))
    parts.append(section('interests', H['interests'], '<ul class="chips">' + ''.join(f'<li>{e(x)}</li>' for x in T['interests']) + '</ul>'))
    parts.append(section('edu', H['edu'], '<ol class="list">' + ''.join(
        f'<li><span class="yr">{e(a)}</span><div><b>{e(b)}</b>{T["sep"]}{e(c)}'
        + (f'<br><span class="muted">{e(d)}</span>' if d else '') + '</div></li>'
        for a, b, c, d in T['edu']) + '</ol>'))

    field = f'<p class="role">{e(T["field_role"])}</p><ol class="list">' + ''.join(
        f'<li><span class="yr">{e(yr)}</span><div><b>{e(zh if lang == "zh" else en_)}</b> '
        f'<span class="pill">{T["deploy"].format(n=n)}</span></div></li>'
        for yr, en_, zh, n in GROUPED) + '</ol>'
    parts.append(section('field', H['field'], field))

    parts.append(section('journal', H['journal'] + f' <span class="note">{T["pub_note"]}</span>', pub_rows('journal', 'J')))
    parts.append(section('book', H['book'], pub_rows('book', 'B')))
    parts.append(section('preprint', H['preprint'], pub_rows('preprint', 'P')))
    parts.append(section('thesis', H['thesis'], pub_rows('thesis', 'T')))
    if awards:
        parts.append(section('awards', H['awards'], '<ol class="list">' + ''.join(
            f'<li><span class="yr">{y}</span><div><b>{e(a)}</b>{T["sep"]}{e(v)}</div></li>' for y, a, v in awards) + '</ol>'))

    def conf_list(items, prefix):
        return '<ol class="list small">' + ''.join(
            f'<li><span class="tag">{prefix}{i + 1}</span><span class="yr">{y}</span><div>{clean(pick(it, "text", lang))}</div></li>'
            for i, (y, it) in enumerate(items)) + '</ol>'
    parts.append(section('confs', H['confs'],
                         f'<h3>{H["intl"].format(n=len(intl))}</h3>' + conf_list(intl, 'C') +
                         f'<h3>{H["dom"].format(n=len(domestic))}</h3>' + conf_list(domestic, 'D')))

    camp_rows = ''.join(f'<li><span class="yr">{e(c["when"][:7].strip())}</span>'
                        f'<div>{e(pick(c, "title", lang))} <span class="muted">{T["dash"]}{e(pick(c, "where", lang))}</span></div></li>'
                        for c in camps)
    parts.append(section('field', H['camps_all'].format(n=len(camps)), f'<ol class="list small">{camp_rows}</ol>'))
    parts.append(section('skills', H['skills'], '<table class="skills">' + ''.join(
        f'<tr><th>{e(a)}</th><td>{e(b)}</td></tr>' for a, b in T['skills']) + '</table>'))

    fonts = ('"Noto Sans TC", "Noto Sans CJK TC", "Inter", Arial, sans-serif' if lang == 'zh'
             else '"Inter", "Noto Sans TC", "Noto Sans CJK TC", Arial, sans-serif')
    lh = 1.45 if lang == 'zh' else 1.42
    return f'''<!doctype html><html lang="{T["html_lang"]}"><head><meta charset="utf-8"><title>{T["name"]} — CV</title>
<style>
@page {{ size: A4; margin: 14mm 14mm 15mm 14mm; }}
* {{ box-sizing: border-box; }}
:root {{ --navy: #0b2545; --teal: #0f9b8e; --blue: #1f6fb2; --coral: #e0573a; --amber: #d98e04; --muted: #5b6878; --line: #dbe3ec; --soft: #f1f6f9; }}
body {{ font-family: {fonts}; color: #1a2433; font-size: 9.4pt; line-height: {lh}; margin: 0; }}
header {{ display: grid; grid-template-columns: {'96px ' if SHOW_PHOTO else ''}1fr; gap: 18px; align-items: center;
  padding: 14px 16px; border-radius: 12px; color: #fff;
  background: linear-gradient(120deg, #0b2545 0%, #13406b 60%, #0f7f78 100%); }}
.photo {{ width: 96px; height: 96px; border-radius: 50%; object-fit: cover; border: 3px solid rgba(255,255,255,.85); }}
h1 {{ font-size: 21pt; margin: 0; letter-spacing: .2px; line-height: 1.15; white-space: nowrap; }}
h1 small {{ font-size: 11.5pt; font-weight: 500; opacity: .8; margin-left: 8px; }}
.role-line {{ margin: 4px 0 0; font-weight: 600; color: #8fe3d8; }}
.unit {{ margin: 1px 0 0; color: #d2deeb; font-size: 8.8pt; }}
.contact {{ font-size: 8.2pt; line-height: 1.5; color: #d2deeb; margin-top: 6px; display: flex; flex-wrap: wrap; gap: 2px 14px; }}
.contact div {{ white-space: nowrap; }}
.contact b {{ color: #fff; font-weight: 600; margin-right: 4px; }}
.metrics {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; margin: 10px 0 4px; }}
.m {{ border: 1px solid var(--line); border-top: 3px solid var(--teal); border-radius: 8px; padding: 6px 8px; text-align: center; background: var(--soft); }}
.m:nth-child(1) {{ border-top-color: var(--amber); }} .m:nth-child(2) {{ border-top-color: var(--coral); }}
.m:nth-child(3) {{ border-top-color: var(--blue); }} .m:nth-child(4) {{ border-top-color: var(--navy); }}
.m b {{ display: block; font-size: 17pt; line-height: 1.1; color: var(--navy); }}
.m span {{ display: block; font-size: 8.2pt; font-weight: 600; }}
.m small {{ display: block; font-size: 7.4pt; color: var(--muted); }}
section {{ margin-top: 11px; }}
h2 {{ display: flex; align-items: center; gap: 7px; font-size: 10.6pt; text-transform: uppercase; letter-spacing: .8px; color: var(--navy);
  margin: 0 0 6px; padding-bottom: 3px; border-bottom: 1.5px solid var(--line); }}
h2 svg {{ width: 15px; height: 15px; fill: none; stroke: var(--teal); stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; flex: none; }}
h2 .note {{ margin-left: auto; text-transform: none; letter-spacing: 0; font-weight: 400; font-size: 8pt; color: var(--muted); }}
h3 {{ font-size: 9.4pt; color: var(--blue); margin: 6px 0 4px; }}
.summary {{ margin: 0; text-align: justify; }}
.chips {{ list-style: none; padding: 0; margin: 0; display: flex; flex-wrap: wrap; gap: 5px; }}
.chips li {{ padding: 2px 10px; border-radius: 999px; background: #e7f5f3; color: #0b5e57; font-size: 8.6pt; }}
.list {{ list-style: none; padding: 0; margin: 0; }}
.list li {{ display: grid; grid-template-columns: 84px 1fr; gap: 8px; margin-bottom: 4px; break-inside: avoid; }}
.list.pubs li, .list.small li:has(.tag) {{ grid-template-columns: 26px 44px 1fr; gap: 6px; }}
.list.small li {{ font-size: 8.6pt; margin-bottom: 2.5px; }}
.tag {{ color: var(--muted); font-size: 7.8pt; font-weight: 600; padding-top: 1px; }}
.pub.first .tag {{ color: var(--coral); }}
.ptitle {{ font-weight: 600; }}
.yr {{ color: var(--teal); font-weight: 700; font-variant-numeric: tabular-nums; }}
.muted {{ color: var(--muted); }}
.role {{ margin: 0 0 5px; padding: 5px 9px; background: var(--soft); border-left: 3px solid var(--teal); border-radius: 4px; font-size: 8.8pt; }}
.pill {{ display: inline-block; font-size: 7.6pt; font-weight: 600; padding: 0 7px; border-radius: 999px; background: #e7f5f3; color: #0b5e57; margin-left: 4px; }}
.doi {{ color: var(--muted); font-size: 8pt; }}
.skills {{ border-collapse: collapse; }} .skills th {{ text-align: left; padding: 1px 12px 1px 0; color: var(--navy); white-space: nowrap; vertical-align: top; }} .skills td {{ padding: 1px 0; }}
b {{ font-weight: 700; }}
</style></head><body>
<header>
  {photo}
  <div>
    <h1>{T["name"]}<small>{T["name_sub"]}</small></h1>
    <p class="role-line">{T["title"]}</p>
    <p class="unit">{T["unit"]}</p>
    <div class="contact">{contact}</div>
  </div>
</header>
<div class="metrics">{metrics}</div>
{''.join(parts)}
</body></html>'''


for lang, fname in [('en', 'cv.html'), ('zh', 'cv_zh.html')]:
    out = os.path.join(ROOT, 'tools', fname)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(build(lang))
    print('wrote', out)
print('stats', STATS)
print('groups', [(g[0], g[1], g[3]) for g in GROUPED], 'ungrouped', [c.get('title_en') for c in OTHER])
