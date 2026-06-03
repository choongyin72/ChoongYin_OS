"""
Rebuild the evidence Word document with actual EC Web App screenshots.
"""
from docx import Document
from docx.shared import Pt, RGBColor, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from datetime import datetime
from pathlib import Path

SCRIPTS_DIR = Path(r'C:\Projects\ChoongYin_OS\workstreams\production-stability\sql-scripts')
SS_DIR = SCRIPTS_DIR / 'screenshots'


def set_bg(cell, color):
    tc = cell._tc; tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), color)
    tcPr.append(shd)


def hdr(cell, text, size=9):
    cell.text = ''
    p = cell.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text); run.bold = True; run.font.size = Pt(size)
    run.font.color.rgb = RGBColor(255, 255, 255); set_bg(cell, '1F497D')


def cv(cell, text, size=8.5, bold=False, color=None, bg=None, center=False):
    cell.text = ''
    p = cell.paragraphs[0]
    if center: p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(str(text) if text else '-')
    run.font.size = Pt(size); run.bold = bold
    if color: run.font.color.rgb = RGBColor(*bytes.fromhex(color))
    if bg: set_bg(cell, bg)


doc = Document()
for s in doc.sections:
    s.top_margin = Cm(1.5); s.bottom_margin = Cm(1.5)
    s.left_margin = Cm(2); s.right_margin = Cm(2)

# ── Title ──────────────────────────────────────────────────────────────────────
h = doc.add_heading('', 0); h.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = h.add_run('Issue_1052 — PHD Tag Check Rule Validation')
r.font.size = Pt(16); r.bold = True; r.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)
sub = doc.add_paragraph(); sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
r2 = sub.add_run('Test Evidence Document — COPS DEV Environment')
r2.font.size = Pt(11); r2.italic = True; r2.font.color.rgb = RGBColor(0x59, 0x59, 0x59)
doc.add_paragraph()

# ── Info ───────────────────────────────────────────────────────────────────────
info = doc.add_table(rows=7, cols=2); info.style = 'Table Grid'
for i, (lbl, val) in enumerate([
    ('Document Title',  'Issue_1052 — PHD Check Rule Validation Evidence'),
    ('Prepared by',     'Choong-Yin Lee  |  choong-yin.lee@quorumsoftware.com'),
    ('Date',            datetime.now().strftime('%d %B %Y')),
    ('Environment',     'COPS DEV  |  EC 14.1.5.1'),
    ('Database',        'db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev'),
    ('Schema',          'ECKERNEL_EC'),
    ('JIRA Reference',  'Issue_1052 — Review PHD Validations for added TAGs >= 1 Dec 2025'),
]):
    hdr(info.rows[i].cells[0], lbl, 9); cv(info.rows[i].cells[1], val, 9)
doc.add_paragraph()

# ── Section 1 ──────────────────────────────────────────────────────────────────
doc.add_heading('1. Purpose', level=1)
p1 = doc.add_paragraph(
    'This document provides evidence that the check rule SQL script for Issue_1052 has been '
    'successfully tested in the COPS DEV environment. The script implements check rules for '
    '131 PHD tags (added since 1 Dec 2025) that had NO check rule validation configured.')
p1.runs[0].font.size = Pt(10)

# ── Section 2 ──────────────────────────────────────────────────────────────────
doc.add_heading('2. Script Tested', level=1)
t2 = doc.add_table(rows=2, cols=3); t2.style = 'Table Grid'
for i, txt in enumerate(['Script File', 'Purpose', 'Status']): hdr(t2.rows[0].cells[i], txt)
cv(t2.rows[1].cells[0], 'Issue1052_PHD_Check_Rules.sql', 8.5)
cv(t2.rows[1].cells[1], 'INSERT / UPDATE 8 check rules — UPDATE-then-INSERT pattern (re-runnable)', 8.5)
cv(t2.rows[1].cells[2], 'PASS  ✅', 9, bold=True, bg='00B050', color='FFFFFF', center=True)
doc.add_paragraph()

# ── Section 3 ──────────────────────────────────────────────────────────────────
doc.add_heading('3. Test Steps & Results', level=1)
t3 = doc.add_table(rows=4, cols=4); t3.style = 'Table Grid'
for i, txt in enumerate(['Step', 'Action', 'Expected', 'Actual Result']): hdr(t3.rows[0].cells[i], txt)
for i, (step, action, exp, act) in enumerate([
    ('1', 'Verify baseline — no check rules exist in DB', '0 rows', '0 rows    PASS'),
    ('2', 'Run Issue1052_PHD_Check_Rules.sql\n8 rules INSERTED, COMMIT OK', '8 INSERTED', '8 rules INSERTED    PASS'),
    ('3', 'Verify after INSERT — query DB for all 8 rules', '8 rows', '8 rows confirmed    PASS'),
]):
    bg = 'F2F2F2' if i % 2 == 0 else 'FFFFFF'
    cv(t3.rows[i+1].cells[0], step, 9, center=True, bg=bg)
    cv(t3.rows[i+1].cells[1], action, 8.5, bg=bg)
    cv(t3.rows[i+1].cells[2], exp, 8.5, center=True, bg=bg)
    cv(t3.rows[i+1].cells[3], act, 8.5, bold=True, bg='E2EFDA')
doc.add_paragraph()

# ── Section 4 ──────────────────────────────────────────────────────────────────
doc.add_heading('4. Database Evidence — Check Rules Verified', level=1)
doc.add_paragraph(
    'Records confirmed in TV_CTRL_CHECK_RULES and TV_CTRL_CHECK_RULE_VARIABLE '
    '(timestamp: ' + datetime.now().strftime('%Y-%m-%d') + '):'
).runs[0].font.size = Pt(9)
t4 = doc.add_table(rows=9, cols=6); t4.style = 'Table Grid'
for i, txt in enumerate(['CHECK_ID', 'CHECK_NAME', 'TABLE_ID', 'SEV', 'VARIABLE  VALUE', 'REV_TEXT']):
    hdr(t4.rows[0].cells[i], txt, 8)
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
    bg = 'F2F2F2' if i % 2 == 0 else 'FFFFFF'
    for j, val in enumerate([str(row[0]), row[1], row[2], row[3], row[4], row[5]]):
        cv(t4.rows[i+1].cells[j], val, 8, bg=bg)
doc.add_paragraph()

# ── Section 5 — EC WEB APP SCREENSHOTS ────────────────────────────────────────
doc.add_heading('5. EC Web App Screen Evidence — Maintain Check Rules (CO.0201)', level=1)
doc.add_paragraph(
    'Screenshots captured from EC Web App (https://app-plutodev.woodside-pluto.tieto-og.cloud/) '
    'showing the 8 PHD check rules successfully created in the Maintain Check Rules screen.\n'
    'All 8 rules visible across page 6 (rule 1142) and page 7 (rules 1143-1149).'
).runs[0].font.size = Pt(9)

ss_list = [
    ('screen1_page6.png',       'Screen 1A — Maintain Check Rules (Page 6 of 7)\nRule 1142: PHD_STRM_COMP_MOL_PCT_VAL1 visible at bottom — TABLE_ID: RV_STRM_COMP_ANALYSIS'),
    ('screen1_phd_rules_page7.png', 'Screen 1B — Maintain Check Rules (Page 7 of 7)\nRules 1143–1149 all visible — TANK_DAY_DIP_STATUS and STRM_ANALYSIS rules'),
]

for fname, caption in ss_list:
    fpath = SS_DIR / fname
    if fpath.exists():
        doc.add_heading(f'  {caption.split(chr(10))[0]}', level=2)
        note = doc.add_paragraph(caption.split('\n')[1] if '\n' in caption else '')
        note.runs[0].font.size = Pt(8)
        note.runs[0].font.color.rgb = RGBColor(0x60, 0x60, 0x60)
        doc.add_picture(str(fpath), width=Inches(6.5))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_paragraph()
    else:
        doc.add_paragraph(f'[Screenshot not found: {fname}]')

# ── Section 6 ──────────────────────────────────────────────────────────────────
doc.add_heading('6. Overall Test Result', level=1)
rt = doc.add_table(rows=1, cols=1); rt.style = 'Table Grid'
c = rt.rows[0].cells[0]; set_bg(c, '00B050'); c.text = ''
pp = c.paragraphs[0]; pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
r4 = pp.add_run('OVERALL RESULT:   PASS   ✅')
r4.font.size = Pt(14); r4.bold = True; r4.font.color.rgb = RGBColor(255, 255, 255)
doc.add_paragraph()
sp = doc.add_paragraph(
    f'Tested by: Choong-Yin Lee    |    '
    f'Date: {datetime.now().strftime("%d %B %Y")}    |    '
    f'Environment: COPS DEV (EC 14.1.5.1)')
sp.alignment = WD_ALIGN_PARAGRAPH.CENTER
sp.runs[0].font.size = Pt(9); sp.runs[0].italic = True

out = str(SCRIPTS_DIR / 'Issue1052_Evidence_COPS_DEV.docx')
doc.save(out)
print(f'Saved: {out}')
