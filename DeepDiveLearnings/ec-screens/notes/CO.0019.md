# CO.0019 - Facility Class 1

_Deep-dive 2026-06-22 (deterministic runner). Module: CO._

## Identity
- BF_CODE: CO.0019 - URL: `/com.ec.frmw.co.screens/manage_object_groupmodel_nav/GROUPMODEL/FCTY_CLASS_1/TARGET/FCTY_CLASS_1/CLASS_NAME/FCTY_CLASS_1`

## DB binding (metadata-resolved)
| Class | Type/Scope | Base table | View |
|---|---|---|---|
| `FCTY_CLASS_1` | OBJECT/VERSIONED | `PRODUCTION_FACILITY` | `OV_FCTY_CLASS_1` |

## Screen type
OV (master-data object)

## Help (description)
This is a generic screen; see description of generic screens in the beginning of the configuration manual.

Facility class 1 is the first of two generic facility classes in EC. Facility class 1 is always used, while facility class 2 might not be used. Facility class 1 should represent facilities near the wells. It can be a steel jacket production facility, FPSO vessel, onshore area with processing capabilities or another area covering production wells. The objects of facility class 1 do not need to be real physical facilities, but they often are.

Access to data in EC is often controlled by facility class 1 objects. This is implemented in the group model navigator where staff for a facility only can access their own data. Facility class 1 is only included in the operational group model and not in the geographical group model. Above facility class 1 in the operational tree, we can typical
