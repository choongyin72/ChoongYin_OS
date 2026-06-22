# CO.0007 - Product

_Deep-dive 2026-06-22 (deterministic runner). Module: CO._

## Identity
- BF_CODE: CO.0007 - URL: `/com.ec.frmw.co.screens/manage_object_nav/CLASS_NAME/PRODUCT`

## DB binding (metadata-resolved)
| Class | Type/Scope | Base table | View |
|---|---|---|---|
| `PRODUCT` | OBJECT/VERSIONED | `PRODUCT` | `OV_PRODUCT` |

## Screen type
OV (master-data object)

## Help (description)
This is a generic screen; see description of generic screens in the beginning of the configuration manual.

Product is the final product being sold. It can be crude oil, condensate, butane and more. Product is associated with storage, a storage has one product and all tanks connected to the storage have the same product.

Note! Transport specific attributes will not be available if only EC Production is installed.
