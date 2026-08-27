# JOURNAL - Document Template (CD.0013) OV IUD

_Refreshed 2026-08-28 (deliverable backfill, `docs/lean-deliverable-backfill-workorder.md`
Batch 12, the FINAL batch) to cover the 2026-08-24 Bank-pattern conversion (PR #484), modeled on
`screens/Configuration/Assets/Financial_Objects/Bank/JOURNAL.md`'s structure. The original
2026-07-26 entry is kept below as history._

## Built
- **2026-07-26 (original build):** reusable OV engine `py/ec_object_iud.py` + thin driver
  `py/document_template_iud.py`; label-driven T3
  `pageobjects/Configuration/Assets/Revenue_Document_Objects/document_template_page.resource`;
  RF suite `tests/Configuration/Assets/Revenue_Document_Objects/document_template_iud.robot`
  (4-TC). `verify_screen.py` -> OVERALL PASS (robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4,
  Playwright 7/7).
- **2026-08-24 (PR #484, "Document Template - upgrade to Bank pattern (Phase 3)"):** upgraded
  Document Template's existing label-driven-only RF automation to the full Bank-pattern shape
  (properties-file-driven insert/update/verify + explicit grid-filter wiring), matching
  `bank_page.resource`/`berth_page.resource` exactly. Classified **PARTIAL** by
  `ec-bank-pattern-converter` (had `Fill OV Field By Label` but neither `Insert Object From
  Properties` nor `Find <Screen> Row By Filter`). Rebuilt T3 + suite (TC01-05, added TC04 Find);
  added 4 new `testdata/document_template_{insert,update,form_verify,grid_verify}.properties`
  files; added `DOCUMENT_TEMPLATE_EC_USER/PASS` to `resources/credentials.py` (additive only);
  fixed test code changed to `AUTOTEST_DOCUMENT_TEMPLATE`; `py/document_template_iud.py`
  (Playwright side) left unchanged, still 7/7 from 2026-07-26.
- **2026-08-25 (alignment fix, same registry row):** removed 2 leftover inline DB-verify keywords
  (`Document Template Should Exist/Not Exist In DB`) from the `.robot` TC02/TC05 that violated
  Bank's pure-screen-only verification convention (2026-08-18) - same deviation class as DOA Credit
  Limit (PR #503). Re-verified live 5/5, dryrun 810/810, filter fired 18x, DB self-clean 0
  residual (per the registry row's own note).

## Done well
- Full I-U-D DB-verified vs `OV_DOC_TEMPLATE` (insert Code/Name/Document Title, update Name,
  delete End=Start); self-clean 0 residual, confirmed via a fresh independent `oracledb`
  connection at PR #484's own merge.
- PR #484 trusted the already-proven Playwright driver's `Document Title` field as de-facto
  mandatory over the Phase-3 static scanner's "no mandatory dropdowns" note (a documented Phase-3
  shared-findings gotcha) - a real instance of preferring a proven driver's actual field set over
  a static scan, rather than re-deriving from scratch.
- Delete's `objectdates` End Date field id resolved BY LABEL at runtime (`OV Field Id By Label`)
  rather than a fresh, unverified hardcode - the same "read the real DOM, don't guess an id"
  discipline this repo requires for any destructive write.
- No shared `manage_object.resource`/`common.resource` edits were needed for the conversion.

## Done wrong / lessons
- The original 2026-07-26 SOW/README/CHECKLIST/VERIFY-REPORT predated both the JOURNAL/evidence/
  KB-map restoration rule and PR #484's Bank-pattern conversion - they still described the
  pre-conversion 4-TC, label-driven-only shape (no properties files, no explicit grid-filter
  wiring, no TC04 Find) as if it were the current state. This backfill is the direct fix for that
  gap (owner decision 2026-08-27 retiring the 2026-08-23/26 lean waiver, Section H of
  `docs/IUD-DELIVERABLE-CHECKLIST.md`).
- PR #484's own body does not disclose any live-run flake, wrong classification, or shared-file
  regression for this conversion - the one real, disclosed issue in this screen's history is the
  2026-08-25 alignment fix above (2 inline DB-verify keywords that violated the pure-screen-only
  convention), which is carried into this JOURNAL rather than smoothed over.

## Blockers -> resolution
- No live-run blocker is recorded in PR #484's own body (live RF 5/5 on the first cited attempt,
  full-tree dryrun 775/775, zero collisions).
- This backfill's own evidence-capture run (2026-08-28): dryrun 5/5 and live 5/5 both passed on
  the first attempt, no retry needed - see "Evidence" below.

## Decisions
- Playwright driver `py/document_template_iud.py` and its `investigation/recon.py` stay unchanged
  and permanently un-rebuilt for Bank-pattern work - the Universal Screen Engine is the
  owner-decided replacement for hand-written Playwright drivers going forward (Section H,
  `docs/IUD-DELIVERABLE-CHECKLIST.md`).
- Registry (`docs/ec_screen_registry.md`) and scorecard (`docs/automation-scorecard.md`) rows were
  MODIFIED IN PLACE by PR #484 (not new rows) - this backfill does not touch them again.
- Fixed test code `AUTOTEST_DOCUMENT_TEMPLATE` (not per-run timestamped) is deliberate: TC05
  (delete) must complete every run so the code stays free for the next run, same convention as
  every other Bank-pattern-converted screen.

## Evidence
- Original 2026-07-26 build: `evidence/document_template_0[1-5]_*.png` + `evidence/rf_report.html`
  (Playwright 7/7, RF 4/4, `VERIFY-REPORT.md` OVERALL PASS) - preserved unchanged.
- PR #484 conversion (2026-08-24) + 2026-08-25 alignment fix: live RF 5/5, full-tree dryrun
  810/810, filter fired 18x, fresh-connection DB self-clean 0 residual - all cited in the registry
  row and PR #484's own body (this backfill did not re-verify those historical numbers, only its
  own fresh run below).
- This backfill (2026-08-28): `evidence/backfill_2026-08-28/` - dryrun 5/5, live 5/5 (screenshots
  per TC step + `log.html`/`report.html`/`output.xml`), robocop 9 issues (baseline noise, see
  `results_summary.md`), hygiene PASS, filter fired 15x, DB self-clean 0 residual (before and
  after this task's own live run) - real numbers captured by this task, see that folder's
  `results_summary.md`.
