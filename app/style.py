"""Neo-brutalist press-sheet styling for the existing Streamlit app."""
from __future__ import annotations
import base64
from pathlib import Path
import streamlit as st

ASSETS=Path(__file__).resolve().parent/'assets'


def inject_style():
    regular=base64.b64encode((ASSETS/'HostGrotesk-Regular.ttf').read_bytes()).decode('ascii')
    heavy=base64.b64encode((ASSETS/'HostGrotesk-ExtraBold.ttf').read_bytes()).decode('ascii')
    st.markdown(f'''<style>
@font-face {{font-family:'NeoBrutalismHost';src:url(data:font/truetype;base64,{regular}) format('truetype');font-weight:400;font-display:swap}}
@font-face {{font-family:'NeoBrutalismHost';src:url(data:font/truetype;base64,{heavy}) format('truetype');font-weight:700 900;font-display:swap}}
:root {{
  --dp-color-ground:#fff5d6;--dp-color-ink:#000000;--dp-color-emphasis:#ffed00;
  --dp-color-signal:#ff4332;--dp-color-field:#d4bdff;--dp-color-contrast:#ffffff;
  --dp-typography-face:'NeoBrutalismHost',sans-serif;
  --dp-typography-body:17px;--dp-typography-reading:16px;
  --dp-typography-small:14px;--dp-typography-metadata:13px;
  --dp-typography-label:12px;--dp-typography-reading-weight:700;
  --dp-typography-emphasis-weight:800;--dp-typography-display-weight:900;
  --dp-typography-display-tracking:-.065em;
  --dp-spacing-gap:24px;--dp-spacing-gap-compact:18px;
  --dp-radius-control:0;--dp-border-panel:4px;--dp-border-divider:3px;
  --dp-border-annotation:2px;--dp-motion-interaction:0s;
}}
html,body,.stApp,[class*="css"] {{font-family:var(--dp-typography-face);color:#000}}
.stApp {{background:var(--dp-color-ground)}}
div[data-testid="stMainBlockContainer"].block-container {{max-width:1260px!important;padding-top:4.5rem!important;padding-bottom:4.8rem!important}}
header[data-testid="stHeader"] {{background:var(--dp-color-ground)}}
.stMarkdown p,p,li {{font-family:var(--dp-typography-face);font-size:16px;line-height:1.55;color:#000}}
h1,h2,h3 {{font-family:var(--dp-typography-face);color:#000;letter-spacing:-.035em;font-weight:800}}
h2 {{font-size:clamp(1.65rem,2.7vw,2.5rem);line-height:1.17;margin:0 0 .7rem}}
h3 {{font-size:1.15rem}}
/* The native Streamlit controls remain keyboard accessible. */
[data-testid="stRadio"] > div {{gap:10px;flex-wrap:wrap}}
[data-testid="stRadio"] label {{border:3px solid #000;border-radius:0;background:#fff;padding:7px 13px;margin-right:0;box-shadow:4px 4px 0 #000;font-weight:800;transition:none}}
[data-testid="stRadio"] label:has(input:checked) {{background:var(--dp-color-emphasis)}}
[data-testid="stRadio"] label p {{font-size:14px;font-weight:800;line-height:1.2}}
[data-testid="stRadio"] label:focus-within {{outline:3px solid var(--dp-color-signal);outline-offset:5px}}
[data-testid="stSelectbox"] > div > div {{border:3px solid #000;border-radius:0;background:#fff;box-shadow:4px 4px 0 #000}}
[data-testid="stSelectbox"]:focus-within > div > div {{outline:3px solid var(--dp-color-signal);outline-offset:4px}}
[data-testid="stSelectbox"] label p {{font-weight:800}}
[data-testid="stExpander"] {{border:3px solid #000;border-radius:0;background:#fff;box-shadow:5px 5px 0 #000}}
[data-testid="stExpander"] summary {{font-weight:800}}
[data-testid="stExpander"] summary:focus-visible {{outline:3px solid var(--dp-color-signal);outline-offset:3px}}
[data-testid="stDataFrame"],div.stPlotlyChart {{background:#fff;border:4px solid #000;border-radius:0;padding:5px;box-shadow:8px 8px 0 #000}}
[data-testid="stDownloadButton"] button,button[kind="secondary"] {{background:var(--dp-color-emphasis);color:#000;border:3px solid #000;border-radius:0;box-shadow:5px 5px 0 #000;font-weight:900;transition:none}}
[data-testid="stDownloadButton"] button:hover,button[kind="secondary"]:hover {{background:var(--dp-color-field);color:#000;transform:translate(-2px,-2px);box-shadow:7px 7px 0 #000}}
[data-testid="stDownloadButton"] button:active,button[kind="secondary"]:active {{transform:translate(3px,3px);box-shadow:2px 2px 0 #000}}
button:focus-visible,[role="button"]:focus-visible {{outline:3px solid var(--dp-color-signal)!important;outline-offset:5px!important}}
/* Reading order stays in document flow; only decorative pieces overlap. */
.brand {{display:flex;align-items:center;justify-content:space-between;border-bottom:4px solid #000;padding:3px 0 12px;margin-bottom:22px;gap:18px}}
.brand-name {{font-size:20px;font-weight:900;letter-spacing:-.045em}}
.brand-dot {{display:inline-block;width:18px;height:18px;background:var(--dp-color-signal);border:3px solid #000;margin-right:8px;vertical-align:-1px}}
.brand-meta {{font-size:13px;font-weight:800;letter-spacing:.04em;text-transform:uppercase}}
.hero {{background:var(--dp-color-emphasis);color:#000;border:5px solid #000;box-shadow:12px 12px 0 #000;padding:23px 28px 22px;position:relative;margin:20px 13px 30px 0;overflow:visible}}
.hero-top {{display:flex;justify-content:space-between;align-items:start;gap:20px}}
.hero-label {{font-size:14px;letter-spacing:.025em;font-weight:800;border-bottom:3px solid #000;padding-bottom:4px}}
.hero-arrow {{display:flex;align-items:center;justify-content:center;background:var(--dp-color-signal);border:4px solid #000;width:58px;height:58px;font-size:38px;font-weight:900;line-height:1;transform:rotate(5deg);flex:none}}
.poster-strips {{display:flex;flex-direction:column;align-items:flex-start;gap:7px;margin:15px 0 6px}}
.strip {{display:inline-block;font-weight:900;letter-spacing:-.065em;text-transform:uppercase;line-height:.96;padding:5px 13px 9px;font-size:clamp(2.2rem,5vw,4.7rem);border:4px solid #000}}
.strip-white {{background:#fff;transform:rotate(-1deg);z-index:2}}
.strip-black {{background:#000;color:#fff;transform:rotate(.7deg);margin-left:30px}}
.hero h1 {{font-size:clamp(5rem,8vw,7.6rem);font-weight:900;letter-spacing:-.095em;line-height:.9;margin:10px 0 6px;color:#000;text-transform:none}}
.hero p {{display:none}}
.hero-foot {{font-size:14px;font-weight:700;border-top:3px solid #000;padding-top:9px;margin-top:12px}}
.hero-band {{background:var(--dp-color-field);border:4px solid #000;box-shadow:8px 8px 0 #000;padding:18px 22px;margin:0 15px 29px 0;display:flex;align-items:center;justify-content:space-between;gap:24px}}
.hero-band p {{font-size:17px;font-weight:400;line-height:1.55;margin:0;max-width:850px}}
.hero-band b {{display:inline-block;border:3px solid #000;background:#fff;padding:7px 10px;white-space:nowrap;font-size:13px;text-transform:uppercase}}
.statrow {{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin:24px 10px 36px 0}}
.stat {{background:#fff;border:4px solid #000;box-shadow:7px 7px 0 #000;padding:17px 19px;min-height:118px}}
.stat:nth-child(2) {{background:var(--dp-color-field)}}
.stat:nth-child(3) {{background:var(--dp-color-emphasis)}}
.stat .value {{font-size:clamp(1.7rem,3.2vw,3rem);font-weight:900;letter-spacing:-.065em;line-height:1}}
.stat .label {{font-size:15px;font-weight:700;line-height:1.4;border-top:2px solid #000;padding-top:8px;margin-top:9px}}
.eyebrow {{font-size:13px;letter-spacing:.09em;text-transform:uppercase;font-weight:900;border:3px solid #000;background:var(--dp-color-signal);display:inline-block;padding:3px 8px;margin:20px 0 12px;transform:rotate(-1deg)}}
.deck {{font-size:17px;font-weight:400;max-width:920px;line-height:1.58;margin-bottom:18px}}
.feature {{background:#fff;border:4px solid #000;box-shadow:7px 7px 0 #000;padding:18px 20px;margin:7px 8px 17px 0}}
.feature:nth-child(2) {{background:var(--dp-color-emphasis)}}
.feature strong {{font-size:clamp(1.8rem,3vw,2.9rem);font-weight:900;letter-spacing:-.065em;line-height:1}}
.feature p {{font-size:16px;font-weight:400;line-height:1.45;border-top:2px solid #000;margin:9px 0 0;padding-top:8px}}
.note {{border:4px solid #000;background:var(--dp-color-field);box-shadow:6px 6px 0 #000;padding:13px 17px;margin:25px 8px 22px 0;font-size:16px;font-weight:400;line-height:1.55}}
.caption {{font-size:15px;font-weight:400;line-height:1.55;margin:10px 0 25px}}
.sectionline {{border-top:4px solid #000;margin:38px 0 18px}}
.intro-poster {{background:var(--dp-color-emphasis);border:5px solid #000;box-shadow:12px 12px 0 #000;padding:27px 31px;margin:22px 13px 34px 0}}
.intro-poster .kicker {{font-size:14px;font-weight:800;letter-spacing:.04em;text-transform:uppercase;border-bottom:3px solid #000;display:inline-block;padding-bottom:5px}}
.intro-poster h1 {{font-size:clamp(2.2rem,5.3vw,5rem);line-height:1.02;letter-spacing:-.065em;font-weight:900;text-transform:uppercase;max-width:1000px;margin:19px 0 14px}}
.intro-poster p {{font-size:18px;line-height:1.55;max-width:900px;margin:0}}
.intro-grid {{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin:18px 9px 28px 0}}
.intro-card {{background:#fff;border:4px solid #000;box-shadow:7px 7px 0 #000;padding:17px 18px}}
.intro-card:nth-child(2) {{background:var(--dp-color-field)}}
.intro-card:nth-child(3) {{background:var(--dp-color-emphasis)}}
.intro-card .num {{font-size:13px;font-weight:900;background:#000;color:#fff;display:inline-block;padding:2px 7px;margin-bottom:10px}}
.intro-card h3 {{font-size:21px;line-height:1.15;margin:0 0 8px}}
.intro-card p {{font-size:16px;font-weight:400;line-height:1.52;margin:0}}
.flow-grid {{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:15px;margin:17px 9px 26px 0}}
.flow-step {{background:#fff;border:3px solid #000;padding:14px 15px;box-shadow:5px 5px 0 #000}}
.flow-step b {{font-size:13px;background:var(--dp-color-signal);border:2px solid #000;padding:2px 6px}}
.flow-step h3 {{font-size:18px;line-height:1.2;margin:11px 0 5px}}
.flow-step p {{font-size:15px;line-height:1.48;margin:0}}
.req-list {{border:4px solid #000;background:#fff;box-shadow:8px 8px 0 #000;margin:18px 9px 25px 0}}
.req-row {{display:grid;grid-template-columns:48px minmax(0,1fr) 165px;gap:15px;align-items:start;padding:15px 17px;border-bottom:2px solid #000}}
.req-row:last-child {{border-bottom:0}}
.req-num {{font-size:20px;font-weight:900;line-height:1}}
.req-main b {{font-size:17px;font-weight:800}}
.req-main p {{font-size:15px;line-height:1.5;margin:5px 0 0}}
.req-status {{font-size:12px;font-weight:900;text-transform:uppercase;border:2px solid #000;background:var(--dp-color-emphasis);padding:5px 7px;line-height:1.3}}
.req-status.pending {{background:var(--dp-color-field)}}
/* Compact controls and zero motion at reduced-motion preference. */
@media(max-width:1050px) {{.hero {{padding:23px}}.strip {{font-size:clamp(2rem,5vw,4rem)}}.statrow {{gap:14px}}.flow-grid {{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
@media(max-width:720px) {{
 div[data-testid="stMainBlockContainer"].block-container {{padding-left:1rem!important;padding-right:1rem!important}}
 .brand {{align-items:flex-start}}.brand-meta {{display:none}}
 .hero {{padding:18px;margin-right:7px;box-shadow:7px 7px 0 #000}}
 .poster-strips {{gap:5px}}.strip {{font-size:clamp(1.8rem,8vw,3.8rem);transform:none;margin-left:0;padding:4px 7px 7px}}
 .hero-arrow {{width:43px;height:43px;font-size:27px;transform:none}}
 .hero-band {{display:block;margin-right:7px;box-shadow:5px 5px 0 #000}}
 .hero-band b {{margin-top:10px}}
 .statrow {{grid-template-columns:repeat(2,minmax(0,1fr));gap:13px}}
 .stat:last-child:nth-child(3) {{grid-column:span 2}}
 .stat {{box-shadow:5px 5px 0 #000;padding:12px;min-height:105px}}
 [data-testid="stDataFrame"],div.stPlotlyChart {{box-shadow:5px 5px 0 #000}}
 .feature {{box-shadow:5px 5px 0 #000}}
 .intro-poster {{padding:19px;margin-right:7px;box-shadow:7px 7px 0 #000}}
 .intro-grid {{grid-template-columns:1fr;gap:13px}}
 .intro-card {{box-shadow:5px 5px 0 #000}}
 .req-row {{grid-template-columns:32px minmax(0,1fr);gap:8px 12px}}
 .req-status {{grid-column:2;justify-self:start}}
}}
@media(max-width:420px) {{
 .brand-name {{font-size:16px}}.strip {{font-size:clamp(1.5rem,7.7vw,2.7rem)}}
 .hero h1 {{font-size:4.5rem}}.statrow {{grid-template-columns:1fr}}.stat:last-child:nth-child(3) {{grid-column:auto}}
 [data-testid="stRadio"] label {{padding:6px 8px}}[data-testid="stRadio"] label p {{font-size:12px}}
 .flow-grid {{grid-template-columns:1fr}}
}}
@media(prefers-reduced-motion:reduce) {{*,*::before,*::after {{scroll-behavior:auto!important;transition:none!important;animation:none!important}}}}
</style>''',unsafe_allow_html=True)
