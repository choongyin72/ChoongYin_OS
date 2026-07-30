"""Update the 3 tracking docs for a delivered plain OV screen (idempotent-ish):
  - ov-reuse-targets.md: tick the screen's [ ] -> [x] + bump covered/uncovered totals
  - ec_screen_registry.md: append a row
  - automation-scorecard.md: append a row
Usage: py tmp/deliver_docs.py '<json config with extra: ordinal, base_note>'
"""
import json, re, sys
from pathlib import Path

ROOT = Path(r"C:\Projects\ChoongYin_OS")
EC = ROOT / "workstreams" / "master-plan" / "ec-automation"
c = json.loads(sys.argv[1])
bf = c["bfcode"]; screen = c["screen"]; view = c["view"].upper(); slug = c["slug"]
folder = c["folder"].strip("/"); ordn = c.get("ordinal", "?"); base_note = c.get("base_note", "")
code_l = c["code_label"]; name_l = c["name_label"]; date_l = c["date_label"]; end_l = c["end_label"]

# 1) tracker
tp = EC / "docs" / "ov-reuse-targets.md"
s = tp.read_text(encoding="utf-8")
# tick the line for this bf (any leading text screen name)
s2 = re.sub(r"- \[ \] ([^\n]*`%s`[^\n]*)" % re.escape(bf),
            lambda m: "- [x] %s (done 2026-07-26)" % m.group(1), s, count=1)
assert s2 != s, "tracker line not found/ticked for %s" % bf
# bump totals
def bump(m):
    cov = int(m.group(1)) + 1; unc = int(m.group(2)) - 1
    return "**%d covered · %d uncovered**" % (cov, unc)
s3 = re.sub(r"\*\*(\d+) covered · (\d+) uncovered\*\*", bump, s2, count=1)
tp.write_text(s3, encoding="utf-8")
print("tracker: ticked %s + bumped totals" % bf)

# 2) registry (append row at EOF)
rp = EC / "docs" / "ec_screen_registry.md"
rr = rp.read_text(encoding="utf-8")
row = ("| %s | %s > %s (%s) | OV (Bank family) ✅ live 4/4 RF + 7/7 Playwright (2026-07-26) - "
       "**%s OV-reuse-target**; verify_screen.py OVERALL PASS; label-driven (zero hardcoded field ids), "
       "generator-scaffolded | `%s` (versioned) | manage-object (date nav + GO to load) | End Date = Start Date | "
       "`manage_object_nav_nav:form:T_data` | `%s/%s_page.resource` - **label-driven**: mandatory `%s` / `%s` / `%s` "
       "(optional dropdowns skipped); UPDATE `%s` (DB-verified via `Field Should Equal In View %s`); "
       "DELETE objectdates `%s`. Playwright = `py/%s_iud.py` |"
       % (screen, folder.replace("/", " > "), screen, bf, ordn, view, folder, slug,
          code_l, name_l, date_l, name_l, view, end_l, slug))
if row not in rr:
    rp.write_text(rr.rstrip() + "\n" + row + "\n", encoding="utf-8")
print("registry: appended row")

# 3) scorecard (append row at EOF)
sp = ROOT / "docs" / "automation-scorecard.md"
sc = sp.read_text(encoding="utf-8")
srow = ("| %s (OV, %s) | ✅ Done 2026-07-26 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), "
        "DB-verified vs %s (Name), self-clean; %s OV-reuse-target; label-driven, generator-scaffolded%s | "
        "see docs/ov-reuse-targets.md |" % (screen, bf, view, ordn, (" " + base_note) if base_note else ""))
if srow not in sc:
    sp.write_text(sc.rstrip() + "\n" + srow + "\n", encoding="utf-8")
print("scorecard: appended row")
print("DELIVER_DOCS DONE %s" % slug)
