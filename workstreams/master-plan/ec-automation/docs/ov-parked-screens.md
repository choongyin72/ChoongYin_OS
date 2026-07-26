# OV IUD sweep — PARKED screens (revisit later)

_Recorded 2026-07-26 during the autonomous OV IUD sweep. Rule: BUILD only plain Bank-layout OV
(`manage_object_nav`, single Date+GO nav, mandatory = Code/Name/Start Date only, **no mandatory
dropdowns**, opens via the standard menu-search → tv-link gesture). Anything else is parked here with
the reason, verified by recon (not assumed)._

Sweep result: **14 built** this session (Port/Berth/Canal + 11 generator-scaffolded → PRs #203–#216),
**17 parked** below. Classification came from `tmp/batch_recon.py` (live read-only form-open per screen)
plus individual recon for Storage Flow and Deferment Group.

## A. Mandatory reference dropdown(s) — engine has no mandatory-dropdown fill yet (14)
| Screen | BF | View | Mandatory dropdown(s) |
|---|---|---|---|
| Storage Flow | CO.2091 | OV_STORAGE_FLOW | Flow Direction, Storage |
| Input List | CD.0035 | OV_STREAM_ITEM_COLLECTION | List Category |
| HCB System | CD.0097 | OV_BALANCE | HCB Category |
| UOP Key | CD.0099 | OV_FIN_UOP_DEPR_KEY | Company, Key Type |
| EC Code Object | CD.0135 | OV_EC_CODE_OBJECT | EC Code Type, EC Code |
| Chemical Product | CO.0072 | OV_CHEM_PRODUCT | Meas. Units |
| Orifice Plate | CO.0089 | OV_ORIFICE_PLATE | Material |
| Meter Run | CO.0091 | OV_METER_RUN | Type of Taps, Pipe Material, Location of Taps |
| Process Train | CO.0120 | OV_PROCESS_TRAIN | Production Facility Class 1 |
| Reservoir Block Formation | CO.0137 | OV_RESV_BLOCK_FORMATION | Reservoir Block, Reservoir Formation |
| Calculation Group Context | CO.0245 | OV_CALC_GRP_CONTEXT | Calculation Group Object Class, Calculation Group List Class |
| Config Variable | IN.0031 | OV_CONFIG_VARIABLE | Calculation Context |
| Data Extract Setup | SP.0043 | OV_SUMMARY_SETUP | Data Extract Type |
| Data Extract Set | SP.0049 | OV_SUMMARY_SET | Owner Class |

**To unpark:** add mandatory-dropdown fill to the engine/T2 (`Select EC Dropdown Option` by label →
match `data-item-label`), then feed the dropdown label+value through the generator config.

## B. Extra mandatory non-dropdown field — buildable with a small generator tweak (2)
| Screen | BF | View | Extra mandatory field |
|---|---|---|---|
| Document Template | CD.0013 | OV_DOC_TEMPLATE | Document Title (text) |
| Transactional Inventory Properties | IN.0023 | OV_TRANS_INVENTORY | Sequence Number |

**To unpark:** extend `tmp/gen_ov_screen.py` + driver INSERT_FIELDS to accept extra mandatory
text/number fields (the label resolver already supports it; only the fixed 3-field insert keyword needs widening).

## C. Does not open via the standard gesture — needs manual label/nav check (1)
| Screen | BF | View | Issue |
|---|---|---|---|
| Deferment Group | CO.0149 | OV_DEFERMENT_GROUP | menu-search → tv-link `Deferment Group` not found by that exact label; confirm the real menu label / whether it is gated before building |

**To unpark:** open the screen manually, capture the exact tv-link label (or the gated navigator), then build.
