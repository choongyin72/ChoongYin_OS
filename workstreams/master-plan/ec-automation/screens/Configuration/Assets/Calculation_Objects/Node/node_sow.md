# SOW - Node IUD (Configuration > Assets > Calculation Objects > Node)

## 1. Screen identity
- **Screen:** Node   **BF code:** CD.0006   **View:** `OV_NODE`   **Base:** `NODE`
- **Type:** OV-GM (manage-object, groupmodel) - grid `manageObject:form:T_data`, **navigator-GATED**.
- **Date-effective:** YES (TIME_SCOPE_CODE = VERSIONED) -> DELETE = **End Date = Start Date**.

## 2. Navigator (gated) - proven cascade
`nav:form:G:0:R:1:C:1..3:dd` = **Production Unit -> Area -> Facility Class 1**. Filled first-available
parent->child + GO (`button:form:B`); the grid is empty until then. Capability:
`apply_ovgm_navigator` (Playwright) / `Apply OV-GM Navigator First Available` (RF) - returns the C:1
top-parent PU, reused as the insert **Op Production Unit** (required for grid visibility under scope).

## 3. New-Object form (scanned; fields resolved BY LABEL, not hardcoded rows)
| Field | Label | Mandatory | Kind |
|---|---|---|---|
| Code | Node Code | yes | text |
| Name | Node Name | yes | text |
| Start Date | Start Date | yes | date |
| **Calculation Sequence Number** | Calculation Sequence Number | **yes** | text (numeric) |
| Op Production Unit | Op Production Unit | no* | dropdown |

*Not yellow-mandatory. Set to **first-available** (`__FIRST__`). GROUND TRUTH (`tmp/node/probe_op_pu.py`):
the Op PU panel offers only 5 PUs (EC-UT-GENERIC / FRMW / P1 / P3 / automation_ui_test) and the navigator
first-available PU (AS1 EC Exploration Norway) is **NOT** among them - yet the inserted row still lists in
the nav-filtered grid after GO (proven by the PW driver 8/8 + RF 4/4). So on Node the Op PU need not equal
the nav PU (contrast: Area, where it did). Op Area / Op Facility Class 1 left default.

## 4. Known risks
- **OV-GM lazy redraw:** grid redraws asynchronously after Save+GO -> the T3 `Node Row Should Exist`
  awaits the row element (`Wait For Elements State visible 20s`) before the assert.
- **Op PU date-filtering:** the Op Production Unit dropdown offers only PUs effective at the form Start
  Date -> Start Date = 2000-01-01 (proven to offer the first-available nav PU).

## 5. IUD plan
- INSERT: New Object -> Code/Name/Start Date + Calculation Sequence Number + Op Production Unit(=nav PU) -> Save -> GO.
- UPDATE: select row -> edit Node Name (updateAttributes) -> Save -> GO.
- DELETE: select row -> End Date = Start Date -> Save -> GO (true delete from OV_NODE).
- Test data: `AUTOTEST_ND_<timestamp>`; self-clean = absent in OV_NODE after End=Start; 0 residual re-read.

## 6. Deliverables
- Playwright driver `py/node_iud.py`; RF T3 `pageobjects/.../Calculation_Objects/node_page.resource`;
  RF suite `tests/.../Calculation_Objects/node_iud.robot`; this SOW; `VERIFY-REPORT.md` (auto-generated
  by `scripts/verify_screen.py` from real exit codes/pass counts).
