# CO.0042 - Production Separator

_Deep-dive 2026-06-26 (deterministic runner). Module: CO._

## Identity
- BF_CODE: CO.0042 - URL: `/com.ec.frmw.co.screens/manage_object_groupmodel_nav/GROUPMODEL/PRODSEPARATOR/TARGET/PRODSEPARATOR/CLASS_NAME/PRODSEPARATOR`

## DB binding (metadata-resolved)
| Class | Type/Scope | Base table | View |
|---|---|---|---|
| `PRODSEPARATOR` | OBJECT/VERSIONED | `SEPARATOR` | `OV_PRODSEPARATOR` |

## Screen type
OV (master-data object)

## Help (description)
Production separator is used to process oil, gas and water under normal operations. Data gathered here is typically temperature and pressure readings for the separator.

Any outgoing metered streams are modeled as streams and are therefore not a data class for the production separator.
