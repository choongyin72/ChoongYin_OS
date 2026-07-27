# OV Non-Bank Targets - the 55 OV-GM object screens beyond the 71

**Scope:** OV (`CLASS_TYPE=OBJECT`) screens NOT in the 71 Bank-layout list and not yet automated.
Grouped by NAVIGATOR pattern (owner's recipe `tmp/ov_gm_55_nav_recipe.xlsx`). Build order = easiest first.
Nav values resolved FIRST-AVAILABLE live (recipe gives the nav *shape*, not hardcoded P1/SS1).
Two OV flavours: **manage-object** (grid `manage_object_nav_nav:form:T_data` + GO) vs **custom-URL**
(grid `nav:form:T_data`, no GO, toolbar Refresh) - recon each; engine `click_go` now does GO-or-Refresh.

**Legend:** [x] done+verified · [~] driver-proven/partial · [ ] pending · (P) parked (reason).

## A. No navigator (manage-object no-cascade OR custom-URL)  (17)
**Progress: 1/55 done.**

| BF | Screen | OV_ view | Folder | Status |
|---|---|---|---|---|
| CD.0008 | Stream Item | OV_STREAM_ITEM | Assets > Stream Objects | [ ] |
| CD.0109 | Document Sequence | OV_DOC_SEQUENCE | Assets > Revenue Document Objects | [ ] |
| CO.0021 | Facility Class 2 | OV_FCTY_CLASS_2 | Assets > Facility Objects | [ ] |
| CO.0100 | Production Sub Unit | OV_PROD_SUB_UNIT | Assets > Basic Objects | [ ] |
| CO.0102 | Constant Standard | OV_CONSTANT_STANDARD | Assets > Hydrocarbon Objects | [ ] |
| CO.0158 | Report Group | OV_REPORT_GROUP | Assets > Facility Objects | [ ] |
| CO.0191 | Task Process | OV_TASK_PROCESS | Task List | [ ] |
| CO.0193 | Action Trigger | OV_CONTROL_POINT | Business Action | [ ] |
| CO.0227 | External Location | OV_EXTERNAL_LOCATION | Assets > Facility Objects | [ ] |
| CO.0264 | Truck | OV_TRUCK | Assets > Transport Objects | [ ] |
| CO.0265 | Trailer | OV_TRAILER | Assets > Transport Objects | [ ] |
| CO.0266 | Driver | OV_DRIVER | Assets > Transport Objects | [ ] |
| CO.1033 | Production Day Table | OV_PRODUCTION_DAY | System | [ ] |
| CO.1049 | Conversion Group | OV_CONVERSION_GROUP | System > Units | [x] Conversion Group #TBD (custom-URL OV) |
| CO.1060 | Calculation Library | OV_CALC_LIBRARY | Assets > Calculation Objects | [ ] |
| CO.2038 | Contract Area Setup | OV_CONTRACT_AREA_SETUP | Assets > Contract Objects | [ ] |
| FC.0010 | Forecast | OV_FORECAST_GROUP | Forecasting | [ ] |

## B. Production Unit + Area + Facility Class 1  (20)
| BF | Screen | OV_ view | Folder | Status |
|---|---|---|---|---|
| CD.0006 | Node | OV_NODE | Assets > Calculation Objects | [ ] |
| CO.0034 | Storage | OV_STORAGE | Assets > Tank and Storage Objects | [ ] |
| CO.0040 | Test Separator | OV_TESTSEPARATOR | Assets > Facility Objects | [ ] |
| CO.0042 | Production Separator | OV_PRODSEPARATOR | Assets > Facility Objects | [ ] |
| CO.0049 | Well | OV_WELL | Assets > Well and Reservoir Objects | [ ] |
| CO.0051 | Well Hole | OV_WELL_HOLE | Assets > Well and Reservoir Objects | [ ] |
| CO.0070 | Chemical Tank | OV_CHEM_TANK | Assets > Chemical Objects | [ ] |
| CO.0108 | Well Hookup | OV_WELL_HOOKUP | Assets > Facility Objects | [ ] |
| CO.0123 | Test Device | OV_TEST_DEVICE | Assets > Equipment Objects | [ ] |
| CO.0212 | Chemical Injection Point | OV_CHEM_INJ_POINT | Assets > Chemical Objects | [ ] |
| CO.0224 | Shift | OV_SHIFT | Assets > Facility Objects | [ ] |
| CO.0258 | Chemical Stream | OV_CHEM_STREAM | Assets > Chemical Objects | [ ] |
| CO.0260 | Chemical Stream Hookup | OV_CHEM_STRM_HOOKUP | Assets > Chemical Objects | [ ] |
| CO.2004 | Lifting Account | OV_LIFTING_ACCOUNT | Assets > Transport Objects | [ ] |
| CO.2077 | Channel | OV_CHANNEL | Assets > Transport Objects | [ ] |
| CO.2078 | Loading Arm | OV_LOADING_ARM | Assets > Transport Objects | [ ] |
| CO.2079 | Pilot | OV_PILOT | Assets > Transport Objects | [ ] |
| CO.2080 | Tug Boat | OV_TUG_BOAT | Assets > Transport Objects | [ ] |
| CO.2081 | Pilot Boat | OV_PILOT_BOAT | Assets > Transport Objects | [ ] |
| CP.0030 | Cargo Planning Forecast | OV_FCST_MNGR_FCST_LIST | Cargo Planning > Forecast | [ ] |

## C1. Business Unit only  (5)
| BF | Screen | OV_ view | Folder | Status |
|---|---|---|---|---|
| CO.2103 | Service | OV_SERVICE | Assets > Service Objects | [ ] |
| CO.3009 | Price Index | OV_PRICE_INDEX | Assets > Sales Objects | [ ] |
| CO.3016 | Price Object | OV_PRICE_OBJECT | Assets > Sales Objects | [ ] |
| CO.3024 | Price Rate | OV_PRICE_RATE | Assets > Sales Objects | [ ] |
| SP.0059 | Property | OV_PROPERTY | Assets > Data Mapping Objects | [ ] |

## C2. Business Unit + Contract Area  (5)
| BF | Screen | OV_ view | Folder | Status |
|---|---|---|---|---|
| CO.2016 | Contract | OV_CONTRACT | Assets > Contract Objects | [ ] |
| CO.2044 | Contract Capacity | OV_CONTRACT_CAPACITY | Assets > Contract Objects | [ ] |
| CO.2054 | Contract Inventory | OV_CONTRACT_INVENTORY | Assets > Contract Objects | [ ] |
| RC.0058 | Division Order | OV_DIVISION_ORDER | Royalty > Royalty USA | [ ] |
| RC.0059 | Royalty Contract | OV_ROYALTY_CONTRACT | Royalty > Royalty Canada | [ ] |

## D. Production Unit + Area  (3)
| BF | Screen | OV_ view | Folder | Status |
|---|---|---|---|---|
| CO.0019 | Facility Class 1 | OV_XFCTY_CLASS_1 | Assets > Facility Objects | [ ] |
| CO.0205 | Collection Point | OV_COLLECTION_POINT | Assets > Facility Objects | [ ] |
| CO.0244 | Operator Route | OV_OPERATOR_ROUTE | Assets > Facility Objects | [ ] |

## E. Well hierarchy  (2)
| BF | Screen | OV_ view | Folder | Status |
|---|---|---|---|---|
| CO.0054 | Well Bore | OV_WELL_BORE | Assets > Well and Reservoir Objects | [ ] |
| CO.0247 | Planned Well | OV_PLANNED_WELL | Assets > Well and Reservoir Objects | [ ] |

## E3. Well hierarchy (deepest)  (2)
| BF | Screen | OV_ view | Folder | Status |
|---|---|---|---|---|
| CO.0057 | Well Bore Interval | OV_WELL_BORE_INTERVAL | Assets > Well and Reservoir Objects | [ ] |
| CO.0153 | Perforation Interval | OV_PERF_INTERVAL | Assets > Well and Reservoir Objects | [ ] |

## F. Functional Area  (1)
| BF | Screen | OV_ view | Folder | Status |
|---|---|---|---|---|
| CO.0236 | Message Group | OV_MESSAGE_GROUP | Messaging | [ ] |
