# JOURNAL — Report Context IUD

_Screen: Reporting > Excel Report Templates > Report Context (RP.0007). Custom-URL OV,
no navigator. View `OV_REPT_CONTEXT`._
_This JOURNAL is a backfill (2026-08-28, `docs/lean-deliverable-backfill-workorder.md` Batch 12) —
the bundle predates the JOURNAL requirement (built lean under Section G's since-retired waiver).
Content below is pulled from the original build PR #487 (merged 2026-08-24), not invented._

## Built (2026-08-24, PR #487)
- Brand-new Bank-pattern RF IUD suite — no prior automation existed for this screen at all.
- T3 page object `pageobjects/Reporting/Excel_Report_Templates/report_context_page.resource`
  (label-driven, properties-file-driven, T2-consolidated pattern, mirrors Bank/WBS).
- Suite `tests/Reporting/Excel_Report_Templates/report_context_iud.robot` (5 TCs: clean-state,
  insert, update, find, delete).
- 4 properties files: `report_context_{insert,update,form_verify,grid_verify}.properties`.
- Additive credential pair `REPORT_CONTEXT_EC_USER`/`REPORT_CONTEXT_EC_PASS` in `credentials.py`.
- Registry row (`ec_screen_registry.md`) + scorecard row (`automation-scorecard.md`), both new.

## Done well
- Full I-U-D DB-verified vs `OV_REPT_CONTEXT`: insert Code/Name/Start Date, update Name, delete via
  objectdates End Date = Start Date. Fixed test code `AUTOTEST_REPORT_CONTEXT`, confirmed absent
  before the build and confirmed 0 residual after (fresh oracledb connection).
  Full `tests/` dryrun 790/790 pass on the whole tree at build time. No shared T1/T2 file edits —
  a clean new 3-level menu subfolder (`Reporting/Excel_Report_Templates/`).
  Grid-filter keyword (`Find Object Row By Filter`) confirmed fired via an `output.xml` grep
  (15 hits) — the explicit filter wiring was included from the start, not bolted on after.

## Done wrong / lessons
- **LABEL lookup mismatch:** `class_property_cnfg.LABEL` for `CLASS_NAME=REPT_CONTEXT` reads
  "Reporting context" (lowercase, generic), NOT "Report Context" (the actual menu name /
  `BUSINESS_FUNCTION.NAME`). The stock `resolve_ec_screen.py`/`scan_ec_screen.py` LABEL-keyed
  lookup silently misses this screen as a result (returns no match / `CLASS_TYPE=None`). Fixed by
  querying `class_cnfg` directly by `CLASS_NAME` instead of trusting the LABEL lookup, and by
  patching a local (uncommitted) copy of the scan script to hardcode the DB-confirmed
  `CLASS_TYPE=OBJECT`.
- **First live attempt was 4/5, not 5/5:** TC02 failed on a `nav:form:T:sfilter0_ft_filter`
  visibility timeout inside the shared T2 grid-filter-toggle mechanism. Re-ran the identical suite
  with zero code changes — passed clean 5/5. Root-caused as a one-off environment/timing flake, not
  a code defect; no shared T1/T2 file was touched to "fix" it (nothing needed fixing).
- **Navigator assumption risk:** sibling screen Report Area (also under top-level Reporting) uses
  a manage-object+GO shape. Report Context does NOT — confirmed live (`fields=[]`, `go=[]`) before
  assuming Bank's usual Apply-Navigator step applied. Two screens sharing a parent menu do not
  necessarily share a navigator shape.

## Blockers -> resolution
- Live TC02 4/5 -> resolved by a clean retry (flake, not a defect) — see "Done wrong" above.
- No hard blockers. No data damage; the fixed test code was self-cleaning throughout.

## Decisions
- Built as an RF-only lean deliverable at the time (owner-approved Section G waiver, since
  retired 2026-08-27) — no Playwright bundle, no SOW/JOURNAL/evidence/KB map at build time. This
  backfill restores those items per Section H without touching the automation itself.
- Isolated sparse-checkout clone under `Workplaces/report_context/` used for the original build
  (per PR #487's body); this backfill uses its own separate isolated worktree
  (`C:/tmp/wt-reportcontext-backfill`) and touches none of the original automation files.

## Evidence
- Original live run (2026-08-24): retry 5/5 (first attempt 4/5, flake) — see PR #487 body and
  registry/scorecard rows for the original citation.
- Backfill evidence capture (2026-08-28, this bundle): `evidence/log.html`, `evidence/report.html`,
  `evidence/output.xml` — live headless run, 5/5 PASS, first attempt (no retry needed this time).
  Per-TC step screenshots also in `evidence/`. DB self-clean re-confirmed via a fresh connection:
  0 residual `AUTOTEST_REPORT_CONTEXT` rows in `OV_REPT_CONTEXT` post-run.
