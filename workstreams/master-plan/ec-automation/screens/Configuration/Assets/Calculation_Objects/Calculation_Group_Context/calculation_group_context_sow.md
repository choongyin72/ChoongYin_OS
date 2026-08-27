# SOW - Calculation Group Context IUD

## Classification
- **Screen:** Configuration > Assets > Calculation_Objects > Calculation Group Context (BF_CODE **CO.0245**)
- **Type/pattern:** OV (Manage-Object, `manage_object_nav`) - date-effective; plain **Bank-pattern** (no mandatory
  navigator dropdowns; full Bank-pattern shape as of PR #455, batch 7, 2026-08-23)
- **DB view:** `OV_CALC_GRP_CONTEXT` (versioned); key `CODE`
- **Grid id:** `manage_object_nav_nav:form:T_data` (reused via shared T2 constant `${OV_MANAGE_OBJECT_TABLE}`,
  threaded through the T3 as `${CALCULATION_GROUP_CONTEXT_TABLE}`)
- **Delete:** End Date = Start Date -> row leaves `OV_CALC_GRP_CONTEXT`

## Nav / grid / cells
- **Open:** menu search "Calculation Group Context" -> `label.tv-link`. Navigator = single **Date + GO**; grid needs GO
  (`Open Calculation Group Context Screen` = `Open EC Screen` + `Apply Navigator`).
- **Grid:** shared T2 `${OV_MANAGE_OBJECT_TABLE}`, with explicit grid-filter wiring added in PR #455:
  `Find Calculation Group Context Row By Filter` / `Clear Calculation Group Context Row Filter` delegate to the
  shared T2 `Find Object Row By Filter` / `Clear Object Row Filter` on the Code column.
- **NO hardcoded field ids** - resolved BY LABEL via T2 `Fill OV * By Label` / `OV Field Id By Label` (kept from the
  original 2026-07-26 build, not thrown away by the PR #455 conversion):
  - **Insert (objectForm):** mandatory `Calculation Group Context Code`, `Calculation Group Context Name`,
    `Start Date`. Optional dropdowns (`Calculation Group Object Class`, `Calculation Group List Class`) filled
    `__FIRST__` via properties, not mandatory.
  - **Update (updateAttributes):** `Calculation Group Context Name` (Code read-only; loaded-check via
    `OV Field Id By Label` on `Calculation Group Context Code`).
  - **Delete (objectdates):** `End Date` = Start Date.
- **Mandatory fields:** Code, Name, Start Date. No mandatory navigator scope value (plain Date+GO nav).

## Test data
- **Original build (2026-07-26):** `AUTOTEST_CGC_<timestamp>` unique per run.
- **Current (PR #455, batch 7, 2026-08-23):** **fixed** test code `AUTOTEST_CGC_BANK` (matching Bank's own
  fixed-code convention), confirmed absent from `OV_CALC_GRP_CONTEXT` before being wired in; every run must
  complete TC05 (delete) so the code stays free for the next run. Driven by
  `testdata/calculation_group_context_{insert,update,form_verify,grid_verify}.properties`. Start/End =
  `2000-01-01`. Dedicated credentials `CALCULATION_GROUP_CONTEXT_EC_USER`/`_PASS` (added in
  `resources/credentials.py`, additive only). Never touches real rows.

## Dev story
Recon-first (DB `CLASS_TYPE=OBJECT` => OV; live form) -> plain Bank-layout OV, no mandatory dropdowns. Built
label-driven on the shared engine + T2, zero engine changes (2026-07-26 original build): Playwright driver 7/7;
RF T3+suite label-driven -> live 4/4; `verify_screen.py` OVERALL PASS.

**PR #455 (batch 7, 2026-08-23)** then brought the screen up to the full Bank-pattern shape used by
`bank_page.resource`/`customer_page.resource`: properties-file-driven Insert/Update/Verify, explicit grid-filter
wiring (`Find Calculation Group Context Row By Filter`), a 5-TC per-TC login/logout suite (added TC04 Find), and
the fixed test code `AUTOTEST_CGC_BANK` - added on top of the pre-existing label-driven `Fill OV Field By Label`
mechanics, which were kept rather than rewritten. Live 5/5 pass; DB self-clean verified via a fresh oracledb
connection (`AUTOTEST_CGC_BANK` count = 0); grid-filter wiring confirmed fired via `output.xml` grep
(`Find Object Row By Filter`/`Filter Grid Text Column By Value` = 23 hits). No shared T1/T2
(`resources/manage_object.resource`/`resources/common.resource`) changes - batch 7 hard rule. `robot --dryrun`
on the full `tests/` tree: 753/753 pass at the time of the PR.

## Lessons / known risks
- Optional dropdowns skipped (none mandatory) - both before and after the PR #455 conversion.
- Delete uses the engine's `wait_for_row_absent` equivalent (async grid redraw) via the shared T2.
- The Code field's label on this screen is NOT the generic "Code" (unlike Bank) - it is "Calculation Group
  Context Code", threaded through every T2 call as `code_label=${CALCULATION_GROUP_CONTEXT_CODE_LABEL}`.
