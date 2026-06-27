# CO.0040 - Test Separator

_Deep-dive 2026-06-26 (deterministic runner). Module: CO._

## Identity
- BF_CODE: CO.0040 - URL: `/com.ec.frmw.co.screens/manage_object_groupmodel_nav/GROUPMODEL/TESTSEPARATOR/TARGET/TESTSEPARATOR/CLASS_NAME/TESTSEPARATOR`

## DB binding (metadata-resolved)
| Class | Type/Scope | Base table | View |
|---|---|---|---|
| `TESTSEPARATOR` | OBJECT/VERSIONED | `SEPARATOR` | `OV_TESTSEPARATOR` |

## Screen type
OV (master-data object)

## Help (description)
This is a generic screen; see description of generic screens in the beginning of the configuration manual.

Test separator is used to test a well or a set of wells. It is used to determine the well potential, as most well normally are not metered. The test separator is a one stage separation and there are normally three outgoing metered streams, oil, gas and water. Because the test separator normally operates under pressure much higher than atmosphere, some of the gas remains in the oil phase. This is compensated for using shrinkage factors to shrink the oil and gas in solution factors to increase the gas amount to derive results as close to standard conditions as possible.
