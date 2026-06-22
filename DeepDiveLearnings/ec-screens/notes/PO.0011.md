# PO.0011 - Daily Equipment Status

_Deep-dive 2026-06-22 (deterministic runner). Module: PO._

## Identity
- BF_CODE: PO.0011 - URL: `/com.ec.prod.po.screens/daily_equipment_status`

## DB binding (metadata-resolved)
| Class | Type/Scope | Base table | View |
|---|---|---|---|
| `EQPM_DAY_STATUS` | DATA/DAY | `EQPM_DAY_STATUS` | `DV_EQPM_DAY_STATUS` |

## Screen type
N1 daily-status grid

## Help (description)
This BF is used to keep track of equipment status. This list of equipment is configurable and Energy Components creates one new record for each item of equipment for a production day.

Only equipment having attribute "equipment status screen" set to YES will appear in this screen. The drop-down lists are configurable.
