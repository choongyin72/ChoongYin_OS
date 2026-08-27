# SOW - Well Bore Interval IUD (Configuration > Assets > Well_and_Reservoir_Objects)

_Refreshed 2026-08-28 (Batch 5, `docs/lean-deliverable-backfill-workorder.md`) to cover the
Area-pattern STRUCTURE conversion (PR #563, merged 2026-08-27). The section below this note is the
ORIGINAL 2026-07-31 base-build SOW text (kept for history, not deleted) - it still accurately
describes the screen's genuine navigator/popup shape, which the conversion did not change. See
"Area-pattern conversion (PR #563)" further down for what actually changed._

## Area-pattern conversion (PR #563, 2026-08-27) - dev story pulled from the real PR body
Converted Well Bore Interval's RF automation from the OLD 4-TC/suite-level-login/timestamped-code/
inline-DB-verify shape to the full Area-pattern structure: 5 TCs (Verify Clean State / Insert /
Update / Find / Delete), per-TC Login/Logout on one Suite-Setup browser, a FIXED test code
`AUTOTEST_WBI` (confirmed free in `OV_WELL_BORE_INTERVAL` before and after the live run, 0/0),
properties-file-driven insert/update/verify (`testdata/well_bore_interval_{navigator,insert,
update,form_verify,grid_verify}.properties`, all new), explicit grid-filter wiring (`Find/Clear
Well Bore Interval Row By Filter`), and zero inline DB-verify calls (verification now delegates to
the shared T2 `Verify Object Insert Exists/Form Record/Found/Removed/Does Not Exist` family).

**Real gotcha, and why a BESPOKE T3 keyword was used instead of the shared one:** this screen was
correctly classified, on TWO separate live per-field checks, as a genuine navigator NON-FIT for
the shared T2 `Apply Navigator From Properties` keyword - the navigator is **6 PER-FIELD groups**
(`nav:form:G:1..G:6:R:1:C:0`), not the single-row/increasing-column cascade shape that keyword
supports. This is NOT the same kind of "non-fit" mistake made earlier on Meter/Tract (where those
screens were WRONGLY called non-fit and actually did fit); Well Bore Interval's per-field shape
held up both times it was checked live. What made the screen convertible anyway, without
compromising that finding, was building a BESPOKE, screen-local T3 keyword
(`Apply Well Bore Interval Navigator` in `well_bore_interval_page.resource`) modeled on
`well_page.resource`'s own pre-2026-08-26 "Apply Well Navigator" keyword - the project's existing
precedent for a genuinely per-field-groups navigator. The bespoke keyword loops through the
groups the already-proven driver (`py/well_bore_interval_iud.py`) actually fills - G:1 Production
Unit / G:2 Area / G:3 Facility Class 1 / G:4 'Well & Well Hookup' / G:6 'Well Bore' - reads each
value from `testdata/well_bore_interval_navigator.properties`, and clicks GO once. G:5 ('Well') is
deliberately skipped: present in the DOM with mandatory-yellow styling when empty, but offering
ZERO usable options under this scope (live-reconfirmed 2026-08-27,
`Workplaces/well-bore-interval-area-pattern/recon_wbi_nav_live.py`, read-only, no save) - the same
"phantom mandatory nav group" EC quirk already logged for this screen's own siblings (Well G:5,
Well Bore G:5). Because the shared T2 keyword genuinely does not support this shape,
`resources/manage_object.resource` was NOT touched by this conversion - the bespoke keyword lives
entirely in the screen's own T3 file, which is exactly the "bespoke-but-legitimate" outcome (as
opposed to Tract's shared-keyword-EXTENSION approach, where Tract's own navigator shape turned out
to fit the shared keyword once verified field-by-field).

The mandatory 'Well Bore' POPUP (list grid `Objects:form:T_data`, not the generic
`PopupList:form:T_data`) was kept via the existing screen-local picker, reusing the navigator's own
G:6 value (FIELD-REUSE RULE) - unchanged in substance by the conversion, just re-wired to read from
the new properties file instead of a hardcoded value.

Cited evidence in PR #563's own body: live `EC_HEADLESS=true robot` 5/5 pass; full-tree dryrun
881/881 (zero collisions); robocop 7 issues (2 VAR02 + 5 DOC02), exact parity with
`area_page.resource`/`area_iud.robot`'s own baseline; fresh-connection DB self-clean 0 residual
`AUTOTEST%` rows; `grep -c "Find Object Row By Filter"` on that session's `output.xml` = 15
(confirming the grid-filter keyword fired repeatedly, not just once).

---

## Original 2026-07-31 base-build SOW (kept for history)

- **Screen:** Well Bore Interval   **BF:** CO.0057   **View:** `OV_WELL_BORE_INTERVAL` (167 rows, DB-verified)   **Base:** `WEBO_INTERVAL`
- **Type:** OV-GM with **6 PER-FIELD nav groups** `nav:form:G:1..G:6:R:1:C:0`. Grid `manageObject:form:T_data`.
- **SPECIFIC nav values (recon-verified):** G:1 P1 Production Unit -> G:2 P1 Area -> G:3 P1 Facility 1 ->
  G:4 **P1 W008 OP** (a REAL well) -> **G:6 P1 W008 WB001** (the WELL BORE). **G:5 returns ZERO
  options** under this scope (unusable filter, skipped) - the same pattern as Well Bore's G:5. Grid
  then lists the real interval `P1 W008 WB001 WBI001`.
- **Mandatory form field: 'Well Bore' POPUP** (pin R:4) whose list grid is **`Objects:form:T_data`**
  (recon-verified; contains exactly `P1 W008 WB001` under this scope) - not `PopupList:form:T_data`,
  so the generic engine/T1 helpers report a false "empty source list". Screen-local picker selects
  the nav-scope well bore BY VALUE.
- Start Date 2020-01-01. DELETE = End Date = Start Date. Unique `AUTOTEST_WBI_<timestamp>` per run;
  self-cleaning; the existing 167 intervals untouched.
- **Third screen of the well hierarchy** (Well -> Well Bore -> Well Bore Interval), all three now automated.

## Known risks
- Nav + popup values are DATA-dependent (P1 W008 OP / P1 W008 WB001); re-derive if the sandbox changes.
- G:5's purpose is unknown (no options in any scope tried) - if it ever populates, revisit whether it
  is a required filter.
