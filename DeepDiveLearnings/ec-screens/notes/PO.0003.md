# PO.0003 — Daily Water Stream Status

_Deep-dive 2026-06-22. Module: PO. Water twin of [PO.0002](PO.0002.md) (gas) / [PO.0001](PO.0001.md) (oil)._

## Identity
- **BF_CODE:** PO.0003 · **URL:** `/com.ec.prod.po.screens/daily_stream_status/CLASS_NAME/STRM_DAY_STREAM_MEAS_WAT/CLASS_NAME_DETAIL/STRM_DAY_STREAM_DER_WAT`
- Treeview: EC Production → Daily (by Stream) → Daily Water Stream Status

## Help (description)
> Used when daily **water** stream data is available (manual or auto-loaded). One entry per stream per day; EC
> auto-creates records for a new production day for all water streams in the stream set (blank line per measured
> water stream at Day start). Second section = **derived streams** — calculated on the fly, not editable.

## DB binding
| Section | Class | Type/Scope | Base | View |
|---|---|---|---|---|
| Measured | `STRM_DAY_STREAM_MEAS_WAT` | DATA/DAY | `STRM_DAY_STREAM` | `OV_STRM_DAY_STREAM_MEAS_WAT` |
| Derived | `STRM_DAY_STREAM_DER_WAT` | DATA/DAY | `V_STRM_DAY_DER_STREAM` | `OV_STRM_DAY_STREAM_DER_WAT` |

## Type & behaviour
**N1 daily-status grid** (UPDATE-only; edit-in-place). Same shape as PO.0001/PO.0002; phase = water.

## Pattern note (PO.0001/0002/0003)
The three Daily *phase* Stream Status screens are one BF (`daily_stream_status`) parameterised by the stream
data class (`STRM_DAY_STREAM_MEAS_{OIL|GAS|WAT}` + `..._DER_{..}`). All write to **`STRM_DAY_STREAM`**, all are
N1 daily-status, measured-editable + derived-readonly. Projects spin up instances per stream set via the treeview param.
