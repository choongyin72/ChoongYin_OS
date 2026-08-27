# SOW - Well IUD (Configuration > Assets > Well_and_Reservoir_Objects)

**Backfill note (2026-08-27, Batch 2 of `docs/lean-deliverable-backfill-workorder.md`):** this file
originally documented only the 2026-07-30 base build. It is refreshed here to also cover the
Area-pattern STRUCTURE conversion (PR #540, merged 2026-08-26) — the base-build facts below are
unchanged (same screen, same navigator, same view); the "Area-pattern conversion" section is new.

## Classification
- **Screen:** Well   **BF:** CO.0049   **View:** `OV_WELL` (versioned)   **Base:** `WELL`.
  **Class match note:** resolver returned `['WELL','FORECAST_WELL']`; `OV_WELL` confirmed as the
  live view by REAL lookup (`'P1 W001 OP'` present, 506 rows).
- **Type:** OV-GM (groupmodel manage-object), grid `manageObject:form:T_data`, with a 5-dd
  navigator, but **only the standard 3-level cascade is required**: SPECIFIC P1 values
  (P1 Production Unit -> P1 Area -> P1 Facility 1) + GO lists the wells while the 2nd-row dds
  (Well & Well Hookup / Well) stay EMPTY — owner screenshot ground truth (2026-07-30). The
  original park ("5th level empty under first-available AS1") was a data-scope artifact, not a
  structural blocker.

## Navigator shape (base-build fact, unchanged by the conversion)
3-level same-row cascade at `nav:form:C:1` (Production Unit) / `C:2` (Area) / `C:3` (Facility
Class 1), filled with SPECIFIC values (P1 Production Unit / P1 Area / P1 Facility 1), then GO.
Real field labels confirmed live: `objectForm`/`updateAttributes` use SCREEN-PREFIXED
"Well Code"/"Well Name" (like Area's "Area Code"/"Area Name"), NOT the generic "Code"/"Name"
Bank/Object List use.

## Grid / mandatory fields
- Grid id: `manageObject:form:T_data`.
- Insert mandatory fields: Well Code, Well Name, Start Date, Well Type (dropdown, first-available
  via the `__FIRST__` sentinel). No Op Production Unit field on the insert form — the row lists
  under the nav scope regardless (same as Facility Class 1).
- Delete = End Date = Start Date (true delete in `OV_WELL`).

## Test data used
- `testdata/well_navigator.properties` — `Op Production Unit=P1 Production Unit`,
  `Op Area=P1 Area`, `Op Facility Class 1=P1 Facility 1`.
- `testdata/well_insert.properties` — `Well Code=AUTOTEST_WELL`, `Well Name=Automation Test Well`,
  `Start Date=2020-01-01`, `Well Type=__FIRST__`.
- `testdata/well_update.properties` — `Well Name=Automation Test Well UPDATED`.
- `testdata/well_form_verify.properties` / `well_grid_verify.properties` — merged post-insert +
  post-update expected state.
- Fixed test code `AUTOTEST_WELL` (the Area-pattern conversion switched from a timestamped
  `AUTOTEST_WE_<timestamp>` code to this fixed code; confirmed absent from `OV_WELL` via a fresh
  oracledb connection both before and after the live run).

## Dev story

### Base build (2026-07-30, branch `feature/well-iud-v2`)
Originally PARKED: an earlier scan found 5 mandatory nav dds with the 5th empty under a
first-available AS1 path (fill timeout, grid never loaded). UNPARKED by an owner screenshot: with
only the standard 3-level cascade filled with SPECIFIC P1 values + GO, the grid lists wells while
the 2nd-row dds stay empty — they are optional filters, and the park was a data-scope artifact of
the AS1 path, not a structural blocker. Built HAND-WRITTEN (no generator — specific nav values were
not generator-supported at the time): thin driver `py/well_iud.py` with a screen-local
`apply_well_navigator`, and a T3 with a screen-local `Apply Well Navigator` keyword (built on T1's
`Select EC Dropdown Option` + `Apply Navigator`). `verify_screen.py` -> OVERALL PASS (robocop 0,
hygiene 0, dryrun 4/4, live RF 4/4, Playwright 8/8, DB residual 0).

### Area-pattern STRUCTURE conversion (PR #540, merged 2026-08-26 08:06 UTC, branch
`feature/well-area-pattern`)
Converted Well's RF IUD automation from its OLD 4-TC pattern (suite-level login, timestamped test
code, inline DB-verify calls) to the full Area-pattern STRUCTURE (5 TCs incl. TC04 Find, per-TC
login/logout, fixed test code, properties-file-driven insert/update/verify), while **keeping Well's
genuine 3-level P1 navigator cascade unchanged**. The navigator fill itself was ALSO changed by
this PR: the screen's own bespoke `Apply Well Navigator` T3 keyword (from the 2026-07-30 base
build) was retired and replaced with a call to the shared T2 `Apply Navigator From Properties`
(`resources/manage_object.resource`) driven by the new `testdata/well_navigator.properties` — Well
is one of the screens explicitly documented there as a proven same-row 3-level cascade case. No
edits were made to `resources/manage_object.resource` itself by PR #540 (that shared keyword
already existed from the earlier Area conversion work — see "Regression-canary role" below).

Live run: 5/5 pass. Fresh oracledb connection pre/post-run: `AUTOTEST_WELL` = 0 rows both times
(self-clean confirmed). Full-tree `robot --dryrun` on `tests/`: 850/850 pass (zero new failures vs.
baseline at the time). `grep -c "Find Well Row By Filter" output.xml` = 14 (grid-filter keyword
confirmed firing). Zero inline DB-verify calls remain in `well_iud.robot` (grep-confirmed). robocop
on the two Well files -> 7 issues (2 VAR02 + 5 DOC02), matching Area's own baseline exactly
(parity, no regression).

Real gotcha carried into the conversion, not new to it: Well Type's mandatory first-available
dropdown continues to use the pre-existing `__FIRST__` sentinel; Start Date/End Date are excluded
from the `WELL_FORM_LABELS` round-trip comparison (they live only in `objectdates`, not
`objectForm`/`updateAttributes`'s fill-once trio) — both carried over from the base build's own
documented caveats.

## Regression-canary role (separate, earlier event — same session as the Area shared-keyword work)
Before PR #540 converted Well's OWN navigator-fill logic, Well was used — UNCHANGED, still running
its OLD bespoke `Apply Well Navigator` keyword and 4-TC structure — as one of **two regression
canaries** when the shared T2 `Apply Navigator From Properties` keyword was first added to
`resources/manage_object.resource` for the Area conversion. Per `docs/automation-scorecard.md`'s
Area (CO.0003) row: "2 existing OV-GM canary screens with their OWN bespoke navigator-fill logic
re-run live UNCHANGED to prove zero regression from the shared-file addition: Well 4/4, Test
Separator 4/4." This confirms the shared-file edit made for Area's own conversion did not break
Well's pre-existing, independent navigator gesture. Only afterward, in the separate PR #540, was
Well itself migrated onto the new shared keyword.

## Known risks
- Nav scope is DATA-dependent (P1 objects) — if the P1 cascade is renamed/removed the suite fails
  at navigator-apply; re-derive a working scope (owner walk-through or DB) if this happens.
- Shared-keyword dependency: Well's navigator fill now depends on `resources/manage_object.resource`'s
  `Apply Navigator From Properties` keyword — any future edit to that shared file should re-run
  Well live as a regression check (same discipline Well itself benefited from as a canary before
  its own conversion).
