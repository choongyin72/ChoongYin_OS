"""
Generate Issue_1052 evidence document using Technical Gap Analysis template.
Template: C:\Projects\ChoongYin_OS\Template Sources\Technical Gap Analysis.dotx
"""
import shutil, zipfile, os
from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from datetime import datetime
from pathlib import Path
from copy import deepcopy
from lxml import etree

SCRIPTS_DIR = Path(r'C:\Projects\ChoongYin_OS\workstreams\production-stability\sql-scripts')
SS_DIR = SCRIPTS_DIR / 'screenshots'
TPL_SRC = r'C:\Projects\ChoongYin_OS\Template Sources\Technical Gap Analysis.dotx'
OUT = str(SCRIPTS_DIR / 'Issue1052_Evidence_COPS_DEV.docx')

# Template color scheme
CLR_DARK_BLUE = '1F497D'
CLR_LIGHT_BLUE = '548DD4'
CLR_TBL_HDR_BG = 'DAEEF3'
CLR_WHITE = 'FFFFFF'
CLR_PASS_GREEN = '00B050'
CLR_ALT_ROW = 'EEF3FB'


# ── Load template by patching content type ─────────────────────────────────────
def load_template(src):
    tmp = src + '_tmp.docx'
    shutil.copy(src, tmp)
    with zipfile.ZipFile(tmp) as zin:
        ct = zin.read('[Content_Types].xml')
    ct2 = ct.replace(
        b'wordprocessingml.template.main+xml',
        b'wordprocessingml.document.main+xml'
    )
    tmp2 = src + '_patched.docx'
    with zipfile.ZipFile(tmp, 'r') as zin:
        with zipfile.ZipFile(tmp2, 'w', zipfile.ZIP_DEFLATED) as zout:
            for item in zin.namelist():
                zout.writestr(item, ct2 if item == '[Content_Types].xml' else zin.read(item))
    doc = Document(tmp2)
    os.remove(tmp); os.remove(tmp2)
    return doc


# ── Helpers ────────────────────────────────────────────────────────────────────
def set_bg(cell, color):
    tc = cell._tc; tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), color)
    tcPr.append(shd)


def add_run(para, text, size=10, bold=False, color=None, italic=False):
    run = para.add_run(text)
    run.font.size = Pt(size); run.bold = bold; run.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*bytes.fromhex(color))
    return run


def hdr_cell(cell, text, size=9, bg=CLR_TBL_HDR_BG, color='17375E'):
    cell.text = ''
    p = cell.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text); run.bold = True; run.font.size = Pt(size)
    run.font.color.rgb = RGBColor(*bytes.fromhex(color))
    set_bg(cell, bg)


def data_cell(cell, text, size=8.5, bold=False, bg=None, center=False):
    cell.text = ''
    p = cell.paragraphs[0]
    if center: p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(str(text) if text else '-')
    run.font.size = Pt(size); run.bold = bold
    if bg: set_bg(cell, bg)


def section_heading(doc, text, level=1):
    p = doc.add_paragraph(style=f'Heading {level}')
    p.clear()
    run = p.add_run(text)
    run.bold = True
    run.font.name = 'Arial'
    run.font.color.rgb = RGBColor(*bytes.fromhex(CLR_DARK_BLUE))
    if level == 1: run.font.size = Pt(14)
    else: run.font.size = Pt(12)
    return p


def body_para(doc, text, size=10):
    try:
        p = doc.add_paragraph(style='Normal (Boxtext)')
    except:
        p = doc.add_paragraph()
    p.clear()
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.name = 'Arial'
    return p


# ── Build Document ─────────────────────────────────────────────────────────────
print("Loading template...")
doc = load_template(TPL_SRC)

# Clear ALL existing content from the template
for element in list(doc.element.body):
    if element.tag.endswith('}sectPr'):
        continue  # keep section properties
    doc.element.body.remove(element)

print("Building evidence document from template...")

# ── TITLE BLOCK ────────────────────────────────────────────────────────────────
# "Project Management Methodology" banner
p_banner = doc.add_paragraph()
try:
    p_banner.style = doc.styles['Normal (Boxtext)']
except:
    pass
p_banner.alignment = WD_ALIGN_PARAGRAPH.LEFT
run = p_banner.add_run('\tProject Management Methodology')
run.bold = True; run.font.name = 'Arial'; run.font.size = Pt(10)
run.font.color.rgb = RGBColor(*bytes.fromhex(CLR_LIGHT_BLUE))

# Document title
p_title = doc.add_paragraph()
try: p_title.style = doc.styles['Title']
except: pass
p_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
run = p_title.add_run('Issue_1052 — PHD Tag Check Rule Validation')
run.font.name = 'Arial'; run.font.size = Pt(22); run.bold = True
run.font.color.rgb = RGBColor(*bytes.fromhex(CLR_DARK_BLUE))

p_sub = doc.add_paragraph()
try: p_sub.style = doc.styles['Title']
except: pass
run2 = p_sub.add_run('Test Evidence Document — COPS DEV Environment')
run2.font.name = 'Arial'; run2.font.size = Pt(14)
run2.font.color.rgb = RGBColor(*bytes.fromhex(CLR_LIGHT_BLUE))
doc.add_paragraph()

# ── SUMMARY TABLE (template style) ────────────────────────────────────────────
p_sh = doc.add_paragraph()
try: p_sh.style = doc.styles['Small Heading']
except: pass
run = p_sh.add_run('Summary Page')
run.font.name = 'Arial'; run.bold = True; run.font.size = Pt(11)
run.font.color.rgb = RGBColor(*bytes.fromhex(CLR_DARK_BLUE))

tbl_info = doc.add_table(rows=8, cols=2)
tbl_info.style = 'Table Grid'
summary_data = [
    ('Document Name',    'Issue_1052 — PHD Check Rule Validation Evidence'),
    ('Author',           'Choong-Yin Lee'),
    ('Project',          'Woodside Pluto ECaaS Implementation (12839)'),
    ('Project Phase',    'Wave 03 — UAT'),
    ('Project Task ID',  '12839 / 15681'),
    ('Document Issue',   f'Draft — {datetime.now().strftime("%d %B %Y")}'),
    ('Environment',      'COPS DEV  |  EC 14.1.5.1'),
    ('JIRA Reference',   'Issue_1052 — PHD Validations for TAGs >= 1 Dec 2025'),
]
for i, (lbl, val) in enumerate(summary_data):
    hdr_cell(tbl_info.rows[i].cells[0], lbl, 9, bg=CLR_TBL_HDR_BG, color='17375E')
    data_cell(tbl_info.rows[i].cells[1], val, 9)
doc.add_paragraph()

# ── DOCUMENT HISTORY TABLE ─────────────────────────────────────────────────────
p_hist = doc.add_paragraph()
try: p_hist.style = doc.styles['Small Heading']
except: pass
run = p_hist.add_run('Document History')
run.font.name = 'Arial'; run.bold = True; run.font.size = Pt(11)
run.font.color.rgb = RGBColor(*bytes.fromhex(CLR_DARK_BLUE))

tbl_hist = doc.add_table(rows=2, cols=5); tbl_hist.style = 'Table Grid'
for i, txt in enumerate(['Version', 'Date', 'Author', 'Section', 'Summary of Changes']):
    hdr_cell(tbl_hist.rows[0].cells[i], txt, 9, bg=CLR_TBL_HDR_BG)
for j, val in enumerate(['1.0', datetime.now().strftime('%d %B %Y'), 'Choong-Yin Lee', 'All', 'Initial evidence document']):
    data_cell(tbl_hist.rows[1].cells[j], val, 9)
doc.add_paragraph()

# ── SECTION 1: PURPOSE ─────────────────────────────────────────────────────────
section_heading(doc, '1.  Purpose', level=1)
body_para(doc,
    'This document provides evidence that the check rule SQL script for Issue_1052 has been '
    'successfully tested in the COPS DEV environment. '
    'The script implements check rules for 131 PHD tags (added since 1 Dec 2025) that had '
    'NO check rule validation configured in the system.')
doc.add_paragraph()

# ── SECTION 2: SCRIPT TESTED ──────────────────────────────────────────────────
section_heading(doc, '2.  Script Tested', level=1)
t2 = doc.add_table(rows=2, cols=3); t2.style = 'Table Grid'
for i, txt in enumerate(['Script File', 'Purpose', 'Status']):
    hdr_cell(t2.rows[0].cells[i], txt, 9, bg=CLR_DARK_BLUE, color=CLR_WHITE)
data_cell(t2.rows[1].cells[0], 'Issue1052_PHD_Check_Rules.sql', 9)
data_cell(t2.rows[1].cells[1], 'INSERT / UPDATE 8 check rules — UPDATE-then-INSERT pattern (re-runnable)', 9)
data_cell(t2.rows[1].cells[2], 'PASS  ✅', 9, bold=True, bg=CLR_PASS_GREEN, center=True)
t2.rows[1].cells[2].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
doc.add_paragraph()

# ── SECTION 3: TEST STEPS ─────────────────────────────────────────────────────
section_heading(doc, '3.  Test Steps & Results', level=1)
t3 = doc.add_table(rows=4, cols=4); t3.style = 'Table Grid'
for i, txt in enumerate(['Step', 'Action', 'Expected', 'Actual Result']):
    hdr_cell(t3.rows[0].cells[i], txt, 9, bg=CLR_DARK_BLUE, color=CLR_WHITE)
for i, (step, action, exp, act) in enumerate([
    ('1', 'Verify baseline — no check rules exist in DB', '0 rows', '0 rows    PASS'),
    ('2', 'Run Issue1052_PHD_Check_Rules.sql\n8 rules INSERTED, COMMIT OK', '8 INSERTED', '8 rules INSERTED    PASS'),
    ('3', 'Verify after INSERT — query DB for all 8 rules', '8 rows', '8 rows confirmed    PASS'),
]):
    bg = CLR_ALT_ROW if i % 2 == 0 else CLR_WHITE
    data_cell(t3.rows[i+1].cells[0], step, 9, center=True, bg=bg)
    data_cell(t3.rows[i+1].cells[1], action, 9, bg=bg)
    data_cell(t3.rows[i+1].cells[2], exp, 9, center=True, bg=bg)
    data_cell(t3.rows[i+1].cells[3], act, 9, bold=True, bg='E2EFDA')
doc.add_paragraph()

# ── SECTION 4: DB EVIDENCE ────────────────────────────────────────────────────
section_heading(doc, '4.  Database Evidence — Check Rules Verified', level=1)
body_para(doc, f'Records confirmed in TV_CTRL_CHECK_RULES and TV_CTRL_CHECK_RULE_VARIABLE ({datetime.now().strftime("%Y-%m-%d")}):', 9)
t4 = doc.add_table(rows=9, cols=6); t4.style = 'Table Grid'
for i, txt in enumerate(['CHECK_ID', 'CHECK_NAME', 'TABLE_ID', 'SEV', 'VARIABLE  VALUE', 'REV_TEXT']):
    hdr_cell(t4.rows[0].cells[i], txt, 8, bg=CLR_DARK_BLUE, color=CLR_WHITE)
for i, row in enumerate([
    (1142,'PHD_STRM_COMP_MOL_PCT_VAL1',    'RV_STRM_COMP_ANALYSIS', 'ERROR','MolPct = MOL_PCT',                    'ECPR-Issue1052'),
    (1143,'PHD_STRM_COMP_WT_PCT_VAL1',     'RV_STRM_COMP_ANALYSIS', 'ERROR','WtPct = WT_PCT',                      'ECPR-Issue1052'),
    (1144,'PHD_STRM_ANALYSIS_DENSITY_VAL1','RV_STRM_ANALYSIS',       'ERROR','Density = DENSITY',                   'ECPR-Issue1052'),
    (1145,'PHD_STRM_ANALYSIS_GCV_VAL1',    'RV_STRM_ANALYSIS',       'ERROR','Gcv = GCV_MJPERSM3',                  'ECPR-Issue1052'),
    (1146,'PHD_TANK_DIP_GRS_VOL_VAL1',     'RV_TANK_DAY_DIP_STATUS','ERROR','GrsVol = GRS_VOL_SM3',               'ECPR-Issue1052'),
    (1147,'PHD_TANK_DIP_GRS_MASS_VAL1',    'RV_TANK_DAY_DIP_STATUS','ERROR','GrsMass = ZWP_GRS_MASS_TONNES',      'ECPR-Issue1052'),
    (1148,'PHD_TANK_DIP_AVG_TEMP_VAL1',    'RV_TANK_DAY_DIP_STATUS','ERROR','AvgTemp = AVG_TEMP_C',               'ECPR-Issue1052'),
    (1149,'PHD_TANK_DIP_STD_DENSITY_VAL1', 'RV_TANK_DAY_DIP_STATUS','ERROR','StdDensity = MEAS_STD_DENSITY_KGPERSM3','ECPR-Issue1052'),
]):
    bg = CLR_ALT_ROW if i % 2 == 0 else CLR_WHITE
    for j, val in enumerate([str(row[0]),row[1],row[2],row[3],row[4],row[5]]):
        data_cell(t4.rows[i+1].cells[j], val, 8, bg=bg)
doc.add_paragraph()

# ── SECTION 5: EC WEB APP SCREENSHOTS ─────────────────────────────────────────
section_heading(doc, '5.  EC Web App Screen Evidence — Maintain Check Rules (CO.0201)', level=1)
body_para(doc,
    'Screenshots captured from EC Web App (https://app-plutodev.woodside-pluto.tieto-og.cloud/). '
    'All 8 PHD check rules visible across page 6 (rule 1142) and page 7 (rules 1143-1149).', 9)
doc.add_paragraph()

ss_list = [
    ('screen1_page6.png',
     '5.1  Page 6 of 7 — Rule 1142: PHD_STRM_COMP_MOL_PCT_VAL1',
     'Rule 1142 (PHD_STRM_COMP_MOL_PCT_VAL1) visible at bottom — TABLE_ID: RV_STRM_COMP_ANALYSIS | WHERE: (MolPct IS NULL OR MolPct < 0 OR MolPct > 100)'),
    ('screen1_phd_rules_page7.png',
     '5.2  Page 7 of 7 — Rules 1143–1149 (all PHD tank and analysis rules)',
     'Rules 1143–1149 all visible — covering STRM_COMP_ANALYSIS, STRM_ANALYSIS and TANK_DAY_DIP_STATUS classes'),
]
for fname, heading, caption in ss_list:
    fpath = SS_DIR / fname
    section_heading(doc, heading, level=2)
    body_para(doc, caption, 8)
    if fpath.exists():
        doc.add_picture(str(fpath), width=Inches(6.2))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    else:
        body_para(doc, f'[Screenshot not found: {fname}]', 9)
    doc.add_paragraph()

# ── SECTION 6: OVERALL RESULT ──────────────────────────────────────────────────
section_heading(doc, '6.  Overall Test Result', level=1)
rt = doc.add_table(rows=1, cols=1); rt.style = 'Table Grid'
c = rt.rows[0].cells[0]; set_bg(c, CLR_PASS_GREEN); c.text = ''
pp = c.paragraphs[0]; pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
r4 = pp.add_run('OVERALL RESULT:   PASS   ✅')
r4.font.size = Pt(14); r4.bold = True; r4.font.name = 'Arial'
r4.font.color.rgb = RGBColor(255, 255, 255)
doc.add_paragraph()

# Sign-off
p_sign = doc.add_paragraph()
p_sign.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p_sign.add_run(
    f'Tested by: Choong-Yin Lee    |    '
    f'Date: {datetime.now().strftime("%d %B %Y")}    |    '
    f'Environment: COPS DEV (EC 14.1.5.1)')
run.font.size = Pt(9); run.italic = True; run.font.name = 'Arial'
run.font.color.rgb = RGBColor(*bytes.fromhex(CLR_LIGHT_BLUE))

# Save

# POST-BUILD FIXES
for section in doc.sections:
    for para in section.header.paragraphs:
        for run in para.runs:
            if 'Technical Gap Analysis' in (run.text or ''):
                run.text = run.text.replace('Technical Gap Analysis', 'Test Evidence')
for para in list(doc.paragraphs):
    if 'Project Management Methodology' in para.text:
        para._element.getparent().remove(para._element)

doc.save(OUT)
print(f'Saved: {OUT}')
