# EC Calculation Screens — VERIFIED Reference (REFER to this; do NOT re-scan/guess)

_Sandbox: web ap-f0a7g341jn6d...:8443 (sysadmin) · DB localhost:1521/ORCL (ECKERNEL_EC). All ids below are
VERIFIED by scan/use on 2026-06-28/29. Mark = ✅ proven · ⚠️ open issue. Refer here first; only scan if an
element is NOT listed here._

## Full flow
Create calc (1) → set Equation (2) → Connect calc as a Job to an allocation network (3) → Run via Daily
Allocation with Simulate (4) → read the log. To RUN a calc it MUST be connected as a Calculation Job (step 3).

## 1. Create Calculation  ✅
- Nav: Date `nav:form:G:0:R:1:C:0:da_input` · Calculation Context dd `nav:form:G:1:R:1:C:0:dd` (e.g. **Production Allocation** = EC_PROD) · GO `button:form:B`.
- Grid `calculation:form:T_data` cols: **C0=Code, C1=Name, C2=Start Date, C3=End Date, C4=Period, C5=Type**.
- **CREATE (from base) = the toolbar `+` icon** → adds a new blank row in PUBLIC CALCULATIONS. Fill the new row
  (verified ids, e.g. row index 1): Code `…:T:<r>:C0_in`, Name `…C1_in`, Start Date `…C2_da_input`,
  **Calculation Period dd `…C4_dd_button`** (e.g. Day), **Calculation Type dd `…C5_dd_button`** (e.g. Equations)
  → **Save**. Code/Name/Start/Period/Type are all mandatory (Period + Type render yellow). DB-verify the
  `CALCULATION` row (e.g. `AUTOTEST_BASE_TEST | EQUATIONS | MAIN | EC_PROD | DAY | 2000-01-01`).
- **CORRECTION (2026-06-29):** my earlier note "`+` does not create a calc" was a WRONG, unverified assumption.
  `+` DOES create from base. Copy-To-New was discarded as the create method (per owner: "throw copy parts").
- ⚠️ A from-base calc has **NO equation** — it exists but produces nothing on a run until an equation is authored
  in the canvas editor (`mathEqEditor`, not headless-typable). Author it manually when a runnable calc is needed.

## 2. Maintain Calculation — author equation on a PROCESS DIAGRAM calc  ✅ steps 4-7 verified 2026-06-29
- Nav: Date `nav:form:G:0:R:1:C:0:da_input` · Calculation Context dd `nav:form:G:1:R:1:C:0:dd` (e.g. Production
  Allocation) · **Calculation dd `nav:form:G:2:R:1:C:0:dd`** (pick by NAME) · GO `button:form:B`.
- **FLOWCHART tab is a CANVAS** (svg=0, canvas=2); default Process-Diagram = **Start -> Step 1 -> Stop**. The
  process boxes are canvas pixels (NOT DOM); on a maximised window the **Step 1 box centres ~viewport (1080,577)**.
- **Step 5 - Implement Step 1 as Equations:** **right-click the Step 1 box** (canvas coords) -> a **DOM** context
  menu appears (Copy/Paste/Delete/Edit label/Edit description/Edit iterations/Convert to Library/Add new
  element... / **Implement as...**). Hover **"Implement as..."** -> submenu **Process / Equations / Excel
  workbook / Library calculation** -> click **"Equations"** (plural!). Click **Save** -> Step 1 then shows a
  **sigma (Σ) icon** = implemented as Equations.
- **Step 6 - Drill into Step 1:** **double-click** the Step 1 box -> breadcrumb shows "<calc> └ Step 1", the
  **EQUATIONS** sub-tab becomes active.
- **Step 7 - Add an equation row:** toolbar **`+`** -> submenu lists the sub-grids (EQUATIONS / LOCAL SETS /
  DB OBJECTS SET CONDITIONS / FILTER SET CONDITIONS / COMBINATION SET LIST / SET EQUATIONS / LOCAL VARIABLES)
  -> click **"EQUATIONS"** -> new row in `maintab:tabPanel:equations:form:T_data` (cols: Eqn# / Disable / Doc /
  Iterations `C3_b` / Condition `C4_b` / **Equation `C5_b`**). NOTE: this `+`+submenu is FLAKY under automation
  (retry; or have the user click it).
- ✅✅ **Step 8 - Enter the formula = EXERCISED + DB-PROVEN end-to-end (2026-06-29).** Authored
  `INFO = 'AUTOTEST equation log'` in the editor, ran it (Simulate Success, log line appeared), DB-verified in
  CALC_EQUATION, then self-cleaned. The editor (`mathEqEditor`, OK/CANCEL) is a **RIGHT-CLICK context-menu
  builder, NOT free text** (typing "INFO" pops Insert-Iterator). Two automation gotchas that cracked it:
  1. **The context menu is CANVAS-drawn, not DOM** → navigate by **mouse COORDINATES** (right-click the `?`,
     then click menu items by position), not by Playwright locators.
  2. **Menu labels are CSS-uppercased** (rendered "EQUATIONS" but real text "Equations") → match
     case-insensitively (this is why the earlier `+ → EQUATIONS` row-add kept "failing").
  - **Proven path for `INFO = 'text'`:** open editor (`...:T:0:C5_b`) → right-click the `?` → **Log messages →
    Insert 'INFO'** → right-click → **Insert assignment** (gives `INFO = ?`) → left-click the new `?` → right-click
    → **Operands → Insert constant text...** → type in the popup → OK → **OK** (editor) → **Save** → DB-verify.
  Full menu tree + syntax in [[EC_EQUATION_SYNTAX]]. **The equation editor is no longer a gap — proven hands-on.**

## 3. Calculation Group Setup (connect calc as a Job)  ✅ RESOLVED 2026-06-29
- Nav: Date `nav:form:G:0:R:1:C:0:da_input` · Calculation Group Context dd `nav:form:G:0:R:1:C:1:dd` = **"Allocation Network Calculation"** · GO `button:form:B`.
- Network grid `nav_model:form:T_data` → click the network row (e.g. **P1_DAY_ALLOC**).
- Bottom tabs: CALCULATION GROUP / LIST / **CALCULATION JOB CONNECTION** (match tab text containing "job connection", case-insensitive — NOT a `translate()` half-lowercase).
- Job grid `tab:tabPanel:calc_group_conn_table:form:T_data`. ADD = hover Insert(+) toolbar (`//a[.//span[contains(@class,'ui-icon-insert')]]`) → click **"Calculation Job"** submenu (enabled only when this tab is active). New row cols: **C0=Start Date(da_input), C1=End Date(da_input), C2=Calculation Job dd (`…:T:0:C2_dd_button`), C3_cb=Block**. Pick the calc in C2 dd → Save.
- ✅ **ROOT CAUSE of the earlier silent-reject + FIX:** the Insert drops the new blank row in the **MIDDLE**
  (existing rows shift to higher indices) — so filling a fixed index (e.g. T:2) left the *actual* new blank
  row empty, and EC silently rejects the whole Save on that blank row's mandatory fields (banner: "Required
  fields are empty … Start Date / Calculation Job on row N"). **FIX: after Insert, read every row's Start Date,
  find the one that is EMPTY, and fill THAT row** (Start Date + Calculation Job dd). Then **click Save** (EC
  never auto-saves) and DB-verify.
- ✅ **Correct backing table = `tv_alloc_network_job_conn`** (keyed alloc_network_id + job_id; resolve codes
  via `ecdp_objects.GetObjCode`). DEPENDENT_CALC_JOB is the WRONG table.
- Eligibility note: NOT limited to PROCESS calcs — EQUATIONS calcs connect fine (11 EQUATIONS jobs already
  connected across networks). So calc-type is not a connection blocker.
- ✅ Proven: connected AUTOTEST_CALC_TEST to P1_DAY_ALLOC (CALC_TEST + EC_DAILY_VOLUME retained intact).

## 4. Daily Allocation (RUN a calc)  ✅ PROVEN 2026-06-29
- Nav: From Date `nav:form:G:0:R:1:C:0:da_input` · **To Date `nav:form:G:1:R:1:C:0:da_input`** · Allocation Network Group/Network dd `nav:form:G:2:R:1:C:0:dd` (e.g. **"P1 Day Allocation"**) · Allocation Network dd `nav:form:G:3:R:1:C:0:dd` · **Calculation Job dd `nav:form:G:4:R:1:C:0:dd`** (the connected calc) · GO `button:form:B`.
- Run panel: Log Level dd **`dateStartJob:form:G:0:R:1:C:1:dd`** (pick "Full") · **Simulate checkbox `dateStartJob:form:G:0:R:1:C:2:cb`** (an EC ECCheckboxCell — `.check()` it; Simulate = SAFE dry-run, no real write) · Run button = `get_by_role("button", name=/run calc/i)` · then OK = `get_by_role("button", name=/^ok$/i)`.
- After run: click GO again → log grid shows the Run row (Exit Status **"Simulate Success"**) + the calc's log text. EC_PROD calc results/log land in **`ALLOC_JOB_LOG`** (the "Calculation Log" screen).
- ✅ Proven: ran "Calculation Test" → Run No 2, Simulate Success, log "This is Simple Equation".
- ✅ Proven (own calc): ran "AUTOTEST Calc Test" → Run No 3, **Simulate Success**, log INFO "Test: 3".
- Note: a lingering autocomplete dd panel (`...dd_panel` ui-helper-hidden ui-connected-overlay-exit-active)
  can invisibly intercept clicks on GO/Simulate — hide it (`display:none` on `.ui-autocomplete-panel`) or
  use `force=True` / the GO shortcut `Control+g`.

## Delete a calc (cleanup)  ✅
Create Calculation → select the calc row → **"Delete Calculation"** button → confirm "Yes". (Verified clean: 0 rows, 0 orphan equations.)

## 5. Calculation Objects config grids (Simple/Database Object Types, Variable Definitions, Global Attributes)  ✅ Simple Object Types PROVEN 2026-06-30
- **Common navigator:** Date `nav:form:G:0:R:1:C:0:da_input` + **Calculation Context dd `nav:form:G:1:R:1:C:0:dd_button`** (14 contexts; pick e.g. **Production Allocation** = EC_PROD) → GO `button:form:B`. (Database Object Types loads without a context dd.) Set the **date FIRST**, then open the dd (else the panel collapses).
- **Frames:** `db_object_type` · `simple_predefined_object_type` · `variable_definition` · `global_attribute`.
- **Simple Object Types grid** `tab:tabPanel:spObjectType:form:T_data`; cols **C0=Object Type code, C1=Label Override, C2=Object Type Label (readonly/derived), C3=Data Type dd (Date/Number/String)**. Only **C0 is mandatory**.
- ✅ **INSERT gesture (verified):** **hover** the toolbar insert anchor `//a[.//span[contains(@class,'ui-icon-insert')]]` → a **flyout submenu** appears whose item is the **grid name** (e.g. "Simple Object Types") — **CSS-uppercased in render** ("SIMPLE OBJECT TYPES") so match the menuitem **case-insensitively** and click the **visible** one. Row inserts **mid-grid** → scan `…:T:<i>:C0_in` for the **empty** one and fill THAT. **Do NOT press Tab between cells** (Tab fires a row-commit AJAX that detaches sibling cells) — fill cells directly. Then **Save** (`//a[@title='Save [Ctrl+s]' and not(...ui-state-disabled)]`).
- ✅ **DELETE gesture (verified):** select the row (click its C0 cell) → **hover** the delete anchor `//a[.//span[contains(@class,'ui-icon-delete')]]` → click the same case-insensitive flyout item → Save. (No confirm dialog appeared.)
- ✅✅ **PROVEN end-to-end 2026-06-30:** created `AUTOTEST_PHASE` (DB `CALC_OBJECT_TYPE` category=SIMPLE, data_type=STRING) → deleted → DB clean (0 rows) → re-created. Scripts: `investigation/phase1a_create_simpletype.py` + `phase1a_delete_simpletype.py`.
- 🔎 **Learning:** `CALC_OBJECT_TYPE.OBJECT_ID` = the **Calculation Context id** (AUTOTEST_PHASE got EC_PROD's id) → **object types are context-scoped**, created within the context picked in the navigator (corrects the earlier "object types are global" note in EC_CALC_CONFIG_OBJECTS).

### 5b. Variable Definitions screen  ✅ Var A (variable + Simple-type dimension) PROVEN 2026-06-30
- Same navigator (date + Calculation Context **Production Allocation** + GO). Frame `variable_definition`.
- **Main grid** `variable_definition_table:form:T` — cols **C0=Variable Name, C1..C5=Dimension 1..5** (each a **dropdown** of object types; my `AUTOTEST_PHASE` appeared as an option). Data type/precision are NOT grid columns.
- **Insert flyout labels** (hover insert icon): **`VARIABLE DEFINITION`** (new variable), **`CLASS READ MAPPING`** / `CLASS KEY READ MAPPING` / `CLASS WRITE MAPPING` / `CLASS KEY WRITE MAPPING` (these add rows to the mapping sub-grids — same flyout mechanism). Match case-insensitively + click the visible one.
- **Sub-tabs:** DEFINITION (form `tab:tabPanel:definition:form` — data type dd + precision + active cb), **READ MAPPINGS** (grid `tab:tabPanel:readMapping:form:T_data` cols: Data Set, Class Type, **Class Name**, Class Label, **Value Attribute** (C4 dd), Value Attr Label) + an `attrMapping` sub-grid (Class Key → dimension), **WRITE MAPPINGS**, RECORD STATUS, REVISION INFO, APPROVAL, HINTS&TIPS, VALIDATION, TRENDING, ATTACHMENTS.
- ✅ **Var A PROVEN:** `AUTOTEST_gvPhaseKey` dimensioned by `[AUTOTEST_PHASE]`, no mapping → `CALC_VARIABLE` row (data_type defaulted NUMBER, dim1=AUTOTEST_PHASE). Script `investigation/phase1b_create_varA.py`. Fill **C0 name**, set **C1 dd** = the dimension object type, Save. (Engine is dynamically typed so an explicit data type isn't mandatory to persist.)
- 🧭 **Known-good exemplar for a read-mapped variable (clone for Var B):** `CO2_InitialNStdVol` = NUMBER prec 2, dims `[ALLOC_NODE, DAY]`, read mapping `PWEL_DAY_DATA` / value attr `THEOR_CO2_RATE` / date-handling FIXED_INTERVALS (`investigation/phase1b_exemplar_db.py`). `ALLOC_NODE` = DB object type, `DAY` = predefined.
- ✅ **Var B1 PROVEN 2026-06-30:** `AUTOTEST_rCO2Rate` dimensioned by `[ALLOC_NODE (Database type), DAY (predefined)]` → `CALC_VARIABLE` dims=[ALLOC_NODE,DAY]. With Var A this means **all 3 object-type categories used as dimensions** (SIMPLE/DATABASE/predefined). Script `investigation/phase1b_create_varB1.py` (dimension dds match by data-item-label "Allocation Node"/"Day").
- ✅✅✅ **Var B2 (the READ MAPPING) — FULLY COMPLETE + DB-verified 2026-06-30** (binds a variable to a `_DATA` class = the item-1 data-model rule, hands-on, exact values). `AUTOTEST_rCO2Rate` →
  - **Part 1** `CALC_VAR_READ_MAPPING` (1 row): cls=`PWEL_DAY_DATA`, attr=`THEOR_CO2_RATE` (EXACT — asserted equal).
  - **Part 2** `CALC_VAR_KEY_READ_MAPPING` (2 rows, **auto-derived on the Part 1 Save**): `OBJECT_ID`→CALC_DIM_MAPPING_CODE=DIMENSION DIM_NO 1, `DAYTIME`→DIMENSION DIM_NO 2.
  Scripts `investigation/phase1b_varB2_part1.py` (build+save+verify) + `phase1b_verify_part2.py`. **The proven gestures:**
  1. **MASTER-SELECT the variable: click its `C0_in` then press `Escape`** → row goes `ui-state-highlight`. *Without this the CLASS READ MAPPING insert is a disabled no-op* (`phase1b_b2_diag3.py`: menuitem enabled only after proper select).
  2. New mapping-row cells = **type-ahead autocomplete dropdowns** (`C1_dd`=Class Type, `C2_dd`=Class Name, `C4_dd`=Value Attribute; `C0_dd`=Data Set defaults "Default"; C3/C5 derived) — **type the needle into `_dd_input`**, then click the option; **match the EXACT label** (typing `THEOR_CO2` filters to exactly `THEOR_CO2_RATE`; a loose `CO2_RATE` wrongly grabbed `PREC_THEOR_CO2_RATE` — always match exact). Order: Class Type=Data → Class Name=PWEL_DAY_DATA → Value Attribute.
  3. **Part 2 is automatic:** `CLASS KEY READ MAPPING` stays disabled until Part 1 is **SAVED**; on save EC **auto-derives** the class-key→dimension rows (OBJECT_ID→dim1, DAYTIME→dim2) into `CALC_VAR_KEY_READ_MAPPING`. No manual key entry needed for a standard key/dimension match.
  - Deleting the variable **cascades** both `CALC_VAR_READ_MAPPING` + `CALC_VAR_KEY_READ_MAPPING` (verified clean — signature gone).
  - Only ONE insert toolbar (top `screenToolbar:form:menuBar`); its flyout lists VARIABLE DEFINITION + the four mapping types.
- 🔎 **Delete-order learning:** an object type **in use as a variable dimension cannot be deleted** (EC blocks it — `AUTOTEST_PHASE` delete silently failed while `AUTOTEST_gvPhaseKey` referenced it). **Self-clean order = delete variables FIRST, then the object type.** Cleanup scripts: `phase1b_cleanup_vars.py` + `phase1a_delete_simpletype.py`.
