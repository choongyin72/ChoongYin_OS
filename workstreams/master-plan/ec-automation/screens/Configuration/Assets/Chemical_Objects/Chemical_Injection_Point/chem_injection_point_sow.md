# SOW - Chemical Injection Point IUD (Configuration > Assets > Chemical Objects)

## 1. Identity
- **Screen:** Chemical Injection Point   **BF:** CO.0212   **View:** `OV_CHEM_INJ_POINT`   **Base:** `CHEM_INJ_POINT`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED. Sibling of Node.
- **Date-effective:** YES (VERSIONED) -> DELETE = End Date = Start Date.

## 2. Navigator (gated)
`nav:form:G:0:R:1:C:1..3:dd` = Production Unit -> Area -> Facility Class 1; first-available + GO.

## 3. New-Object form (scanned; BY LABEL)
| Field | Label | Mandatory | Kind |
|---|---|---|---|
| Code | Chem Inj Point Code | yes | text |
| Name | Chem Inj Point Name | yes | text |
| Start Date | Start Date | yes | date |
| Op Production Unit | Op Production Unit | no | dropdown (first-available, grid visibility) |

## 4. IUD plan
INSERT -> UPDATE (Name) -> DELETE (End=Start). Test data `AUTOTEST_CIP_<timestamp>`; self-clean = absent in
OV_CHEM_INJ_POINT; 0 residual re-read.

## 5. Deliverables
Driver `py/chem_injection_point_iud.py`; T3 `pageobjects/.../Chemical_Objects/chem_injection_point_page.resource`;
suite `tests/.../Chemical_Objects/chem_injection_point_iud.robot`; this SOW; `VERIFY-REPORT.md`.
