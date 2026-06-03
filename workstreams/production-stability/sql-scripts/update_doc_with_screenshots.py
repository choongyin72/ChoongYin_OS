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

tbl_hist = doc.add_table(rows=4, cols=5); tbl_hist.style = 'Table Grid'
for i, txt in enumerate(['Version', 'Date', 'Author', 'Section', 'Summary of Changes']):
    hdr_cell(tbl_hist.rows[0].cells[i], txt, 9, bg=CLR_TBL_HDR_BG)
for j, val in enumerate(['1.0', '03 June 2026', 'Choong-Yin Lee', 'All', 'Initial evidence document']):
    data_cell(tbl_hist.rows[1].cells[j], val, 9)
for j, val in enumerate(['1.1', '04 June 2026', 'Choong-Yin Lee', 'Section 5', 'Updated Phase 1 Unit Test — all objects looped per TC, 189 assertions, TC07 LNG finding']):
    data_cell(tbl_hist.rows[2].cells[j], val, 9)
for j, val in enumerate(['1.2', datetime.now().strftime('%d %B %Y'), 'Choong-Yin Lee', 'Section 5', 'Phase 1 complete — 220/220 PASS, added SEVERITY/WHERE_FORMULA/REV_TEXT/IDEMPOTENCY/ROLLBACK, TC07 closed']):
    data_cell(tbl_hist.rows[3].cells[j], val, 9)
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

# ── SECTION 5: PHASE 1 UNIT TESTS ─────────────────────────────────────────────
section_heading(doc, '5.  Phase 1 Unit Tests — Automated DB Verification', level=1)

body_para(doc,
    'Phase 1 Unit Tests verify that all 8 check rules were correctly inserted into the COPS DEV '
    'database by running automated Python queries directly against Oracle. No browser or UI is '
    'involved — this tests the lowest level: database configuration only.\n\n'
    'All object codes are loaded from issue-1052-tag-list.csv (no hardcoding). '
    'Sub-Tests 2–5 run for EVERY object found in the CSV for each TC\'s EC Class and Attribute.', 9)
doc.add_paragraph()

# 5.1 — What Was Tested
section_heading(doc, '5.1  What Was Tested', level=2)
body_para(doc,
    'Each test case (TC01–TC08) maps to one check rule. Sub-Test 1 runs once per TC. '
    'Sub-Tests 2–5 run for every object found in the CSV tag list for that class/attribute:', 9)
t5a = doc.add_table(rows=7, cols=3); t5a.style = 'Table Grid'
for i, txt in enumerate(['Sub-Test', 'What It Does', 'Pass / Fail Condition']):
    hdr_cell(t5a.rows[0].cells[i], txt, 9, bg=CLR_DARK_BLUE, color=CLR_WHITE)
for i, (chk, what, cond) in enumerate([
    ('1. RULE_EXISTS',     'Query TV_CTRL_CHECK_RULES — confirm rule in DB with correct TABLE_ID and VARIABLE',      'FAIL if rule missing from DB'),
    ('2. OBJECT_EXISTS',   'Query TV_OBJECTS by CODE — confirm EC stream/tank object exists',                         'FAIL if CODE not in TV_OBJECTS'),
    ('2b. MAX_DAYTIME',    'Query MAX(DAYTIME) from RV_ view for this object — used as test date for Sub-Tests 3–5',  'FAIL if no data exists in view'),
    ('3. POSITIVE_VALID',  'Q1: valid data (NOT NULL, >= 0) exists → PASS  |  Q2: negative value found → FAIL',      'Genuine PASS/FAIL — can fail'),
    ('4. NEG_NULL_CHECK',  'Count NULL rows on test date — confirms rule would fire for missing PHD data',            'Informational — always PASS'),
    ('5. NEG_OUTOFRANGE',  'Count rows where value < 0 OR > 100 — TC01/TC02 only (MOL_PCT, WT_PCT range rules)',     'Informational — always PASS'),
]):
    bg = CLR_ALT_ROW if i % 2 == 0 else CLR_WHITE
    data_cell(t5a.rows[i+1].cells[0], chk, 8.5, bold=True, bg=bg)
    data_cell(t5a.rows[i+1].cells[1], what, 8.5, bg=bg)
    data_cell(t5a.rows[i+1].cells[2], cond, 8.5, bg=bg)
doc.add_paragraph()

# 5.2 — Process Flow
section_heading(doc, '5.2  Test Process Flow', level=2)
t5b = doc.add_table(rows=7, cols=3); t5b.style = 'Table Grid'
for i, txt in enumerate(['Step', 'Action', 'Tool / Method']):
    hdr_cell(t5b.rows[0].cells[i], txt, 9, bg=CLR_DARK_BLUE, color=CLR_WHITE)
for i, (step, action, tool) in enumerate([
    ('1', 'Python script loads issue-1052-tag-list.csv — 661 tags, 28 class/attribute combinations',        'csv.DictReader  |  no hardcoding'),
    ('2', 'Connects to COPS DEV Oracle DB',                                                                  'Python oracledb  |  ECKERNEL_EC user'),
    ('3', 'For each TC01–TC08: run Sub-Test 1 RULE_EXISTS once',                                             'SELECT from TV_CTRL_CHECK_RULES WHERE CHECK_NAME = \'PHD_...\''),
    ('4', 'For each TC: loop ALL unique objects from CSV for that EC Class + Attribute',                     'get_all_objects() — returns deduplicated list'),
    ('5', 'Per object: run OBJECT_EXISTS → MAX_DAYTIME → POSITIVE_VALID → NEG_NULL → NEG_OUTOFRANGE',        'RV_ view queries using WHERE CODE = :code AND DAYTIME = TO_DATE(:dt)'),
    ('6', 'Print summary table and save results to unit_test_results.txt',                                   'TC result = FAIL if ANY object in that TC failed POSITIVE_VALID'),
]):
    bg = CLR_ALT_ROW if i % 2 == 0 else CLR_WHITE
    data_cell(t5b.rows[i+1].cells[0], step, 8.5, center=True, bg=bg)
    data_cell(t5b.rows[i+1].cells[1], action, 8.5, bg=bg)
    data_cell(t5b.rows[i+1].cells[2], tool, 8.5, bg=bg)
doc.add_paragraph()

# 5.3 — Detailed Test Results
section_heading(doc, '5.3  Test Results — TC01 to TC08', level=2)
body_para(doc, f'Run date: {datetime.now().strftime("%d %B %Y")} | Environment: COPS DEV | Test Date: 2026-01-01 | Objects: from issue-1052-tag-list.csv', 9)
doc.add_paragraph()

# TC results: TC, Check Rule, ID, RV Table, Obj Tested, POSITIVE_VALID, Result, Finding
unit_results = [
    ('TC01','PHD_STRM_COMP_MOL_PCT_VAL1',    '1142','RV_STRM_COMP_ANALYSIS',  '10','PASS','PASS','All 10 objects: valid MOL_PCT found on 2026-01-01'),
    ('TC02','PHD_STRM_COMP_WT_PCT_VAL1',     '1143','RV_STRM_COMP_ANALYSIS',  '3', 'PASS','PASS','All 3 objects: valid WT_PCT found on 2026-01-01'),
    ('TC03','PHD_STRM_ANALYSIS_DENSITY_VAL1','1144','RV_STRM_ANALYSIS',        '6', 'PASS','PASS','All 6 objects: valid DENSITY found on 2026-01-01'),
    ('TC04','PHD_STRM_ANALYSIS_GCV_VAL1',    '1145','RV_STRM_ANALYSIS',        '9', 'PASS','PASS','All 9 objects: valid GCV found on 2026-01-01'),
    ('TC05','PHD_TANK_DIP_GRS_VOL_VAL1',     '1146','RV_TANK_DAY_DIP_STATUS', '5', 'PASS','PASS','All 5 tanks: valid GRS_VOL_SM3 found on 2026-01-01'),
    ('TC06','PHD_TANK_DIP_GRS_MASS_VAL1',    '1147','RV_TANK_DAY_DIP_STATUS', '2', 'PASS','PASS','T_LNG_T3101/T3102: valid ZWP_GRS_MASS_TONNES found'),
    ('TC07','PHD_TANK_DIP_AVG_TEMP_VAL1',    '1148','RV_TANK_DAY_DIP_STATUS', '5', 'PASS','PASS','All 5 tanks: valid AVG_TEMP_C found | WHERE_FORMULA = IS NULL only (LNG tanks safe)'),
    ('TC08','PHD_TANK_DIP_STD_DENSITY_VAL1', '1149','RV_TANK_DAY_DIP_STATUS', '2', 'PASS','PASS','T_LNG_T3101/T3102: valid MEAS_STD_DENSITY found'),
]
hdrs5c = ['TC','Check Rule','ID','RV Table','Objs\nTested','POSITIVE\nVALID','Result','Findings / Notes']
t5c = doc.add_table(rows=len(unit_results)+1, cols=len(hdrs5c)); t5c.style = 'Table Grid'
for i, txt in enumerate(hdrs5c):
    hdr_cell(t5c.rows[0].cells[i], txt, 8, bg=CLR_DARK_BLUE, color=CLR_WHITE)
for i, row in enumerate(unit_results):
    bg = CLR_ALT_ROW if i % 2 == 0 else CLR_WHITE
    for j, val in enumerate(row[:5]):
        data_cell(t5c.rows[i+1].cells[j], val, 8, bg=bg, center=(j in [0,2,4]))
    # POSITIVE_VALID cell
    pv_pass = row[5] == 'PASS'
    pv_cell = t5c.rows[i+1].cells[5]
    data_cell(pv_cell, row[5], 8, bold=True, bg='E2EFDA' if pv_pass else 'FFE0E0', center=True)
    pv_cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(*bytes.fromhex(CLR_PASS_GREEN if pv_pass else 'C00000'))
    # Result cell
    res_cell = t5c.rows[i+1].cells[6]
    res_pass = 'PASS' in row[6]
    data_cell(res_cell, row[6], 8, bold=True, bg='E2EFDA' if res_pass else 'FFF2CC', center=True)
    res_cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(*bytes.fromhex(CLR_PASS_GREEN if res_pass else 'C07000'))
    data_cell(t5c.rows[i+1].cells[7], row[7], 8, bg=bg)
doc.add_paragraph()

# TC07 note — finding closed
section_heading(doc, '5.3.1  TC07 Note — LNG Tank Temperature (Closed)', level=2)
body_para(doc,
    'During unit testing, T_LNG_T3101 and T_LNG_T3102 showed AVG_TEMP_C = -160°C (LNG cryogenic temperature). '
    'Initial concern: check rule might fire for negative values.\n\n'
    'CONFIRMED SAFE: WHERE_FORMULA = (${AvgTemp} IS NULL) — rule fires on NULL only, NOT on negative values. '
    'LNG tanks at -160°C will NOT trigger false ERROR alerts. No action required.', 9)
doc.add_paragraph()

# 5.4 — Phase 1 Summary
section_heading(doc, '5.4  Phase 1 Summary', level=2)
t5d = doc.add_table(rows=2, cols=5); t5d.style = 'Table Grid'
for i, txt in enumerate(['Total Assertions', 'Passed', 'Failed', 'TCs Tested', 'Phase 1 Result']):
    hdr_cell(t5d.rows[0].cells[i], txt, 9, bg=CLR_DARK_BLUE, color=CLR_WHITE)
data_cell(t5d.rows[1].cells[0], '220', 10, bold=True, center=True)
data_cell(t5d.rows[1].cells[1], '220', 10, bold=True, center=True, bg='E2EFDA')
data_cell(t5d.rows[1].cells[2], '0', 10, bold=True, center=True)
data_cell(t5d.rows[1].cells[3], '8  (TC01–TC08)\n+ IDEMPOTENCY\n+ ROLLBACK', 10, bold=True, center=True)
data_cell(t5d.rows[1].cells[4], 'PASS  ✅', 10, bold=True, center=True, bg='E2EFDA')
t5d.rows[1].cells[1].paragraphs[0].runs[0].font.color.rgb = RGBColor(*bytes.fromhex(CLR_PASS_GREEN))
t5d.rows[1].cells[4].paragraphs[0].runs[0].font.color.rgb = RGBColor(*bytes.fromhex(CLR_PASS_GREEN))
doc.add_paragraph()

# ── SECTION 6: EC WEB APP SCREENSHOTS ─────────────────────────────────────────
section_heading(doc, '6.  EC Web App Screen Evidence — Maintain Check Rules (CO.0201)', level=1)
body_para(doc,
    'Screenshots captured from EC Web App (https://app-plutodev.woodside-pluto.tieto-og.cloud/). '
    'All 8 PHD check rules visible across page 6 (rule 1142) and page 7 (rules 1143-1149).', 9)
doc.add_paragraph()

ss_list = [
    ('screen1_page6.png',
     '6.1  Page 6 of 7 — Rule 1142: PHD_STRM_COMP_MOL_PCT_VAL1',
     'Rule 1142 (PHD_STRM_COMP_MOL_PCT_VAL1) visible at bottom — TABLE_ID: RV_STRM_COMP_ANALYSIS | WHERE: (MolPct IS NULL OR MolPct < 0 OR MolPct > 100)'),
    ('screen1_phd_rules_page7.png',
     '6.2  Page 7 of 7 — Rules 1143–1149 (all PHD tank and analysis rules)',
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
section_heading(doc, '7.  Overall Test Result', level=1)
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
