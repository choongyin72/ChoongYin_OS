# PO.0001 — Daily Oil Stream Status

_Deep-dive 2026-06-22. Module: PO. Oil twin of [PO.0002](PO.0002.md) (gas)._

## Identity
- **BF_CODE:** PO.0001 · **URL:** `/com.ec.prod.po.screens/daily_stream_status/CLASS_NAME/STRM_DAY_STREAM_MEAS_OIL/CLASS_NAME_DETAIL/STRM_DAY_STREAM_DER_OIL`
- Treeview: EC Production → Daily (by Stream) → Daily Oil Stream Status

## Help (description)
> Used when daily **oil** stream data is available (manual or auto-loaded). One entry per stream per day; EC
> auto-creates records for a new production day for all oil streams in the stream set (value instantiation at
> Day start = blank line per measured oil stream). Second section = **derived streams** — *calculated on the
> fly, not editable*; derived-stream config is done in the **Stream Form**.

## DB binding
| Section | Class | Type/Scope | Base | View |
|---|---|---|---|---|
| Measured | `STRM_DAY_STREAM_MEAS_OIL` | DATA/DAY | `STRM_DAY_STREAM` | `OV_STRM_DAY_STREAM_MEAS_OIL` |
| Derived | `STRM_DAY_STREAM_DER_OIL` | DATA/DAY | `V_STRM_DAY_DER_STREAM` | `OV_STRM_DAY_STREAM_DER_OIL` |

## Type & behaviour
**N1 daily-status grid** (UPDATE-only; edit-in-place). Nav: Date + Production Unit + Area + Facility Class → GO.
Measured grid editable; derived grid read-only (calculated). Same shape as PO.0002; only the phase (oil) differs.
