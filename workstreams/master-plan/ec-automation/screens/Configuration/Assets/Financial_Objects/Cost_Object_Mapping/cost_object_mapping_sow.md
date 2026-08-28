# EC Screen IUD Operation Test — Statement of Work (SOW)
**Project:** EC Web App System Test (local sandbox)
**Task:** EC Screen Insert/Update/Delete (IUD) Automation — Cost Object Mapping
**Author:** Choong-Yin Lee / Claude
**Original date:** 2026-06-11 (legacy Playwright build, superseded)
**Rebuilt:** 2026-08-23, PR #442, Batch 4 of the Bank-pattern conversion project
**Backfilled:** 2026-08-28 (`docs/lean-deliverable-backfill-workorder.md`, Batch 7 — Section H of
`docs/IUD-DELIVERABLE-CHECKLIST.md` retired the 2026-08-23/26 lean waiver, requiring this SOW/
README/JOURNAL/evidence/CHECKLIST/KB-map refresh)
**Version:** 2.0 — Bank-pattern RF suite, live + DB-verified. This revision replaces the 1.0
Playwright-era content below with the current RF-only implementation's real facts (pulled from
`cost_object_mapping_page.resource`, `cost_object_mapping_iud.robot`, `docs/ec_screen_registry.md`
line 66, and PR #442's real body).

---

## 1. CLASSIFICATION
Plain **manage-object (OV)** screen, **no navigator** — Bank-pattern (not Area-pattern). Confirmed
live during PR #442's conversion: despite the "Mapping" name, this is a genuine Code/Name
manage-object OV, not a linking-only grid.

| Property | Value |
|---|---|
| Treeview path | Configuration > Assets > Financial Objects > Cost Object Mapping |
| Screen type | Manage Object (OV), no mandatory navigator |
| Grid id | `manage_object_nav_nav:form:T_data` (shared T2 constant `${OV_MANAGE_OBJECT_TABLE}`) |
| DB view | `OV_FIN_COST_OBJECT` |
| Delete semantics | End Date = Start Date (true delete) |

## 2. FORM SHAPE (confirmed live 2026-08-23, PR #442)
`objectForm` order: Code, Alternative Code, Name, Start Date, End Date, Description, Object Type,
Cost Object, Line Item Type, Company, Node, Product, Distribution Object Type, Profit Centre.

**Mandatory fields** (confirmed via `MandatoryCellStyle`-on-wrapping-`<span>`, same technique as
VAT Code/Customer): Code, Name, plus **4 mandatory reference dropdowns**:
- Object Type (options: Cost Center / Revenue Order / WBS Element)
- Cost Object — **CASCADE dropdown**, empty ("Dependent field 'Start Date' is empty" banner) until
  BOTH Start Date and Object Type are already set
- Company (literal option `Acme Chemicals` used — avoids other options with internal
  double-spaces)
- Distribution Object Type (options: Country / Delivery Point / Field / Process Train / Well)

Line Item Type / Node / Product / Profit Centre are **not mandatory** and are omitted (IUD fills
only needed fields).

Grid columns: Code, Name, Start Date (3-column, same as Bank/Account/Country).

## 3. TEST DATA
Fixed test code `AUTOTEST_CMAP` (not a per-run timestamp — confirmed absent from
`OV_FIN_COST_OBJECT` before each run). Start Date/End Date `2003-01-01` (reference-dropdown
date-scope convention). All 4 dropdown values use **real literal option text**, not `__FIRST__`
(the Batch 2 VAT Code gotcha — `__FIRST__` never resolves to literal text for the round-trip
Verify-Insert-Exists comparison): Object Type=`Cost Center`, Cost Object=`AA` (cascade-populated
once Start Date + Object Type are set), Company=`Acme Chemicals`, Distribution Object
Type=`Country`.

## 4. DEV STORY (real, from PR #442's body — not invented)
Converted from the older hardcoded-field-id/generated-code IUD suite to the label-driven,
properties-file-driven, T2-consolidated "Bank pattern" (Batch 4 of the Bank-pattern conversion
project). A live Playwright recon (`tmp/recon_com.py` + `tmp/recon_com_insert.py` +
`tmp/recon_com_cleanup.py`, deleted before the final commit) confirmed the field order, the 4
mandatory dropdowns, and the Cost Object cascade dependency before any config was written. A
throwaway `RECON_CMAP_TEST` insert+delete round-trip proved the fill order/value set actually
saves and self-cleans before the real suite was built. Result: live 5/5 PASS, DB self-clean
confirmed via a fresh `oracledb` connection (0 residual `AUTOTEST_CMAP` rows, 90 total rows
unchanged), full-tree dryrun 740/740 PASS at the time, robocop 9 issues (parity with the
established Bank baseline).

## 5. TEST EXECUTION
| Run | Mode | Result | Source |
|---|---|---|---|
| RF `--dryrun` (screen-scoped) | headless | 5/5 PASS | PR #442 body cites full-tree 740/740; this backfill's own screen-scoped re-run 2026-08-28 (5/5) |
| RF live | headless | 5/5 PASS | PR #442 body (2026-08-23, original) + this backfill's own live re-run 2026-08-28 (5/5, first attempt, no retry needed) |
| DB self-clean | fresh connection | 0 residual `AUTOTEST_CMAP`, 90 total rows unchanged | PR #442 body + this backfill's own fresh-connection check 2026-08-28 (identical result) |
| Legacy Playwright reference (2026-06-11, pre-conversion) | headless | historical only — superseded by the RF suite; kept in `playwright/`/`investigation/` for reference, not re-run by this backfill (RF is the maintained automation) |

## 6. DELIVERABLES
RF page object `pageobjects/Configuration/Assets/Financial_Objects/cost_object_mapping_page.resource`
+ suite `tests/Configuration/Assets/Financial_Objects/cost_object_mapping_iud.robot` + 4 properties
files under `testdata/` (already merged, PR #442). This bundle (SOW/README/JOURNAL/CHECKLIST/
evidence, refreshed by this backfill) + KB map `ec-ui-knowledge/screens/cost_object_mapping.md`
(new, this backfill). Registry row: `docs/ec_screen_registry.md` line 66 (added by PR #442, not
duplicated here).

## 7. LESSONS
1. A screen named "...Mapping" is not automatically a linking-only grid — live recon proved this
   is a genuine Code/Name manage-object OV (the same conclusion later reached for Account Mapping
   and Sales Order in later batches, per the registry).
2. Cascade-dependent reference dropdowns (Cost Object here) need their prerequisite fields (Start
   Date, Object Type) filled BEFORE them in the properties file — `PropertiesReader`/`Insert
   Object From Properties` fill strictly in file order.
3. Literal option text beats `__FIRST__` for any mandatory reference dropdown that gets
   round-trip-verified against the same properties file (the VAT Code gotcha, reapplied here).
