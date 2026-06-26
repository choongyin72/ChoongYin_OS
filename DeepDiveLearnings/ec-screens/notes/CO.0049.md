# CO.0049 - Well

_Deep-dive 2026-06-26 (deterministic runner). Module: CO._

## Identity
- BF_CODE: CO.0049 - URL: `/com.ec.prod.co.screens/manage_object_groupmodel_well/GROUPMODEL/WELL/TARGET/WELL/CLASS_NAME/WELL`

## DB binding (metadata-resolved)
| Class | Type/Scope | Base table | View |
|---|---|---|---|
| `WELL` | OBJECT/VERSIONED | `WELL` | `OV_WELL` |

## Screen type
OV (master-data object)

## Help (description)
This is a generic screen; see description of generic screens in the beginning of the configuration manual.

A well in EC is the physical string located at the surface or seabed. There is a quite extensive list of screens in EC for registering data against wells.

A well in EC will only have one single fluid flow tubing head with associated instrumentation. If there are two or more fluid flow tubing heads with separate instrumentation sets, they should be configured as two or more wells sharing the same well hole.

Examples of data that can be relevant to register or calculate for a well in EC:

- well head sensor data like temperature, pressure and choke position

- well bottom hole sensor data like temperature and pressure

- well rate data, multiphase metering, gas lift data, pump data

- production tests and test results.

- theoretical production and injection, volume or mass

- allo
