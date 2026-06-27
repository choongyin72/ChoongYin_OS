# CO.0039 - Tank Strapping

_Deep-dive 2026-06-26 (deterministic runner). Module: CO._

## Identity
- BF_CODE: CO.0039 - URL: `/com.ec.prod.co.screens/tank_strapping`

## DB binding (metadata-resolved)
| Class | Type/Scope | Base table | View |
|---|---|---|---|
| `TANK_STRAPPING` | DATA/EVENT | `TANK_STRAPPING` | `DV_TANK_STRAPPING` |

## Screen type
DATA/EVENT

## Help (description)
The concept of tank strapping tables is used to calculate the tank's volume, based on a level dip. This is a lookup table, and any number of lookup points may be modified at any time, allowing for modeling non-linear correlations between dip level and volume.

The Tank Strapping Table screen provides an interface for specifying the storage volume on a specific dip level on a tank. A tank can have several dip levels. The storage volume and dip levels are being used for calculation of the total volume of the tank. A storage volume and a dip level are time dependent, which implies that the size of the tank is time dependent. Please note that the storage volume in this context is the tank inventory volume and has nothing to do with the Object Class Storage.

The group navigator on the top (see snapshot) is used for navigation down to the tank object where tank strapping will be performed. Th
