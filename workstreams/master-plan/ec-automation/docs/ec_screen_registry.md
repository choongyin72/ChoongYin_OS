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

---

## How to add a new screen (recon-first protocol)
1. Recon: search the treeview for the screen; capture its `EC_USER_OBJECT` URL, list/grid id, key field/cell ids, navigator + GO, and (for run screens) the output table.
2. Identify the **type** (OV / TV / RUN-verify) — reuse that type's T2 + patterns above.
3. Write the T3 page object (mirror an existing same-type one) + the test; set relative-import depth to the folder depth.
4. **Dryrun** (structure) → **live run** (behaviour) → **DB verify** (ground truth).
5. Add a row to the table above + persist any new gotcha to memory.
