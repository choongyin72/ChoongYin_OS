# EC Calculation Screens — VERIFIED Reference (REFER to this; do NOT re-scan/guess)

_Sandbox: web ap-f0a7g341jn6d...:8443 (sysadmin) · DB localhost:1521/ORCL (ECKERNEL_EC). All ids below are
VERIFIED by scan/use on 2026-06-28/29. Mark = ✅ proven · ⚠️ open issue. Refer here first; only scan if an
element is NOT listed here._

## Full flow
Create calc (1) → set Equation (2) → Connect calc as a Job to an allocation network (3) → Run via Daily
Allocation with Simulate (4) → read the log. To RUN a calc it MUST be connected as a Calculation Job (step 3).

## 1. Create Calculation  ✅
- Nav: Date `nav:form:G:0:R:1:C:0:da_input` · Calculation Context dd `nav:form:G:1:R:1:C:0:dd` (e.g. **Production Allocation** = EC_PROD) · GO `button:form:B`.
- Grid `calculation:form:T_data` cols: **C0=Code, C1=Name, C2=Start Date, C3=End Date(da_input), C4=Period, C5=Type** (existing rows: only C0/C3 editable).
- CREATE is NOT the toolbar "+" (it does not add an inline row). Use the **VERSIONS area**: click a donor row (e.g. `RUN_NO_TEST`, an EQUATIONS calc) → fill New Code `copyCalculationForm:form:G:0:R:0:C:1:in`, New Name `…C:3:in`, New Start `…C:5:da_input` → click **"Copy To New Calculation"** = `copybutton:form:B`. (Copy inherits the donor's equations.)

## 2. Maintain Calculation (equation editor)
- Nav: Date `nav:form:G:0:R:1:C:0:da_input` · Context dd `nav:form:G:1:R:1:C:0:dd` · **Calculation dd `nav:form:G:2:R:1:C:0:dd`** (pick by NAME, e.g. "AUTOTEST Calc Test") · GO.
- EQUATIONS tab grid `maintab:tabPanel:equations:form:T_data`, row cols: C0=Eqn# · C1_cb=Disable · C2=Doc · C3=Iterations(matheq) · C4=Condition(matheq) · **C5=Equation(matheq)**. Each math cell has button **`maintab:tabPanel:equations:form:T:0:C5_b`** = open Equation editor.
- ⚠️ Equation editor `mathEqEditor:mathEqDialog` is a **CANVAS math widget** (Calc.MathEqReg) — NO DOM-editable input (MathML stored hidden in `mathEqEditor:form:editor:mathml`). OK=`mathEqEditor:form:ok` · Cancel=`mathEqEditor:form:cancel`. **NOT headless-typable** — author manually, or keep the donor's inherited equation.

## 3. Calculation Group Setup (connect calc as a Job)  ⚠️ save did not persist last run
- Nav: Date `nav:form:G:0:R:1:C:0:da_input` · Calculation Group Context dd `nav:form:G:0:R:1:C:1:dd` = **"Allocation Network Calculation"** · GO `button:form:B`.
- Network grid `nav_model:form:T_data` → click the network row (e.g. **P1_DAY_ALLOC**).
- Bottom tabs: CALCULATION GROUP / LIST / **CALCULATION JOB CONNECTION** (match tab text containing "job connection", case-insensitive — NOT a `translate()` half-lowercase).
- Job grid `tab:tabPanel:calc_group_conn_table:form:T_data`. ADD = hover Insert(+) toolbar (`//a[.//span[contains(@class,'ui-icon-insert')]]`) → click **"Calculation Job"** submenu (enabled only when this tab is active). New row cols: **C0=Start Date(da_input), C1=End Date(da_input), C2=Calculation Job dd (`…:T:0:C2_dd_button`), C3_cb=Block**. Pick the calc in C2 dd → Save.
- ⚠️ **OPEN: last add showed "saved" but did NOT persist** (calc absent from Daily Allocation Calc-Job dd + DB). Silent reject — DIAGNOSE next: scan the new row for an unfilled mandatory/yellow cell, and check for a save-error notification, BEFORE re-trying. (Backing table for this grid still to confirm; DEPENDENT_CALC_JOB was the WRONG table to verify against.)

## 4. Daily Allocation (RUN a calc)  ✅ PROVEN 2026-06-29
- Nav: From Date `nav:form:G:0:R:1:C:0:da_input` · **To Date `nav:form:G:1:R:1:C:0:da_input`** · Allocation Network Group/Network dd `nav:form:G:2:R:1:C:0:dd` (e.g. **"P1 Day Allocation"**) · Allocation Network dd `nav:form:G:3:R:1:C:0:dd` · **Calculation Job dd `nav:form:G:4:R:1:C:0:dd`** (the connected calc) · GO `button:form:B`.
- Run panel: Log Level dd **`dateStartJob:form:G:0:R:1:C:1:dd`** (pick "Full") · **Simulate checkbox `dateStartJob:form:G:0:R:1:C:2:cb`** (an EC ECCheckboxCell — `.check()` it; Simulate = SAFE dry-run, no real write) · Run button = `get_by_role("button", name=/run calc/i)` · then OK = `get_by_role("button", name=/^ok$/i)`.
- After run: click GO again → log grid shows the Run row (Exit Status **"Simulate Success"**) + the calc's log text. EC_PROD calc results/log land in **`ALLOC_JOB_LOG`** (the "Calculation Log" screen).
- ✅ Proven: ran "Calculation Test" → Run No 2, Simulate Success, log "This is Simple Equation".

## Delete a calc (cleanup)  ✅
Create Calculation → select the calc row → **"Delete Calculation"** button → confirm "Yes". (Verified clean: 0 rows, 0 orphan equations.)
