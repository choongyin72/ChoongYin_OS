# CO.0077 - Initiate Day

_Deep-dive 2026-06-28 (deterministic runner). Module: CO._

## Identity
- BF_CODE: CO.0077 - URL: `/com.ec.prod.co.screens/initiate_day`

## DB binding (metadata-resolved)
| Class | Type/Scope | Base table | View |
|---|---|---|---|
| (no class resolved from URL/LABEL) | | | |

## Screen type
unknown (no class resolved)

## Help (description)
The initiate day screen contains a button that invokes the instantiation that is configured as EC codes using the code_type INITIATE_DAY. The instantiation procedures run might also be procedures instantiating for other product areas like transport and sales. This will then be configured equally as EC codes within the respective product area.

By default two stored procedures for production instantiation are configured in EC codes to be run by this button:

ec_bs_instantiate.new_day_start(start_date): This procedure creates a new date in a table holding only valid production dates. This happens at the beginning of the production day.

ec_bs_instantiate.new_day_end(start_date,end_date): This procedure creates a new record for all classes and objects having instantiation. If a new object has been defined effective back in time, you must rerun this process manually to include this new objec
