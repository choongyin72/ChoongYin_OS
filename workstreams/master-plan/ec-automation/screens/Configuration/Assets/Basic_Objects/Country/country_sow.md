# EC Screen IUD Operation Test — Statement of Work (SOW)
**Project:** EC Web App System Test (local sandbox)
**Task:** EC Screen Insert/Update/Delete (IUD) Automation — Country
**Author:** Choong-Yin Lee / Claude
**Original build date:** 2026-06-11 (v1.0, hardcoded-field-id + Playwright reference)
**Bank-pattern conversion:** PR #428, merged 2026-08-23 (Batch 2 of 5, `ec-bank-pattern-converter`)
**Documentation backfill:** 2026-08-28 (Batch 6, lean-waiver retirement — see
`docs/lean-deliverable-backfill-workorder.md`)
**Version:** 2.0 — Bank-pattern conversion, live + DB-verified, documentation backfilled

---

## 1. REQUIREMENT
Automate Insert / Update / Delete on the **Country** screen and prove, at DB level,
that EC creates, modifies and truly deletes the record. Constraints: NEVER touch
existing data; test data uses the fixed code `AUTOTEST_COUNTRY` (Bank/State convention,
confirmed free in `OV_COUNTRY` before use); environment = local EC sandbox, user sysadmin.

| Operation | Pass condition | Status |
|---|---|---|
| INSERT | AUTOTEST row in grid AND present in `OV_COUNTRY` | PASS |
| UPDATE | Name change visible in grid row + form round-trip | PASS |
| FIND | Row locatable via explicit grid-filter wiring | PASS |
| DELETE | End Date = Start Date -> gone from grid AND absent in `OV_COUNTRY` | PASS |
| CLEANUP | zero leftover test data (fresh-connection DB re-read) | PASS |

## 2. DESIGN

### 2.1 Screen classification
| Property | Value |
|---|---|
| Treeview path | Configuration > Assets > Basic Objects > Country |
| Screen type | Manage Object (OV), **plain — no navigator dropdown/date** |
| Pattern | **Bank pattern** (label-driven, properties-file-driven, T2-consolidated) — matches
`bank_page.resource`/`berth_page.resource`'s shape, NOT Area's OV-GM navigator shape |
| List/grid id | `manage_object_nav_nav:form:T_data` (reused as `${OV_MANAGE_OBJECT_TABLE}`) |
| DB view (ground truth) | `OV_COUNTRY` |
| Delete semantics | End Date = Start Date (true delete) |

### 2.2 Screen-specific notes
- Field labels are **screen-prefixed**: "Country Code" / "Country Name" (NOT the generic
  "Code"/"Name" that Bank/Object List use) — confirmed live 2026-08-23 via a field-label recon
  script dumping every ECCell label in both `objectForm` (Insert, 14 labels) and
  `updateAttributes` (Update, 10 labels).
- Only **Country Code / Country Name / Start Date** are `MandatoryCellStyle`-confirmed mandatory
  (Start Date is Insert-only, not present in `updateAttributes`). Master System Code/Name, Local
  Name, Dialing Code, Comments, Description, Nationality name are all optional and omitted
  (IUD-fill-only-needed-fields convention).
- Explicit grid-filter wiring (`Find/Clear Country Row By Filter` -> shared T2
  `Find/Clear Object Row By Filter`) included from the start of the Bank-pattern conversion,
  matching Account/Bank/State's convention (owner, 2026-08-22).
- `${COUNTRY_DEL_ENDDATE}` objectdates field id reused unmodified from the framework-invariant
  Bank/State/Account row layout (Start Date C:1, End Date label C:2, End Date input C:3) — not
  independently re-verified per the batch's shared ground rules.

### 2.3 DOM reference
Pre-conversion (2026-06-11):
```
INSERT objectForm : Code  tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
                    Name  tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
                    Start tab:tabPanel:objectForm:form:G:0:R:5:C:1:da_input
UPDATE            : Code  tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in (guard)
                    Name  tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
DELETE objectdates: End   tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
```
Post-conversion (PR #428, 2026-08-23) — label-driven, no hardcoded field ids for Insert/Update;
only the DELETE objectdates field id is still a raw id (`${COUNTRY_DEL_ENDDATE}` =
`tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input`, reused from Bank/State/Account).

### 2.4 Test data
| Field | Value |
|---|---|
| Country Code | `AUTOTEST_COUNTRY` (fixed code, confirmed free in `OV_COUNTRY` before wiring in) |
| Country Name / Country Name (update) | `AUTOTEST Country` / `AUTOTEST Country UPDATED` |
| Start = End (delete) | `2000-01-01` |

Source properties files: `testdata/country_insert.properties`, `country_update.properties`,
`country_form_verify.properties`, `country_grid_verify.properties`.

## 3. DEVELOPMENT — what it took

### 3.1 Original build (2026-06-11)
Recon'd via the (now-superseded) `investigation/` scripts; pure reuse of the OV pattern (grid id,
navigator GO, End=Start delete) established by Bank — worked first time on the live run.

### 3.2 Bank-pattern conversion (PR #428, 2026-08-23) — real narrative from the PR body
Rebuilt the Country screen IUD suite from the older hardcoded-field-id pattern to the
label-driven, properties-file-driven, T2-consolidated "Bank pattern" already used by
Bank/State/Object List/Account/Cost Centre, including the explicit grid Find/Clear Row By
Filter wiring **from the start** — this was Batch 2 of 5 parallel screen conversions
(Country/County/Regulatory Permits/Currency/VAT Code). Field labels ("Country Code"/"Country
Name") and mandatory scope were confirmed via a live RF field-label recon script BEFORE building
(not assumed from a sibling screen), then the recon script was deleted (throwaway, per repo
convention). No shared T1/T2 file (`resources/common.resource`/`resources/manage_object.resource`)
was touched — the existing `${code_label}` parameter (added on State's PR) was reused unchanged.

## 4. TEST EXECUTION
| Run | Mode | Result | When |
|---|---|---|---|
| RF dryrun (structure) | headless | 5/5 PASS | 2026-08-23 (PR #428) + re-confirmed 2026-08-28 |
| RF live batch | headless | 5/5 PASS, DB-verified | 2026-08-23 (PR #428) + re-confirmed 2026-08-28 |
| Grid-filter wiring | headless | 5 `Find Country Row By Filter` hits in output.xml | 2026-08-23 + 2026-08-28 |
| robocop (2 RF files) | — | 9 issues (4 VAR02 + 5 DOC02), same baseline as State exemplar | 2026-08-23 + 2026-08-28 |
| Playwright reference run (superseded, pre-conversion) | headless | see `evidence/country_results.json` | 2026-06-11 |

Evidence: `evidence/` (2026-06-11 Playwright screenshots, preserved) +
`evidence/rf_backfill_2026-08-28/` (this backfill's RF re-run: log.html, output.xml, 26 per-step
screenshots, results summary).

## 5. DELIVERABLES
| Deliverable | Where |
|---|---|
| RF suite (maintained test) | `tests/Configuration/Assets/Basic_Objects/country_iud.robot` |
| RF page object (Bank pattern) | `pageobjects/Configuration/Assets/Basic_Objects/country_page.resource` |
| Properties files | `testdata/country_{insert,update,form_verify,grid_verify}.properties` |
| Playwright reference (superseded, kept for history) | `playwright/ec_iud_country.py` (+ `_shared/iud_engine.py`) |
| Recon trail (pre-conversion) | `investigation/` |
| Registry row | `workstreams/master-plan/ec-automation/docs/ec_screen_registry.md` (line ~43) |
| Scorecard row | `docs/automation-scorecard.md` |

## 6. LESSONS LEARNED (carried forward from both builds)
1. **Silent reject = mandatory field**: a Save that produces no row + the banner
   "Required fields are empty: <field>" — fill the named dropdown.
2. **Code/Name rows are NOT always R0/R1** — recon the `:C:0:la` labels first
   (State/County have Master System rows above them).
3. **Screen-prefixed labels are not universal** — Country uses "Country Code"/"Country Name"
   while Bank/Object List use the generic "Code"/"Name"; always confirm live, never assume from
   a sibling screen (same lesson class as the CLAUDE.md Contract Inventory / Tract incidents).
4. **The UI can lie**: groupmodel grids redraw lazily; ALWAYS verify at the DB — this is why
   `Verify Object Removed` asserts `Code Should Be Absent In View OV_COUNTRY`, not just the grid.
5. **Reuse the shared T2 grid-filter keyword explicitly** rather than relying on the implicit
   3s-timeout fallback in `Select Object Row` (owner, 2026-08-22).
