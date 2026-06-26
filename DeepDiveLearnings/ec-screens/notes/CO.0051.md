# CO.0051 - Well Hole

_Deep-dive 2026-06-26 (deterministic runner). Module: CO._

## Identity
- BF_CODE: CO.0051 - URL: `/com.ec.frmw.co.screens/manage_object_groupmodel_nav/GROUPMODEL/WELL_HOLE/TARGET/WELL_HOLE/CLASS_NAME/WELL_HOLE`

## DB binding (metadata-resolved)
| Class | Type/Scope | Base table | View |
|---|---|---|---|
| `WELL_HOLE` | OBJECT/VERSIONED | `WELL_HOLE` | `OV_WELL_HOLE` |

## Screen type
OV (master-data object)

## Help (description)
This is a generic screen; see description of generic screens in the beginning of the configuration manual.

A well hole is a physical hole in the ground that is defined by a casing head or integrity boundary. The Well hole may contain one or more production/injection tubings, each being defined as wells in EC. The class well hole can have transactional event data associated with it. These are normally focusing on measurements that are used for well hole integrity control, such as various casing head pressures. The well hole concept is also used for grouping two or more wells (production/injection tubings) together and therefore serves as a common replacement for physical terms like "drillfloor hatch", "well slot", "well riser". It is optional to use well hole concept in EC.
