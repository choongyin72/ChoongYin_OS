# SOW — Report Area IUD

## Classification
- **Screen:** Reporting > Report Area (BF_CODE **RP.0017**)
- **Type/pattern:** OV (Manage-Object, `manage_object_nav`) — date-effective; **plain, simplest OV** (no dropdowns, no Description)
- **DB view:** `OV_REPORT_AREA` (base `REPORT_AREA`/versioned); key `CODE`
- **Delete:** End Date = Start Date → row leaves `OV_REPORT_AREA`

## Nav / grid / cells
- **Open:** menu search "Report Area" → `label.tv-link`. **Grid needs GO** to load (no default rows).
- **Grid:** `manage_object_nav_nav:form:T_data`
- **Insert (objectForm):** Report Area Code `R0:C1:in`, Report Area Name `R1:C1:in`, Start date `R2:C1:da_input` (mandatory); End date `R3` optional
- **Update (updateAttributes):** Report Area Name `R1:C1:in` (Code `R0` read-only)
- **Delete (objectdates):** End date `R0:C3:da_input` = Start Date

## Test data
- `AUTOTEST_RPTA_<timestamp>` unique per run; Start/End = `${TEST_START_DATE}` (2000-01-01).

## Dev story
Recon-first (DB + live form) confirmed the simplest OV shape (Code/Name/Start Date; no Description). Playwright
thin driver over the shared engine → 7/7 first run. Temp-row recon of `updateAttributes`/`objectdates` ids
(self-cleaned) → RF T3+suite reuse T2 `manage_object` + `DbVerify.py` → live 4/4, update DB-verified via
`Field Should Equal In View`.

## Lessons / known risks
- Under top-level **Reporting** menu (not Configuration/Assets); RF/bundle in `Reporting/`.
- Grid does not auto-load — GO after open (T3 `Open ... Screen` calls `Apply Navigator`).
- No Description column — update = Name only.

---

## Addendum 2026-08-28 — Batch 9 Bank-pattern rebuild (PR #468, merged 2026-08-23)

_This addendum documents the real rebuild that superseded the section above's 2026-07-25
description. Backfilled per `docs/lean-deliverable-backfill-workorder.md` (Batch 10) — the RF
conversion shipped under the 2026-08-23/26 lean waiver without a doc/evidence refresh; this closes
that gap. No RF/automation file was touched to produce this addendum._

### What changed (from PR #468's real body)
Upgraded from the partial label-driven build (`Fill OV Field By Label`, no properties-file-driven
insert, no explicit grid-filter wiring) to the full Bank/Berth pattern:
`Insert/Update Object From Properties`, `Verify Object Insert Exists/Form Record/Found/Removed/Does
Not Exist`, and explicit `Find/Clear Report Area Row By Filter` wired into Update/Find/
Verify-Found/Delete. Switched from a per-run timestamped code to a **fixed test code
`AUTOTEST_RPTA`** (confirmed free in `OV_REPORT_AREA` via a fresh oracledb connection before use),
with per-TC Login/Logout on one browser opened once in Suite Setup (matches the exemplar suite
style). Added TC04 Find — the suite is now 5 TCs (Clean/Insert/Update/Find/Delete), not the
original 4.

### Test data (current)
- Fixed code `AUTOTEST_RPTA` (not the old per-run timestamped code).
- `testdata/report_area_{insert,update,form_verify,grid_verify}.properties` drive the T2
  properties-file keywords; Start/End dates via `${START_DATE}`/`${END_DATE}` in the suite
  (2000-01-01).

### Real gotcha (from PR #468)
The date field's real label is **"Start date"** (lowercase "date"), not "Start Date" (capital D) —
confirmed live via a reproducible 30s locator timeout with the capital-D form, then fixed by
matching the pre-existing page object's own recon comment. This is the opposite direction of the
Section 1 table above (which used "Start Date" loosely) — the exact-match label lookup requires the
real casing.

### Verification at PR #468 merge time (cited in the PR body)
Live 5/5; `Find Object Row By Filter` fired 28x (grep on that run's `output.xml`); DB self-clean via
fresh oracledb connection (`SELECT CODE, NAME FROM OV_REPORT_AREA WHERE CODE LIKE 'AUTOTEST%'` → 0
rows); full-tree dryrun 762/762 pass; robocop parity with `berth_page.resource`/`berth_iud.robot`'s
own baseline (9 identical-category issues — VAR02 unused suite variables + DOC02 missing TC docs).

### This backfill's own fresh re-verification (2026-08-28, doc/evidence only)
- `robot --dryrun tests/Reporting/report_area_iud.robot` → 5/5 PASS.
- Full-tree `robot --dryrun tests/` → **883/883 PASS**, no regressions.
- `EC_HEADLESS=true robot` live re-run → **5/5 PASS**, first attempt, no flake; artifacts in
  `evidence/2026-08-28_backfill/`.
- `py -m robocop check pageobjects/Reporting/report_area_page.resource
  tests/Reporting/report_area_iud.robot` → **9 issues** (same VAR02+DOC02 shape cited at PR #468
  merge time — no new category, no regression).
- `Find Object Row By Filter` → **15 hits** in this session's own `output.xml` (count differs from
  PR #468's 28 — expected, since this is a fresh 5-TC run vs. that PR's own build-time run; same
  keyword, same wiring, no regression).
- DB self-clean (fresh oracledb connection, new `investigation/check_autotest_residual.py`) → `[]`
  (0 residual `AUTOTEST%` rows) after the live run.
- `py scripts/check_bundle_hygiene.py` → PASS (167 bundles + 273 recon scripts scanned; the one WARN
  is a pre-existing, unrelated Contract Area recon script, not this screen).
