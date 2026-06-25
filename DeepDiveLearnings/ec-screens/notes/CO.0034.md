# CO.0034 - Storage

_Deep-dive 2026-06-24 (deterministic runner). Module: CO._

## Identity
- BF_CODE: CO.0034 - URL: `/com.ec.frmw.co.screens/manage_object_groupmodel_nav/GROUPMODEL/STORAGE/TARGET/STORAGE/CLASS_NAME/STORAGE`

## DB binding (metadata-resolved)
| Class | Type/Scope | Base table | View |
|---|---|---|---|
| `STORAGE` | OBJECT/VERSIONED | `STORAGE` | `OV_STORAGE` |

## Screen type
OV (master-data object)

## Help (description)
Storage is a logical concept in EC, holding all tanks having the same product and purpose. One example of a storage object can be CRUDE_EXPORT, which holds all tanks having Crude and are available for export. That storage does not include dehydration tanks or other tanks not direct available for export. Other examples can be CRUDE_DEHY, which holds all dehydration tanks, or COND_EXPORT, which holds all condensate export tanks.

Storage is used in the cargo business functions. All parcels lifted must be from storage and not from individual tanks (even if that is what physically happens). Storage is also used to keep track of over / under lifting per lifting account.

Storage can also be used for reporting purpose only. Rather than report on individual tanks, storage will automatically include all tanks connected and report totals.

Storage is connected to facility, either facility class 1
