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
