# OV IUD sweep — PARKED screens (revisit later)

_Recorded 2026-07-26 during the autonomous OV IUD sweep. Rule: BUILD only plain Bank-layout OV
(`manage_object_nav`, single Date+GO nav, mandatory = Code/Name/Start Date only, **no mandatory
dropdowns**, opens via the standard menu-search → tv-link gesture). Anything else is parked here with
the reason, verified by recon (not assumed)._

Sweep result: **14 built** this session (Port/Berth/Canal + 11 generator-scaffolded → PRs #203–#216),
**17 parked** below. Classification came from `tmp/batch_recon.py` (live read-only form-open per screen)
plus individual recon for Storage Flow and Deferment Group.

**Update 2026-07-26 (PRs #219–#233):** the mandatory-dropdown-fill capability (`select_dropdown` +
`Fill OV Dropdown By Label`, including the `__FIRST__` cascade-fallback from #229) unparked 13/14 of
section A, all of section B, and section C (Deferment Group's "gesture" issue was transient — plain
menu-search → tv-link worked once built). Only Chemical Product remains parked.

## A. Mandatory reference dropdown(s) — engine has no mandatory-dropdown fill yet (14)
| Screen | BF | View | Mandatory dropdown(s) |
|---|---|---|---|
| Storage Flow | CO.2091 | OV_STORAGE_FLOW | Flow Direction, Storage — ✅ done 2026-07-26 (#229, `__FIRST__` cascade) |
| Input List | CD.0035 | OV_STREAM_ITEM_COLLECTION | List Category — ✅ done 2026-07-26 (#219) |
| HCB System | CD.0097 | OV_BALANCE | HCB Category — ✅ done 2026-07-26 (#220) |
| UOP Key | CD.0099 | OV_FIN_UOP_DEPR_KEY | Company, Key Type — ✅ done 2026-07-26 (#230) |
| EC Code Object | CD.0135 | OV_EC_CODE_OBJECT | EC Code Type, EC Code — ✅ done 2026-07-26 (#234, `__FIRST__` cascade) |
| Chemical Product | CO.0072 | OV_CHEM_PRODUCT | Meas. Units — still parked |
| Orifice Plate | CO.0089 | OV_ORIFICE_PLATE | Material — ✅ done 2026-07-26 (#223) |
| Meter Run | CO.0091 | OV_METER_RUN | Type of Taps, Pipe Material, Location of Taps — ✅ done 2026-07-26 (#226) |
| Process Train | CO.0120 | OV_PROCESS_TRAIN | Production Facility Class 1 — ✅ done 2026-07-26 (#231, `__FIRST__` cascade) |
| Reservoir Block Formation | CO.0137 | OV_RESV_BLOCK_FORMATION | Reservoir Block, Reservoir Formation — ✅ done 2026-07-27 (#235 driver + #238 RF suite fix): verify_screen OVERALL PASS, all 5 gates green (robocop 0, dryrun 5/5, LIVE RF 5/5 DB-verified 0 residual, Playwright driver 15/15) |
| Calculation Group Context | CO.0245 | OV_CALC_GRP_CONTEXT | Calculation Group Object Class, Calculation Group List Class — ✅ done 2026-07-26 (#232, `__FIRST__` cascade) |
| Config Variable | IN.0031 | OV_CONFIG_VARIABLE | Calculation Context — ✅ done 2026-07-26 (#222) |
| Data Extract Setup | SP.0043 | OV_SUMMARY_SETUP | Data Extract Type — ✅ done 2026-07-26 (#224) |
| Data Extract Set | SP.0049 | OV_SUMMARY_SET | Owner Class — ✅ done 2026-07-26 (#225) |

**To unpark:** add mandatory-dropdown fill to the engine/T2 (`Select EC Dropdown Option` by label →
match `data-item-label`), then feed the dropdown label+value through the generator config.

## B. Extra mandatory non-dropdown field — buildable with a small generator tweak (2)
| Screen | BF | View | Extra mandatory field |
|---|---|---|---|
| Document Template | CD.0013 | OV_DOC_TEMPLATE | Document Title (text) — ✅ done 2026-07-26 (#227) |
| Transactional Inventory Properties | IN.0023 | OV_TRANS_INVENTORY | Sequence Number — ✅ done 2026-07-26 (#228) |

**To unpark:** extend `tmp/gen_ov_screen.py` + driver INSERT_FIELDS to accept extra mandatory
text/number fields (the label resolver already supports it; only the fixed 3-field insert keyword needs widening).

## C. Does not open via the standard gesture — needs manual label/nav check (1)
| Screen | BF | View | Issue |
|---|---|---|---|
| Deferment Group | CO.0149 | OV_DEFERMENT_GROUP | menu-search → tv-link `Deferment Group` not found by that exact label; confirm the real menu label / whether it is gated before building — ✅ done 2026-07-26 (#233 — issue was transient, plain menu-search → tv-link worked) |

**To unpark:** open the screen manually, capture the exact tv-link label (or the gated navigator), then build.
