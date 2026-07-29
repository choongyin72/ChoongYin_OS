# SOW - Chemical Tank IUD (Configuration > Assets > Chemical Objects > Chemical Tank)

## 1. Screen identity
- **Screen:** Chemical Tank   **BF code:** CO.0070   **View:** `OV_CHEM_TANK`   **Base:** `CHEM_TANK`
- **Type:** OV-GM (manage-object, groupmodel) - grid `manageObject:form:T_data`, navigator-GATED. Sibling of Node.
- **Date-effective:** YES (VERSIONED) -> DELETE = End Date = Start Date.

## 2. Navigator (gated)
`nav:form:G:0:R:1:C:1..3:dd` = Production Unit -> Area -> Facility Class 1; filled first-available + GO
(capability `apply_ovgm_navigator` / `Apply OV-GM Navigator First Available`).

## 3. New-Object form (scanned; fields BY LABEL)
| Field | Label | Mandatory | Kind |
|---|---|---|---|
| Code | Chemical Tank Code | yes | text |
| Name | Chemical Tank Name | yes | text |
| Start Date | Start Date | yes | date |
| **Measure unit** | Measure unit | **yes** | dropdown (first-available) |
| Op Production Unit | Op Production Unit | no* | dropdown (first-available) |

*Set first-available for grid visibility (probe per screen - the nav PU is not necessarily a valid Op PU option; see Node).

## 4. IUD plan
INSERT: New Object -> Code/Name/Start Date + Measure unit + Op Production Unit -> Save -> GO.
UPDATE: select row -> edit Chemical Tank Name -> Save -> GO. DELETE: End Date = Start Date -> Save -> GO.
Test data `AUTOTEST_CT_<timestamp>`; self-clean = absent in OV_CHEM_TANK; 0 residual re-read.

## 5. Deliverables
Driver `py/chemical_tank_iud.py`; T3 `pageobjects/.../Chemical_Objects/chemical_tank_page.resource`;
suite `tests/.../Chemical_Objects/chemical_tank_iud.robot`; this SOW; `VERIFY-REPORT.md` (auto-generated).
