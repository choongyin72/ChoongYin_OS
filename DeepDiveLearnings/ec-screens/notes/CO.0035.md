# CO.0035 - Maintain Storages

_Deep-dive 2026-06-24 (deterministic runner). Module: CO._

## Identity
- BF_CODE: CO.0035 - URL: `/com.ec.frmw.co.screens/manage_copy_object/GROUPMODEL/STORAGE/TARGET/STORAGE/CLASS_NAME/STORAGE`

## DB binding (metadata-resolved)
| Class | Type/Scope | Base table | View |
|---|---|---|---|
| `STORAGE` | OBJECT/VERSIONED | `STORAGE` | `OV_STORAGE` |

## Screen type
OV (master-data object)

## Help (description)
This is a generic screen; see description of generic screens in the beginning of the configuration manual.

This screen retrieves records from the Storage class. The version that is valid within the specified values in the navigator will be displayed. It displays all enabled attributes of Storage object. The screen provides the ease to update more than one record at the same time. It also allows creation of a new Storage as a copy of an existing Storage. To copy a Storage, select the Storage to copy from and then enter the new Storage Name, Storage Code, and Start Date, then hit Create a Copy button.
