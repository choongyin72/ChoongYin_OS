# CO.0070 - Chemical Tank

_Deep-dive 2026-06-28 (deterministic runner). Module: CO._

## Identity
- BF_CODE: CO.0070 - URL: `/com.ec.frmw.co.screens/manage_object_groupmodel_nav/GROUPMODEL/CHEM_TANK/TARGET/CHEM_TANK/CLASS_NAME/CHEM_TANK`

## DB binding (metadata-resolved)
| Class | Type/Scope | Base table | View |
|---|---|---|---|
| `CHEM_TANK` | OBJECT/VERSIONED | `CHEM_TANK` | `OV_CHEM_TANK` |

## Screen type
OV (master-data object)

## Help (description)
A chemical tank object is a representation of a physical chemical tank used for chemical storage or hooked up to chemical injection lines and pumps. The object can also represent a virtual tank for movable and interchangeable tanks.

Measurement / input data

The input data is for a selected chemical tank is:

Tank level volume as NET volume
Comments

Chemical tank calculations

The chemical tank object has settings for calculations performed on a chemical tank as:

Available volume
Chemical tank rate (drainage rate)
Remaining days to empty

The following properties can be set in the chemical tank object:

Min Fill Volume(only available in full version)
Under plate volume(adjust available volume for the volume beneath the drain)
dVol limit(only available in full version)
No. dV less than Limit to set rate 0(only available in ful version)

The chemical tank rate is based on dV/dt where dV
