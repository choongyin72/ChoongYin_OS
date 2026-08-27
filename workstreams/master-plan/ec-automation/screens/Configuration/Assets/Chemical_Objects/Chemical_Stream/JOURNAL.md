# JOURNAL - Chemical Stream (CO.0258) OV-GM + mandatory-popup IUD

## 2026-07-30
- **Branch:** `feature/chemical-stream-iud-v3`. Previously PARKED twice: the mandatory From
  Connection popup reported "empty source list" under the first-available AS1 nav scope.
- **UNPARKED in two steps, all real facts:**
  1. Owner screenshot proved the popup HAS entries under the P1 scope (Object Type CHEM_TANK,
     P1 CT001..CT014) -> navigator switched to SPECIFIC P1 values.
  2. First P1 driver run STILL failed -> popup recon (`investigation/recon_chs_popup*.py`) found this
     is NOT the standard object_popup: `stream_node_ref_popup` has an inner navigator (inherits the
     outer scope), an **Object Type dd** (`nav:form:G:4`, EMPTY on open), an **inner GO**
     (`button:form:B`), and its list grid is **`manage_object_nav_nav:form:T_data`** (NOT
     `PopupList:form:T_data`) - the generic engine `pick_popup` / T1 popup keywords wait for
     PopupList and drive no inner steps, hence the misleading "empty source" error.
- **Built HAND-WRITTEN with screen-LOCAL popup handlers** (shared engine + T1 popup.resource
  untouched): driver `pick_from_connection_popup` + T3 `Open From Connection Popup List` /
  `Pick From Connection Popup` (split to satisfy robocop LEN03 after a first FAIL exit=1).
  Insert: Start Date FIRST (form quirk: R:0 precedes Code), Chemical Stream Type first-available,
  From Connection = first CHEM_TANK row.
- `verify_screen.py` -> **OVERALL PASS** (2nd run; 1st = robocop LEN03 only, live 4/4 both runs):
  robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4, Playwright 8/8. DB residual 0.
- **#265 lesson applied:** registry/scorecard rows column-diffed vs the Channel sibling; wording
  corrected to the popup + specific-values facts.

## Lessons
- "Popup empty source" can mean the popup NEEDS INNER DRIVING (Object Type + GO), not that data is
  missing - recon the popup's inner frame before concluding. Popup grid ids differ per popup TYPE
  (object_popup = PopupList:form:T_data; stream_node_ref_popup = manage_object_nav_nav:form:T_data).
- Third data-scope unpark in a row (Lifting Account, Well, Chemical Stream): first-available is a
  convention, not a guarantee - a known-good scope beats structural workarounds.

## 2026-08-16 - closing Universal Screen Engine open-items tracker #6 (click-stall + modal bug)

Two loose threads from item #5's investigation (the pacing-artifact click-stall bug, confirmed on
Price Object/Service/Contract Capacity but left inconclusive on this screen) were picked up and
closed:

**6a - click-stall theory re-tested, CONFIRMED does not reproduce here.** Structural recon via the
new engine's read-only `field_inventory()` first corrected a stale fact: this screen's
`updateAttributes` (Update) form has **36 fields, 21 of them dropdowns** - not just Code+Name as
`ec-ui-knowledge/screens/chemical_stream.md` previously claimed (now fixed, see below). Swept all
21 dropdowns via the actual production `Engine.select()` (already properly paced - `ajax()` waits
for `networkidle` + a 900ms buffer, same mechanism proven on Bank/Language) on a completely fresh
page load, real data (`P1 CS001 CT001 SI`), no Save. Result: **0/21 stalled** - reproduces and
reinforces the original design-doc finding (section 27) via the real engine this time, not a
bespoke script. Closed - no stall exists on this screen under any tested condition.

**6b - root-caused and fixed.** Reproduced the blocking modal on the first attempt: dirty a field
(no Save) via `Engine.select()`, then call `open_screen()` again in the same page session. It is
EC's own genuine "Unsaved Changes" confirmation dialog (title `UNSAVED CHANGES`, real buttons
`confirmationForm:yesbtn`/`nobtn`/`cancelbtn` = YES/NO/CANCEL) - not an EC defect, the same prompt
a real user would see. The actual gap was that neither `open_screen()` nor any other engine action
had code to detect or dismiss it, so the next click just hung against the dialog's overlay for a
full timeout with a confusing "element intercepts pointer events" error.

First fix attempt (a manual check inside `open_screen()` alone) turned out to be **insufficient**:
verified live that the SAME dialog re-appears on a *different* trigger too - `select_row()` opening
a different record's Update Attributes form, with different wording ("unsaved changes in Update
Attributes") - meaning the dirty flag isn't cleared by dismissing the dialog once for one action.
**Real fix:** centralized the dismissal inside `universal_classifier.ajax()` (the one function
nearly every state-changing engine action already calls), always clicking **NO** (discard the
unsaved change, let the caller's action proceed) - never CANCEL (would silently strand the caller
on the old screen) and never YES (the engine has no way to judge whether a half-filled form is
safe to persist). Verified: the exact repro that failed before now passes end-to-end (re-navigation
succeeds, and a subsequent row-select on a different record also succeeds, no manual dismiss code
needed at either call site). Owner decision, followed exactly: default behavior stays "always Save
before switching screens" (unchanged, already true for every real IUD driver); NO is only exercised
when a caller deliberately abandons unsaved state, e.g. this kind of investigation script.

Since this touched shared `engine.py`/`universal_classifier.py`, the mandatory `engine_canary.py`
regression gate was re-run after both the fix and the consolidation - Bank + Language both
`ALL PASS`, confirming no regression to the two proven exemplar screens.

Also fixed: `ec-ui-knowledge/screens/chemical_stream.md`'s Update/Delete section, which stated only
`Chemical Stream Code`/`Chemical Stream Name` exist on the Update form - corrected to the real,
live-verified 36-field/21-dropdown set (see the note's own updated content for the full list).

Investigation scripts moved into `investigation/`: `chs_find_real_code.py` (real DB codes under
the P1 scope), `chs_structural_recon.py` (field_inventory before/after nav+row-select),
`chs_pacing_sweep.py` (the 21-dropdown sweep), `chs_modal_repro.py` (the modal repro + fix proof).

## 2026-08-26 - Area-pattern conversion (PR #545)

_From here on, the entry style matches Bank's JOURNAL (Built / Done well / Done wrong-or-lessons /
Blockers -> resolution / Decisions / Evidence), per `docs/lean-deliverable-backfill-workorder.md`._

### Built
- Converted the RF suite from its old 4-TC/single-suite-login/inline-DB-verify shape to Area's full
  5-TC/per-TC-login/properties-file-driven/pure-screen-verify shape, per the owner's 2026-08-26
  standing rule: any EC screen whose navigator matches Area's same-row cascade layout must follow
  Area's FULL pattern, not just the navigator-fill piece.
- `pageobjects/.../chemical_stream_page.resource` rebuilt: navigator fill delegates to the shared T2
  `Apply Navigator From Properties` (`resources/manage_object.resource`), driven by new
  `testdata/chemical_stream_navigator.properties`, replacing the old screen-local
  `Apply Chemical Stream Navigator` keyword. The **From Connection popup keywords were left
  UNTOUCHED** (`Open From Connection Popup List` / `Pick From Connection Popup`) - orthogonal to
  the outer navigator, per explicit task instruction not to refactor working popup logic.
- `tests/.../chemical_stream_iud.robot` rebuilt: 5 TCs (added TC04 Find), per-TC
  `Login To EC Application`/`Logout From EC Application` on ONE browser opened once in Suite Setup,
  switched from a per-run timestamped code to a fixed test code `AUTOTEST_CHS` (confirmed free in
  `OV_CHEM_STREAM` via a fresh oracledb connection before wiring it in), zero inline DB-verify calls
  left in the `.robot` file (the DB check now lives only inside the shared T2
  `Verify Object Removed`).
- New properties files: `testdata/chemical_stream_{insert,update,form_verify,grid_verify}.properties`
  driving the shared T2 `Insert/Update Object From Properties`/`Verify Object *` for the plain
  fields, plus explicit `Find/Clear Chemical Stream Row By Filter` grid-filter wiring into
  Update/Find/Verify-Found/Delete.
- `resources/credentials.py`: additive-only `CHEMICAL_STREAM_EC_USER`/`CHEMICAL_STREAM_EC_PASS`.

### Done well
- Live RF 5/5 pass (PR #545). Full-tree `robot --dryrun tests/` 850/850 pass at PR #545 time - no
  regressions to any other screen's suite.
- Filter-keyword wiring confirmed fired: `Find Object Row By Filter` -> 15 hits in live
  `output.xml` (PR #545; re-confirmed 15 hits again in this session's own live re-run, see Evidence
  below).
- The mandatory From Connection popup's screen-local mechanism needed ZERO changes - confirmed
  still executing successfully during TC02 Insert both at PR #545 time and in this session's re-run.
- No shared T1/T2 file changes needed - `resources/manage_object.resource`'s existing
  `Apply Navigator From Properties` already supported this screen's 3-level same-row cascade shape
  without modification.

### Done wrong / lessons
- None disclosed in PR #545's own body beyond the popup-preservation caveat already covered above -
  this was a clean structural conversion of an already-working screen, not a new investigation.
- This screen's bundle (SOW/README/JOURNAL/CHECKLIST/evidence/KB map) was NOT refreshed at PR #545
  merge time - the 2026-08-23..26 lean waiver (later retired 2026-08-27, Section H) allowed the RF
  conversion to ship without the doc/evidence bundle around it. This 2026-08-27 entry is that
  backfill, not a new build.

### Blockers -> resolution
- No blockers in PR #545's own body. This backfill session hit none either (network to the EC
  sandbox reachable, no stray chrome.exe processes, live run passed first attempt).

### Decisions
- Popup logic (`stream_node_ref_popup` handling) stays screen-local and untouched - it is a
  distinct EC popup TYPE (list grid `manage_object_nav_nav:form:T_data`, not the generic
  `PopupList:form:T_data`), not a navigator, so the Area-pattern conversion applies only to the
  outer navigator + TC structure, never to this popup's own driving logic.
- Playwright driver (`py/chemical_stream_iud.py`) is out of scope for both PR #545 and this
  backfill - kept unchanged, permanently waived per Section H (Universal Screen Engine replaces
  that role going forward).

### Evidence
- PR #545 (2026-08-26): live RF 5/5 pass; DB self-clean via fresh oracledb connection, 0 residual
  `AUTOTEST%` rows in `OV_CHEM_STREAM` before and after.
- This backfill (2026-08-27, doc/evidence only, no RF file touched):
  - `robot --dryrun tests/Configuration/Assets/Chemical_Objects/chemical_stream_iud.robot` -> 5/5
    pass.
  - Full-tree `robot --dryrun tests/` -> **883/883 pass**, no regressions.
  - `EC_HEADLESS=true robot` live re-run -> **5/5 pass**; artifacts kept in
    `evidence/2026-08-27_area_pattern_backfill/` (`log.html`, `output.xml`, `report.html`,
    per-TC screenshots, `robocop_output.txt`).
  - `Find Object Row By Filter` -> 15 hits confirmed again in this session's own `output.xml`.
  - `py -m robocop check` on the changed files -> **7 issues** (VAR02 x2 + DOC02 x5) - same shape
    as Area's own current baseline and Chemical Stream Hookup's; PR #545 cited 10 issues at its own
    merge time, the count difference reflects robocop/config drift over the intervening period, not
    a functional regression (no new issue category, same two files, same VAR02/DOC02 kinds).
  - `py scripts/check_bundle_hygiene.py` (repo root) -> `PASS` (167 bundles + 271 recon scripts
    scanned; the one WARN in the output is a pre-existing, unrelated Contract Area recon script).
  - `investigation/check_autotest_residual.py` (new, this session) -> `AUTOTEST residual rows: []`
    both before and after the live re-run.
