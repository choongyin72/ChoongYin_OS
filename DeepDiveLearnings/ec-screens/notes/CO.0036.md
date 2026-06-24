# CO.0036 - Tank

_Deep-dive 2026-06-24 (deterministic runner). Module: CO._

## Identity
- BF_CODE: CO.0036 - URL: `/com.ec.frmw.co.screens/manage_object_groupmodel_nav/GROUPMODEL/TANK/TARGET/TANK/CLASS_NAME/TANK`

## DB binding (metadata-resolved)
| Class | Type/Scope | Base table | View |
|---|---|---|---|
| `TANK` | OBJECT/VERSIONED | `TANK` | `OV_TANK` |

## Screen type
OV (master-data object)

## Help (description)
This is a generic screen; see the description of generic screens in the beginning of the configuration manual.

Tanks are used to store Products from the oil and gas production, and not Chemical Products. Products and Chemical Products are not the same.

Tanks can have a single product, like propane or sulfur, but Tanks can also have oil which contains more or less water in the oil or as a free water layer in the bottom of the tank. Tanks in EC can, therefore, be for either one single product or for two products where one have to be water.

Tanks having the same product are normally connected to Storage. Reporting from Storage will automatically sum all Tank data and report total Storage. However, Storage is a logical grouping of Tanks and Storage do not have its own data. One Tank can, in fact, belong to more than one Storage at the same point in time. This could be handy for reporting 
