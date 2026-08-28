# SOW - Calculation Context IUD

_Updated 2026-08-28 under `docs/lean-deliverable-backfill-workorder.md` (Batch 9) to reflect the
screen's CURRENT automation shape after its full Bank-pattern conversion (PR #456, 2026-08-23) and
subsequent pure-screen-verify alignment fix (PR #514, 2026-08-25). Original SOW (2026-07-26) described
the pre-conversion partial label-driven build; this revision does not invent new facts, it restates
the real current state pulled from those two PR bodies + the live `.robot`/`.resource` files._

## Classification
- **Screen:** Configuration > Assets > Calculation_Objects > Calculation Context (BF_CODE **CO.1059**)
- **Type/pattern:** OV (Manage-Object, `manage_object_nav`) - date-effective; plain Bank-family
  (no mandatory navigator dropdown beyond the universal Date + GO bar)
- **DB view:** `OV_CALC_CONTEXT` (versioned); key `CODE`
- **Delete:** End Date = Start Date -> row leaves `OV_CALC_CONTEXT`

## Nav / grid / cells
- **Open:** menu search "Calculation Context" -> `label.tv-link`. Navigator = single **Date + GO**;
  grid needs GO (`Apply Navigator`) to load - confirmed no default rows on open.
- **Grid:** shared T2 `${OV_MANAGE_OBJECT_TABLE}` (= `manage_object_nav_nav:form:T_data`).
- **NO hardcoded field ids** - resolved BY LABEL via T2 `Fill OV * By Label` / `OV Field Id By Label`:
  - **Insert (objectForm):** `Calc Context Code`, `Calc Context Name`, `Start Date` (mandatory);
    `Description`, `Comments` optional but filled by the suite's test data; End Date left blank.
  - **Update (updateAttributes):** `Calc Context Name`, `Description`, `Comments` (Code read-only;
    Start/End Date live only in objectdates, not updateAttributes - confirmed by the live
    field-inventory scan on 2026-08-23).
  - **Delete (objectdates):** `End Date` = Start Date, hardcoded field id
    `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (independently live-verified on this screen,
    2026-08-23, not just carried over from Bank's precedent).

## Test data
- Fixed code `AUTOTEST_CALCCTX` (matches Bank's convention; confirmed free in `OV_CALC_CONTEXT` before
  first use, 2026-08-23). Start/End = `2000-01-01`. Driven by four properties files:
  `testdata/calculation_context_{insert,update,form_verify,grid_verify}.properties`.

## Dev story (real history, pulled from PR bodies - not invented)
- **2026-07-26 (PR #214):** original OV IUD build - generator-scaffolded, label-driven, on the shared
  engine + T2. Playwright driver 7/7, RF T3+suite live 4/4 (TC01-04, no Find TC). `verify_screen.py`
  OVERALL PASS.
- **2026-08-23 (PR #456, Batch 7 of the Bank-pattern conversion project):** brought the screen up to
  FULL Bank-pattern parity on top of that partial label-driven build - added properties-file-driven
  Insert/Update (`testdata/calculation_context_*.properties`), explicit
  `Find/Clear Calculation Context Row By Filter` grid-filter wiring (Update/Find/Verify-Found/Delete),
  a dedicated `CALC_CONTEXT_EC_USER`/`CALC_CONTEXT_EC_PASS` credential pair, per-TC login/logout on one
  browser, and TC04 Find (5-TC total). Live 5/5; robocop clean; full-tree dryrun 753/753; DB self-clean
  0 residual via a fresh connection; grid-filter keyword confirmed fired via output.xml grep. No shared
  T1/T2 file changes needed - screen genuinely Bank-shaped.
- **2026-08-25 (PR #514, "remove inline DB-verify from 3 remaining Bank-pattern suites"):** a Reviewer
  sweep (Issue #504) found this suite still had a leftover screen-local
  `Calculation Context Should Exist In DB` keyword + its TC02 call, plus 5 direct
  `Field Should Equal In View` calls across TC02/TC03 - a deviation from Bank's owner-requested
  pure-screen-only verification convention (2026-08-18), same class as DOA Credit Limit (PR #503) and
  Document Template (PR #505). Removed; coverage unchanged since T2's
  `Verify Calculation Context Record Exists/Updated` already compares the same fields on-screen.
  Re-verified live 5/5, full-tree dryrun 841/841, DB self-clean 0 residual.

## Lessons / known risks
- Optional dropdowns skipped (none mandatory). Delete uses engine `wait_for_row_absent` (async redraw).
- The 2026-08-25 fix is the concrete lesson worth carrying forward: a "Bank-pattern conversion" PR can
  still leave inline DB-verify residue if the original pre-conversion suite had its own bespoke DB
  keyword - always re-check a converted suite against Bank's pure-screen-verify convention, not just
  its structural shape (5-TC, filter wiring, properties files).
