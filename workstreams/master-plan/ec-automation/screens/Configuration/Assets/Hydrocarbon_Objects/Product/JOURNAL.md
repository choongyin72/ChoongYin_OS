# JOURNAL — Product IUD

_Screen: Configuration > Assets > Hydrocarbon Objects > Product (BF CO.0007, class PRODUCT). Plain
OV (Bank family), date-effective. View `OV_PRODUCT`._
_This JOURNAL is a Batch 12 backfill (2026-08-28) of PR #485 (merged 2026-08-24) — the bundle was
built under the 2026-08-23/26 lean-waiver rule that skipped SOW/JOURNAL/evidence/KB for brand-new
Bank-shaped screens; that waiver was retired 2026-08-27 (`docs/IUD-DELIVERABLE-CHECKLIST.md`
Section H), so this documents what PR #485 actually did, from its own PR body and commits._

## Built (PR #485, 2026-08-24)
- RF-only Insert/Update/Find/Delete automation for Product — genuinely new, zero prior automation
  existed for this class.
- `pageobjects/Configuration/Assets/Hydrocarbon_Objects/product_page.resource` (T3, new).
- `tests/Configuration/Assets/Hydrocarbon_Objects/product_iud.robot` (suite, new, 5 TCs).
- `testdata/product_{insert,update,form_verify,grid_verify}.properties` (new).
- `resources/credentials.py` — additive `PRODUCT_EC_USER`/`PRODUCT_EC_PASS` (no existing entries
  touched).
- Registry row (`docs/ec_screen_registry.md`) and scorecard row (`docs/automation-scorecard.md`) —
  new rows, no prior entry existed.
- Built via the `ec-bank-pattern-new-screen` skill (Phase 3 batch, `tmp/phase3_shared_findings.md`).

## Done well
- DB metadata resolved BEFORE any build step (`resolve_ec_screen.py`: `CLASS_TYPE=OBJECT`,
  `TIME_SCOPE_CODE=VERSIONED`, base table `PRODUCT`, view `OV_PRODUCT`) plus a live scan
  (`scan_ec_screen.py`) confirming the plain manage-object shape — no field/label was assumed from a
  sibling screen (matches the repeat-offence-2026-08-17 rule of checking the screen's own recon
  first, never extrapolating from a similar-looking screen).
- Correctly identified and threaded the screen-prefixed "Product Code"/"Product Name" labels
  (`code_label=${PRODUCT_CODE_LABEL}` on every T2 call) instead of assuming the generic "Code"/"Name"
  Bank uses.
- Correctly identified that Product Type/ERP Code exist on Insert's `objectForm` but are absent from
  `updateAttributes` — confirmed live, not assumed from Insert's field set.
- Live run: **5/5 pass, first attempt** (TC01–TC05). No shared T1/T2 files (`manage_object.resource`,
  `common.resource`) touched — thin, config-only T3 build reusing the existing Bank-family engine.
- Self-clean confirmed via a **fresh** oracledb connection (separate from the one used to run the
  test) after the run: 0 residual rows across `PRODUCT` (base), `PRODUCT_VERSION`, and `OV_PRODUCT`
  (view, `CODE` column).
- Grid-filter wiring confirmed fired: `grep -c "Find Object Row By Filter" output.xml` = 15 hits.

## Done wrong / lessons
- None disclosed in PR #485's body — first-attempt 5/5 pass with no reported flake, wrong
  classification, or shared-file regression. (Recorded here explicitly, per the backfill workorder's
  instruction not to smooth over gaps — there is no gap to report for this PR.)
- Retrospectively (owner decision 2026-08-27): the lean-waiver rule this screen was built under is
  now retired — PR #485 itself did nothing wrong under the rule that existed at the time, but the
  missing SOW/JOURNAL/evidence/KB map are exactly what this backfill batch restores.

## Blockers → resolution
- No hard blockers. Optional dropdown fields (Hydrocarbon Component, Product Group, Product Type,
  ERP Code) had no live-verified valid option values for AUTOTEST data, so they were deliberately
  left unset rather than guessed — not a blocker, a scoped-out decision (see Decisions below).

## Decisions
- Left Hydrocarbon Component / Product Group / Product Type / ERP Code unset (optional dropdowns,
  no live-verified valid AUTOTEST option value) — matches the "IUD fill only needed fields" rule;
  only Product Code / Product Name / Start Date (mandatory) plus Description / Sort Order (extra
  plain-text fields, added so Update has real values to change) are filled.
- Reused `${OV_MANAGE_OBJECT_TABLE}` from T2 for the grid id rather than re-hardcoding the literal
  string on Product's own T3.
- Kept the fixed test code `AUTOTEST_PRODUCT` (confirmed absent from `PRODUCT.OBJECT_CODE` before
  wiring in) rather than a per-run generated unique code — every run must complete TC05 (Delete) to
  keep the code reusable.

## Evidence
- Original PR #485: live 5/5 (`EC_HEADLESS=true`), first attempt; fresh-connection DB self-clean
  0/0/0 residual across `PRODUCT`/`PRODUCT_VERSION`/`OV_PRODUCT`; grid-filter grep = 15 hits.
- Batch 12 backfill re-run (2026-08-28): see `evidence/` in this bundle and `CHECKLIST.md` for the
  dryrun + live re-confirmation captured during this documentation pass.
