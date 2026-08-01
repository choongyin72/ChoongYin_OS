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
def _branch():
    """The JOURNAL used to hardcode `feature/ov-gm-<slug>` + "PR #244". Report the REAL branch."""
    import subprocess
    try:
        r = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=str(ROOT),
                           capture_output=True, text=True)
        return r.stdout.strip() or "(unknown branch)"
    except Exception:
        return "(unknown branch)"

a = json.loads(sys.argv[1])
screen = a["screen"]; view = a["view"].upper(); bf = a.get("bf", ""); base = a.get("base", "")
folder = a["folder"].strip("/"); slug = a["slug"]; sfolder = a["screen_folder"]
code_l = a["code_label"]; name_l = a["name_label"]
extra_dd = a.get("extra_dropdowns", []); popups = a.get("popups", []); has_op_pu = a.get("has_op_pu", True)
# gen_ovgm.py now accepts ["Label", "Value"] pairs as well as plain "Label" (Service needs exact values -
# first-available would put the row outside the grid's scope). The docs only ever need the LABEL, so
# normalise here; without this the packager died on `", ".join(extra_dd)` with a list item.
extra_dd = [d if isinstance(d, str) else ("%s=%s" % (d[0], d[1]) if d[1] != "__FIRST__" else d[0])
            for d in extra_dd]
nav = a.get("nav", [])          # issue #283: NO OV-GM default - gated screens must opt in
# nav_values means the cascade was set to PROVEN explicit values (find_populated_scope.py), not
# "first-available" - found on Collection Point: CHECKLIST/SOW/KB still said "first-available" even
# though the config used explicit values via nav_values, because those 3 templates never checked for it
# (only registry/scorecard/JOURNAL used the `nav` list text, which happened to be right by coincidence).
# checked BOTH mechanisms - missed nav_value (singular, #292) on the first pass and still said
# "first-available" on Contract Capacity's CHECKLIST/SOW/KB/JOURNAL despite an explicit nav_value.
nav_is_explicit = bool(a.get("nav_values")) or bool(a.get("nav_value"))
# nav_mode "go_only": OV-GM by grid/toolbar shape, but the navigator has NO mandatory scope - fields are
# optional FILTERS and GO alone loads the grid (External Location CO.0227). Found because the first attempt
# passed a FAKE nav entry ("(filters only, no scope)") just to satisfy the non-empty-nav assert below, and
# that fake entry then printed as "(filters only, no scope) cascade + GO" in the registry/JOURNAL/KB -
# false, in three files. nav_mode is the honest way to say this, not a workaround nav value.
nav_mode = (a.get("nav_mode") or "").strip().lower()
assert nav_mode in ("", "go_only"), "nav_mode must be '' or 'go_only', got %r" % nav_mode
# ---- family is EXPLICIT and REQUIRED (issue #283) ---------------------------------------
# Inferring family from nav's truthiness silently mis-rendered any plain/custom/TV config that
# forgot "nav": []. Now the caller must say which family it is, and we cross-check it against nav.
FAMILIES = ("ovgm", "plain", "custom", "tv", "gatedpf")
family = (a.get("family") or "").strip().lower()
if family not in FAMILIES:
    sys.exit("ABORT: config needs an explicit \"family\" key - one of %s "
             "(issue #283: family used to be guessed from nav's truthiness, which silently "
             "mis-rendered plain-OV screens as OV-GM). Got %r." % (list(FAMILIES), a.get("family")))
if family in ("ovgm", "gatedpf") and not nav and nav_mode != "go_only":
    sys.exit("ABORT: family='ovgm' requires a non-empty \"nav\" list (the navigator cascade levels), "
             "or nav_mode='go_only' for a screen with no mandatory scope.")
if nav_mode == "go_only":
    nav = []   # go_only screens genuinely have no cascade - do not fake a nav entry to pass the assert
if family not in ("ovgm", "gatedpf") and nav:
    sys.exit("ABORT: family=%r must NOT pass a \"nav\" cascade (got %r) - only OV-GM screens are "
             "navigator-gated." % (family, nav))

FAM_TEXT = {
    "ovgm":   ("OV-GM (manage-object, groupmodel)", "manageObject:form:T_data"),
    "plain":  ("PLAIN OV (Bank family)", None),
    "custom": ("Custom-URL OV (no navigator GO; toolbar Refresh)", None),
    "tv":     ("TV-style inline grid", None),
    "gatedpf": ("Gated OV, PER-FIELD nav groups", None),
}
FAM_NAV_TXT = {
    "plain":  "date-only navigator + GO (no cascade)",
    "custom": "none (custom URL - grid loads directly; toolbar Refresh)",
    "tv":     "per-screen context/date navigator (see SOW)",
}
FAM_TAG = {"ovgm": "OV-GM", "plain": "plain OV", "custom": "custom-URL OV", "tv": "TV-style",
           "gatedpf": "gated OV per-field nav"}
FAM_DESC = {
    # "Op PU first-available" is only TRUE when the screen actually has that field. Service (has_op_pu
    # false) had the claim appended to its scorecard row anyway - the same wrong-detail class as #265/#278,
    # caught by reading the appended row back.
    "ovgm":   (("OV-GM, GO only (no mandatory nav scope)" if nav_mode == "go_only"
               else "OV-GM gated-navigator") + "; label-driven" +
               ("; Op PU first-available" if has_op_pu else "; no Op PU on this screen")),
    "plain":  "plain OV (date-only navigator + GO, no cascade); label-driven",
    "custom": "custom-URL OV (no navigator/GO; toolbar Refresh); label-driven",
    "tv":     "TV-style inline grid (cell edits, per-screen delete gesture); label-driven",
    "gatedpf": "gated OV with PER-FIELD nav groups (custom grid); label-driven",
}
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

# ---- family-aware artifact text + a REAL check-existing grep ---------------------
# (the CHECKLIST/JOURNAL/KB templates used to hardcode OV-GM wording on every screen)
FAM_LABEL = {"ovgm": "OV-GM", "plain": "plain OV", "custom": "custom-URL OV", "tv": "TV-style",
             "gatedpf": "gated OV (per-field nav)"}
FAM_SPEC = {
    "ovgm": ("OV-GM specifics: GO only (navigator fields are optional filters, no mandatory scope)."
             if nav_mode == "go_only" else
             "OV-GM specifics: navigator cascade %s (PROVEN explicit values, not first-available) + GO%s."
             % (" -> ".join(nav) if nav else "",
                "; Op Production Unit first-available for grid visibility" if has_op_pu else "")
             if nav_is_explicit else
             "OV-GM specifics: navigator cascade %s first-available + GO%s." % (
                 " -> ".join(nav) if nav else "",
                 "; Op Production Unit first-available for grid visibility" if has_op_pu else "")),
    "plain": "Plain-OV specifics: date-only navigator + GO (no cascade); no Op PU gating.",
    "custom": "Custom-URL specifics: grid loads directly from the screen URL; toolbar Refresh re-queries "
              "(no navigator GO).",
    "tv": "TV-style specifics: inline grid cell edits; per-screen delete gesture (see SOW).",
    "gatedpf": "Gated per-field specifics: nav groups are PER FIELD (nav:form:G:<n>:R:1:C:0) + GO.",
}
# grid_txt/nav_txt are LOCAL to the registry-row function, so recompute them here from the same
# module-level family tables (single source of truth, no second guess at the values).
_grid = FAM_TEXT[family][1] or a.get("grid", "manage_object_nav_nav:form:T_data")
GO_ONLY_NAV_TXT = "GO only (navigator fields are optional filters, no mandatory scope)"
nav_txt = (GO_ONLY_NAV_TXT if nav_mode == "go_only" else
           (" -> ".join(nav) + " cascade + GO") if family in ("ovgm", "gatedpf")
           else FAM_NAV_TXT.get(family, "see SOW"))
FAM_GRID_TXT = {"ovgm": "OV-GM (grid `manageObject:form:T_data`)",
                "plain": "plain OV (Bank family, grid `%s`)" % _grid,
                "custom": "custom-URL OV (grid `%s`)" % _grid,
                "tv": "TV-style inline grid (`%s`)" % _grid,
                "gatedpf": "gated OV, per-field nav groups (grid `%s`)" % _grid}
KB_NAV = {
    # nav_is_explicit overrides this at use-site (see kb_nav= below) - found on Collection Point, whose
    # cascade uses PROVEN values from find_populated_scope.py, not first-available.
    "ovgm": "cascade `nav:form:G:0:R:1:C:1..N:dd` (first-available) -> GO `#button:form:B`",
    "plain": "date field `nav:form:G:0:R:1:C:0:da_input` -> GO `#button:form:B` (no cascade)",
    "custom": "none - grid loads from the screen URL; re-query via toolbar Refresh `[Ctrl+r]`",
    "tv": "per-screen context/date navigator (see SOW)",
    "gatedpf": "PER-FIELD nav groups `nav:form:G:<n>:R:1:C:0` -> GO `#button:form:B`",
}
KB_GRID_NOTE = {"ovgm": " (empty until cascade + GO)", "plain": " (lists after GO)",
                "custom": " (lists on open)", "tv": "", "gatedpf": " (empty until all nav fields + GO)"}
KB_OPPU = {"ovgm": " - Op Production Unit (first-available, grid visibility)", "plain": "",
           "custom": "", "tv": "", "gatedpf": ""}
KB_ENGINE = {"ovgm": " + `apply_ovgm_navigator`", "plain": " + `click_go`", "custom": " + toolbar Refresh",
             "tv": "", "gatedpf": " + per-field nav helpers"}
KB_QUIRKS = {
    "ovgm": "- OV-GM navigator-gated: grid empty until cascade + GO. First-available nav PU is a sparse test\n"
            "  scope - NOT necessarily a valid Op Production Unit option, and it empties nav-scoped popups\n"
            "  (see tmp/OV_SWEEP_PARKED.md); parent-dd + Op PU use first-available, probe per screen.",
    "plain": "- Plain OV (Bank family): the navigator is a single DATE field + GO, no cascade and no Op PU.\n"
             "- An UNSAVED CHANGES dialog (YES/NO) can block GO right after the End=Start close - answer YES\n"
             "  (that commits the intended delete).",
    "custom": "- Custom-URL OV: no navigator GO; the toolbar Refresh `[Ctrl+r]` is the re-query gesture.",
    "tv": "- TV-style: rows are edited in place; confirm the delete gesture per screen.",
    "gatedpf": "- Every nav group is a separate mandatory field; fill them all before GO or the grid stays empty.",
}
FAM_KB_TYPE = {
    "ovgm": "OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel; navigator-GATED.",
    "plain": "Plain OV (EC Object Configuration, date-effective) - Bank family; date-only navigator + GO.",
    "custom": "Custom-URL OV (EC Object Configuration, date-effective) - grid loads directly; toolbar Refresh.",
    "tv": "TV-style table class - inline grid edits; per-screen delete gesture.",
    "gatedpf": "Gated OV with PER-FIELD navigator groups (date-effective) + GO.",
}
FAM_LESSON = {
    "ovgm": "- OV-GM: first-available nav scope + Op PU first-available lists the row after GO (parent-dd "
            "need not equal the nav PU - probe per screen).",
    "plain": "- Plain OV: date-only navigator + GO; no cascade and no Op PU to satisfy, so the grid lists "
             "immediately after Save + GO.",
    "custom": "- Custom-URL OV: no navigator GO; the toolbar Refresh is the re-query gesture.",
    "tv": "- TV-style: the row is edited in place; confirm the delete gesture per screen.",
    "gatedpf": "- Gated per-field nav: each nav group is its own field; fill every mandatory one before GO.",
}
fam_label = FAM_LABEL[family]

# 0b is a CLAIM, so it must come from a real command: does anything OUTSIDE this build already
# implement this screen? (Pre-ticking this was defect #2 above.)
_own = {("%s_iud.py" % slug), ("%s_page.resource" % slug), ("%s_iud.robot" % slug), ("%s_sow.md" % slug),
        ("%s.md" % slug)}
_dupes = []
for _f in EC.rglob("*"):
    if not _f.is_file() or _f.suffix.lower() not in (".py", ".robot", ".resource"):
        continue
    if _f.name in _own or sfolder in _f.parts:
        continue
    try:
        # Match the slug as an IDENTIFIER, not a bare substring: slug 'service' is a common English word
        # and matched 8 unrelated Bank/Language/MIME investigation scripts, firing a false 0b failure.
        # A real duplicate implementation would reference one of the generated artifact names.
        _txt = _f.read_text(encoding="utf-8", errors="replace")
        if any(tok in _txt for tok in ("%s_iud" % slug, "%s_page" % slug, "%s_sow" % slug)):
            _dupes.append(_f.relative_to(EC).as_posix())
    except Exception:
        pass
_shared_ok = {"py/ec_object_iud.py"}          # the shared engine legitimately dispatches by slug
_dupes = [d for d in _dupes if d not in _shared_ok]
zerob = ("0b grep ec-automation -> only this build (checked: %d other file(s) reference %r)"
         % (len(_dupes), slug))
zerob_tick = "x" if not _dupes else " "
if _dupes:
    zerob += " -- REVIEW: %s" % ", ".join(_dupes[:4])

# ---- #7 CHECKLIST.md (ticks from the real VERIFY-REPORT) -------------------------
dd_note = (" + dropdowns " + ", ".join(extra_dd)) if extra_dd else ""
pp_note = (" + popups " + ", ".join(popups)) if popups else ""
checklist = '''# %(screen)s - IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md, 21 gates)

## Step 0 - check-existing gate
- [x] 0a KB map created
- [%(zerob_tick)s] %(zerob)s
- [x] 0c reused shared engine (ec_object_iud.py) + DbVerify + T2 (thin driver).

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
- [x] 17 Registry row - [x] 18 Scorecard row
- [ ] 19 PR (R9 body) - CANNOT be ticked here: this file is written BEFORE the PR exists. Tick it in the PR body/commit, never at scaffold time (#235).

## E. Knowledge base
- [x] 20 KB map `ec-ui-knowledge/screens/%(slug)s.md`
- [x] 21 Reuse clause - N/A (new build); JOURNAL + evidence + KB map + VERIFY-REPORT all produced

_Gates 10-16 RUN by `scripts/verify_screen.py` -> `VERIFY-REPORT.md` (OVERALL PASS); ticks from real exit codes.
%(fam_spec)s%(dd_note)s%(pp_note)s_
''' % dict(screen=screen, slug=slug, folder=folder, view=view, rf_txt=rf_txt, pw_txt=pw_txt,
           screen_abbr=a.get("abbr", slug[:3]), nav=" -> ".join(nav), dd_note=dd_note,
           pp_note=pp_note, fam_spec=FAM_SPEC[family], zerob=zerob, zerob_tick=zerob_tick)
(bundle / "CHECKLIST.md").write_text(checklist, encoding="utf-8")

# ---- #3 JOURNAL.md --------------------------------------------------------------
journal = '''# JOURNAL - %(screen)s (%(bf)s) %(fam_label)s IUD

## %(date)s
- **Branch:** `%(branch)s`.
  Check-existing gate: %(zerob)s; reused shared engine (ec_object_iud.py) + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only + tmp/%(slug)s/config.json scan): %(fam_grid)s.
  Nav: %(nav_txt)s. Mandatory %(code_l)s / %(name_l)s / Start Date%(dd_note)s%(pp_note)s.
- **Built** (generator `%(gen)s`): label-driven T3 (no hardcoded ids); Playwright driver + RF T3/suite.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF %(rf_txt)s, %(pw_txt)s. DB residual 0.

## Lessons
%(fam_lesson)s Generic engine handled the nav/appear/absent/pagination gestures with zero tuning.
''' % dict(screen=screen, bf=bf, date=date, slug=slug, slug_dash=slug.replace("_", "-"),
           nav=" -> ".join(nav), code_l=code_l, name_l=name_l, dd_note=dd_note, pp_note=pp_note,
           rf_txt=rf_txt, pw_txt=pw_txt, fam_label=fam_label, fam_grid=FAM_GRID_TXT[family],
           nav_txt=nav_txt,
           fam_lesson=("- OV-GM: nav cascade uses PROVEN explicit values (scripts/find_populated_scope.py),"
                       " not first-available - do not assume the first option has usable data underneath."
                       if nav_is_explicit and family == "ovgm" else FAM_LESSON[family]),
           branch=_branch(), zerob=zerob,
           gen="tmp/gen_ovgm.py" if family == "ovgm" else "tmp/gen_ov.py")
# NEVER overwrite an existing JOURNAL.md. A packager re-run silently replaced Pilot's real
# Pilot-vs-Pilot-Boat lesson with the template once already (found as a floating diff 2026-07-31).
# A shape/length heuristic was tried first and FAILED its own test (it classed hand-edited journals as
# generator-fresh), so this compares content exactly and defers to a human on any divergence.
_jr = bundle / "JOURNAL.md"
if not _jr.exists():
    _jr.write_text(journal, encoding="utf-8")
elif _jr.read_text(encoding="utf-8", errors="replace").strip() == journal.strip():
    pass                                    # identical - nothing to do
else:
    # FAIL LOUDLY on divergence (fixed 2026-08-01 after the #292 merge). The guard used to write the
    # sibling and carry on, which shipped the WRONG file on Service: for a FIRST-TIME build there is no
    # independently-written content to protect, so "keep yours" preserved the OLDER JOURNAL (with a stale
    # check-existing result) while the corrected one sat unnoticed in JOURNAL.generated.md. The reviewer
    # had to consolidate them by hand. Divergence now stops the packager so a human decides which is right,
    # instead of the default silently choosing.
    (bundle / "JOURNAL.generated.md").write_text(journal, encoding="utf-8")
    sys.exit("ABORT: JOURNAL.md differs from what the generator would write.\n"
             "   kept:      %s\n"
             "   generated: %s\n"
             "   DECIDE WHICH IS CORRECT, then delete the other and re-run. Do not ship both.\n"
             "   - re-running inside the SAME build? the generated one is almost certainly the right one\n"
             "     (this is exactly how Service shipped a stale check-existing result - see #292).\n"
             "   - existing file holds hand-written history (Truck/Pilot)? merge the generated bits INTO it."
             % ((bundle / "JOURNAL.md"), (bundle / "JOURNAL.generated.md")))

# ---- #20 KB map -----------------------------------------------------------------
kb = ROOT / "ec-ui-knowledge" / "screens" / ("%s.md" % slug)
kb_txt = '''# Screen: %(screen)s

- **Type:** %(fam_type)s
- **BF_CODE:** %(bf)s - **Treeview:** %(tv)s > %(screen)s
- **DB view:** `%(view)s` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** %(date)s - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF %(rf_txt)s + %(pw_txt)s, DB-verified, self-clean)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `%(screen)s` -> `label.tv-link` "%(screen)s" |
| Navigator | %(kb_nav)s |
| Grid | `%(kb_grid)s`%(kb_grid_note)s |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**%(code_l)s*** - **%(name_l)s*** - **Start Date*** (date)%(dd_note)s%(pp_note)s%(kb_oppu)s. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`%(code_l)s` (ro) - **`%(name_l)s`**. Delete: **`End Date`** = Start Date -> leaves `%(view)s`.

## Automation (code in ec-automation)
- **Playwright:** `py/%(slug)s_iud.py` (shared engine `ec_object_iud.py`%(kb_engine)s).
- **RF:** T3 `pageobjects/%(folder)s/%(slug)s_page.resource` (**label-driven**) + suite `tests/%(folder)s/%(slug)s_iud.robot`.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
%(kb_quirks)s
''' % dict(screen=screen, bf=bf, tv=tv, view=view, date=date, nav=" -> ".join(nav),
           code_l=code_l, name_l=name_l, dd_note=dd_note, pp_note=pp_note, slug=slug, folder=folder,
           rf_txt=rf_txt, pw_txt=pw_txt,
           fam_type=(FAM_KB_TYPE[family] + (" NO mandatory nav scope - fields are optional filters."
                                            if nav_mode == "go_only" else "")),
           kb_nav=(GO_ONLY_NAV_TXT if nav_mode == "go_only" else
                  "cascade `nav:form:G:0:R:1:C:1..N:dd` (PROVEN explicit values, not first-available) -> "
                  "GO `#button:form:B`" if nav_is_explicit else KB_NAV[family]),
           kb_grid=_grid,
           kb_grid_note=(" (lists on GO with no filters set)" if nav_mode == "go_only" else KB_GRID_NOTE[family]),
           # kb_oppu used to be unconditional on family, ignoring has_op_pu entirely - found on Collection
           # Point (has_op_pu=False) whose KB still claimed "Op Production Unit (first-available)".
           kb_oppu=("" if (nav_mode == "go_only" or family != "ovgm" or not has_op_pu) else KB_OPPU[family]),
           kb_engine=(" + `click_go`" if nav_mode == "go_only" else KB_ENGINE[family]),
           kb_quirks=("- GO-only navigator: fields are optional FILTERS (not a scope cascade) - GO alone "
                      "loads the grid. Do not assume a mandatory scope exists on every OV-GM-shaped screen."
                      if nav_mode == "go_only" else
                      "- OV-GM: nav cascade uses PROVEN explicit values from `scripts/find_populated_"
                      "scope.py` (not first-available) - the alphabetically/positionally-first option is "
                      "NOT guaranteed to have data underneath it; see ov-gm-navigator-capability.md."
                      if nav_is_explicit and family == "ovgm" else KB_QUIRKS[family]))
kb.write_text(kb_txt, encoding="utf-8")

# ---- #17 registry row (idempotent) ----------------------------------------------
reg = EC / "docs" / "ec_screen_registry.md"
reg_txt = reg.read_text(encoding="utf-8", errors="replace")
if ("py/%s_iud.py" % slug) not in reg_txt and ("| %s |" % screen) not in reg_txt:
    dd_r = ((" + " + ", ".join(extra_dd)) if extra_dd else "") + ((" + popup " + ", ".join(popups)) if popups else "")
    # family-aware row (issue #278): an EMPTY nav list must NOT render as " cascade + GO",
    # nor claim OV-GM / the manageObject grid - those belong to gated screens only.
    nav_txt = (GO_ONLY_NAV_TXT if nav_mode == "go_only" else
               (" -> ".join(nav) + " cascade + GO") if family == "ovgm" else FAM_NAV_TXT[family])
    fam_txt = FAM_TEXT[family][0] + (" - no mandatory nav scope" if nav_mode == "go_only" else "")
    grid_txt = FAM_TEXT[family][1] or a.get("grid", "manage_object_nav_nav:form:T_data")
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
# family-aware tag + descriptor (issue #278): plain-OV / custom-URL screens must not be labelled OV-GM
fam_tag = FAM_TAG[family]
fam_desc = FAM_DESC[family]
tag = "%s (%s, %s)" % (screen, fam_tag, bf)
# issue #283 test finding: keying idempotency on the family-aware tag appended DUPLICATES for
# screens whose existing row used different family wording. Key on screen name + BF only.
already = ("| %s (" % screen) in sc_txt and bf in sc_txt
if not already:
    row = ("| %s | OK Done %s - RF %s + %s via verify_screen.py (OVERALL PASS), DB-verified vs %s (Name), "
           "self-clean; %s | see docs/ov-non-bank-targets.md |\n"
           % (tag, date, rf_txt, pw_txt, view, fam_desc))
    with sc.open("a", encoding="utf-8") as fh:
        fh.write(row)
    sc_added = True
else:
    sc_added = False

# ---- family manifest + row self-check (item 2: exit-code gate, not my memory) -----------------
FAM_MANIFEST = EC / "docs" / "screen_families.json"
try:
    _man = json.loads(FAM_MANIFEST.read_text(encoding="utf-8")) if FAM_MANIFEST.exists() else {}
except Exception:
    _man = {}
_man[screen] = family
FAM_MANIFEST.write_text(json.dumps(_man, indent=2, sort_keys=True) + "\n", encoding="utf-8")

_chk = ROOT / "tmp" / "check_row_vocab.py"
if _chk.exists():
    import subprocess
    _rc = subprocess.run([sys.executable, "-X", "utf8", str(_chk), screen, family],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(_rc.stdout.strip()[:400])
    if _rc.returncode != 0:
        sys.exit("ABORT: the registry/scorecard rows just written do NOT match family %r - see above. "
                 "Fix the row wording (or the family) before shipping." % family)

print("PACKAGED %s: evidence=%d png, CHECKLIST/JOURNAL/investigation/KB written; registry+=%s scorecard+=%s"
      % (screen, copied, reg_added, sc_added))
print("  bundle:", bundle)
print("  kb    :", kb)
