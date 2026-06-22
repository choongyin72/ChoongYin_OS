# CO.0010 - Hydrocarbon Component

_Deep-dive 2026-06-22 (deterministic runner). Module: CO._

## Identity
- BF_CODE: CO.0010 - URL: `/com.ec.prod.co.screens/hydrocarbon_component`

## DB binding (metadata-resolved)
| Class | Type/Scope | Base table | View |
|---|---|---|---|
| `HYDROCARBONCOMPONENT_REF` | TABLE/EVENT | `HYDROCARBON_COMPONENT` | `TV_HYDROCARBONCOMPONENT_REF` |
| `HYDROCARBON_COMPONENT` | TABLE/EVENT | `HYDROCARBON_COMPONENT` | `TV_HYDROCARBON_COMPONENT` |

## Screen type
TV (table-class)

## Help (description)
Hydrocarbon Components is a class holding all components used by EC. Typical components are C1, C2, C3, iC4, nC4, C5+. The component having + includes all heavier components as well.

Hydrocarbon Components is a table class and not an object class. That means that the list of Hydrocarbon Components does not have a START_DATE or END_DATE, all components are valid forever. Which components that should be used is controlled in the BF Component Set List.

The Mol. Wt values for components are updated referring to GPA Midstream Standard 2145-16.
