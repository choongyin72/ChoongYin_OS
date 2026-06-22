# PO.0002 — Daily Gas Stream Status

_Deep-dive 2026-06-22 (screen #1, template). Module: PO — Production Operations._

## Identity
- **BF_CODE:** PO.0002
- **Name:** Daily Gas Stream Status
- **URL:** `/com.ec.prod.po.screens/daily_stream_status/CLASS_NAME/STRM_DAY_STREAM_MEAS_GAS/CLASS_NAME_DETAIL/STRM_DAY_STREAM_DER_GAS`
- **Treeview:** EC Production → (Daily, by Stream) → Daily Gas Stream Status

## Help (in-session `openOnlineHelp()`)
> This BF is used when daily gas stream data is available. Data can be entered manually or loaded
> automatically. The BF requires **one entry per stream per day**, and EC **automatically creates new records
> for a new production day** for all gas streams that are part of a **stream set** for this screen — i.e. it has
> **value instantiation at Day start** (a blank line for every measured gas stream is inserted). A project can
> set up several instances of this screen by passing the correct **stream data class** as a treeview parameter.
> The second section lists **derived streams** (calculated).

## DB binding
| Section | Class | CLASS_TYPE | TIME_SCOPE | Base table | Object view |
|---|---|---|---|---|---|
| Measured (top grid) | `STRM_DAY_STREAM_MEAS_GAS` | DATA | DAY | `STRM_DAY_STREAM` | `OV_STRM_DAY_STREAM_MEAS_GAS` |
| Derived (lower grid) | `STRM_DAY_STREAM_DER_GAS` | DATA | DAY | `V_STRM_DAY_DER_STREAM` | `OV_STRM_DAY_STREAM_DER_GAS` |

Day-status data physically lives in **`STRM_DAY_STREAM`** keyed by stream object + production day (DAYTIME).

## Screen type & behaviour
- **N1 daily-status grid** (CLASS_TYPE=DATA + TIME_SCOPE=DAY). **UPDATE-only** — New/Delete don't apply; one
  (stream × day) row is **batch-instantiated** at day start, you **edit-in-place** the measured value
  (set / change / clear→NULL). Clearing+Save nulls the column (update-to-null, NOT a record delete).
- **Navigator** (from the live screen): Date + **Production Unit** + **Area** + **Facility Class 1** (all yellow =
  mandatory) → **GO** (`button:form:B`) loads the pre-instantiated rows. Two stacked grids: measured then derived.
- Self-clean for any automation = restore the original cell value.

## Business purpose / where it sits
Daily capture of **gas stream** measurements (the per-stream daily production record) — the upstream input that
feeds stream allocation (`STRM_DAY_ALLOC*`) and downstream gas accounting. "Measured" = entered/loaded;
"Derived" = EC-calculated from the measured + config. Configurable per **stream set** so projects run several
instances (Pluto, Scarborough, etc.) off the same BF by swapping the stream data class in the treeview.

## Cross-refs
- Sibling: PO.0001 Daily Oil Stream Status, PO Daily Oil Stream Status - Mass. Same N1 pattern, different class.
- Pattern doc: `ec-automation/docs/ec_screen_registry.md` (N1 type); [[reference_db_design]].
- Method note: **Help only opens in-session** — open the screen then `openOnlineHelp()`; direct `help.jsf?screenId=` → **Forbidden**.
