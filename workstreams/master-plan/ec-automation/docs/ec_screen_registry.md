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
| Production Sub Unit | Configuration > Assets > Basic Objects > Production Sub Unit | EXCLUDED | `OV_PROD_SUB_UNIT` | — | — | `manageObject:form:T_data` | **Excluded 2026-06-11 (Choong-Yin):** the screen's operational groupmodel is NOT enabled in this environment, so the grid can never query/list data (inserts persist to DB but stay invisible). Do not automate until the groupmodel is turned on. |

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
- **Login:** `Login To EC` (Keycloak `#username`/`#password`/`#kc-login`).
- **Navigate:** `Navigate To Screen <label>` — treeview search box `menu:searchForm:searchTxt`, click `.tv-link` with exact text; confirm via `screenToolbar:form:screenLabel`.
- **PrimeFaces id grammar:** `form:component:T:{row}:C{col}_{suffix}` — `_la` label, `_in`/`_input` input, `_da_input` date, `_data` datatable body.
- **Navigator + GO is MANDATORY** after filling navigator data (date/filters) — the screen does not refresh on its own. (See memory: EC Navigator GO Button.)
- **Hidden vs visible submit:** a matching id is not proof — verify the element is the VISIBLE/intended control (e.g. GO was `navButton:form:B`, NOT the hidden `nav:form:defaultSubmit`).
- **Verify at DB ground truth** via `DbVerify` — the UI can lie (optimistic state, pagination, grain). Dryrun checks structure only; the live run + DB check is the proof.
- **Silent reject = mandatory field missing.** If Save produces no row, look for the EC banner *"Required fields are empty: <field>"* — fill the named dropdown via `Select EC Dropdown Option` (T1 table.resource). Seen on Object List (Class Name) and Regulatory Permits (Regulatory Agency).
- **Insert-form field rows vary per class** — recon `tab:tabPanel:objectForm:form:G:0:R:{r}:C:0:la` labels first (Code/Name are not always R0/R1: State/County have Master System rows above them).

---

## How to add a new screen (recon-first protocol)
1. Recon: search the treeview for the screen; capture its `EC_USER_OBJECT` URL, list/grid id, key field/cell ids, navigator + GO, and (for run screens) the output table.
2. Identify the **type** (OV / TV / RUN-verify) — reuse that type's T2 + patterns above.
3. Write the T3 page object (mirror an existing same-type one) + the test; set relative-import depth to the folder depth.
4. **Dryrun** (structure) → **live run** (behaviour) → **DB verify** (ground truth).
5. Add a row to the table above + persist any new gotcha to memory.
