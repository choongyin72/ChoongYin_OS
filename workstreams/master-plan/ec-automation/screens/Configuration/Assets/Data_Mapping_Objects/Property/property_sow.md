# SOW - Property IUD (Configuration > Assets > Data_Mapping_Objects)

- **Screen:** Property   **BF:** SP.0059   **View:** `OV_PROPERTY`   **Base:** `CONTRACT_AREA`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED,
  date-effective. Converted to the full **Area-pattern** structure via PR #559 (merged
  2026-08-26).
- **Navigator shape:** TWO DOM groups - `G:0` ("Date") and `G:1` ("Business Unit") - which
  superficially resembles the disqualifying "per-field navigator groups" shape, but is NOT: PR
  #559's own live read-only recon (`Workplaces/property-area-pattern/recon_property_nav.py`, no
  Save/Insert/Delete, 2026-08-26) confirmed `G:0`'s Date field already carries a non-empty
  default on load (`MandatoryCellStyleWhite`), so `G:1`'s Business Unit dropdown at `C:0` (not the
  usual `C:1`) is the ONLY genuinely mandatory+empty field - the same single-group-needs-fill
  shape already proven to fit Area's pattern on Tract (PR #555). This proactive application (no
  wrong-then-corrected detour) is called out explicitly in PR #559's own body.
- **Shared-keyword extension:** the T2 `Apply Navigator From Properties`
  (`resources/manage_object.resource`) gained optional `${group}`/`${start_col}` arguments for
  Tract's own conversion (PR #555, merged 2026-08-26, ahead of Property's). PR #559's body states
  Property calls it with `group=1 start_col=0` to match this screen's own group/column position -
  both args additive-only, default behavior unchanged for every other caller (Area, Well, Test
  Separator, Chemical Tank, Price Object, Meter).
- Mandatory fields: Property Code, Property Name, Start Date (>= 2003-01-01, the referenced
  Business Unit "Royalty Canada"'s own effective date), Business Unit Name (must equal the
  navigator's own scope value, "Royalty Canada," or the row is invisible under that scope).
- Test data (fixed since PR #559): code `AUTOTEST_PROPERTY` (confirmed free in `OV_PROPERTY` via a
  fresh oracledb connection before the PR #559 live run);
  `testdata/property_{navigator,insert,update,form_verify,grid_verify}.properties`.
- IUD: INSERT -> UPDATE(Property Name) -> FIND -> DELETE(End=Start). Self-clean = absent in
  `OV_PROPERTY`.
- **Dev story (from PR #559):** converted from the original 2026-08-02 build (4/4 RF + 8/8
  Playwright, hand-written driver `py/property_iud.py`) to the Area-pattern full STRUCTURE: 5 TCs
  (added TC04 Find), per-TC Login/Logout, fixed test code, properties-file-driven insert/update/
  verify, explicit grid-filter wiring, zero inline DB-verify calls. Live 5/5 pass, full-tree
  dryrun 878/878, DB self-clean confirmed (0 residual `AUTOTEST%` rows via a fresh independent
  oracledb connection), robocop parity vs Area's own 7-issue baseline (same VAR02+DOC02 kind/
  count). Built in an isolated worktree after discovering the shared working directory was being
  concurrently checked out/committed to by other parallel Area-pattern-conversion agents mid-task
  (some in-progress doc/credentials edits were clobbered by a forced branch switch and had to be
  re-applied from a dedicated worktree - no functional/page-object files were lost). Playwright
  driver `py/property_iud.py` left untouched (RF-only structural conversion).
- Deliverables: driver `py/property_iud.py` (untouched), T3
  `pageobjects/Configuration/Assets/Data_Mapping_Objects/property_page.resource`, suite
  `tests/Configuration/Assets/Data_Mapping_Objects/property_iud.robot`, this SOW, `README.md`,
  `JOURNAL.md`, `evidence/`, `CHECKLIST.md`, `VERIFY-REPORT.md` (2026-08-02 build's own
  auto-generated report, retained as original evidence).
