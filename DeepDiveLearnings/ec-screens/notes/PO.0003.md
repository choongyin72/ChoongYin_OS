# PO.0003 - Daily Water Stream Status

_Deep-dive 2026-07-05 (deterministic runner). Module: PO._

## Identity
- BF_CODE: PO.0003 - URL: `/com.ec.prod.po.screens/daily_stream_status/CLASS_NAME/STRM_DAY_STREAM_MEAS_WAT/CLASS_NAME_DETAIL/STRM_DAY_STREAM_DER_WAT`

## DB binding (metadata-resolved)
| Class | Type/Scope | Base table | View |
|---|---|---|---|
| `STRM_DAY_STREAM_MEAS_WAT` | DATA/DAY | `STRM_DAY_STREAM` | `DV_STRM_DAY_STREAM_MEAS_WAT` |
| `STRM_DAY_STREAM_DER_WAT` | DATA/DAY | `V_STRM_DAY_DER_STREAM` | `DV_STRM_DAY_STREAM_DER_WAT` |

_Resolved by: url CLASS_NAME_

## Screen type
N1 daily-status grid

## Help (screen screenshot -- local online-help corpus 14.2.5)
![PO.0003 screenshot](PO.0003_shot_1.png)
![PO.0003 screenshot](PO.0003_shot_2.png)

## Help (field-description images -- local online-help corpus 14.2.5)
_(no field-description images in corpus for this BF_CODE)_
