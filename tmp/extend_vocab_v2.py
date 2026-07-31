from pathlib import Path
p = Path(r"C:\Projects\ChoongYin_OS\tmp\check_row_vocab.py")
s = p.read_text(encoding="utf-8")
old = '''    if not bad:
        print("OK: %d row(s) for %r use %r vocabulary consistently" % (len(found), screen, family))
    return 1 if bad else 0'''
assert s.count(old) == 1, "main() tail not found"
new = '''    # the files the ROW-only check never looked at - where the defect class actually survived
    docfails = bundle_doc_mismatches(screen, family)
    if docfails:
        bad = True
        print("MISMATCH (bundle docs) - forbidden for family %r:" % family)
        for where, hits, line in docfails:
            print("   %-22s %s | %s" % (where, hits, line))
    if not bad:
        print("OK: %d row(s) + bundle docs for %r use %r vocabulary consistently"
              % (len(found), screen, family))
    return 1 if bad else 0'''
s = s.replace(old, new)
p.write_text(s, encoding="utf-8")
print("main() now also reports bundle-doc mismatches")
