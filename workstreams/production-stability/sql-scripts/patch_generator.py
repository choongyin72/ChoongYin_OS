fix = """
# POST-BUILD FIXES
for section in doc.sections:
    for para in section.header.paragraphs:
        for run in para.runs:
            if 'Technical Gap Analysis' in (run.text or ''):
                run.text = run.text.replace('Technical Gap Analysis', 'Test Evidence')
for para in list(doc.paragraphs):
    if 'Project Management Methodology' in para.text:
        para._element.getparent().remove(para._element)
"""
path = r'C:\Projects\ChoongYin_OS\workstreams\production-stability\sql-scripts\update_doc_with_screenshots.py'
with open(path, 'r') as f:
    content = f.read()
if 'POST-BUILD FIXES' not in content:
    content = content.replace('doc.save(OUT)', fix + '\ndoc.save(OUT)')
    with open(path, 'w') as f:
        f.write(content)
    print("Generator patched.")
else:
    print("Already patched.")
