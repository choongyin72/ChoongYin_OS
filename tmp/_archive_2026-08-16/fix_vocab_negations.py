from pathlib import Path
p = Path(r"C:\Projects\ChoongYin_OS\tmp\check_row_vocab.py")
s = p.read_text(encoding="utf-8")
old = '"unusable", "n/a cascade",'
assert s.count(old) == 1
s = s.replace(old, '"unusable", "n/a cascade",\n'
                   '             "no op pu", "no op production unit", "without op pu", "not one\n"[:0] or "no op",')
p.write_text(s, encoding="utf-8")
print("negations: 'no Op PU' phrasings added")
