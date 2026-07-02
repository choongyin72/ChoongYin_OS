# CO.0072 - Chemical Product

_Deep-dive 2026-06-28 (deterministic runner). Module: CO._

## Identity
- BF_CODE: CO.0072 - URL: `/com.ec.frmw.co.screens/manage_object_nav/CLASS_NAME/CHEM_PRODUCT`

## DB binding (metadata-resolved)
| Class | Type/Scope | Base table | View |
|---|---|---|---|
| `CHEM_PRODUCT` | OBJECT/VERSIONED | `CHEM_PRODUCT` | `OV_CHEM_PRODUCT` |

## Screen type
OV (master-data object)

## Help (description)
This is a generic screen; see description of generic screens in the beginning of the configuration manual.

Chemical products are chemicals used in conjunction with production or injection of hydrocarbons. It is not produced products and it will not be accounted for in the allocation. Chemical products can be used at many facilities and it can be associated with chemical tanks. It is possible to calculate total inventory of a chemical product for a particular facility. This number can then be used to flag a need to reorder chemical products.

Total inventory for a chemical product can be reported in one unit, even if tanks having the product are measured in other units.

Vendor company is populated in the dropdown if a company is selected as a Chemical Vendor in Company (CO.0013).

LogPow is LogPow i.e. the log(10) of Partition coefficient of Octanol and Water i.e. LogPow = log (Co / Cw)
