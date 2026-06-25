# CO.0038 - Tank Usage

_Deep-dive 2026-06-24 (deterministic runner). Module: CO._

## Identity
- BF_CODE: CO.0038 - URL: `/com.ec.prod.co.screens/tank_usage`

## DB binding (metadata-resolved)
| Class | Type/Scope | Base table | View |
|---|---|---|---|
| (no class resolved from URL/LABEL) | | | |

## Screen type
unknown (no class resolved)

## Help (description)
The Tank Usage Screen is used to connect Tanks to Storages. A tank can be connected to several Storages at the same time. The connection to the Storage is time controlled, where each Tank-Storage (tank usage) connection will have daytime and an end date. The end date can be empty.

The group navigator is used for navigation down to Storage. The Tank dropdown will include all Tanks in the system regardless of navigator choices. The Tank History data section shows all previous connections for the selected tank that have ended and the Other Storage Connection data section shows other current storage connection for the tank chosen in the first data section.
