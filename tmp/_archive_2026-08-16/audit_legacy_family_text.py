import json
from pathlib import Path
R = Path(r"C:\Projects\ChoongYin_OS"); EC = R / "workstreams/master-plan/ec-automation"
def a(s): return str(s).encode("ascii", "replace").decode("ascii")
fams = json.loads((EC / "docs/screen_families.json").read_text(encoding="utf-8"))
BAD = ["ov-gm", "manageobject:form:t_data", "op production unit", "pr #244", "gated-navigator"]
NEG = ["no cascade", "no op pu", "not necessarily",
       "was wrong", "claim was", "family text corrected", "does not describe this screen",
       "still said", "wording that does not", "is historical"]
hits, checked = {}, 0
for scr, fam in sorted(fams.items()):
    if fam == "ovgm":
        continue
    checked += 1
    folder = scr.replace(" ", "_")
    files = [f for d in EC.rglob(folder) if d.is_dir() for f in d.rglob("*.md")]
    kb = R / "ec-ui-knowledge" / "screens" / (folder.lower() + ".md")
    if kb.is_file():
        files.append(kb)
    for f in files:
        for n, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            low = line.lower()
            if any(b in low for b in BAD) and not any(g in low for g in NEG):
                hits.setdefault("%s (%s)" % (scr, fam), []).append("%s:%d" % (f.name, n))
print(a("non-OV-GM screens checked: %d" % checked))
print(a("screens WITH residual OV-GM text: %d" % len(hits)))
for k, v in sorted(hits.items()):
    print(a("   %-32s %d hit(s): %s" % (k, len(v), ", ".join(v[:6]))))
