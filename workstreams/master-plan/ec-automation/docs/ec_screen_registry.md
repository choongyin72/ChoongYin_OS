# EC Screen / Class Registry

Living reference for automating EC (Energy Components) screens in this codebase.
**Consult this before automating a new screen**, and **add a row when a new screen is covered.**
The goal: derive screen facts from here + recon (not by asking), and confirm rather than ask.

> Note: this is the **Woodside Pluto** (COPS DEV) implementation. EC is a configurable
> multi-client product — As-Built docs and screen config are client-specific, so values
> here are true for this engagement, not generic EC.

---

## Screens covered

| Screen | Treeview path | Type | DB (view / table) | Navigator | Delete | List/grid id | Page object |
|---|---|---|---|---|---|---|---|
| Bank | Configuration > Assets > Financial Objects > Bank | OV | `ov_bank` | manage-object | End Date = Start Date | `manage_object_nav_nav:form:T_data` | `Configuration/Assets/Financial_Objects/bank_page.resource` |
| Equipment | Configuration > Assets > Equipment Objects > Equipment | OV | `ov_eqpm` | 5-field cascading | End Date = Start Date | `manageObject:form:T_data` | `Configuration/Assets/Equipment_Objects/equipment_page.resource` |
| MIME Type Mapping | Configuration > System > MIME Type Mapping | TV | `ctrl_mime_type_mapping` | none | physical | `mime_type_table:form:T_data` | `Configuration/System/mime_page.resource` |
| Language | Configuration > System > Language | TV | `t_basis_language` | none | physical | `table:form:T_data` | `Configuration/System/language_page.resource` |
| Validation Overview - Pluto Scarborough | Configuration > System > Validation | RUN-verify | `CTRL_CHECK_LOG` (output) | date From/To | n/a (runs validations) | `groups:form:T_data` | `Configuration/System/Validation/validation_overview_pluto_scarborough.resource` |
| Production Unit | Configuration > Assets > Basic Objects > Production Unit | OV | `OV_PRODUCTIONUNIT` | manage-object | End Date = Start Date | `manage_object_nav_nav:form:T_data` | `Configuration/Assets/Basic_Objects/production_unit_page.resource` |
| Business Unit | Configuration > Assets > Basic Objects > Business Unit | OV | `OV_BUSINESS_UNIT` | manage-object | End Date = Start Date | `manage_object_nav_nav:form:T_data` | `Configuration/Assets/Basic_Objects/business_unit_page.resource` |
| Country | Configuration > Assets > Basic Objects > Country | OV | `OV_COUNTRY` | manage-object | End Date = Start Date | `manage_object_nav_nav:form:T_data` | `Configuration/Assets/Basic_Objects/country_page.resource` |
| State | Configuration > Assets > Basic Objects > State | OV | `OV_STATE` | manage-object | End Date = Start Date | `manage_object_nav_nav:form:T_data` | `Configuration/Assets/Basic_Objects/state_page.resource` |
| County | Configuration > Assets > Basic Objects > County | OV | `OV_COUNTY` | manage-object | End Date = Start Date | `manage_object_nav_nav:form:T_data` | `Configuration/Assets/Basic_Objects/county_page.resource` |
| Region | Configuration > Assets > Basic Objects > Region | OV | `OV_REGION` | manage-object | End Date = Start Date | `manage_object_nav_nav:form:T_data` | `Configuration/Assets/Basic_Objects/region_page.resource` |
| Object List | Configuration > Assets > Basic Objects > Object List | OV | `OV_OBJECT_LIST` | manage-object | End Date = Start Date | `manage_object_nav_nav:form:T_data` | `Configuration/Assets/Basic_Objects/object_list_page.resource` (mandatory dd: Class Name) |
| Functional Area | Configuration > Assets > Basic Objects > Functional Area | OV | `OV_FUNCTIONAL_AREA` | manage-object | End Date = Start Date | `manage_object_nav_nav:form:T_data` | `Configuration/Assets/Basic_Objects/functional_area_page.resource` |
| Regulatory Permits | Configuration > Assets > Basic Objects > Regulatory Permits | OV (custom URL) | `OV_REGULATORY_PERMITS` | manage-object | End Date = Start Date | `nav:form:T_data` | `Configuration/Assets/Basic_Objects/regulatory_permits_page.resource` (mandatory dd: Regulatory Agency) |
| Area | Configuration > Assets > Basic Objects > Area | OV-GM (groupmodel) | `OV_AREA` | PU dropdown + GO (mandatory) | End Date = Start Date (+extra Apply Navigator: lazy redraw) | `manageObject:form:T_data` | `Configuration/Assets/Basic_Objects/area_page.resource` (insert sets Op Production Unit) |
| Sub Area | Configuration > Assets > Basic Objects > Sub Area | OV-GM (groupmodel) | `OV_SUB_AREA` | cascading PU→Area + GO | End Date = Start Date | `manageObject:form:T_data` | `Configuration/Assets/Basic_Objects/sub_area_page.resource` (insert sets Op PU + Op Area) |
| Object List Setup | Configuration > Assets > Basic Objects > Object List Setup | PC (parent-child setup) | `OBJECT_LIST_SETUP` (count-delta) | List Class + Object List + GO (both mandatory) | physical (Delete > Object List Item) | `tab:tabPanel:object_list_table:form:T_data` | `Configuration/Assets/Basic_Objects/object_list_setup_page.resource` |
| Account | Configuration > Assets > Financial Objects > Account | OV | `OV_FIN_ACCOUNT` | none (toolbar Refresh) | End Date = Start Date | `nav:form:T_data` | `Configuration/Assets/Financial_Objects/account_page.resource` (dd: Cost Object Type) |
| Cost Centre | Configuration > Assets > Financial Objects > Cost Centre | OV | `OV_FIN_COST_CENTER` | none (toolbar Refresh) | End Date = Start Date | `nav:form:T_data` | `Configuration/Assets/Financial_Objects/cost_centre_page.resource` |
| Currency | Configuration > Assets > Financial Objects > Currency | OV | `OV_CURRENCY` | manage-object | End Date = Start Date | `manage_object_nav_nav:form:T_data` | `Configuration/Assets/Financial_Objects/currency_page.resource` (mandatory cb: Active) |
| DOA Credit Limit | Configuration > Assets > Financial Objects > DOA Credit Limit | OV | `OV_DOA_CREDIT_LIMIT` | manage-object | End Date = Start Date | `manage_object_nav_nav:form:T_data` | `Configuration/Assets/Financial_Objects/doa_credit_limit_page.resource` (dds: DOA Type, Currency, Role Name) |
| Exchange Rate Source | Configuration > Assets > Financial Objects > Exchange Rate Source | OV | `OV_FOREX_SOURCE` | manage-object | End Date = Start Date | `manage_object_nav_nav:form:T_data` | `Configuration/Assets/Financial_Objects/exchange_rate_source_page.resource` |
| Payment Scheme | Configuration > Assets > Financial Objects > Payment Scheme | OV | `OV_PAYMENT_SCHEME` | manage-object | End Date = Start Date | `manage_object_nav_nav:form:T_data` | `Configuration/Assets/Financial_Objects/payment_scheme_page.resource` |
| Product Description | Configuration > Assets > Financial Objects > Product Description | OV | `OV_PRODUCT_NODE_ITEM` | manage-object | End Date = Start Date | `manage_object_nav_nav:form:T_data` | `Configuration/Assets/Financial_Objects/product_description_page.resource` (dds: Product, Node, Financial Code) |
| Revenue Order | Configuration > Assets > Financial Objects > Revenue Order | OV | `OV_FIN_REVENUE_ORDER` | none (toolbar Refresh) | End Date = Start Date | `nav:form:T_data` | `Configuration/Assets/Financial_Objects/revenue_order_page.resource` |
| Sales Order | Configuration > Assets > Financial Objects > Sales Order | OV | `OV_PRODUCT_SALES_ORDER` | manage-object | End Date = Start Date | `manage_object_nav_nav:form:T_data` | `Configuration/Assets/Financial_Objects/sales_order_page.resource` (dds: Company, Field) |
| VAT Code | Configuration > Assets > Financial Objects > VAT Code | OV | `OV_VAT_CODE` | manage-object | End Date = Start Date | `manage_object_nav_nav:form:T_data` | `Configuration/Assets/Financial_Objects/vat_code_page.resource` (dds: Country, VAT Type; dates at R1/R2!) |
| WBS | Configuration > Assets > Financial Objects > WBS | OV | `OV_FIN_WBS` | none (toolbar Refresh) | End Date = Start Date | `nav:form:T_data` | `Configuration/Assets/Financial_Objects/wbs_page.resource` |
| Bank Account | Configuration > Assets > Financial Objects > Bank Account | OV | `OV_BANK_ACCOUNT` | manage-object | End Date = Start Date | `manage_object_nav_nav:form:T_data` | `Configuration/Assets/Financial_Objects/bank_account_page.resource` (dds: Customer, Bank, Currency; **Start Date 2003-01-01** — see date rule below) |
| Cost Object Mapping | Configuration > Assets > Financial Objects > Cost Object Mapping | OV | `OV_FIN_COST_OBJECT` | manage-object | End Date = Start Date | `manage_object_nav_nav:form:T_data` | `Configuration/Assets/Financial_Objects/cost_object_mapping_page.resource` (dds: Object Type, Company, Distribution Object Type, Cost Object; **Start Date 2003-01-01**) |
| Account Mapping | Configuration > Assets > Financial Objects > Account Mapping | OV (custom URL) | `OV_FIN_ACCOUNT_MAPPING` | none (toolbar Refresh) | End Date = Start Date | `manageObject:form:T_data` | `Configuration/Assets/Financial_Objects/account_mapping_page.resource` — **UNPARKED 2026-06-12**: the 9-dropdown REFERENCE COMBINATION is the screen's unique key (ALT_CODE = FIN_PRODUCT_LIT_CC_STATUS_CLASS); test uses valid-and-unused `JOU_ENT_ALL_ALL_ALL_ACCRUAL_CREDIT` cloned from existing rows; Start Date 2003-01-01; slow 75-row grid → WAITING row assert |
| Company | Configuration > Assets > Commercial Objects > Company | OV | `OV_COMPANY` | manage-object | End Date = Start Date | `manage_object_nav_nav:form:T_data` | `Configuration/Assets/Commercial_Objects/company_page.resource` |
| Customer | Configuration > Assets > Commercial Objects > Customer | OV | `OV_CUSTOMER` | manage-object | End Date = Start Date | `manage_object_nav_nav:form:T_data` | `Configuration/Assets/Commercial_Objects/customer_page.resource` (texts: ERP Customer Code, Official Name; dd: Customer Group) |
| Vendor | Configuration > Assets > Commercial Objects > Vendor | OV | `OV_VENDOR` | manage-object | End Date = Start Date | `manage_object_nav_nav:form:T_data` | `Configuration/Assets/Commercial_Objects/vendor_page.resource` (texts: ERP Vendor Code, Official Name; dd: Vendor Group) |
| Licence | Configuration > Assets > Commercial Objects > Licence | OV | `OV_LICENCE` | manage-object | End Date = Start Date | `manage_object_nav_nav:form:T_data` | `Configuration/Assets/Commercial_Objects/licence_page.resource` |
| MMS Lease | Configuration > Assets > Commercial Objects > MMS Lease | OV | `OV_MMS_LEASE` | manage-object | End Date = Start Date | `manage_object_nav_nav:form:T_data` | `Configuration/Assets/Commercial_Objects/mms_lease_page.resource` |
| State Lease | Configuration > Assets > Commercial Objects > State Lease | OV | `OV_STATE_LEASE` | manage-object | End Date = Start Date | `manage_object_nav_nav:form:T_data` | `Configuration/Assets/Commercial_Objects/state_lease_page.resource` |
| Operator Lease | Configuration > Assets > Commercial Objects > Operator Lease | OV | `OV_OPERATOR_LEASE` | manage-object | End Date = Start Date | `manage_object_nav_nav:form:T_data` | `Configuration/Assets/Commercial_Objects/operator_lease_page.resource` |
| Field Group | Configuration > Assets > Commercial Objects > Field Group | OV | `OV_FIELD_GROUP` | manage-object | End Date = Start Date | `manage_object_nav_nav:form:T_data` | `Configuration/Assets/Commercial_Objects/field_group_page.resource` |
| Commercial Entity | Configuration > Assets > Commercial Objects > Commercial Entity | OV (custom URL) | `OV_COMMERCIAL_ENTITY` | optional Licence dd | End Date = Start Date | `manageObject:form:T_data` | `Configuration/Assets/Commercial_Objects/commercial_entity_page.resource` (update form: Master System rows FIRST — Code/Name at R2/R3!) |
| Company Contact | Configuration > Assets > Commercial Objects > Company Contact | OV (custom URL) | `OV_COMPANY_CONTACT` | Company dd (empty options) | End Date = Start Date | `manageObject:form:T_data` | `Configuration/Assets/Commercial_Objects/company_contact_page.resource` (dd: Company) |
| Field | Configuration > Assets > Commercial Objects > Field | OV-GM (groupmodel) | `OV_FIELD` | Area dropdown + GO (mandatory) | End Date = Start Date (+extra GO) | `manageObject:form:T_data` | `Configuration/Assets/Commercial_Objects/field_page.resource` (insert sets **Geo Area** = navigator Area — that's the groupmodel link, no 'Op Area' dd) |
| Sub Field | Configuration > Assets > Commercial Objects > Sub Field | PARKED | `OV_SUB_FIELD` | none visible | — | `manageObject:form:T_data` | **Parked 2026-06-12:** groupmodel not enabled for SUB_FIELD — inserts persist to DB but the grid can never list them (same as Production Sub Unit); suite in `tests/.../Commercial_Objects/_parked/`; 2 unreachable AUTOTEST rows remain in OV_SUB_FIELD (documented, like the PSU orphans) |
| Production Sub Unit | Configuration > Assets > Basic Objects > Production Sub Unit | EXCLUDED | `OV_PROD_SUB_UNIT` | — | — | `manageObject:form:T_data` | **Excluded 2026-06-11 (Choong-Yin):** the screen's operational groupmodel is NOT enabled in this environment, so the grid can never query/list data (inserts persist to DB but stay invisible). Do not automate until the groupmodel is turned on. |
| Transport System | Configuration > Assets > Dispatching Objects > Transport System | OV-GM (BU-gated) | `OV_TRANSPORT_SYSTEM` | Business Unit dd + GO (mandatory) | End Date = Start Date | `manageObject:form:T_data` | `Configuration/Assets/Dispatching_Objects/transport_system_page.resource` (mandatory dd: Business Unit Name = nav BU) |
| Delivery Point | Configuration > Assets > Dispatching Objects > Delivery Point | OV-GM (BU-gated) | `OV_DELIVERY_POINT` | Business Unit dd + GO (mandatory) | End Date = Start Date | `manageObject:form:T_data` | `Configuration/Assets/Dispatching_Objects/delivery_point_page.resource` (mandatory dd: Business Unit Name = nav BU) |
| Delivery Stream | Configuration > Assets > Dispatching Objects > Delivery Stream | OV-GM (BU-gated) | `OV_DELIVERY_STREAM` | Business Unit dd + GO (mandatory) | End Date = Start Date | `manageObject:form:T_data` | `Configuration/Assets/Dispatching_Objects/delivery_stream_page.resource` — **grid visibility keys on the Entry/Exit DELIVERY POINT's BU, not the stream's own BU column** (insert sets Entry Delivery Point; 2 DP-less AUTOTEST orphans documented, wiped by sandbox refresh) |
| Nomination Point | Configuration > Assets > Dispatching Objects > Nomination Point | OV-GM (BU-gated) | `OV_NOMINATION_POINT` | Business Unit dd + GO (mandatory) | End Date = Start Date | `manageObject:form:T_data` | `Configuration/Assets/Dispatching_Objects/nomination_point_page.resource` (mandatory dd: Contract Name — used 'ECP Norway 3P Gas Purchase' under nav BU ECP Norway) |
| Pipeline Segment | Configuration > Assets > Dispatching Objects > Pipeline Segment | OV-GM (BU-gated) | `OV_PIPELINE_SEGMENT` | Business Unit dd + GO (mandatory) | End Date = Start Date | `manageObject:form:T_data` | `Configuration/Assets/Dispatching_Objects/pipeline_segment_page.resource` (mandatory dd: Pipeline Name — 'TS5 Gas Pipeline' under nav BU 'TS5 BU') |
| Transport Zone | Configuration > Assets > Dispatching Objects > Transport Zone | OV-GM (BU-gated) | `OV_TRANSPORT_ZONE` | Business Unit dd + GO (mandatory) | End Date = Start Date | `manageObject:form:T_data` | `Configuration/Assets/Dispatching_Objects/transport_zone_page.resource` (mandatory dd: Transport System Name — 'TS5 Transport System' under nav BU 'TS5 BU') |
| Meter | Configuration > Assets > Dispatching Objects > Meter | OV-GM + POPUP ✅ live 4/4 (2026-06-13) | `OV_METER` | Business Unit dd + GO (also gates the popup list!) | End Date = Start Date | `manageObject:form:T_data` | `Configuration/Assets/Dispatching_Objects/meter_page.resource` — Delivery Point via NEW T1 `Pick From EC Object Popup` (resources/popup.resource; see docs/meter_popup_notes.md); Meter Type dd (Entry/Exit/Fuel/Transit); insert ORDER: date → popup → code/name → type dd → Save |
| Pipeline | Configuration > Assets > Dispatching Objects > Pipeline | PARKED 2026-06-13 | `OV_PIPELINE` | groupmodel nav + GO | End Date = Start Date | `manageObject:form:T_data` | Full OV-GM with Op/Cp/Geo parent dds (30-row form; Code/Name at R2/R3 after Latitude/Longitude!). **PARKED: the Op PU lives in the GROUPMODEL layer (ov_pipeline.op_productionunit_code = oa.OP_PU_CODE, no column on PIPELINE/PIPELINE_VERSION); insert-form Op PU dd commits visually but the group CONNECTION row is never written (object saves with NULL op-PU = invisible in every PU filter). 3 AUTOTEST_PIPE_* orphans (Mon refresh clears). Same family as PSU/Sub Field groupmodel issues — ask Choong-Yin whether PIPELINE operational groupmodel is fully enabled.** |
| Nomination Cycle | Configuration > Assets > Dispatching Objects > Nomination Cycle | TV ✅ live 4/4 (2026-06-13) | `NOMINATION_CYCLE` (code col NOM_CYCLE_CODE) | none | physical | `table:form:T_data` | `Configuration/Assets/Dispatching_Objects/nomination_cycle_page.resource` — C0 code/C1 name/C2 sort/C3-C6 TIME cells (HH:MM da_input)/**C7 Gas Day Offset dd is MANDATORY-in-effect: leaving it empty makes Save silently reject and the next reload raises a blocking confirmation modal** |
| Daily Production Well Status 1 | EC Production (search) > Daily Production Well Status 1 | **N1 daily-status grid** ✅ SOLVED + live 3/3 (2026-06-13) — edit-in-place DB-verified, self-cleaning | `PWEL_DAY_STATUS` (+`WELL_HOOKUP_DAY_STATUS`), key (OBJECT_ID, DAYTIME) | **iframe** nav 4-level cascade: Date `nav:form:G:0:R:1:C:0:da_input` → PU(G1) → Area(G2) → Facility Class 1(G3) → **Well Hookup(G4, leaf — needed for rows)** → GO `button:form:B`. Date must be data-bearing (2003-01-01 seed) | **none — edit-in-place** (rows pre-instantiated, status P; no IUD) | grid `daily_well_status:form:T_data`; cells `daily_well_status:form:T:{r}:C{c}_in` (+`C{c}_dd_input` for dd cols) | GROUPMODEL/WELL, iframe `/com.ec.prod.wr.screens/daily_well_status`; RECORD STATUS/VALIDATION tabset. Working scope: AS2 EC Exploration Norway/AS2_Onshore Area/AS2_Production Facility no 1/AS2_Lift Gas Manifold 1. Design: `docs/pattern_n1_daily_status_grid_design.md`; recon: `tmp/scripts/wr0001_*` |

---

## Screen TYPES (the reusable patterns — most new work fits one of these)

### OV — Object / Manage-Object (date-effective objects)
- Delegates to T2 `manage_object.resource`. Has a **navigator** (cascading filter dropdowns) + **Apply Navigator** (GO = `button:form:B`), MANDATORY after setting filters.
- Insert: `Open New Object Form` → `objectForm` fields (`tab:tabPanel:objectForm:form:G:0:R:{r}:C:1:in` / `..._da_input` for dates) → `Save` → `Apply Navigator`.
- Update: `Select Object Row` → `updateAttributes` fields → `Save`.
- **Delete = End Date = Start Date** (`objectdates` `..._da_input`) — a true delete for date-effective objects (NOT a physical row delete).
- DB: `OV_*` view; `Code Should Be Present/Absent In View`.

### TV — Table class (inline-editable grid)
- Delegates to T2 `table_class.resource`. **No navigator.** Paginated grid.
- Cell id pattern: `{grid}:form:T:{row}:C{col}_in` (e.g. C0, C1, C2). Mandatory cells render **yellow** — must fill before Save.
- Insert: `Insert New Grid Row` → find blank row → type cells (real keystrokes + Tab commit; NOT fill()) → `Save` → `Refresh Screen`.
- **Delete = PHYSICAL** (`Delete Selected Grid Row    <submenu label>`) — row gone from base table.
- Find row across pages by a key cell value (JS over `input[id$=":C{key}_in"]`).
- DB: base **table** (e.g. `ctrl_mime_type_mapping`, `t_basis_language`).

### OV-GM — groupmodel manage-object (e.g. Area, Sub Area)
- Same T2 `manage_object` mechanics, but the grid loads ONLY after the groupmodel
  navigator dropdown(s) are set (`Select EC Dropdown Option` on `nav:form:G:0:R:1:C:{n}:dd`,
  cascading where applicable) + **Apply Navigator**.
- The inserted object must set its Op-parent dropdown(s) (Op Production Unit / Op Area)
  to the SAME values as the navigator, or it won't appear in the filtered grid.
- **Form dropdowns are effective-date-filtered**: only objects valid at the form's
  Start Date are offered — pick a test Start Date AFTER the parent objects' start.
- Versioned grids redraw lazily after delete — one extra Apply Navigator before asserting.

### PC — parent-child setup (e.g. Object List Setup)
- Navigator picks the PARENT (class + object) + GO → the parent's ITEMS show in an
  inline TV-style grid (`…:T:{row}:C{col}` cells). Insert/Delete toolbar entries are
  named for the item ("Object List Item") — use `Insert New Grid Row By Label` /
  `Delete Selected Grid Row` (both scoped to the right menu-parent).
- New item rows: find by blank key cell (`Find Grid Row By Cell Input Value` with empty
  value), re-find AFTER the object dropdown selection (grid can re-index), fill any
  MANDATORY (yellow) cells (here: Sort Order C5) before Save.
- DB oracle = **count-delta** on the base table (`View Count Where` in DbVerify):
  baseline at suite setup, +1 after insert, back to baseline after delete — immune to
  pre-existing rows in other parents.

### RUN-verify — framework run screens (e.g. Validation Overview)
- Framework screen (`/com.ec.frmw.co.screens/...`). Navigator = **From/To date** + **GO** (`navButton:form:B`), MANDATORY after setting dates (and again after running, to refresh results).
- Group tree: `groups:form:T:{idx}:C0_la` (label) / `:C2_la` (summary). Locate rows by **description text**, derive idx (robust to reordering).
- Run gesture: select row → **[Run Selected Groups]** → GO to refresh Summary.
- Output → `CTRL_CHECK_LOG` (one row **per violating OBJECT**, not per source row — count `DISTINCT OBJECT_ID` for the oracle).

---

## EC web common patterns (all screens)
- **Suite Setup gesture:** `Launch EC And Open Screen    ${<X>_SCREEN}` (T1 common.resource)
  = browser + login + navigate. Every page object's `Open <X> Screen` is a one-line
  delegation to it (OV-GM screens add their navigator dropdown steps + Apply Navigator after).
- **IUD test data:** `Prepare IUD Object Data    <AUTOTEST_prefix_>    <Label>` (T1
  utils.resource) generates the unique code and publishes suite vars `${TEST_CODE}` /
  `${OBJ_NAME}` / `${OBJ_NAME_UPD}` — the standard data step in every IUD Suite Setup.
- **Test dates are CENTRAL:** `${TEST_START_DATE}` (2000-01-01) and
  `${TEST_START_DATE_REFDD}` (2003-01-01, for screens with reference dropdowns) come from
  `environment.py` and are overridable via `EC_TEST_START_DATE(_REFDD)` env vars — never
  hardcode date literals in new suites.
- **Login:** `Login To EC` (Keycloak `#username`/`#password`/`#kc-login`).
- **Navigate:** `Navigate To Screen <label>` — treeview search box `menu:searchForm:searchTxt`, click `.tv-link` with exact text; confirm via `screenToolbar:form:screenLabel`.
- **PrimeFaces id grammar:** `form:component:T:{row}:C{col}_{suffix}` — `_la` label, `_in`/`_input` input, `_da_input` date, `_data` datatable body.
- **Navigator + GO is MANDATORY** after filling navigator data (date/filters) — the screen does not refresh on its own. (See memory: EC Navigator GO Button.)
- **Hidden vs visible submit:** a matching id is not proof — verify the element is the VISIBLE/intended control (e.g. GO was `navButton:form:B`, NOT the hidden `nav:form:defaultSubmit`).
- **Verify at DB ground truth** via `DbVerify` — the UI can lie (optimistic state, pagination, grain). Dryrun checks structure only; the live run + DB check is the proof.
- **OBJECT START DATE = VERSION FILTER (universal!).** Every reference dropdown on an
  object form only offers objects EFFECTIVE AT THE FORM'S START DATE (Choong-Yin,
  2026-06-12: "the object start date is a kind of object version"). A test Start Date
  of 2000-01-01 empties dropdowns whose seed objects start 2003-01-01 (Customers, Cost
  Objects, Financial Accounts, Op Production Units…). Symptom: dropdown populates on a
  fresh form but not after the date is filled. Rule: pick a test Start Date AT/AFTER the
  seed-data epoch (2003-01-01 in this sandbox) on any screen with reference dropdowns.
- **Config-combination screens (e.g. Account Mapping): the reference-dropdown COMBINATION
  is the unique key.** First-option guessing can build an already-taken or incoherent
  combination — both silently reject. Recipe: SELECT existing rows from the OV view,
  decode the combination pattern (ALT_CODE style), pick a VALID-AND-UNUSED combination
  reusing a proven sub-trio (account/category/PKs), choose dropdowns BY VALUE.
- **Silent reject = mandatory field missing.** If Save produces no row, look for the EC banner *"Required fields are empty: <field>"* — fill the named dropdown via `Select EC Dropdown Option` (T1 table.resource). Seen on Object List (Class Name) and Regulatory Permits (Regulatory Agency).
- **Insert-form field rows vary per class** — recon `tab:tabPanel:objectForm:form:G:0:R:{r}:C:0:la` labels first (Code/Name are not always R0/R1: State/County have Master System rows above them).

---

## How to add a new screen (recon-first protocol)
1. Recon: search the treeview for the screen; capture its `EC_USER_OBJECT` URL, list/grid id, key field/cell ids, navigator + GO, and (for run screens) the output table.
2. Identify the **type** (OV / TV / RUN-verify) — reuse that type's T2 + patterns above.
3. Write the T3 page object (mirror an existing same-type one) + the test; set relative-import depth to the folder depth. Use the standard conventions: `Open <X> Screen` delegates to `Launch EC And Open Screen`; Suite Setup data via `Prepare IUD Object Data`; dates via `${TEST_START_DATE}` / `${TEST_START_DATE_REFDD}`.
4. **Dryrun** (structure) → **live run** (behaviour) → **DB verify** (ground truth).
5. Add a row to the table above + persist any new gotcha to memory.

## Changing a SHARED keyword file (resources/, libraries/, _shared/)
MANDATORY protocol — see README "Shared keyword-file change protocol":
**backup first** (`py tmp/scripts/backup_keyword_file.py <file>` → `.keyword_backups/`),
classify the change (additive / conditional / behavioral; signature changes FORBIDDEN),
grep all callers, then verify with the **canary pack** (`py tmp/scripts/run_canary.py` —
Bank OV · Area OV-GM · MIME TV · Object List Setup PC · Account Mapping combination)
**plus one random non-canary suite live** (`py tmp/scripts/run_random_suite.py`)
before commit. Any problem → copy the .bak back over the file = instant revert.
