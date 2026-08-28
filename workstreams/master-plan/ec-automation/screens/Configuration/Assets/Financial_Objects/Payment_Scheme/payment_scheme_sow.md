# EC Screen IUD Operation Test — Statement of Work (SOW)
**Project:** EC Web App System Test (local sandbox)
**Task:** EC Screen Insert/Update/Delete (IUD) Automation — Payment Scheme
**Author:** Choong-Yin Lee / Claude Fable 5
**Date:** 2026-06-11
**Version:** 1.0 — COMPLETE (RF suite + Playwright reference, live + DB-verified)

---

## 1. REQUIREMENT
Automate IUD on the **Payment Scheme** screen with DB-level proof. Constraints: NEVER touch
existing data; test codes `AUTOTEST_PSCH_<timestamp>`; local sandbox, user sysadmin.

| Operation | Pass condition | Status |
|---|---|---|
| INSERT | AUTOTEST row in grid AND present in `OV_PAYMENT_SCHEME` | PASS |
| UPDATE | Name change visible in grid row | PASS |
| DELETE | End=Start -> gone from grid AND absent in `OV_PAYMENT_SCHEME` | PASS |

## 2. DESIGN
| Property | Value |
|---|---|
| Treeview path | Configuration > Assets > Financial Objects > Payment Scheme |
| Screen type | Manage Object (OV) |
| List/grid id | `manage_object_nav_nav:form:T_data` |
| DB view | `OV_PAYMENT_SCHEME` |
| Delete semantics | End Date = Start Date (true delete) |

### DOM reference (rows derived from recon LABELS, not assumed positions)
```
INSERT: Code  tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
        Name  tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
        Start tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
UPDATE: Code  tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in (guard)
        Name  tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
DELETE: End   tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
```

Note: base table was EMPTY at recon time - the DB view was verified live by TC02.

### Test data
Code `AUTOTEST_PSCH_<timestamp>` | Name `Payment Scheme <code>` (+` UPD`) | Start=End `2000-01-01`

## 3. DEVELOPMENT
Generated DATA-DRIVEN from the section recon (`investigation/financial_objects_recon.py`
output): field rows are picked by their `:C:0:la` labels, so row-shift screens and
relocated dates are handled automatically. Extra MANDATORY fields get fixed safe test
values (cleaned up by the delete).

## 4. TEST EXECUTION
| Run | Mode | Result |
|---|---|---|
| RF dryrun | headless | PASS |
| RF live batch | headless | TC01–TC04 4/4 PASS, DB-verified |
| Playwright reference run | headless | see `evidence/payment_scheme_results.json` |

## 5. DELIVERABLES
RF suite + page object under `tests|pageobjects/.../Financial_Objects/payment_scheme_*`,
this bundle, and a registry row in `docs/ec_screen_registry.md`.

## 6. LESSONS (section-wide)
1. Label-driven generation beats positional assumptions (VAT Code keeps its dates at
   R1/R2 and Name at R6; Cost Object/Account Mapping insert an Alternative Code row
   into the update form).
2. Extra mandatory TEXT/checkbox fields need no user decision — safe throwaway values
   suffice (dropdowns DO need a decision; this section had none).
3. Same OV invariants as everywhere: navigator GO after save, DB as ground truth,
   End=Start true delete.

---

## 7. ADDENDUM (2026-08-22) — Bank/State pattern conversion (PR #420)

_Backfilled 2026-08-28 under `docs/lean-deliverable-backfill-workorder.md` (owner decision
2026-08-27 retiring the 2026-08-23/26 lean waiver — Section H of
`docs/IUD-DELIVERABLE-CHECKLIST.md`). The RF work below was already built and merged in PR #420
on 2026-08-22; this addendum documents it from the PR's own body — no automation file was touched
to produce this backfill._

Sections 1-6 above describe the screen's ORIGINAL 2026-06-11 build (timestamp-generated test
code, hardcoded field IDs, Playwright-first). On 2026-08-22, as part of the same Round 2 batch as
Account/Exchange Rate Source, the RF suite was converted from that older hardcoded-field-id/
generated-code pattern to the current **Bank/State pattern**: label-driven field resolution,
properties-file-driven test data, per-TC login/logout, a **fixed** test code
`AUTOTEST_PAYMENT_SCHEME` (replacing `AUTOTEST_PSCH_<timestamp>`), delegating to the shared T2
(`resources/manage_object.resource`) and T1 (`resources/common.resource`) keywords. Landed as
**PR #420** (merged 2026-08-22), title "feat(ec-automation): Payment Scheme screen rebuilt to
Bank pattern."

Per PR #420's body:
- Live recon (throwaway, not committed) confirmed: manage-object OV, grid
  `manage_object_nav_nav:form:T_data` count=1, GO button (`button:form:B`) count=1. `objectForm`
  fields: Code, Name, Start Date, End Date, Comments, Description — only Code/Name/Start Date
  carry the mandatory-yellow background (`rgb(252, 249, 192)`); labels are the generic
  "Code"/"Name" (NOT screen-prefixed like State's "State Code"/"State Name"). No extra mandatory
  dropdown.
- `AUTOTEST_PAYMENT_SCHEME` confirmed free in `OV_PAYMENT_SCHEME` before the build (fresh
  oracledb connection, count=0, total rows in view = 0). `CODE` column confirmed
  `VARCHAR2(32)` — the 23-char test code fits with no shortening needed.
- `robocop check` on the 2 changed files: 9 issues — identical in kind/count to the
  State/Cost Centre/WBS exemplars' own baseline (VAR02 unused `${OBJ_NAME_UPD}` + 5x DOC02
  missing TC docs); zero NEW issues.
- `robot --dryrun tests/` (full tree, at the time): 724 tests, 724 passed, 0 failed.
- Live headless run of `payment_scheme_iud.robot`: 5 tests, 5 passed, 0 failed — first attempt,
  no retry needed.
- Fresh-connection DB re-read post-run: `OV_PAYMENT_SCHEME` count for `AUTOTEST_PAYMENT_SCHEME`
  = 0, total rows unchanged at 0 (self-clean confirmed).

**Files touched by PR #420** (per its own body): `payment_scheme_page.resource` (rewritten, T3),
`payment_scheme_iud.robot` (rewritten, 5 TCs), the 4 `testdata/payment_scheme_*.properties` files
(new), `resources/credentials.py` (additive — `PAYMENT_SCHEME_EC_USER`/`PAYMENT_SCHEME_EC_PASS`),
`docs/ec_screen_registry.md` (Payment Scheme row updated in place), `docs/automation-scorecard.md`
(new row appended after Company's). A minor operational detail worth recording: merging PR #420
required resolving append conflicts in `resources/credentials.py` and
`docs/automation-scorecard.md` against sibling PRs from the same batch (Cost Centre/Revenue
Order/WBS/Exchange Rate Source) that landed around the same time — both were resolved by keeping
both sides (additive credential blocks / additive scorecard rows), not by dropping either PR's
content.

**Current (post-#420) DOM/keyword facts**, superseding the stale Section 2.3 table above:
- Test code is now the **fixed** `AUTOTEST_PAYMENT_SCHEME` (was `AUTOTEST_PSCH_<timestamp>`).
- Insert/Update/Verify field access goes through the shared T2's label-resolved
  `Insert/Update/Verify Object *` keywords with `code_label=Code` — no more direct hardcoded
  field IDs in the T3.
- Grid filtering is now explicit via `Find/Clear Payment Scheme Row By Filter`, delegating to the
  shared T2 `Find/Clear Object Row By Filter` (matches Account/Bank/State/Object List's
  convention).
- Delete End Date field id unchanged: `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input`.
- Grid id unchanged: `manage_object_nav_nav:form:T_data` (GO confirmed present, count=1).
- No mandatory dropdown on this screen (confirmed live 2026-08-22) — Code/Name/Start Date are the
  only mandatory fields.

This screen is Batch 6 of `docs/lean-deliverable-backfill-workorder.md` — the first Bank-pattern
wave of the retroactive documentation/evidence backfill.
