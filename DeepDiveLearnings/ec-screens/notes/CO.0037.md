# CO.0037 - Maintain Tanks

_Deep-dive 2026-06-24 (deterministic runner). Module: CO._

## Identity
- BF_CODE: CO.0037 - URL: `/com.ec.frmw.co.screens/manage_copy_object/GROUPMODEL/TANK/TARGET/TANK/CLASS_NAME/TANK`

## DB binding (metadata-resolved)
| Class | Type/Scope | Base table | View |
|---|---|---|---|
| `TANK` | OBJECT/VERSIONED | `TANK` | `OV_TANK` |

## Screen type
OV (master-data object)

## Help (description)
This is a generic screen; see description of generic screens in the beginning of the configuration manual.

This screen retrieves records from the Tank class. The version that is valid within the specified values in the navigator will be displayed. It displays all enabled attributes of Tank object. The screen provides the ease to update more than one record at the same time. It also allows creation of a new Tank as a copy of an existing Tank. To Copy a Tank, select the well to copy from and then enter the new Tank Name, Tank Code, and Start Date, and then hit Create a Copy button. If the Tank has Tank Usage connections, it will automatically be included in the copy job.
