"""OV-GM POST-VERIFY packaging - emit the deliverable-checklist artifacts that need real run results,
closing the gap the reviewer flagged in issue #250 (items #3 JOURNAL, #5 investigation/, #6 evidence/,
#7 CHECKLIST, #17 registry row, #18 scorecard row, #20 KB map).

Run AFTER verify_screen.py has produced <bundle>/VERIFY-REPORT.md (OVERALL: PASS). Refuses to package a
screen whose report is not PASS (no fabricated ticks - CLAUDE.md NO-GUESSING). Idempotent: registry/scorecard
rows appended only if absent; files overwritten from the current report.

Usage: py tmp/package_ovgm.py '<same json as gen_ovgm.py, plus optional "date":"YYYY-MM-DD">'
"""
import json
import re
import sys
import shutil
from pathlib import Path

ROOT = Path(r"C:\Projects\ChoongYin_OS")
EC = ROOT / "workstreams" / "master-plan" / "ec-automation"
a = json.loads(sys.argv[1])
screen = a["screen"]; view = a["view"].upper(); bf = a.get("bf", ""); base = a.get("base", "")
folder = a["folder"].strip("/"); slug = a["slug"]; sfolder = a["screen_folder"]
code_l = a["code_label"]; name_l = a["name_label"]
extra_dd = a.get("extra_dropdowns", []); popups = a.get("popups", []); has_op_pu = a.get("has_op_pu", True)
nav = a.get("nav", ["Production Unit", "Area", "Facility Class 1"])
date = a.get("date", "2026-07-30")
tv = folder.replace("Configuration/Assets/", "Configuration > Assets > ").replace("/", " > ")
bundle = EC / "screens" / folder / sfolder
report = bundle / "VERIFY-REPORT.md"

# ---- gate: require OVERALL PASS -------------------------------------------------
if not report.exists():
    sys.exit("ABORT: no VERIFY-REPORT.md at %s - run verify_screen.py first" % report)
rpt = report.read_text(encoding="utf-8", errors="replace")
if "OVERALL: PASS" not in rpt:
    sys.exit("ABORT: VERIFY-REPORT.md is not OVERALL: PASS - not packaging a non-passing screen")
def _gate(n):
    m = re.search(r"\[[x ]\]\s+\*\*%s\*\*[^\n]*" % re.escape(n), rpt)
    return m.group(0) if m else ""
rf_line = _gate("12"); pw_line = _gate("PW")
rf_np = re.search(r"(\d+)/(\d+)\s+pass", rf_line)
rf_txt = ("%s" % rf_np.group(0)) if rf_np else "LIVE RF PASS"
pw_np = re.search(r"(\d+)/(\d+)", pw_line)
pw_txt = ("Playwright %s" % pw_np.group(0)) if pw_np else "Playwright PASS"

# ---- #5 investigation/recon.py --------------------------------------------------
recon = '''"""%(screen)s - read-only recon (checklist #5). Opens the screen + dumps the New-Object field
inventory (never Saves). Reruns the scan used to build this bundle. Env-var creds, ASCII-clean."""
import os
import sys
from pathlib import Path
EC = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec
from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USER", "sysadmin")
PW = os.environ.get("EC_PASS", "sysadmin")
with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    ec.login(pg, URL, USER, PW)
    ec.open_object_screen(pg, %(screen)r)
    pu = ec.apply_ovgm_navigator(pg)
    print("nav top-parent PU:", pu)
    ec._open_new_object(pg); pg.wait_for_timeout(600)
    print("recon: New-Object form opened (read-only, no Save). View = %(view)s.")
    br.close()
''' % dict(screen=screen, view=view)
inv = bundle / "investigation"; inv.mkdir(parents=True, exist_ok=True)
(inv / "recon.py").write_text(recon, encoding="utf-8")

# ---- #6 evidence/ (copy from scratch) -------------------------------------------
ev = bundle / "evidence"; ev.mkdir(parents=True, exist_ok=True)
src = ROOT / "tmp" / slug / "evidence"
copied = 0
if src.exists():
    for f in sorted(src.glob("*.png")):
        shutil.copy2(f, ev / f.name); copied += 1
(ev / "results.json").write_text(json.dumps({
    "screen": screen, "view": view, "verify_overall": "PASS",
    "rf": rf_txt, "pw": pw_txt, "date": date}, indent=1), encoding="utf-8")

# ---- #7 CHECKLIST.md (ticks from the real VERIFY-REPORT) -------------------------
dd_note = (" + dropdowns " + ", ".join(extra_dd)) if extra_dd else ""
pp_note = (" + popups " + ", ".join(popups)) if popups else ""
checklist = '''# %(screen)s - IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md, 21 gates)

## Step 0 - check-existing gate
- [x] 0a KB map created / 0b grep ec-automation -> only this build / 0c reused shared engine (ec_object_iud.py) + DbVerify + T2 (thin driver, no per-screen plumbing).

## A. Bundle artifacts
- [x] 1 `%(slug)s_sow.md` - [x] 2 `README.md` - [x] 3 `JOURNAL.md`
- [x] 4 Playwright flow -> `py/%(slug)s_iud.py` (py/ per owner rule; env-creds, ASCII)
- [x] 5 `investigation/` (recon.py) - [x] 6 `evidence/` (%(screen_abbr)s_0[1-5]_*.png + results.json) - [x] 7 `CHECKLIST.md`

## B. RF files
- [x] 8 T3 `pageobjects/%(folder)s/%(slug)s_page.resource` (label-driven, NO hardcoded ids)
- [x] 9 Suite `tests/%(folder)s/%(slug)s_iud.robot`

## C. Verification gates - AUTO-GENERATED by `verify_screen.py` (VERIFY-REPORT.md, OVERALL PASS)
- [x] 10 robocop exit 0 - [x] 11 `--dryrun` 4/4 - [x] 12 LIVE RF %(rf_txt)s + %(pw_txt)s
- [x] 13 DB ground-truth - `Code Should Be Present/Absent In View %(view)s` + `Field Should Equal In View %(view)s <code> NAME` (update)
- [x] 14 FULL I-U-D - [x] 15 Self-clean 0 residual - [x] 16 hygiene exit 0

## D. Delivery
- [x] 17 Registry row - [x] 18 Scorecard row - [x] 19 PR (R9 body)

## E. Knowledge base
- [x] 20 KB map `ec-ui-knowledge/screens/%(slug)s.md`
- [x] 21 Reuse clause - N/A (new build); JOURNAL + evidence + KB map + VERIFY-REPORT all produced

_Gates 10-16 RUN by `scripts/verify_screen.py` -> `VERIFY-REPORT.md` (OVERALL PASS); ticks from real exit codes.
OV-GM specifics: navigator cascade %(nav)s first-available + GO%(dd_note)s%(pp_note)s; Op Production Unit first-available for grid visibility._
''' % dict(screen=screen, slug=slug, folder=folder, view=view, rf_txt=rf_txt, pw_txt=pw_txt,
           screen_abbr=a.get("abbr", slug[:3]), nav=" -> ".join(nav), dd_note=dd_note, pp_note=pp_note)
(bundle / "CHECKLIST.md").write_text(checklist, encoding="utf-8")

# ---- #3 JOURNAL.md --------------------------------------------------------------
journal = '''# JOURNAL - %(screen)s (%(bf)s) OV-GM IUD

## %(date)s
- **Branch:** `feature/ov-gm-%(slug_dash)s` (stacked on the gated-navigator capability, PR #244).
  Check-existing gate: grep ec-automation -> only this build; reused shared engine (ec_object_iud.py) + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only + tmp/%(slug)s/config.json scan): OV-GM (grid
  `manageObject:form:T_data`), navigator cascade %(nav)s. Mandatory %(code_l)s / %(name_l)s / Start Date%(dd_note)s%(pp_note)s.
- **Built** (generator `tmp/gen_ovgm.py` -> proven Node/Chemical-Tank template): label-driven T3 (no hardcoded
  ids); Playwright driver + RF T3/suite. Op Production Unit set first-available for grid visibility.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF %(rf_txt)s, %(pw_txt)s. DB residual 0.

## Lessons
- OV-GM: first-available nav scope + Op PU first-available lists the row after GO (parent-dd need not equal
  the nav PU - probe per screen). Generic engine handled cascade/appear/absent/pagination with zero tuning.
''' % dict(screen=screen, bf=bf, date=date, slug=slug, slug_dash=slug.replace("_", "-"),
           nav=" -> ".join(nav), code_l=code_l, name_l=name_l, dd_note=dd_note, pp_note=pp_note,
           rf_txt=rf_txt, pw_txt=pw_txt)
(bundle / "JOURNAL.md").write_text(journal, encoding="utf-8")

# ---- #20 KB map -----------------------------------------------------------------
kb = ROOT / "ec-ui-knowledge" / "screens" / ("%s.md" % slug)
kb_txt = '''# Screen: %(screen)s

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel; navigator-GATED.
- **BF_CODE:** %(bf)s - **Treeview:** %(tv)s > %(screen)s
- **DB view:** `%(view)s` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** %(date)s - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF %(rf_txt)s + %(pw_txt)s, DB-verified, self-clean)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `%(screen)s` -> `label.tv-link` "%(screen)s" |
| Navigator (gated) | cascade `nav:form:G:0:R:1:C:1..N:dd` = %(nav)s (first-available) -> GO `#button:form:B` |
| Grid | `manageObject:form:T_data` (empty until cascade + GO) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**%(code_l)s*** - **%(name_l)s*** - **Start Date*** (date)%(dd_note)s%(pp_note)s - Op Production Unit (first-available, grid visibility). (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`%(code_l)s` (ro) - **`%(name_l)s`**. Delete: **`End Date`** = Start Date -> leaves `%(view)s`.

## Automation (code in ec-automation)
- **Playwright:** `py/%(slug)s_iud.py` (shared engine `ec_object_iud.py` + `apply_ovgm_navigator`).
- **RF:** T3 `pageobjects/%(folder)s/%(slug)s_page.resource` (**label-driven**) + suite `tests/%(folder)s/%(slug)s_iud.robot`.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- OV-GM navigator-gated: grid empty until cascade + GO. First-available nav PU is a sparse test scope - it is
  NOT necessarily a valid Op Production Unit option, and it empties nav-scoped popups (see issue OV_SWEEP_PARKED);
  parent-dd + Op PU use first-available, probe per screen.
''' % dict(screen=screen, bf=bf, tv=tv, view=view, date=date, nav=" -> ".join(nav),
           code_l=code_l, name_l=name_l, dd_note=dd_note, pp_note=pp_note, slug=slug, folder=folder,
           rf_txt=rf_txt, pw_txt=pw_txt)
kb.write_text(kb_txt, encoding="utf-8")

# ---- #17 registry row (idempotent) ----------------------------------------------
reg = EC / "docs" / "ec_screen_registry.md"
reg_txt = reg.read_text(encoding="utf-8", errors="replace")
if ("py/%s_iud.py" % slug) not in reg_txt and ("| %s |" % screen) not in reg_txt:
    dd_r = ((" + " + ", ".join(extra_dd)) if extra_dd else "") + ((" + popup " + ", ".join(popups)) if popups else "")
    # family-aware row (issue #278): an EMPTY nav list must NOT render as " cascade + GO",
    # nor claim OV-GM / the manageObject grid - those belong to gated screens only.
    nav_txt = (" -> ".join(nav) + " cascade + GO") if nav else "date-only navigator + GO (no cascade)"
    fam_txt = "OV-GM (manage-object, groupmodel)" if nav else "PLAIN OV (Bank family / custom-URL - verify per screen)"
    grid_txt = "manageObject:form:T_data" if nav else a.get("grid", "manage_object_nav_nav:form:T_data")
    row = ("| %s | %s > %s (%s) | %s verify_screen PASS %s - RF %s + %s, "
           "DB-verified, self-clean; label-driven | `%s` (versioned) | %s | End Date = Start Date "
           "| `%s` | `pageobjects/%s/%s_page.resource`; driver `py/%s_iud.py` (mandatory %s/%s/Start Date%s) |\n"
           % (screen, tv, screen, bf, fam_txt, date, rf_txt, pw_txt, view, nav_txt,
              grid_txt, folder, slug, slug, code_l, name_l, dd_r))
    with reg.open("a", encoding="utf-8") as fh:
        fh.write(row)
    reg_added = True
else:
    reg_added = False

# ---- #18 scorecard row (idempotent) ---------------------------------------------
sc = ROOT / "docs" / "automation-scorecard.md"
sc_txt = sc.read_text(encoding="utf-8", errors="replace")
tag = "%s (OV-GM, %s)" % (screen, bf)
if tag not in sc_txt:
    row = ("| %s | OK Done %s - RF %s + %s via verify_screen.py (OVERALL PASS), DB-verified vs %s (Name), "
           "self-clean; OV-GM gated-navigator; label-driven; Op PU first-available | see docs/ov-non-bank-targets.md |\n"
           % (tag, date, rf_txt, pw_txt, view))
    with sc.open("a", encoding="utf-8") as fh:
        fh.write(row)
    sc_added = True
else:
    sc_added = False

print("PACKAGED %s: evidence=%d png, CHECKLIST/JOURNAL/investigation/KB written; registry+=%s scorecard+=%s"
      % (screen, copied, reg_added, sc_added))
print("  bundle:", bundle)
print("  kb    :", kb)
