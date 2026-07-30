"""Cross-ref the 71 Bank-layout (manage_object_nav) screens vs existing RF coverage. READ-ONLY.
Coverage key = the OV_ view name referenced in ec-automation pageobjects/tests."""
import re
from pathlib import Path

NOTES = Path(r"C:\Projects\ChoongYin_OS\DeepDiveLearnings\ec-screens\notes")
EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")

# 1) gather all existing RF text (pageobjects + tests), lowercased
blob = []
for sub in ("pageobjects", "tests"):
    for f in (EC / sub).rglob("*"):
        if f.suffix in (".resource", ".robot"):
            try:
                blob.append(f.read_text(encoding="utf-8", errors="ignore").lower())
            except Exception:
                pass
blob = "\n".join(blob)

# 2) the 71: parse notes with Bank's controller
rows = []
for md in NOTES.glob("*.md"):
    txt = md.read_text(encoding="utf-8", errors="ignore")
    if "manage_object_nav/CLASS_NAME" not in txt:
        continue
    title = txt.splitlines()[0].lstrip("# ").strip()
    m = re.search(r"OV_[A-Z0-9_]+", txt)
    view = m.group(0) if m else "?"
    covered = view != "?" and bool(re.search(r"\b" + re.escape(view.lower()) + r"\b", blob))
    rows.append((title, view, covered))

rows.sort()
cov = [r for r in rows if r[2]]
unc = [r for r in rows if not r[2]]
print(f"TOTAL manage_object_nav screens: {len(rows)}  |  COVERED: {len(cov)}  |  UNCOVERED: {len(unc)}\n")
print("=" * 60)
print(f"UNCOVERED (reuse targets) - {len(unc)}")
print("=" * 60)
for t, v, _ in unc:
    print(f"  [ ] {t:<45} {v}")
print("\n" + "=" * 60)
print(f"COVERED (already have RF suite) - {len(cov)}")
print("=" * 60)
for t, v, _ in cov:
    print(f"  [x] {t:<45} {v}")
