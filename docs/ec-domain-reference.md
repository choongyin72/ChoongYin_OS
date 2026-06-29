# EC Domain Reference — Automated Reviewer

_Read by the automated reviewer at the start of each session to ground SME-level review judgements.
Maintained by the Reviewer session. Worker does not edit this file._

_Last updated: 2026-06-28_

---

## 1. Screen Pattern Types

The most important judgement the reviewer makes is: **did the Worker choose the right pattern for this screen?** A wrong pattern that passes tests is a deferred failure (MUST-FIX).

### 1.1 OV — Bank Family (most common)
**What it is:** A date-effective object with a code, name, and optional attributes. Managed via a "New Object" toolbar button (insert) and an updateAttributes form (update).

**How to identify:**
- Navigator has a date filter only (no mandatory dropdown gate)
- Toolbar shows "New Object" button (enabled)
- DB view is `OV_<CLASS>` e.g. `OV_ROYALTY_OWNER`, `OV_CONTRACT_AREA`
- Class resolves via `EC_CLASS.CLASS_NAME`

**Correct patterns:**
- INSERT: "New Object" toolbar → fill form → Save
- UPDATE: select row → updateAttributes → edit → Save
- DELETE: End Date = Start Date (zero-length effective window = true physical delete from the OV view)
- DB assert: `Code Should Be Present In View    ov_<class>    ${TEST_CODE}` (TC02), `Code Should Be Absent In View    ov_<class>    ${TEST_CODE}` (TC04)
- T2 base: `manage_object.resource`

**Common mistakes:**
- Using `DV_*` view instead of `OV_*` for Bank family (DV = derived/display view, may include extra joins that mask a failed delete)
- Asserting against base table instead of OV view (OV view enforces date-effectivity)
- Trusting that End-Date=Start-Date soft-deletes — it is a TRUE physical delete in EC; the row disappears from the OV view immediately

---

### 1.2 OV-GM — Gated / Manage-Object Family
**What it is:** An OV screen gated behind a parent navigator dropdown (GO button). The object list only loads after the parent is selected via GO.

**How to identify:**
- Navigator has a mandatory parent dropdown PLUS a GO button
- Grid loads only after GO is clicked
- DB view is `OV_<CLASS>` but the class is a child of a parent object
- T2 base: `manage_object.resource` PLUS the gating nav keywords

**Correct patterns:**
- Navigator: select parent dropdown → click GO → grid loads
- INSERT/UPDATE/DELETE: same as Bank family, but always within the gated scope
- R17 MANDATORY: T3 `<Screen> Row Should Exist` keyword MUST include `Wait For Elements State    visible    20s` before the T1 assert (lazy grid redraw after save)
- DB assert: same `Code Should Be Present/Absent In View` pattern

**Common mistakes:**
- Missing R17 wait wrapper — test passes locally on fast sandbox, fails on slow/loaded sandbox
- Asserting without re-applying the GO navigation after a save (grid may reset to unfiltered state)
- Wrong parent selected in recon vs live run (different effective date ranges)

---

### 1.3 TV — Language / Table-Class Family
**What it is:** A code-table screen (no date-effectivity). Simple insert/update/delete of lookup values.

**How to identify:**
- No date navigator
- DB view is `TV_<CLASS>` e.g. `TV_STREAM_SET_LIST`
- Toolbar shows Add/Delete row buttons (not "New Object")
- T2 base: `table_class.resource`

**Correct patterns:**
- INSERT: Add row → fill inline → Save
- UPDATE: click cell → edit inline → Save
- DELETE: select row → Delete → Save (physical row delete)
- DB assert: `Code Should Be Present In View    tv_<class>    ${TEST_CODE}` / `Code Should Be Absent In View`

**Common mistakes:**
- Using `manage_object.resource` (T2 Bank) instead of `table_class.resource` (T2 Language)
- Expecting a "New Object" form — TV screens edit inline, no form popup

---

### 1.4 PC — Parent-Child / Setup Screens
**What it is:** A membership/setup screen where a child object (e.g. Perf Interval) is assigned to a parent (e.g. Unit Agreement). No code of its own — uniqueness is by the parent+child pair.

**How to identify:**
- No standalone Code column for the child membership
- DB view often `DV_<PARENT>_<CHILD>_SETUP` e.g. `DV_UNIT_WELL_SETUP`, `DV_TRACT_WELL_SETUP`
- Insert adds a row; delete removes the row (physical)
- T2 base: `table_class.resource` (same as TV)

**Correct patterns:**
- INSERT: select child from dropdown → Save → count-delta +1 in DV view
- UPDATE: edit a non-key attribute (e.g. COMMENTS) → Save → sentinel present in DV view
- DELETE: select row → Delete → Save → count-delta back to 0
- DB assert: `View Count Where Should Be    DV_<VIEW>    <COLUMN>    <VALUE>    <COUNT>` for INSERT/DELETE; `Code Should Be Present In View    DV_<VIEW>    ${SENTINEL}` for UPDATE
- Parent must be pre-confirmed as empty (baseline-0) OR the test must use a unique child that has no existing membership

**Common mistakes:**
- Using `Code Should Be Present In View` for the INSERT check when the membership has no code column — use count-delta instead
- Not confirming baseline-0 before the test (an existing membership with the same child makes TC02 ambiguous)
- Not cleaning residual rows from failed test runs before the final live run

---

### 1.5 Custom-URL OV
**What it is:** An OV screen with a non-standard URL structure. The grid is loaded via a direct URL, not via the standard navigator cascade.

**How to identify:**
- URL contains the screen identifier directly (e.g. `/calendar`, `/calendarCollection`)
- Grid id is `nav:form:T_data` (NOT `manage_object_nav_nav:form:T_data`)
- NO GO button in the navigator
- T2 `Save And Refresh List` uses Refresh (not re-navigate + GO)

**Correct patterns:**
- Same Bank family I-U-D pattern, but grid locator must be confirmed via `preflight_grid_locator.py` — never assumed from a sibling screen
- Navigator: date filter only, no GO
- After Save: `Save And Refresh List` → grid refreshes in place

**Common mistakes:**
- Assuming the grid id from a sibling term screen — THE most common clone error for this family
- Missing the pre-flight guard (`preflight_grid_locator.py`) before the live run
- Using GO navigation keywords that don't exist on this screen type

---

### 1.6 Event-Log / Code-Less Screens (R19)
**What it is:** A screen that records events with no unique code column. Uniqueness is by timestamp + other composite key.

**How to identify:**
- No CODE column in the DB view
- Base table is an event/audit table (e.g. `FCTY_DAY_ALARM`)
- Delete is physical (no end-date pattern)

**Correct patterns:**
- R19: use a unique per-run MARKER oracle (e.g. `view_count_where_should_be`) to assert insert/delete
- DELETE proof: marker count = 0 in BOTH the OV view AND the base table
- T2 base: `table_class.resource`

**Common mistakes:**
- Using `Code Should Be Present In View` when there is no code column
- Only asserting against the OV view but not the base table (OV may filter; base table confirms physical delete)

---

## 2. View Naming Conventions

| Prefix | Type | Example | Notes |
|--------|------|---------|-------|
| `OV_` | Object View (date-effective) | `OV_CONTRACT_AREA` | Primary assertion target for Bank/OV-GM family |
| `TV_` | Table View (code table) | `TV_STREAM_SET_LIST` | Primary assertion for Language/TV family |
| `DV_` | Derived/Display View | `DV_UNIT_WELL_SETUP` | Used for PC screens; may include extra joins |
| `ZWP_V_` | Client-specific derived view | `ZWP_V_DEF_RAU_SUB_004` | Woodside/Pluto custom views — read-only, never written |

**Key rule:** Always confirm the view name from the DB (`EC_CLASS` / `SELECT * FROM OV_<guess>` with a LIMIT) — never assume from the class slug. View name ≠ screen slug (e.g. `OV_UNIT_AGR` not `OV_UNIT_AGREEMENT`).

---

## 3. Delete Patterns by Family

| Family | Delete mechanism | DB evidence |
|--------|-----------------|-------------|
| OV / Bank | End Date = Start Date | Row absent from `OV_*` view |
| OV-GM / Gated | End Date = Start Date | Row absent from `OV_*` view |
| TV / Language | Toolbar Delete row | Row absent from `TV_*` view |
| PC / Setup | Toolbar Delete row | Count = 0 in `DV_*` view |
| Custom-URL OV | End Date = Start Date | Row absent from `OV_*` view |
| Event-Log | Toolbar Delete row | Count = 0 in OV view AND base table |

---

## 4. T2 Base Keyword Selection

| Screen family | Correct T2 resource |
|---------------|-------------------|
| OV / Bank | `manage_object.resource` |
| OV-GM / Gated | `manage_object.resource` + gating nav keywords |
| TV / Language | `table_class.resource` |
| PC / Setup | `table_class.resource` |
| Custom-URL OV | `manage_object.resource` (Refresh variant) |
| Event-Log | `table_class.resource` |

---

## 5. DB Assertion Cheat Sheet

| Scenario | Correct assertion |
|----------|------------------|
| OV/Bank INSERT (TC02) | `Code Should Be Present In View    ov_<class>    ${TEST_CODE}` |
| OV/Bank DELETE (TC04) | `Code Should Be Absent In View    ov_<class>    ${TEST_CODE}` |
| PC INSERT/DELETE | `View Count Where Should Be    DV_<view>    <col>    <val>    <count>` |
| PC UPDATE sentinel | `Code Should Be Present In View    DV_<view>    ${UPDATE_SENTINEL}` |
| TV INSERT | `Code Should Be Present In View    tv_<class>    ${TEST_CODE}` |
| Event-log INSERT | `view_count_where_should_be` (R19 marker oracle) |
| Event-log DELETE | `view_count_where_should_be = 0` in OV AND base table |

---

## 6. Common Clone Errors (Batch Screens)

When the Worker clones an exemplar for a sibling screen, check ALL of these are substituted:

| Token | Example wrong (pilot) | Example correct (clone) |
|-------|----------------------|------------------------|
| OV view name | `OV_DOC_DATE_TERM` | `OV_DOC_RECEIVED_TERM` |
| DV view name | `DV_UNIT_WELL_SETUP` | `DV_TRACT_WELL_SETUP` |
| AUTOTEST prefix | `AUTOTEST_DDT_` | `AUTOTEST_DRT_` |
| SOW filename | `document_date_term_sow.md` | `document_received_term_sow.md` |
| Grid id | `nav:form:T_data` | confirm independently via preflight |
| Form row indices | R:6, R:7 from pilot | must be re-verified from THIS screen's DOM |
| CHECKLIST item 15 | cites pilot view | must cite THIS screen's view |
| README DB ground truth | cites pilot view | must cite THIS screen's view |
| Registry/scorecard rows | pilot's CD/RC code | this screen's code |

---

## 7. Sandbox Environment Notes

| Environment | Purpose | Write-safe? |
|-------------|---------|-------------|
| `localhost:1521/ORCL` (Docker) | Worker's local Oracle sandbox | Yes — all IUD live runs |
| `db.plutodev.woodside-pluto.tieto-og.cloud` | EC Dev (PLUTODEV) | Yes — config SQL only |
| `dev.db.non-prod.plp.wde.ecaas.cloud/QDB` (ECAASDEV) | Client investigation | READ-ONLY — never write |
| Production | Client production | NEVER TOUCH |

Sandbox can be down after laptop/Docker restart — the runner has a DB retry loop (R: `EC_LEARN_DB_RETRIES`, default 3 × 20s). Worker IUD suites have no retry; if sandbox is down, Worker must restart Docker first.

---

## 8. Key Rules Quick Reference

| Rule | One-liner |
|------|-----------|
| R1 | Unit conversion guard before any DB write (multiplicative units only) |
| R8 | Sync feature branch with master before every push |
| R9 | PR body MUST use EXACT 6 field headers |
| R12 | Shared T1/T2 edit → run canary + 1 sibling and cite it |
| R13 | ONE live N/N count, identical across title/body/scorecard/README/SOW |
| R16 | Playwright bundle credentials MUST use env vars (EC_USER/EC_PASS) |
| R17 | OV-GM T3 MUST have Wait For Elements State visible 20s before T1 assert |
| R18 | Files printed to Windows console MUST be ASCII-only |
| R19 | Event-log: use marker oracle; prove physical delete in OV AND base table |
| R20 | Author every bundle .py ASCII at authoring time |
| R21 | PR body Files-touched must list every file in the diff |
| R23 | Long-lived branch must show zero -lines on reviewer-owned docs vs master |
| R24 | Detached worktree push MUST use HEAD:refs/heads/<branch> |
| R25 | When a tool/connection breaks, own the troubleshooting |
| R26 | 19-item IUD checklist is a hard gate — all items green before PR |
