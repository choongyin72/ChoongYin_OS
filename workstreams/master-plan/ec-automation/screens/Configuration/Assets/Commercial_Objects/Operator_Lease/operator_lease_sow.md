# EC Screen IUD Operation Test — Statement of Work (SOW)
**Project:** EC Web App System Test (local sandbox)
**Task:** EC Screen Insert/Update/Delete (IUD) Automation — Operator Lease
**Author:** Choong-Yin Lee / Claude Fable 5
**Date:** 2026-06-12
**Version:** 1.0 — COMPLETE (RF suite + Playwright reference, live + DB-verified)

---

## 1. REQUIREMENT
Automate IUD on the **Operator Lease** screen with DB-level proof. Constraints: NEVER touch
existing data; test codes `AUTOTEST_OPL_<timestamp>`; local sandbox, user sysadmin.

| Operation | Pass condition | Status |
|---|---|---|
| INSERT | AUTOTEST row in grid AND present in `OV_OPERATOR_LEASE` | PASS |
| UPDATE | Name change visible in grid row | PASS |
| DELETE | End=Start -> gone from grid AND absent in `OV_OPERATOR_LEASE` | PASS |

## 2. DESIGN
| Property | Value |
|---|---|
| Treeview path | Configuration > Assets > Commercial Objects > Operator Lease |
| Screen type | Manage Object (OV) |
| List/grid id | `manage_object_nav_nav:form:T_data` |
| DB view | `OV_OPERATOR_LEASE` |
| Delete semantics | End Date = Start Date (true delete) |

### DOM reference (rows derived from recon LABELS)
```
INSERT: Code  tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
        Name  tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
        Start tab:tabPanel:objectForm:form:G:0:R:3:C:1:da_input
UPDATE: Code  tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in (guard)
        Name  tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
DELETE: End   tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
```

### Test data
Code `AUTOTEST_OPL_<timestamp>` | Name `Operator Lease <code>` (+` UPD`) | Start=End `2003-01-01`
(section-wide 2003-01-01: reference dropdowns are effective-date-filtered — the object
Start Date acts as a version; seed objects start 2003-01-01)

## 3. DEVELOPMENT
Generated DATA-DRIVEN from the section recon (`investigation/commercial_objects_recon.py`).
Banner-discovered mandatory dropdowns resolved in fix round 1; Field links into its groupmodel via the Geo Area dropdown (= navigator Area).

## 4. TEST EXECUTION
| Run | Mode | Result |
|---|---|---|
| RF dryrun | headless | PASS |
| RF live | headless | TC01–TC04 4/4 PASS, DB-verified |
| Playwright reference run | headless | see `evidence/operator_lease_results.json` |

## 5. DELIVERABLES
RF suite + page object under `tests|pageobjects/.../Commercial_Objects/operator_lease_*`,
this bundle, registry row in `docs/ec_screen_registry.md`.

---

## 6. BANK-PATTERN CONVERSION (PR #436, 2026-08-23) — supersedes Sections 2-4 above

_Added 2026-08-28 (deliverable backfill, `docs/lean-deliverable-backfill-workorder.md` Batch 6,
first Bank-pattern wave), modeled on `screens/Configuration/Assets/Financial_Objects/Bank/JOURNAL.md`'s
structure. The 2026-06-12 sections above are kept as history — the DOM ids/test-code convention they
describe (per-run `AUTOTEST_OPL_<timestamp>`) were replaced by PR #436._

**Pattern:** Bank pattern — converted from the older hardcoded-field-id, no-properties-file pattern to
the label-driven, properties-file-driven, T2-consolidated Bank/State/Country pattern (Batch 3 of 5:
Customer/Field Group/Licence/MMS Lease/Operator Lease, 5 parallel isolated clones), with grid-filter
wiring included from the start.

**Grid / cell shape (live-verified 2026-08-23):**
- Grid `manage_object_nav_nav:form:T_data` (T2's `${OV_MANAGE_OBJECT_TABLE}` constant, reused not
  re-hardcoded). Confirmed nav-free live — the top Date+GO bar is the same universal as-at-date filter
  Bank also has, not a blocking mandatory nav requirement (verified via a direct side-by-side
  screenshot compare against the live Bank screen).
- Field labels are **screen-prefixed**: "Operator Lease Code"/"Operator Lease Name" (same convention
  as Country/State), NOT the generic "Code"/"Name" Bank/Object List use. `objectForm` (Insert): 7
  `ECCell` labels, mandatory = Code/Name/Start Date only. `updateAttributes` (Update): 3 labels,
  mandatory = Code/Name only, Description optional.
- The grid held 0 real Operator Lease rows in this environment at conversion time, so
  `updateAttributes` labels were confirmed via a live throwaway Insert+Delete round-trip
  (`RECON_OL_TMP`, self-cleaned, DB re-checked empty after) rather than off an existing row.
- Grid columns confirmed live: Operator Lease Code / Operator Lease Name / Start Date / End Date.
- Delete: `objectdates` End Date = Start Date (true delete), field id
  `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input`, matching Bank/State/Country/Account's
  already-proven row layout.

**Test data (current, since PR #436):** fixed test code `AUTOTEST_OPERATOR_LEASE` (not the old
per-run `AUTOTEST_OPL_<timestamp>`) — confirmed absent from `OV_OPERATOR_LEASE` via a fresh
`oracledb` connection before first use (2026-08-23), and re-confirmed absent both before and after
this backfill's own live re-run (2026-08-28). Insert: Operator Lease Code =
`AUTOTEST_OPERATOR_LEASE`, Operator Lease Name = `AUTOTEST Operator Lease`, Start Date =
`2000-01-01`. Update: Operator Lease Name -> `AUTOTEST Operator Lease UPDATED`.

**Verification at PR #436 merge:** full `tests/` dryrun 735/735 pass; robocop 9 issues (4 VAR02 + 5
DOC02), identical in kind/count to the established Bank/State/Country baseline; `Find Operator Lease
Row By Filter` confirmed fired 5 times via `output.xml` grep (Update/Find/Verify-Insert-Exists/
Verify-Found/Delete); live RF 5/5 pass (TC01-TC05); fresh-connection DB self-clean 0 residual.

**Deliverables (current):**
- T3: `pageobjects/Configuration/Assets/Commercial_Objects/operator_lease_page.resource`
- Suite: `tests/Configuration/Assets/Commercial_Objects/operator_lease_iud.robot`
- Testdata: `testdata/operator_lease_{insert,update,form_verify,grid_verify}.properties`
- Playwright driver (pre-existing, permanently waived for further Bank-pattern work per
  `docs/IUD-DELIVERABLE-CHECKLIST.md` Section H): `playwright/ec_iud_operator_lease.py`,
  `investigation/{commercial_objects_recon.py,probe_com_rejects.py}` — untouched by this backfill.
- This SOW, `README.md`, `JOURNAL.md`, `evidence/backfill_2026-08-28/`, `CHECKLIST.md` (added/
  refreshed by the 2026-08-28 deliverable backfill, Batch 6).
