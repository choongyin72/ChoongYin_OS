from pathlib import Path
p = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation\docs\ov-non-bank-targets.md")
s = p.read_text(encoding="utf-8")
for bf, scr, view, pr in (("CO.0264","Truck","OV_TRUCK","#277"), ("CO.0265","Trailer","OV_TRAILER","#279"),
                          ("CO.0266","Driver","OV_DRIVER","#281")):
    old = "| %s | %s | %s | Assets > Transport Objects | [ ] |" % (bf, scr, view)
    assert s.count(old) == 1, old
    s = s.replace(old, "| %s | %s | %s | Assets > Transport Objects | [x] %s (plain OV) |" % (bf, scr, view, pr))
p.write_text(s, encoding="utf-8")
print("3 shipped-screen checkboxes corrected")
