# JOURNAL — Licence IUD

_Screen: Configuration > Assets > Commercial Objects > Licence (OV, manage-object,
nav-free, date-effective). View `OV_LICENCE`._
_This JOURNAL was backfilled 2026-08-28 (bundle predated the JOURNAL rule — Section H
retirement of the Section G lean waiver, `docs/lean-deliverable-backfill-workorder.md`
Batch 6). Content is pulled from PR #438's real body/commit history, not invented._

## Built
- **2026-06-12 (original):** data-driven Playwright + RF pair generated from section
  recon (`investigation/commercial_objects_recon.py`), using the older hardcoded-field-id
  pattern (bespoke per-screen Insert/Update/Delete keywords, no properties-file-driven
  insert). `evidence/licence_results.json` and the `licence_0*_*.png` screenshots date
  from this build.
- **2026-08-23, PR #438 (Batch 3 Bank-pattern conversion):** rebuilt
  `pageobjects/.../licence_page.resource` and `tests/.../licence_iud.robot` from the
  older hardcoded-field-id pattern to the label-driven, properties-file-driven,
  T2-consolidated Bank/Country pattern, including grid Find/Clear Row By Filter wiring
  from the start. New: `testdata/licence_{insert,update,form_verify,grid_verify}.properties`.
  Additive: `resources/credentials.py` gained `LICENCE_EC_USER`/`LICENCE_EC_PASS`. One of
  5 parallel Batch 3 conversions (Customer/Field Group/Licence/MMS Lease/Operator Lease),
  see `tmp/batch3_shared_findings.md`.
- **2026-08-27/28 (this backfill):** SOW/README/JOURNAL/evidence/CHECKLIST.md/KB-map
  bundle added per the owner's 2026-08-27 retirement of the lean waiver. No automation
  file touched.

## Done well
- PR #438 recon confirmed live before writing any config: manage-object OV, nav-free (GO
  button count = 0 of 94 elements present), screen-prefixed "Licence Code"/"Licence Name"
  labels (not the generic "Code"/"Name" Bank/Object List use), and the exact mandatory set
  (Licence Code/Licence Name/Start Date only) via a field-label recon script dumping every
  ECCell label in both `objectForm` (8 labels) and `updateAttributes` (6 labels).
- Full I-U-D DB-verified vs `OV_LICENCE`: live RF run 5/5 PASS (TC01-TC05); full `tests/`
  dryrun 735/735 PASS at the time of the PR.
- Self-clean confirmed via a fresh `oracledb` connection independent of the test run's own
  connection: `SELECT COUNT(*) FROM OV_LICENCE WHERE CODE = 'AUTOTEST_LICENCE'` = 0, both
  pre-run free and post-run clean. Recon scripts (`tmp/recon_licence.robot`,
  `tmp/check_db.py`, etc.) deleted before commit.
- Grid-filter wiring included from day one (not deferred to a later pass) and confirmed
  fired: `grep -c 'name="Find Licence Row By Filter"' output.xml` = 5 hits.
- robocop: 12 issues total (4 VAR02 + 5 DOC02 on the new suite + 3 pre-existing
  `credentials.py` findings) — identical in kind/count to the established Bank/Country
  baseline, no new issue classes introduced.

## Done wrong / lessons
- The PR #438 body records no gotcha or fix-round specific to Licence itself (unlike some
  Batch 3 siblings — e.g. Field's Geo Area/groupmodel link — Licence's own recon and
  conversion went through cleanly on the first pass).
- This backfill's own scope: the original bundle (`licence_sow.md`, `README.md`,
  `evidence/`, `playwright/`) predates the 2026-08-23 Bank-pattern conversion by over two
  months and described the OLD hardcoded-field-id DOM references as current. Backfilled
  the SOW to record both the original (superseded) DOM ids and the current label-resolved
  shape, rather than silently overwriting history.

## Blockers -> resolution
- None recorded for Licence in PR #438 or during this backfill. Live dryrun (5/5) and
  live headless run (5/5) both passed on the first attempt during backfill re-verification
  (2026-08-28) — no retry needed.

## Decisions
- RF suite stays the sole currently-maintained automation path; the original 2026-06-12
  standalone Playwright reference (`playwright/ec_iud_licence.py`) is kept for history
  only, per the owner's 2026-08-27 decision that the Universal Screen Engine
  (`py/engine.py`) replaces new hand-written Playwright drivers going forward — it was NOT
  rebuilt or re-verified as part of this backfill.
- Fixed test code `AUTOTEST_LICENCE` (not a timestamped code) — matches Bank/State/
  Country's convention; confirmed free in `OV_LICENCE` before being wired in on 2026-08-23.

## Evidence
- RF (2026-08-23, PR #438): live 5/5 PASS, full-tree dryrun 735/735 PASS, filter-fired
  grep = 5, DB self-clean = 0 residual (all cited in the PR body).
- RF (2026-08-28, this backfill's re-confirmation run): dryrun 5/5 PASS, live headless
  5/5 PASS, filter-fired grep = 5, robocop 9 issues (T3+suite only, matching baseline
  shape), fresh-connection DB self-clean = 0 residual. Raw artifacts in `evidence/`
  (`licence_backfill_dryrun_report.txt`, `licence_backfill_live_report.txt`).
- Playwright (original 2026-06-12 build): `evidence/licence_results.json` +
  `evidence/licence_0[1-8]_*.png`.
