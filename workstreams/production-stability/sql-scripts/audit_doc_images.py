from docx import Document
from docx.oxml.ns import qn
DOC=r"c:/Projects/ChoongYin_OS/workstreams/production-stability/sql-scripts/Issue1052_Evidence_COPS_DEV.docx"
doc=Document(DOC)
# walk body elements in order; track current heading; count inline images (w:drawing / pic)
body=doc.element.body
cur_head="(top)"
img_by_head={}
heads=[]
def text_of(p):
    return ''.join(n.text or '' for n in p.iter(qn('w:t')))
from docx.text.paragraph import Paragraph
for child in body.iterchildren():
    if child.tag==qn('w:p'):
        p=Paragraph(child,doc)
        if p.style.name.startswith('Heading'):
            cur_head=p.text.strip()
            heads.append(cur_head)
            img_by_head.setdefault(cur_head,0)
        # count drawings in this paragraph
        n=len(child.findall('.//'+qn('w:drawing')))
        if n: img_by_head[cur_head]=img_by_head.get(cur_head,0)+n
print("=== screenshots (inline images) per section ===")
for h in heads:
    c=img_by_head.get(h,0)
    flag=' <-- HAS IMAGES' if c else ''
    print(f"  {c:>2}  {h}{flag}")
# total
total=sum(len(p.findall('.//'+qn('w:drawing'))) for p in body.findall('.//'+qn('w:p')))
print("\n  total inline images in doc:", total)
