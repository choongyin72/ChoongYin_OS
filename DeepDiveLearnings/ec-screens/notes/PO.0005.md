# PO.0005 — Daily Tank Status

_Deep-dive 2026-06-22. Module: PO. Distinct from the stream-status screens (tank inventory, not stream flow)._

## Identity
- **BF_CODE:** PO.0005 · **URL:** `/com.ec.prod.po.screens/daily_tank_status_1`
- Treeview: EC Production → Daily (by Tank) → Daily Tank Status

## Help (description)
> Used when daily **tank volume** data — or only **strapping height** (single product) — is available. EC
> auto-creates a new record per production day for all tanks with **tank meter frequency = "DAY"**. For tanks
> with **frequency = "EVENT"** there is **no auto-instantiation** — the user must **press Insert** and pick the
> tank from the dropdown. All data is treated as the **closing tank reading at end of production day** (no time
> component on the reading).

## DB binding
| Class | Type/Scope | Base table | View |
|---|---|---|---|
| `TANK_DAY_STATUS` | DATA / DAY | `TANK_MEASUREMENT` | `OV_TANK_DAY_STATUS` |

Related derived/inventory views: `DV_TANK_DAY_INV_VOL` / `_INV_MASS` / `_INV_OIL`, `DV_TANK_DAY_DIP_STATUS`,
`DV_TANK_DAY_DETAILS`, `DV_TANK_DAY_SINGLE_WELL`.

## Type & behaviour — important nuance vs the stream screens
N1 daily-status (DATA/DAY) **BUT not purely UPDATE-only**: it's a **hybrid** — DAY-frequency tanks are
auto-instantiated (edit-in-place, like the stream screens), whereas **EVENT-frequency tanks support manual
INSERT** (toolbar Insert + tank dropdown). So toolbar New may be **enabled** here (unlike the stream-status
grids). Reading = closing inventory at production-day end. Self-clean: restore edited values; for any
test-inserted EVENT tank row, delete it.

## Cross-ref
First PO screen seen where the N1 daily-status pattern allows record INSERT (frequency-driven) — note for the
screen registry: "tank/EVENT-frequency status grids can insert; stream/DAY-frequency grids are update-only."
