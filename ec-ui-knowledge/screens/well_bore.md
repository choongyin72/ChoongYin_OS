# Screen: Well Bore

- **Type:** OV-GM (EC Object Configuration, groupmodel manage-object, date-effective) —
  navigator-GATED, with a genuinely PER-FIELD navigator (NOT the shared T2 same-row cascade shape
  Area uses — see `docs/navigator-screens-not-matching-area.md` in `ec-automation`).
- **BF_CODE:** CO.0054 — **Treeview:** Configuration > Assets > Well_and_Reservoir_Objects > Well Bore
- **DB view (ground truth):** `OV_WELL_BORE` (versioned; key `CODE`; also `NAME`,
  `OBJECT_START_DATE`, `OBJECT_END_DATE`); base `WEBO_BORE`; 158 rows at last verified count.
- **Last verified:** 2026-08-28 · EC 14.2.4 · local sandbox (`localhost:1521/ORCL`) · live RF 5/5
  (this session's backfill evidence-capture run; automation unchanged since PR #564).
- **Pattern:** converted to the full Area-pattern 5-TC RF STRUCTURE in PR #564 (2026-08-27) while
  REMAINING OV-GM with its own genuine per-field navigator mechanism — this file records what is
  Well Bore-specific.

## Selectors `[from well_bore_page.resource Variables/Keywords sections, transcribed 2026-08-28]`

| Purpose | Selector |
|---|---|
| Grid (rows) | `manageObject:form:T_data` |
| Navigator groups (PER-FIELD, MANDATORY, in fill order) | `nav:form:G:1:R:1:C:0` = Production Unit → `nav:form:G:2:R:1:C:0` = Area → `nav:form:G:3:R:1:C:0` = Facility Class 1 → `nav:form:G:4:R:1:C:0` = Well & Well Hookup (needs a SPECIFIC real well, `P1 W008 OP` — first-available `P1 Graph 001` is a graph object with no bores, yields an empty grid) |
| Navigator group deliberately SKIPPED | `nav:form:G:5` ("Well") — scan-flagged mandatory (CSS) but 0 options under every scope tried; left empty, GO still succeeds, grid loads on 4 levels |
| Navigator fill mechanism | **BESPOKE** screen-local T3 keyword `Apply Well Bore Navigator From Properties` (`well_bore_page.resource`) — NOT the shared T2 `Apply Navigator From Properties` (documented there as a KNOWN LIMITATION for PER-FIELD groups). Reads `testdata/well_bore_navigator.properties` in file order, fills G:1→G:2→G:3→G:4 via the shared T1 `Set Navigator Filter`/`Apply Navigator` (`resources/navigator.resource`), clicks GO once. `resources/manage_object.resource` NOT touched. |
| Grid-filter | `Find/Clear Well Bore Row By Filter` → shared T2 `Find/Clear Object Row By Filter` on the grid's Code column (14 hits in PR #564's own live run; 19 hits in this backfill's independent re-run — both confirm the mechanism fires) |
| 'Well' POPUP grid (mandatory objectForm field) | `Objects:form:T_data` — NOT the generic `PopupList:form:T_data` (a THIRD popup-grid-id variant discovered on this screen, after `PopupList` and `manage_object_nav_nav`). Screen-local keyword `Pick Well Popup` selects the row matching `${WELL_BORE_NAV_WELL}` (`P1 W008 OP`) BY VALUE — the popup's first row is a graph object, deliberately not used. |
| Insert wrapper (screen-local, because of the popup) | `Insert Well Bore Record And Save` — fills Well Bore Code/Name/Start Date by label, then the Well popup, then Save (mirrors Chemical Stream's own "From Connection" popup exception) |
| Delete End Date field | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded, not label-driven — same convention as Area's/Bank's own DEL_ENDDATE constants) |

## Mandatory / yellow fields
- **Navigator (before the grid loads any rows):** Production Unit → Area → Facility Class 1 →
  Well & Well Hookup (all 4 mandatory, each its own PER-FIELD group) + GO.
- **Insert form (`objectForm`):** Well Bore Code, Well Bore Name, Start Date (label-driven text/
  date fields) + the mandatory 'Well' POPUP (filled by value, same value as navigator G:4).
- **Update form (`updateAttributes`):** Well Bore Name only (Well Bore Code is read-only).
- **Delete (`objectdates`):** End Date = Start Date → true delete from `OV_WELL_BORE`.
- Field labels are screen-prefixed: "Well Bore Code" / "Well Bore Name" (not generic "Code"/"Name").

## Quirks
- **Genuinely PER-FIELD navigator, not a same-row cascade** — confirmed by BOTH a live read-only
  DOM recon (each G:n group reports its own `dd_input`) AND the pre-existing driver's own proven
  values, before any conversion code was written. This is exactly why the shared T2 navigator
  keyword's documented "KNOWN LIMITATION" applies here — it was the first screen in the
  Area-pattern conversion program to hit this gap (built in parallel with, and reconciled against,
  Well Bore Interval's identical case, PR #563).
- **G:5 ('Well') is a scan-flagged-mandatory but functionally unusable filter** — 0 options under
  every scope tried; deliberately left empty. Do not try to "fix" this by hunting for a value —
  it has none.
- **THREE popup list-grid-id variants exist across the well hierarchy** (`PopupList`,
  `manage_object_nav_nav`, `Objects`) — always recon the popup frame directly; a generic helper's
  "empty source list" error usually means the wrong grid id was assumed, not a genuinely empty list.
- **Fixed test code `AUTOTEST_WB`** (not a generated/timestamped code, since the PR #564
  conversion) — confirmed free in `OV_WELL_BORE` via a fresh independent connection before use;
  every run must complete TC05 (delete) so the code is free for the next run.
- **Operational note (documented for completeness, not a screen defect):** during the PR #564/#563
  batch's push, a duplicate concurrent-agent dispatch produced a transient duplicate registry row
  for this screen in `docs/ec_screen_registry.md`, caught and removed same-day (commit
  `c35b909b`). No automation or test data was affected — see the bundle's `JOURNAL.md` for the
  full incident writeup.

## Automation (code lives in ec-automation — this file is the MD selector reference)
- **RF (the maintained suite):** T3
  `ec-automation/pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/well_bore_page.resource`
  (bespoke `Apply Well Bore Navigator From Properties` + `Pick Well Popup` keywords) + suite
  `ec-automation/tests/Configuration/Assets/Well_and_Reservoir_Objects/well_bore_iud.robot` (5 TCs:
  Clean State/Insert/Update/Find/Delete, per-TC Login/Logout). Run:
  `EC_HEADLESS=true robot tests/Configuration/Assets/Well_and_Reservoir_Objects/well_bore_iud.robot`
  → 5/5 PASS, self-clean 0 residual in `OV_WELL_BORE`.
- **Playwright (pre-existing reference, waived from further build per Section H of
  `docs/IUD-DELIVERABLE-CHECKLIST.md` — Universal Screen Engine replaces this role going forward):**
  `ec-automation/py/well_bore_iud.py` (shared engine `ec_object_iud.py` + screen-local
  `apply_well_bore_navigator`/`pick_well_popup`), kept unchanged since the 2026-07-31 build.
- Full bundle (SOW/README/JOURNAL/evidence/CHECKLIST):
  `ec-automation/screens/Configuration/Assets/Well_and_Reservoir_Objects/Well_Bore/`.
