# JOURNAL — Product Description IUD

_Screen: Configuration > Assets > Financial Objects > Product Description. OV (Manage-Object,
no navigator), date-effective. View `OV_PRODUCT_NODE_ITEM`._

_This JOURNAL entry for the PR #441 conversion was backfilled 2026-08-28 under
`docs/lean-deliverable-backfill-workorder.md` (owner decision retiring the 2026-08-23/26 lean
waiver — Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`). The RF automation described below was
already built and merged in PR #441 on 2026-08-23; this JOURNAL narrates what that PR's body
actually recorded — it is not a new build and no automation file was touched to produce it. The
2026-06-11 entry below is the original Playwright-era build's own record, kept unchanged._

## 2026-06-11 (original build)
- Built the original RF suite (4 TCs: Clean State/Insert/Update/Delete — no Find TC at this
  stage) + a Playwright reference driver (`playwright/ec_iud_product_description.py`, thin
  config over the shared `_shared/iud_engine.py`), generated DATA-DRIVEN from the section recon
  (`investigation/financial_objects_recon.py`).
- Fields resolved by their `:C:0:la` labels, not positional assumptions, so row-shift screens and
  relocated dates were handled automatically.
- Extra mandatory reference dropdowns (Product/Node/Financial Code, banner-discovered) used
  "first available option" — no fixed literal value decision was made at this stage.
- Live run: RF TC01-TC04 4/4 PASS, DB-verified; Playwright reference run recorded in
  `evidence/product_description_results.json`.

## Built (2026-08-23, PR #441 — Bank-pattern conversion)
Converted the Product Description IUD suite from the older hardcoded-field-id pattern to the
label-driven, properties-file-driven, T2-consolidated "Bank pattern" (Batch 4, one of 5 parallel
screens per `tmp/batch4_shared_findings.md`).

**Files touched by PR #441:**
- `pageobjects/Configuration/Assets/Financial_Objects/product_description_page.resource`
  (rewritten — T3 thin wrappers delegating to T2 `manage_object.resource`/T1 `common.resource`).
- `tests/Configuration/Assets/Financial_Objects/product_description_iud.robot` (rewritten — 5 TC,
  per-TC Login/Logout, fixed test code `AUTOTEST_PD`).
- `resources/credentials.py` (additive — `PRODUCT_DESCRIPTION_EC_USER`/
  `PRODUCT_DESCRIPTION_EC_PASS`).
- `testdata/product_description_insert.properties`, `_update.properties`,
  `_form_verify.properties`, `_grid_verify.properties` (new).
- `docs/ec_screen_registry.md`, `docs/grid-filter-standardization-checklist.md` (25 of 25),
  `docs/bank-pattern-conversion-checklist.md` (flipped to DONE) — ec-automation project docs.
- `docs/automation-scorecard.md` (repo-root) — new Section Coverage row.

## Done well
- **Real gotchas confirmed live, not assumed** (per PR #441's body): confirmed live that this
  screen has NO mandatory nav cascade (universal Date+GO bar only, `NAV_DD_COUNT=0`), that the
  Code label is screen-prefixed ("Product Node Item Code", not generic "Code"), that the grid
  shows 4 columns (Product Node Item Code/Name/Start Date/End Date, not the generic set), and
  that 3 reference dropdowns (Product/Node/Financial Code) are genuinely mandatory
  (`MandatoryCellStyle` on each, confirmed in both `objectForm` and `updateAttributes`).
- **Batch 2 VAT Code gotcha applied:** used LITERAL first-option dropdown values
  (`AS3_CrudeOil`/`Apollo FPSO`/`Frame Agreement`), not `__FIRST__`, since TC02's round-trip
  verify compares the live screen back against the same properties file used to insert.
- Live run (EC_HEADLESS=true) at PR #441 time: **5/5 PASS**. Full `tests/` dryrun: **740/740
  PASS** (baseline was 739/739 before this suite). robocop: **9 issues** (4 VAR02 + 5 DOC02) —
  identical in kind/count to the established Bank/Customer baseline. Filter wiring confirmed
  fired: `grep -c 'name="Find Product Description Row By Filter"' output.xml` → **5 hits**.
- DB self-clean at PR #441 time: fresh oracledb connection (`ECKERNEL_EC`/`localhost:1521/ORCL`)
  — `SELECT COUNT(*) FROM OV_PRODUCT_NODE_ITEM WHERE CODE = 'AUTOTEST_PD'` → **0** (confirmed
  both pre-run free and post-run clean).

## Done wrong / lessons
- No new "done wrong" was disclosed in PR #441's own body — the conversion reported clean on
  first live run (5/5). This backfill's own re-verification run (below) also passed clean on the
  first attempt.
- The screen's own Code label being screen-prefixed ("Product Node Item Code") rather than the
  generic "Code" used by Bank/Cost Centre is a real per-screen divergence worth restating here —
  a converter that assumed the generic label would have failed silently against this screen's
  live DOM.

## Blockers -> resolution
- No hard blockers on the original conversion (PR #441) — merged same-day with clean evidence
  cited in the PR body.
- This backfill session's evidence-capture run (2026-08-28): no blockers. Pre-run DB check
  (`fetch_object("OV_PRODUCT_NODE_ITEM", "AUTOTEST_PD")` → `None`) confirmed the fixed test code
  was free before the live run. The live run completed 5/5 clean on the first attempt — no retry
  needed.

## Decisions
- Product Description stays classified plain **Bank-pattern OV** (Manage-Object, no navigator) —
  the PR #441 conversion did not change this classification, only the RF implementation shape.
- Reused T2's existing consolidated keywords as-is (`Insert/Update Object From Properties`,
  `Verify Object Insert Exists/Form Record/Found/Does Not Exist/Removed`, `Find Object Record`) —
  no edits to `resources/manage_object.resource` or `resources/common.resource`.
- The Playwright driver (`playwright/ec_iud_product_description.py`) and `investigation/
  financial_objects_recon.py` were deliberately left untouched by PR #441 and by this backfill —
  Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md` (2026-08-27) waives items 4/5 (Playwright
  driver + `investigation/`) for Bank-/Area-pattern work permanently (Universal Screen Engine
  replaces that role); the pre-existing bundle here is kept as historical reference, not rebuilt.
- Isolated sparse-checkout clone under `Workplaces/product_description/` was used for the
  original PR #441 build, own feature branch, synced with `origin/master` before push (no
  conflicts — no sibling batch-4 PR had merged yet). This backfill used its own isolated
  worktree (`C:/tmp/wt-productdesc-backfill`), branch
  `docs/product-description-backfill-artifacts`, same discipline.

## Evidence
- PR #441 (2026-08-23): cited live 5/5, full-tree dryrun 740/740 (baseline 739/739), robocop 9
  issues (4 VAR02 + 5 DOC02), grid-filter keyword fired (5 hits), DB self-clean 0/0 (fresh
  connection) — see the PR body (`gh pr view 441`) for the exact commands/output cited.
- This backfill session (2026-08-28):
  - `robot --dryrun tests/Configuration/Assets/Financial_Objects/product_description_iud.robot`
    → **5/5 PASS**.
  - `EC_HEADLESS=true robot --outputdir .../Product_Description/evidence
    tests/.../product_description_iud.robot` → **5/5 PASS** clean, first attempt (no flake).
  - DB self-clean: `libraries.DbVerify.fetch_object("OV_PRODUCT_NODE_ITEM", "AUTOTEST_PD")` →
    `None` both before AND after this session's live run (fresh oracledb connection).
  - `py -m robocop check` on `product_description_page.resource` + `product_description_iud.robot`
    → **9 issues** (4 VAR02 + 5 DOC02) — exact parity with PR #441's own cited count, no drift.
  - `grep -c 'name="Find Product Description Row By Filter"' output.xml` (this session's own
    evidence `output.xml`) → **5 hits** — matches PR #441's cited count.
  - Full-tree dryrun (`robot --dryrun tests/`, this session) → **883/883 PASS** (not committed
    raw — per this backfill task's size guidance, only the pass count is cited here; the repo has
    grown since PR #441's 740/740 baseline as later batches were merged).
  - `py scripts/check_bundle_hygiene.py` (repo-wide) → **PASS** — "no hardcoded creds (R16), pure
    ASCII (R20), no CHECKLIST/VERIFY-REPORT contradictions, doc rows match declared families"
    (167 bundles + 272 recon scripts scanned; the one WARN reported belongs to Contract Area's
    `investigation/`, unrelated to this screen).
  - Evidence artifacts: `evidence/log.html`, `evidence/output.xml`, `evidence/report.html`,
    per-TC step screenshots (this session's clean 5/5 run), alongside the pre-existing 2026-06-11
    Playwright evidence (`evidence/product_description_0[1-8]_*.png`,
    `product_description_results.json`).
