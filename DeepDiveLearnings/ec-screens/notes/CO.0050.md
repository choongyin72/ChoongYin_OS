# CO.0050 - Maintain Wells

_Deep-dive 2026-06-26 (deterministic runner). Module: CO._

## Identity
- BF_CODE: CO.0050 - URL: `/com.ec.frmw.co.screens/manage_copy_object_well/GROUPMODEL/WELL/TARGET/WELL/CLASS_NAME/WELL`

## DB binding (metadata-resolved)
| Class | Type/Scope | Base table | View |
|---|---|---|---|
| `WELL` | OBJECT/VERSIONED | `WELL` | `OV_WELL` |

## Screen type
OV (master-data object)

## Help (description)
This is a generic screen; see description of generic screens in the beginning of the configuration manual.

This screen retrieves records from the Well class. The version that is valid within the specified values in the navigator will be displayed. It displays all enabled attributes of Well object. The screen provides the ease to update more than one record at the same time. It also allows creation of a new Well as a copy of an existing Well. To copy a well, select the well to copy from and then enter the new Well Name, Well Code, and Start Date, then hit Create a Copy button. If the well has sub-surface configuration down to reservoir, it will automatically be included in the copy job.
