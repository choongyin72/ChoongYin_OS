# CO.0001 - Production Unit

_Deep-dive 2026-06-22 (deterministic runner). Module: CO._

## Identity
- BF_CODE: CO.0001 - URL: `/com.ec.frmw.co.screens/manage_object_nav/CLASS_NAME/PRODUCTIONUNIT`

## DB binding (metadata-resolved)
| Class | Type/Scope | Base table | View |
|---|---|---|---|
| `PRODUCTIONUNIT` | OBJECT/VERSIONED | `GEOGRAPHICAL_AREA` | `OV_PRODUCTIONUNIT` |

## Screen type
OV (master-data object)

## Help (description)
This is a generic screen; see description of generic screens in the beginning of the configuration manual.

Production unit is part of the operational group model. It is used to aggregate data to production unit level and to navigate down to data starting from production unit level in the navigator.

Production unit does not have any data classes. It's also optional, and does not need to be configured for small operations.
