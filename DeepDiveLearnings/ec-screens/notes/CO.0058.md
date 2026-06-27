# CO.0058 - Well Bore Interval Split

_Deep-dive 2026-06-27 (deterministic runner). Module: CO._

## Identity
- BF_CODE: CO.0058 - URL: `/com.ec.prod.co.screens/well_bore_interval_split`

## DB binding (metadata-resolved)
| Class | Type/Scope | Base table | View |
|---|---|---|---|
| `WELL_BORE_INTERVAL_SPLIT` | DATA/EVENT | `WEBO_INTERVAL_GOR` | `DV_WELL_BORE_INTERVAL_SPLIT` |

## Screen type
DATA/EVENT

## Help (description)
Like split factors are used for splitting well volumes to well bores, well bore volumes are further split down to their perforation intervals, using these split factors. The allocation routine will allocate data down to the well (production tubing) level. The reservoir allocation will read these allocated data as well as the well bore and well bore interval split factors. These are then used within the calculations to calculate total production/injection from/to each reservoir block formation. Each phase (oil, gas, water, condensate, steam, gas inj and water inj) has its separate set of split factors that must add up to 100% over all active well bore intervals.

Two situations may require the use of the well bore interval split concept in EC:

If the customer wants to allocate down to reservoir zones or reservoir block/formations

If the customer needs to have shrinkage calculations (e.g
