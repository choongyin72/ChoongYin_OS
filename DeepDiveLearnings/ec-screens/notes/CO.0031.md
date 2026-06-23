# CO.0031 - Flowline

_Deep-dive 2026-06-23 (deterministic runner). Module: CO._

## Identity
- BF_CODE: CO.0031 - URL: `/com.ec.frmw.co.screens/manage_object_groupmodel_nav/GROUPMODEL/FLOWLINE/TARGET/FLOWLINE/CLASS_NAME/FLOWLINE`

## DB binding (metadata-resolved)
| Class | Type/Scope | Base table | View |
|---|---|---|---|
| `FLOWLINE` | OBJECT/VERSIONED | `FLOWLINE` | `OV_FLOWLINE` |

## Screen type
OV (master-data object)

## Help (description)
A flowline is a line connecting subsea well templates to facilities. It can also be used to model onshore flowlines connecting wells to a gathering station.

The relation between well and flowline is a many to many. Therefore this connection is not held in the group model.
