from pathlib import Path
p = Path(r"C:\Projects\ChoongYin_OS\tmp\audit_legacy_family_text.py")
s = p.read_text(encoding="utf-8")
old = 'NEG = ["no cascade", "no op pu", "not necessarily"]'
assert s.count(old) == 1
# A line that DESCRIBES the old wrong wording (a correction note, or the #278 history) is not a defect.
new = ('NEG = ["no cascade", "no op pu", "not necessarily",\n'
       '       "was wrong", "claim was", "family text corrected", "does not describe this screen",\n'
       '       "still said", "wording that does not", "is historical"]')
s = s.replace(old, new)
p.write_text(s, encoding="utf-8")
print("audit NEG list extended (corrections/history are not defects)")
