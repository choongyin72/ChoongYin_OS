import json
from pathlib import Path
R = Path(r"C:\Projects\ChoongYin_OS"); EC = R / "workstreams/master-plan/ec-automation"
def a(s): return str(s).encode("ascii", "replace").decode("ascii")
fams = json.loads((EC / "docs/screen_families.json").read_text(encoding="utf-8"))
BAD = ["ov-gm", "manageobject:form:t_data", "op production unit", "pr #244", "gated-navigator"]
NEG = ["no cascade", "no op pu", "not necessarily"]
for scr, fam in sorted(fams.items()):
    if fam == "ovgm":
        continue
    folder = scr.replace(" ", "_")
    files = [f for d in EC.rglob(folder) if d.is_dir() for f in d.rglob("*.md")]
    kb = R / "ec-ui-knowledge" / "screens" / (folder.lower() + ".md")
    if kb.is_file():
        files.append(kb)
    shown = False
    for f in sorted(files):
        for n, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            low = line.lower()
            if any(b in low for b in BAD) and not any(g in low for g in NEG):
                if not shown:
                    print(a("\n##### %s  [%s]" % (scr, fam))); shown = True
                print(a("  %s:%d | %s" % (f.name, n, line.strip()[:170])))
