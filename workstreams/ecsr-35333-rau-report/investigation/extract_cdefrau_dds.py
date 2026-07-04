"""
Chop-extract ONLY section 4.1 'C_DEF_RAU_CALC - Deferment and RAU' (Description/Inputs/Steps/
Outputs) from the local Calc DDS, so we don't load the whole 28MB doc.
Walks body blocks (paragraphs + tables) in order; prints from the 4.1 heading until the next
top-level calc section. Read-only.
"""
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph

DOC = r"C:\Projects\ChoongYin_OS\docs\WSPLU_EC_AsBuilt06_Calculations_v1.0.docx"
doc = Document(DOC)
body = doc.element.body


def iter_blocks(parent):
    for child in parent.iterchildren():
        if child.tag.endswith('}p'):
            yield Paragraph(child, doc)
        elif child.tag.endswith('}tbl'):
            yield Table(child, doc)


def tbl_text(t):
    out = []
    for row in t.rows:
        cells = [c.text.strip().replace('\n', ' ') for c in row.cells]
        out.append(" | ".join(cells))
    return "\n".join(out)


blocks = list(iter_blocks(body))
# find the section-4.1 heading (a Heading-styled paragraph containing C_DEF_RAU_CALC, NOT a TOC line)
start = -1
for i, b in enumerate(blocks):
    if isinstance(b, Paragraph) and 'C_DEF_RAU_CALC' in b.text:
        st = b.style.name if b.style else ''
        if 'Heading' in st or st.startswith('Title'):
            start = i
            break
if start < 0:  # fallback: last occurrence of the term anywhere
    for i, b in enumerate(blocks):
        if isinstance(b, Paragraph) and 'C_DEF_RAU_CALC' in b.text:
            start = i
print(f"start block index = {start} (of {len(blocks)})")
if start < 0:
    raise SystemExit("C_DEF_RAU_CALC heading not found")

printed = 0
for b in blocks[start:start + 200]:
    if isinstance(b, Paragraph):
        txt = b.text.strip()
        st = b.style.name if b.style else ''
        # stop at the next top-level calc section heading (4.2 / next C_ calc), after we've started
        if printed > 3 and ('Heading 1' in st or 'Heading 2' in st) and 'C_DEF_RAU_CALC' not in txt \
           and (txt[:3].startswith('4.2') or txt[:2] == '5 ' or 'CALC' in txt.upper().split(' ')[0:2].__str__()):
            print(f"\n--- stop at next section: <{st}> {txt[:80]} ---")
            break
        if txt:
            print(f"[{st}] {txt}")
            printed += 1
    else:
        print("TABLE:")
        print(tbl_text(b))
        printed += 1
    if printed > 140:
        print("\n...(capped at 140 blocks)")
        break
