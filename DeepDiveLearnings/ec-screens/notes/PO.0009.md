# PO.0009 - Environmental Events

_Deep-dive 2026-06-22 (deterministic runner). Module: PO._

## Identity
- BF_CODE: PO.0009 - URL: `/com.ec.prod.po.screens/environmental_events`

## DB binding (metadata-resolved)
| Class | Type/Scope | Base table | View |
|---|---|---|---|
| `FCTY_SPILL_EVENT` | DATA/DAY | `FCTY_SPILL_EVENT` | `DV_FCTY_SPILL_EVENT` |

## Screen type
N1 daily-status grid

## Help (description)
This BF is used to keep track of environmental events. Event types are configurable and the user can create as many events as needed within a production day.

The user can also decide whether the event should be included in the daily report or not by ticking off the report check box.
