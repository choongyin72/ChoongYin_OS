# CO.0067 - Flowline Well Connection

_Deep-dive 2026-06-27 (deterministic runner). Module: CO._

## Identity
- BF_CODE: CO.0067 - URL: `/com.ec.prod.co.screens/flowline_well_conn`

## DB binding (metadata-resolved)
| Class | Type/Scope | Base table | View |
|---|---|---|---|
| `FLOWLINE_WELL_CONN` | DATA/EVENT | `FLOWLINE_SUB_WELL_CONN` | `DV_FLOWLINE_WELL_CONN` |

## Screen type
DATA/EVENT

## Help (description)
This Business function allows connection between wells and flowlines. One well can be attached to more than one flowline and one flowline can be connected to more than one well. This BF has mandatory navigation till facility class 1. There are also two additional non-mandatory dropdown filters which are flowline and well to allow filtering either by well or flowline or both.

First data section allows to create new connection and display all filtered connections based on navigator's from andto date. These connections have a start and end daytime, where end daytime is exclusive.

Second Data section provides all historical connections to the specific well selected in data section 1.
