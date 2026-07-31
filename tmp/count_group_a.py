import json, re
from pathlib import Path
R = Path(r"C:\Projects\ChoongYin_OS")
def a(s): return str(s).encode("ascii","replace").decode("ascii")

doc = (R/"tmp/unhandled_object_classes.md").read_text(encoding="utf-8", errors="replace")
m_a = re.search(r"^## A\.", doc, re.M); m_b = re.search(r"^## B\.", doc, re.M)
assert m_a, "section '## A.' not found"
sec = doc[m_a.end(): m_b.start() if m_b else len(doc)]

rows = []
for l in sec.splitlines():
    if not l.strip().startswith("|"): continue
    c = [x.strip() for x in l.strip().strip("|").split("|")]
    if len(c) < 3: continue
    if not re.fullmatch(r"\d+", c[0]): continue          # data rows start with an index number
    rows.append((c[1], c[2]))                             # (CLASS, screen label)
assert rows, "no data rows parsed"
print(a("Parsed %d class rows from section A (doc header claims 42)" % len(rows)))

labels = sorted({lab for _, lab in rows})
print(a("Distinct SCREEN labels: %d  (labels shared by >1 class: %s)" % (
    len(labels), sorted({l for l in labels if sum(1 for _, x in rows if x == l) > 1}))))

fam = json.loads((R/"workstreams/master-plan/ec-automation/docs/screen_families.json").read_text(encoding="utf-8"))
reg = (R/"workstreams/master-plan/ec-automation/docs/ec_screen_registry.md").read_text(encoding="utf-8", errors="replace")
parked = (R/"tmp/OV_SWEEP_PARKED.md").read_text(encoding="utf-8", errors="replace").lower()

done, park, todo = [], [], []
for lab in labels:
    in_fam = any(lab.lower() == k.lower() for k in fam)
    in_reg = re.search(r"^\|\s*%s\s*(\(|\|)" % re.escape(lab), reg, re.M | re.I) is not None
    if in_fam or in_reg: done.append(lab)
    elif re.search(r"^#+ %s\b" % re.escape(lab.lower()), parked, re.M): park.append(lab)
    else: todo.append(lab)

print(a("\n  DONE     : %d  %s" % (len(done), done)))
print(a("  PARKED   : %d  %s" % (len(park), park)))
print(a("  REMAINING: %d" % len(todo)))
for i, n in enumerate(todo, 1): print(a("     %2d. %s" % (i, n)))
