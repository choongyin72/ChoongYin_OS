# JOURNAL - Product Group (RC.0053) IUD

_Screen: Configuration > Assets > Royalty Objects > Product Group (OV, manage-object, Bank
pattern). View `OV_PRODUCT_GROUP`. This JOURNAL was backfilled 2026-08-28 under the
retired-lean-waiver work order (`docs/lean-deliverable-backfill-workorder.md`, Batch 7; Section H
of `docs/IUD-DELIVERABLE-CHECKLIST.md`) - the bundle's SOW/README/evidence predated the JOURNAL
rule; PR #445 (the Bank-pattern conversion) is the source of the "Built"/"Done well" content
below, pulled from its real PR body, not invented._

## Built

### Original build (2026-06-25)
- 3rd of 8 screens under Configuration > Assets > Royalty Objects. Manage-object (OV) screen,
  date-only navigator (Bank family, not OV-GM). Playwright freestyle bundle + RF suite (older
  hardcoded-field-id pattern), 4 TCs, per-run generated test code `AUTOTEST_PG_<run>`.

### Bank-pattern conversion (PR #445, merged 2026-08-23, Batch 5) - the real "what happened"
- Rebuilt the RF suite from the older hardcoded-field-id pattern to the label-driven,
  properties-file-driven, T2-consolidated **Bank pattern**, mirroring `state_page.resource`/
  `state_iud.robot` exactly, including explicit grid-filter wiring from day one.
- Live recon (New Object form + `updateAttributes` ECCell label dump) confirmed the
  screen-prefixed labels "Product Group Code"/"Product Group Name" (NOT generic "Code"/"Name")
  and that only **Start Date** is CSS-mandatory beyond Code/Name - Sort Order, Product Group Type
  (dropdown), and Comments are optional and were deliberately left out of the IUD flow.
- Suite grew from 4 TCs to 5 TCs (added TC04 Find), moved to per-TC login/logout, and switched to
  a fixed test code `AUTOTEST_PRODUCT_GROUP` (confirmed free live) instead of a per-run generated
  code.
- New testdata: `testdata/product_group_{insert,update,form_verify,grid_verify}.properties`.
  New dedicated credential pair `PRODUCT_GROUP_EC_USER`/`PRODUCT_GROUP_EC_PASS`
  (`resources/credentials.py`, additive only).
- No shared T1/T2 files (`resources/common.resource`, `resources/manage_object.resource`) were
  touched.
- Registry (`docs/ec_screen_registry.md`), `docs/bank-pattern-conversion-checklist.md`,
  `docs/grid-filter-standardization-checklist.md` (30/30), and `docs/automation-scorecard.md`
  rows updated.

### This backfill (2026-08-28, Batch 7)
- Refreshed `product_group_sow.md` (added a "Dev story / revision history" section covering both
  the original build and PR #445) and `README.md` (exact dryrun/live/DB-self-clean commands,
  current Bank-pattern facts) - both predated the JOURNAL rule and only described the original
  2026-06-25 build.
- Added this `JOURNAL.md`, `CHECKLIST.md`, and the KB selector map
  `ec-ui-knowledge/screens/product_group.md` (new - did not exist before).
- Added `evidence/backfill_2026-08-28/` (fresh dryrun + live headless re-run of the
  already-proven suite) - no automation code touched.

## Done well
- Full I-U-D DB-verified vs `OV_PRODUCT_GROUP` (insert Code+Name+Start Date, update Name only,
  delete End=Start absent); self-clean 0 residual, confirmed via a FRESH oracledb connection
  during both PR #445's own run and this backfill's re-run.
- This backfill's live headless re-run: **5/5 PASS on the first attempt** (TC01-TC05), no retry
  needed, no flake hit.
- Dryrun (this backfill): **5/5 PASS**.
- Robocop re-run this session: **9 issues** (4 VAR02 + 5 DOC02) on
  `product_group_page.resource` + `product_group_iud.robot` - matches PR #445's own cited
  Batch 5 baseline exactly, no new issue classes introduced by re-running.
- Filter-fired grep re-confirmed on this backfill's own live-run `output.xml`: `grep -c "Find
  Product Group Row By Filter"` -> **12 hits** (higher than PR #445's original 5 hits because this
  re-run's TC02/TC03/TC04/TC05 each call Find+Clear around their own action, consistent with the
  suite's design - not a regression).
- `py scripts/check_bundle_hygiene.py` -> **RESULT: PASS** (one unrelated pre-existing WARN about
  a Contract Area `investigation/` script, not related to Product Group).

## Done wrong / lessons
- No real regression or wrong turn was disclosed in PR #445's own body for the Bank-pattern
  conversion itself - it read live labels before configuring, and the only design decision worth
  calling out (not a mistake) is the deliberate exclusion of Sort Order/Product Group Type/
  Comments from the IUD flow since they are optional, per the fill-only-needed-fields convention.
- This backfill's own live re-run hit no flake - 5/5 PASS on the first attempt.

## Blockers -> resolution
- No blockers during this backfill (documentation/evidence-only; the live re-run passed clean on
  the first attempt, matching PR #445's own original result).
- No blockers were disclosed in PR #445's own body for the original conversion either.

## Decisions
- Playwright bundle (`playwright/ec_iud_product_group.py`) stays as-is, NOT rebuilt - it predates
  the Universal Screen Engine, and owner decision 2026-08-27
  (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H) confirms the Playwright driver + `investigation/`
  recon items stay permanently waived for Bank-/Area-pattern work; the engine is the owner-decided
  replacement going forward.
- The RF suite is the sole maintained/live test for this screen.
- Code lives in `ec-automation`; `ec-ui-knowledge/` stays MD-only.

## Evidence
- Original build (2026-06-25): `evidence/product_group_tc0[1-4]_*.png` (4 screenshots,
  pre-Bank-pattern 4-TC shape).
- PR #445 conversion (2026-08-23): live run 5/5 PASS (TC01-TC05), 5 `Find Product Group Row By
  Filter` hits in output.xml, robocop 9 issues (4 VAR02 + 5 DOC02, Batch 5 baseline), full-tree
  dryrun 745/745, DB self-clean 0 residual (fresh oracledb) - all cited in the PR body.
- This backfill (2026-08-28, `evidence/backfill_2026-08-28/`): `dryrun/` (5/5 PASS,
  `log.html`/`report.html`/`output.xml`) and `live/` (5/5 PASS headless, first attempt, no retry,
  `log.html`/`report.html`/`output.xml` + per-TC step screenshots), a re-confirmed 12-hit
  filter-fired grep, a re-confirmed 9-issue robocop parity check against PR #445's own cited
  baseline, a fresh-connection DB self-clean (`OV_PRODUCT_GROUP`: `AUTOTEST_PRODUCT_GROUP` count =
  0), and `py scripts/check_bundle_hygiene.py` -> `RESULT: PASS`.
