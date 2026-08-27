# SOW — Product IUD (Configuration > Assets > Hydrocarbon Objects)

## Classification
- **Screen:** Product   **BF:** CO.0007   **Class:** PRODUCT   **View:** `OV_PRODUCT` (versioned)
- **Type/pattern:** plain OV (Manage-Object, Bank family) — date-effective; no navigator dropdown/
  cascade. **Genuinely brand-new build** — zero prior automation of any kind existed for this class
  before PR #485 (not a conversion of a pre-existing screen).
- Confirmed distinct via `resolve_ec_screen.py`/live scan before building from the already-automated
  siblings "Product Description" (CD.0012) and "Product Group" (RC.0053) — this is `PRODUCT_MAINTAIN`,
  a different class from both.

## Nav / grid / cells
- **Navigator:** single **Date field (optional) + GO** (`button:form:B`) — no mandatory dropdown or
  cascade. Grid stays empty until GO is clicked.
- **Grid id:** `manage_object_nav_nav:form:T_data` — reused from T2's centralized constant
  (`${OV_MANAGE_OBJECT_TABLE}` in `manage_object.resource`), confirmed live via `scan_ec_screen.py`
  (2026-08-24) rather than re-hardcoded.
- **Field labels are SCREEN-PREFIXED** — "Product Code" / "Product Name" (not the generic "Code" /
  "Name" Bank/Object List use), same convention as State/County/Country. Every T2 keyword call passes
  `code_label=${PRODUCT_CODE_LABEL}` explicitly.
- **Mandatory fields (confirmed live via `scan_ec_screen.py`, 2026-08-24):** Product Code, Product
  Name, Start Date. Hydrocarbon Component / Product Group / Product Type / ERP Code are optional
  dropdowns — left unset, no live-verified valid option values for AUTOTEST data.
- **Update form (`updateAttributes`):** Product Code read-only (guard); only Product Name /
  Description are edited. Product Type / ERP Code exist on Insert's `objectForm` but are NOT present
  on `updateAttributes` (confirmed live).
- **Delete:** End Date = Start Date via the `objectdates` row, `C:3` convention (same shape already
  documented on Bank) — `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input`.

## Test data
- Fixed test code `AUTOTEST_PRODUCT` (not a generated unique code) — confirmed absent from
  `PRODUCT.OBJECT_CODE` before wiring in; every run must complete TC05 (delete) so the code stays free
  for the next run.
- Start Date = End Date = `2000-01-01`.
- Insert: Product Name "Autotest Product", Description "Autotest product description", Sort Order
  `10` (`testdata/product_insert.properties`).
- Update: Product Name "Autotest Product UPDATED", Description "Autotest product description
  UPDATED" (`testdata/product_update.properties`).
- Separate `product_form_verify.properties` / `product_grid_verify.properties` hold the merged
  post-update expected state used by TC04's live-DOM round-trip check (independent of the DB
  assertions already run in TC02/TC03).

## Dev story (from PR #485, merged 2026-08-24T03:51:40Z)
Built via the `ec-bank-pattern-new-screen` skill (Phase 3 batch, `tmp/phase3_shared_findings.md`)
after DB metadata resolution (`resolve_ec_screen.py`: `CLASS_TYPE=OBJECT`, `TIME_SCOPE_CODE=VERSIONED`,
base table `PRODUCT`, view `OV_PRODUCT`) and a live scan (`scan_ec_screen.py`) confirming a plain
manage-object (Bank family) shape — no navigator-registry entry existed for Product before this build,
making it eligible under the stricter "zero navigator-column entries" bar used for that batch. Live
run: **5/5 pass, first attempt** (TC01 clean-state / TC02 Insert / TC03 Update / TC04 Find / TC05
Delete). Self-clean confirmed via a fresh oracledb connection: 0 residual rows across `PRODUCT` (base),
`PRODUCT_VERSION`, and `OV_PRODUCT` (view). No shared T1/T2 files (`manage_object.resource`/
`common.resource`) were touched — this was a thin, config-only T3 build reusing the existing Bank-
family engine.

## Lessons / known risks
- Do not confuse this screen with "Product Description" (CD.0012) or "Product Group" (RC.0053) when
  grepping `product_page.resource` — both siblings have their own `_page.resource`/`_iud.robot` files
  with "product" in the name.
- The screen-prefixed "Product Code"/"Product Name" labels mean every shared T2 call here must pass
  `code_label=${PRODUCT_CODE_LABEL}`; a bare default `code_label="Code"` would silently fail to find
  the field.
- Per the 2026-08-23/26 lean-waiver rule (now retired 2026-08-27 by `docs/lean-deliverable-backfill-
  workorder.md`), this screen was originally delivered WITHOUT a Playwright bundle — that omission
  is permanent (Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`: items 4/5 stay waived, the Universal
  Screen Engine is the owner-decided replacement) — only SOW/README/JOURNAL/evidence/CHECKLIST/KB map
  are being backfilled here.
