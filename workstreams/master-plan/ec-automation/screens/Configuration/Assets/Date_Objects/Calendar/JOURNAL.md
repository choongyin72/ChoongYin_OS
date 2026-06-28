# JOURNAL - feature/calendar-iud (CD.0024 Calendar)

## Built
- Full IUD automation for Calendar (OV, date-effective): T3, RF suite (4 TCs clean->insert->update
  ->delete, in-suite DB asserts), Playwright flow, recon script, evidence, SOW, README, CHECKLIST.
- 4th of 5 Date Objects screens. Built to the 19-item IUD deliverable standard.

## Done well
- DB-first + DOM recon confirmed Calendar is the SIMPLEST of the 5: plain Bank-family OV with only
  Code/Name/Start-Date mandatory; the 7 weekday indicator cells (R:6-R:12) are optional checkboxes.
- Checked for a child member grid (the screen has `daytimes`/`versions` sub-tabs) -- confirmed those
  are the standard OV objectdates/versions tabs, NOT a holiday child grid. No PC complexity.
- Wrote a clean plain-OV bundle (no dropdown/offset machinery) rather than carrying term-screen baggage.
- T3 thin; zero shared-file edits; full I-U-D.

## Done wrong / corrected
- **Wrong grid id (the real one).** Assumed Calendar's list grid was `manage_object_nav_nav:form:T_data`
  (like the 3 term screens). Live run: TC02 Insert FAILED at `Row Should Exist`. Diagnosis (not retry):
  the **insert had persisted** (3 AUTOTEST rows in `ov_calendar` + base `CALENDAR`), so it was a UI-read
  failure, not an insert failure. A grid dump showed `manage_object_nav_nav:form:T_data` ABSENT and no GO
  button -- Calendar is a **custom-URL OV** (grid `nav:form:T_data`, no navigator GO, reload via toolbar
  Refresh; cf. Account / Regulatory Permits). Fixed `${CAL_TABLE}` -> `nav:form:T_data`; T2 Save And
  Refresh List auto-falls back to Refresh Screen when no GO. Re-run = 4/4. **Cleaned the 3 residual rows**
  (End=Start via UI) before re-running -- self-clean restored. Lesson: a screen's grid id / GO presence is
  recon ground-truth, not an assumption from siblings (template-trust-boundary). Diagnose silent UI
  failures against the DB before touching the flow.
- Clone substitution missed "Doc Date Term" in the Playwright TEST_NAME -> fixed to "AUTOTEST Calendar".

## To improve
- Last screen = Calendar Collection (CD.0105) -- a "collection of calendars" may genuinely have a
  child member grid (PC). Recon fully before deciding plain-OV vs PC.

## Blockers -> resolution
- None.

## Decisions
- Left the weekday checkboxes at default (optional) -- minimal valid insert. Stacked on CD.0023 (PR #143).

## Evidence
- Live RF 4/4 PASS; Playwright ALL PASS (evidence/results.json).
- DB: TC02 `Code Should Be Present In View ov_calendar`; TC04 `Code Should Be Absent In View`;
  independent re-read AUTOTEST_CAL in OV_CALENDAR = 0 rows.
