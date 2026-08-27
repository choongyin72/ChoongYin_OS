# JOURNAL — Chemical Product IUD

_Screen: Configuration > Assets > Chemical Objects > Chemical Product (`CO.0072`), OV
manage-object, date-effective. View `OV_CHEM_PRODUCT`. Built via `ec-bank-pattern-new-screen`
(genuinely new build, Phase 3), PR #486, merged 2026-08-24. This JOURNAL was backfilled
2026-08-27/28 under the Section H workorder — the bundle predated the restored JOURNAL rule._

## Built (2026-08-24, PR #486)
- **T3 page object** `pageobjects/Configuration/Assets/Chemical_Objects/chemical_product_page.resource`
  (new, 192 lines) — label-driven, properties-file-driven, delegates to the shared T2
  (`manage_object.resource`) and T1 (`common.resource`); no shared-file edits.
- **5-TC suite** `tests/Configuration/Assets/Chemical_Objects/chemical_product_iud.robot` (new)
  — TC01 clean-state, TC02 insert, TC03 update, TC04 find, TC05 delete.
- **4 properties files** `testdata/chemical_product_{insert,update,form_verify,grid_verify}.properties`
  (new) — fixed test code `AUTOTEST_CHEMPROD`.
- **Screen-scoped cleanup library** `libraries/ChemicalProductCleanup.py` (new, 57 lines) — the
  Delete workaround (see below); deliberately NOT folded into the shared `libraries/DbVerify.py`.
- Dedicated credentials `CHEMICAL_PRODUCT_EC_USER`/`CHEMICAL_PRODUCT_EC_PASS` appended to
  `resources/credentials.py`.
- Registry/scorecard/checklist rows appended (`docs/ec_screen_registry.md`,
  `docs/automation-scorecard.md`, `docs/bank-pattern-conversion-checklist.md`,
  `docs/grid-filter-standardization-checklist.md`).

## Done well
- Full I-U-D DB-verified vs `OV_CHEM_PRODUCT`/`CHEM_PRODUCT`: insert Chemical Product Code/Name/
  Start Date/Meas. Units, update Name, delete via End Date = Start Date. Self-clean confirmed via
  a **fresh** oracledb connection (not the live-run session): 0 residual rows in `CHEM_PRODUCT`
  and `OV_CHEM_PRODUCT` for `AUTOTEST%`, 0 orphaned `CHEM_USAGE_REPORT_CONF` rows.
  robocop parity with the `chemical_transport_tank_iud.robot`/`_page.resource` exemplar (11
  issues both sides, same DOC02-only baseline noise — no regression introduced).
  Explicit grid-filter wiring (`Find Chemical Product Row By Filter`/`Clear Chemical Product Row
  Filter` → shared T2), matching Bank/Berth/Chemical Transport Tank's convention. Filter keyword
  fired 26x per `output.xml` grep.
- Live RF: 5/5 (TC01-05). Full-tree dryrun: 779/779, 0 failed.

## Done wrong / lessons
- **Delete initially looked like it "just worked" (no UI error) but silently no-op'd.** The
  standard End=Start Save clicked cleanly with no visible error, yet `OBJECT_END_DATE` stayed
  NULL — caused by a NO-ACTION FK on the auto-created `CHEM_USAGE_REPORT_CONF` child row (a
  genuine EC PRODUCT DEFECT, not an automation gap; the web UI swallows the resulting
  ORA-02292/ORA-20102). This exact issue was already documented in
  `ec-ui-knowledge/EC_KNOWN_ISSUES.md` (2026-07-26/31, PARKED) from an earlier investigation —
  checking that doc BEFORE treating Delete as trivial (per this project's own CLAUDE.md rule)
  avoided re-discovering the root cause from scratch. Fix: apply the doc's own prescribed
  workaround — remove the child row at DB level immediately before the UI Save — in a new
  screen-scoped `ChemicalProductCleanup.py`, never touching the shared T1/T2 files. The known
  issue is now UNPARKED with the fix in place.

## Blockers -> resolution
- No UI screen exists for `CHEM_USAGE_REPORT_CONF` (no way to clear the child row via the UI) ->
  resolved by removing it at DB level via a dedicated Python library function
  (`remove_chem_usage_report_conf_child`), called from the T3's
  `Delete Chemical Product Record And Save` keyword immediately before the standard End=Start
  Save.
- No hard blockers otherwise; recon (`resolve_ec_screen.py` + `scan_ec_screen.py`) confirmed the
  navigator shape (optional date + GO, no mandatory dropdown) and mandatory fields live before any
  code was written — no guessing.

## Decisions
- Fixed test code `AUTOTEST_CHEMPROD` (not a generated unique code), matching Bank/Berth/Chemical
  Transport Tank's convention — confirmed free of existing data before and after the run.
- Delete-workaround code stays screen-scoped (`ChemicalProductCleanup.py`), not merged into the
  shared `DbVerify.py` — keeps the blast radius of an EC product-defect workaround contained to
  one screen.
- No Playwright bundle built (lean RF-only build per `ec-bank-pattern-new-screen`, and per
  Section H of the deliverable checklist, items 4/5 stay permanently waived — the Universal
  Screen Engine replaces that role).

## Evidence
- Original build (PR #486, 2026-08-24): live RF 5/5, full-tree dryrun 779/779, robocop parity
  with `chemical_transport_tank_iud.robot` (11 issues both), DB self-clean via fresh connection
  (0 residual `CHEM_PRODUCT`/`OV_CHEM_PRODUCT` rows, 0 orphaned `CHEM_USAGE_REPORT_CONF` rows).
- This backfill (2026-08-27/28): see `evidence/` in this bundle for the re-run capture.
