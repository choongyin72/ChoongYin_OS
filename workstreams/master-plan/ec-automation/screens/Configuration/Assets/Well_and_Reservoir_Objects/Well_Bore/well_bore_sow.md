# SOW — Well Bore IUD (Configuration > Assets > Well_and_Reservoir_Objects)

**Screen:** Well Bore   **BF:** CO.0054   **View:** `OV_WELL_BORE` (versioned; 158 rows at last
DB-verified count)   **Base:** `WEBO_BORE`   **Pattern:** OV-GM (groupmodel manage-object),
Area-pattern converted 2026-08-27 (PR #564).

## Classification
OV-GM with a genuinely PER-FIELD navigator — confirmed by BOTH a live read-only DOM recon and by
reading the pre-existing proven driver (`py/well_bore_iud.py`) before writing any new code. This is
**NOT** the shared T2 `Apply Navigator From Properties` (`resources/manage_object.resource`)
same-row/increasing-column shape — each cascade level is its own distinct DOM group
(`nav:form:G:<n>:R:1:C:0`), which is exactly the keyword's own documented "KNOWN LIMITATION."

## Navigator shape
- `nav:form:G:1..G:4:R:1:C:0` = Production Unit -> Area -> Facility Class 1 -> "Well & Well
  Hookup", each MANDATORY, each its own group (not a same-row cascade).
- G:4 needs a **specific real well** — the first-available option is `P1 Graph 001` (a graph
  object with no bores -> empty grid); `P1 W008 OP` is used instead.
- A 5th group, `G:5` ("Well"), is scan-flagged mandatory (CSS) but returns **ZERO options under
  every scope tried** — confirmed by the pre-existing driver (recon 2026-07-31, re-verified live
  2026-08-27). Deliberately left EMPTY; GO still succeeds and the grid loads on 4 levels (verified
  by listing the real bore `P1 W008 WB001`).

## Grid / mandatory fields
- Grid id: `manageObject:form:T_data`.
- Mandatory objectForm fields: Well Bore Code, Well Bore Name, Start Date, and a **'Well' POPUP**
  whose list grid is `Objects:form:T_data` (NOT the generic `PopupList:form:T_data` — a third popup
  grid-id variant discovered on this screen, after `PopupList:form:T_data` and
  `manage_object_nav_nav:form:T_data`). Screen-local picker (`Pick Well Popup`) selects the
  nav-scope well **by value** (`P1 W008 OP`, same value as navigator G:4 — field-reuse rule); the
  popup's first row is a graph object and is deliberately not used.
- DELETE = End Date = Start Date (true delete in `OV_WELL_BORE`).

## Test data
- Fixed test code `AUTOTEST_WB` (confirmed FREE in `OV_WELL_BORE` before use via a fresh
  independent `oracledb` connection; 0 residual `AUTOTEST%` rows after the live run).
- Start Date `2020-01-01`. Update changes Well Bore Name only (Well Bore Code is read-only in
  `updateAttributes`).
- Properties files: `testdata/well_bore_{navigator,insert,update,form_verify,grid_verify}.properties`.

## Dev story (from PR #564, merged 2026-08-27)
Well Bore was converted from the old 4-TC/suite-login/generated-code/inline-DB-verify RF build to
the full Area-pattern structure (5-TC incl. TC04 Find, per-TC Login/Logout, fixed `AUTOTEST_WB`
code, properties-file-driven insert/update/verify, explicit grid-filter wiring, zero inline
DB-verify calls). It was the **first screen in the Area-pattern conversion program whose navigator
did not fit the shared T2 keyword's supported shape** — confirmed live before any code was written.
Rather than force-fitting the shared keyword or forking `resources/manage_object.resource`, a
**bespoke screen-local T3 keyword** (`Apply Well Bore Navigator From Properties`) was added to
`well_bore_page.resource`, modeled on `well_page.resource`'s own prior "Apply Well Navigator"
precedent and built in parallel with, then reconciled against, Well Bore Interval's identical
bespoke-navigator approach (PR #563, merged in the same batch) — both screens share the same real
per-field-groups shape and needed the same kind of fix. The bespoke keyword reads the navigator
properties file in file order and fills `nav:form:G:<n>:R:1:C:0` for n = 1..4 via the existing
shared T1 `Set Navigator Filter`/`Apply Navigator` primitives (`resources/navigator.resource`),
clicking GO exactly once — `resources/manage_object.resource` itself was never touched.

**Operational incident (same session, disclosed honestly):** during the batch's multi-PR push
(Well, Well Bore Interval, Well Bore all converted in the same session), a second/duplicate agent
dispatch independently worked the same registry-row updates in the same worktree concurrently.
This produced a transient duplicate "keep-both" row for both Well Bore and Well Bore Interval in
`docs/ec_screen_registry.md` after the merges landed — caught and removed the same day in commit
`c35b909b` ("fix(batch-merge): drop 2 stale keep-both registry rows"). No automation code or test
data was affected; the two independently-built bespoke keywords were compared and matched (same
approach, same proven values), so no corruption resulted, but the duplication was a real
gate-ordering gap — the hygiene hard-gate only confirmed rows existed, it did not police
duplicates, so a by-key dedup check was promoted into the hard-gate chain ahead of any push going
forward.

## Known risks
- Nav + popup values are DATA-dependent (`P1 W008 OP`); re-derive if the sandbox changes.
- Popup grid id is per-popup-TYPE — if EC changes this object's popup, re-recon before reusing the
  screen-local picker.
