# CO.0055 - Well Bore Split

_Deep-dive 2026-06-27 (deterministic runner). Module: CO._

## Identity
- BF_CODE: CO.0055 - URL: `/com.ec.prod.co.screens/well_bore_split`

## DB binding (metadata-resolved)
| Class | Type/Scope | Base table | View |
|---|---|---|---|
| `WELL_BORE_SPLIT_FACTOR` | DATA/EVENT | `WEBO_SPLIT_FACTOR` | `DV_WELL_BORE_SPLIT_FACTOR` |

## Screen type
DATA/EVENT

## Help (description)
In order to determine production volumes pr well bore, a set of split factors is used. The allocation routine will allocate data down to the well (production tubing) level.

The reservoir allocation will read these allocated data as well as the split factors. These are then used within the calculations to calculate total production/injection from/to each reservoir block formation. Each phase (oil, gas, water, condensate, steam, gas injection and water injection) has its separate set of split factors that must add up to 100% over all active well bores.

Two situations may require the use of the well bore splits in EC:

If the customer wants to allocate down to reservoir zones or reservoir block/formations

If the customer needs to have shrinkage calculations (e.g. in well testing) based on reservoir fluid quality stream data. In this case, the connection between well and fluid properties 
