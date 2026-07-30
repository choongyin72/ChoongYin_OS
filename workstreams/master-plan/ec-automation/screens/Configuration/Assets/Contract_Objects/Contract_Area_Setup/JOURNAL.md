# JOURNAL - Contract Area Setup (CO.2038) custom-URL OV IUD

## 2026-07-30
- **Branch:** `feature/contract-area-setup-iud`.
  Check-existing gate: registry-first (not in registry); reused shared engine (ec_object_iud.py) + T2 + DbVerify.
- **Recon** (`tmp/scripts/scan_ec_screen.py`, read-only): CUSTOM-URL OV - grid `nav:form:T_data`,
  **NO navigator, NO GO button** (`navigator: {fields: [], go: []}` in the scan output). Mandatory:
  Contract Area Setup Code / Name / Start Date + 2 reference dropdowns (Contract Area Name, Contract Name).
- **Start Date decision by DB fact:** ref dropdowns only offer objects effective at the form Start Date
  (standing rule) -> queried the sandbox: 28 contract areas + 98 contracts effective at 2020-01-01 ->
  Start Date = 2020-01-01 (NOT the usual 2000-01-01).
- **Built HAND-WRITTEN (no generator):** the OV-GM generator does not fit (it calls apply_ovgm_navigator
  + expects manageObject:form:T_data). Thin driver on the shared engine - `click_go` transparently falls
  back to the toolbar Refresh on GO-less screens; label-driven T3 + suite cloned from the Storage T3
  pattern minus the navigator keyword. First custom-URL OV proven on the SHARED engine (the older
  Calendar/Calendar Collection custom-URL exemplars use legacy hardcoded-ID freestyle drivers).
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4 pass, Playwright 7/7. DB residual 0.

## Lessons
- Custom-URL OV needs zero engine changes: GRID_DATA_ID='nav:form:T_data', skip the navigator call,
  and the engine's click_go Refresh-fallback covers the reload. T2 `Save And Refresh List` likewise.
- Ref-dd effectiveness is a DB-checkable precondition, not a trial-and-error one: count the candidate
  parents effective at the intended Start Date BEFORE picking it.
