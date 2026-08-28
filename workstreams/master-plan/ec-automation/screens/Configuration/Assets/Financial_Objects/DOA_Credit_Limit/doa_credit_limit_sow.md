# EC Screen IUD Operation Test — Statement of Work (SOW)
**Project:** EC Web App System Test (local sandbox)
**Task:** EC Screen Insert/Update/Delete (IUD) Automation — DOA Credit Limit
**Author:** Choong-Yin Lee / Claude Fable 5
**Date:** 2026-06-11
**Version:** 1.0 — COMPLETE (RF suite + Playwright reference, live + DB-verified)

---

## 1. REQUIREMENT
Automate IUD on the **DOA Credit Limit** screen with DB-level proof. Constraints: NEVER touch
existing data; test codes `AUTOTEST_DOA_<timestamp>`; local sandbox, user sysadmin.

| Operation | Pass condition | Status |
|---|---|---|
| INSERT | AUTOTEST row in grid AND present in `OV_DOA_CREDIT_LIMIT` | PASS |
| UPDATE | Name change visible in grid row | PASS |
| DELETE | End=Start -> gone from grid AND absent in `OV_DOA_CREDIT_LIMIT` | PASS |

## 2. DESIGN
| Property | Value |
|---|---|
| Treeview path | Configuration > Assets > Financial Objects > DOA Credit Limit |
| Screen type | Manage Object (OV) |
| List/grid id | `manage_object_nav_nav:form:T_data` |
| DB view | `OV_DOA_CREDIT_LIMIT` |
| Delete semantics | End Date = Start Date (true delete) |

### DOM reference (rows derived from recon LABELS, not assumed positions)
```
INSERT: Code  tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
        Name  tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
        Start tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
        Credit Limit:         tab:tabPanel:objectForm:form:G:0:R:5:C:1:in (MANDATORY text)
UPDATE: Code  tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in (guard)
        Name  tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
DELETE: End   tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
```

### Test data
Code `AUTOTEST_DOA_<timestamp>` | Name `DOA Credit Limit <code>` (+` UPD`) | Start=End `2000-01-01`

| Extra mandatory field | Test value |
|---|---|
| Credit Limit | `1000` |
| DOA Type (reference dropdown, banner-discovered) | first available option |
| Currency (reference dropdown, banner-discovered) | first available option |
| Role Name (reference dropdown, banner-discovered) | first available option |

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
| Playwright reference run | headless | see `evidence/doa_credit_limit_results.json` |

## 5. DELIVERABLES
RF suite + page object under `tests|pageobjects/.../Financial_Objects/doa_credit_limit_*`,
this bundle, and a registry row in `docs/ec_screen_registry.md`.

## 6. LESSONS (section-wide)
1. Label-driven generation beats positional assumptions (VAT Code keeps its dates at
   R1/R2 and Name at R6; Cost Object/Account Mapping insert an Alternative Code row
   into the update form).
2. Extra mandatory TEXT/checkbox fields need no user decision — safe throwaway values
   suffice (dropdowns DO need a decision; this section had none).
3. Same OV invariants as everywhere: navigator GO after save, DB as ground truth,
   End=Start true delete.

## 7. ADDENDUM (2026-08-23, PR #443) — Bank-pattern conversion (Batch 4)

**Classification confirmed unchanged:** plain OV / Manage Object, **no navigator** (only the
universal Date+GO as-at-date bar) — confirmed live 2026-08-23.

Converted the RF suite (Playwright reference above stays as-is, untouched) from the older
hardcoded-field-id pattern to the label-driven, properties-file-driven, T2-consolidated
Bank/VAT Code pattern:
- 4 TCs -> **5 TCs** (added TC04 Find), fixed test code `AUTOTEST_DOA` (was a generated/unique
  code), per-TC `Login To EC Application`/`Logout From EC Application`.
- Properties-file-driven Insert/Update:
  `testdata/doa_credit_limit_{insert,update,form_verify,grid_verify}.properties`.
- Explicit `Find/Clear DOA Credit Limit Row By Filter` grid-filter wiring into
  Update/Find/Verify-Found/Delete, wired in from the start.
- Own credentials: `DOA_CREDIT_LIMIT_EC_USER`/`_PASS` in `resources/credentials.py`.

**Fields confirmed live 2026-08-23** (raw outerHTML/`MandatoryCellStyle` dump, screen-prefixed
labels, not assumed from a sibling screen):
- `DOA Credit Limit Code` / `DOA Credit Limit Name` (screen-prefixed, not generic Code/Name).
- `DOA Type` (reference dropdown, mandatory) — literal `Amount Based` (first of 2 real options:
  Amount Based/Quantity Based).
- `Credit Limit` (mandatory numeric text, `ECNumberCell`) — test value `5000`.
- `Currency` (reference dropdown) — statically `{mandatory:false}` but a real **conditional-mandatory
  EC business rule**: a live Save without it failed with "Amount Based DOA Requires a currency"
  when DOA Type = Amount Based. `Currency=USD` (a real catalogued option, not the dropdown's first
  option ARS) added to the insert data as a result.
- `Role Name` (reference dropdown, mandatory) — literal `ANALYTICS.REPORTADMIN` (first of 33 real
  catalogued options). Re-renders as its Description (`Report Administrator`) on
  `updateAttributes` reload, not the raw code — excluded from the live-DOM round-trip form-label
  check; covered by DB ground-truth (`ROLE_ID` column) instead.

**Test evidence (PR #443, 2026-08-23):** live `EC_HEADLESS=true` run 5/5 PASS; `Find DOA Credit
Limit Row By Filter` fired 7 times (`output.xml`); fresh-connection DB self-clean = 0 residual
`AUTOTEST_DOA` rows, 0 residual `RECON_DOA_SAVE` rows, total `OV_DOA_CREDIT_LIMIT` row count back
to the original 3.

**2026-08-25 alignment fix (separate follow-up):** removed a leftover inline DB-verify keyword +
its TC02 call that violated Bank's pure-screen-only verification convention (2026-08-18); coverage
unchanged, DB ground-truth still covered by `DOA Credit Limit Should Exist/Not Exist In DB` at the
TC05/TC01 level. Re-verified live 5/5.

**2026-08-28 backfill (this bundle):** documentation/evidence backfill only, per
`docs/lean-deliverable-backfill-workorder.md` (owner decision 2026-08-27, Section H of
`docs/IUD-DELIVERABLE-CHECKLIST.md`) — added `JOURNAL.md`, `CHECKLIST.md`, refreshed `README.md`,
captured a fresh live-run evidence set, and added the KB selector map
(`ec-ui-knowledge/screens/doa_credit_limit.md`). No RF automation file was modified. Re-run this
session: dryrun 5/5, live 5/5 clean (first attempt), robocop 7 issues (same DOC02 baseline
category), DB self-clean 0 residual (fresh connection), hygiene PASS.
