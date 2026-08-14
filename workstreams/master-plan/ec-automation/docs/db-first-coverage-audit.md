# DB-First Coverage Audit - OBJECT-type classes not yet automated

Generated 2026-08-03 via `SELECT class_name FROM CLASS_CNFG WHERE CLASS_TYPE='OBJECT'` (295 total), cross-referenced against every tracking doc to find genuinely unautomated classes, then live-verified for a real EC UI screen. Excludes 45 `TEST_*` framework scaffolding classes, 17 `IMP_*` interface/import config classes, and 3 `X`-prefixed shadow classes (`XAREA`/`XPRODUCTIONUNIT`/`XWELL`) already covered under their base class name, and 1 `INVALID_PACKAGE_TEST` (no LABEL, test-only).

**Has EC Screen legend:** `Yes` = confirmed real screen exists (live-verified, or shipped) - `Maybe` = an exact live label match exists but has NOT been cross-checked for a label collision with a different class (2 confirmed collisions already found and marked `No`: FORECAST_TRAN_CP, INVENTORY_PRICE_OBJECT) - `Unclear` = related screens exist under a different title, needs manual investigation (this is exactly how both shipped screens were found - see JOURNAL.md for Contact Group Set / Remote Endpoint Configuration) - `No` = no related screens found live, likely backend/config-only, or a confirmed label collision.

**Summary:** 73 classes total - 7 Yes (2 shipped, 2 found-but-complex, 3 confirmed 2026-08-14 as Phase 4 pilot candidates: FINANCIAL_ITEM, COST_MAPPING, COST_MAPPING_NAV) - 2 No (both label collisions) - 64 Unclear (need manual title investigation, same method as the 2 shipped screens)

| Class | Label | Time Scope | Base Table | Rows | Has EC Screen | Notes |
|---|---|---|---|---|---|---|
| ALLOC_NETWORK | Allocation Network | VERSIONED | CALC_COLLECTION | 37 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| ALLOC_NETWORK_GROUP | Allocation Network Group | VERSIONED | CALC_COLLECTION | 3 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| CALC_PROCESS_ELEMENT | Calculation Process Element | VERSIONED | CALC_PROCESS_ELEMENT | 1077 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| CALC_PROCESS_TRANSITION | Calculation Process Transition | VERSIONED | CALC_PROCESS_TRANSITION | 1041 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| CNTR_CAPACITY_LIST | Contract Capacity List | VERSIONED | CONTRACT_CAPACITY | 47 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| COMPANY_CAP_RELEASE | Company Capacity Release | VERSIONED | COMPANY | 1210 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| CONFIG_VARIABLE_PARAM | Configuration Variable Param | VERSIONED | CONFIG_VARIABLE_PARAM | 91 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| CONTACT_GROUP | Contact Group | VERSIONED | CONTACT_GROUP | 11 | Unclear | Related screens found, no exact-label match: Maintain Contact Group Set - needs manual title investigation |
| CONTACT_GROUP_SET | Contact Group Set | VERSIONED | CONTACT_GROUP | 9 | Yes | SHIPPED - PR #354 (CO.0225), real title 'Maintain Contact Group Set' |
| CONTRACT_CAPACITY_RESULT | Contract Capacity Result | VERSIONED | CONTRACT_CAPACITY | 47 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| CONTRACT_CAP_RELEASE | Contract Capacity Release | VERSIONED | CONTRACT | 102 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| CONTRACT_DOC | Contract Document | VERSIONED | CONTRACT_DOC | 33 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| CONTRACT_GROUP | Contract Group | VERSIONED | CALC_COLLECTION | 8 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| CONVERSION_CONTEXT | Conversion Context | INVARIANT | ENUMERATION | 7 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| COST_MAPPING | Data Mapping | VERSIONED | COST_MAPPING | 2 | Yes | CONFIRMED 2026-08-14 (Phase 4 pilot recon) - **Project Data Mapping Setup** is a real, IUD-capable OV screen (objectForm, 21 fields, 5 mandatory: Code/Name/Start Date/Mapping Type/Data Entry Source/Dataset-Report; Insert enabled/Delete disabled; grid id not auto-detected by the classifier, needs manual recon before building). **Project Data Mapping** (no "Setup") is a DIFFERENT, separate N-family status screen with a 4-level mandatory navigator cascade and toolbar Insert DISABLED - not IUD-capable, do not confuse the two. Project Data Mapping Accrual not investigated. |
| COST_MAPPING_NAV | Data Mapping | VERSIONED | COST_MAPPING | 2 | Yes | Same class family as COST_MAPPING above - see that row for the confirmed screen split. |
| ENDPOINT_CONFIG | Endpoint configuration | INVARIANT | ENDPOINT_CONFIG | 5 | Yes | SHIPPED - PR #355 (CO.1082), real title 'Remote Endpoint Configuration' |
| ENTRY_DELIVERY_POINT | Entry Delivery Point | VERSIONED | DELIVERY_POINT | 15 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| EXIT_DELIVERY_POINT | Exit Delivery Point | VERSIONED | DELIVERY_POINT | 19 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| FINANCIAL_ITEM | Financial Item | VERSIONED | FINANCIAL_ITEM | 23 | Yes | CONFIRMED 2026-08-14 (Phase 4 pilot recon) - two real, distinct, IUD-capable screens under this family: **Financial Item Definition** (OV, custom-URL, grid `manageObject:form:T_data`, no navigator, Insert enabled/Delete disabled) and **Financial Item Template** (TV, grid `templ:form:T_data`, Insert+Delete both enabled). Daily Financial Item/Daily Financial Item Calculation/Monthly Financial Item are separate N-family status screens (Insert/Delete disabled), not IUD-capable, not investigated further. |
| FIN_ACCOUNT_MAP_NAV | Fin Account Mapping Nav | VERSIONED | FIN_ACCOUNT_MAPPING | 75 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| FIN_AFE | AFE | VERSIONED | FIN_OBJECTS | 0 | Unclear | Related screens found, no exact-label match: Daily Safety, Health and Environment - needs manual title investigation |
| FIN_ITEM_GROUP | Financial Item Group | VERSIONED | CALC_COLLECTION | 3 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| FORECAST | Quantity Forecast Case | VERSIONED | FORECAST | 2 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| FORECAST_COMPARISON | Forecast Comparison Object | VERSIONED | FCST_COMPARISON | 3 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| FORECAST_PROD | Scenario | VERSIONED | FORECAST | 16 | Unclear | Related screens found, no exact-label match: Forecast and Scenarios; Forecast Compare Scenario - Direct; Forecast Compare Scenario - Graphical; Forecast Define Scenarios to Compare; Forecast Scenario Curves - needs manual title investigation |
| FORECAST_SALE_PR | Price Forecsast | VERSIONED | FORECAST | 2 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| FORECAST_SALE_SA | Forecsast Sale Sa | VERSIONED | FORECAST | 2 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| FORECAST_SALE_SD | Forecsast Sale Sd | VERSIONED | FORECAST | 3 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| FORECAST_TRAN_CP | Cargo Planning Forecast | VERSIONED | FORECAST | 5 | No | Label collides with already-shipped Cargo Planning Forecast (CP.0030, different class) - no own screen |
| FORECAST_TRAN_FC | Forecast Fc | VERSIONED | FORECAST | 0 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| INVENTORY | Inventory | VERSIONED | INVENTORY | 27 | Unclear | Related screens found, no exact-label match: Contract Inventory; Daily Contract Inventory Matrix; Daily Contract Location Inventory; Daily Contract Location Inventory - Contract Swap; Daily Contract Location Inventory - Location Swap - needs manual title investigation |
| INVENTORY_FIELD | Inventory Field | VERSIONED | INVENTORY_FIELD | 49 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| INVENTORY_PRICE_OBJECT | Price Object | VERSIONED | PRODUCT_PRICE | 113 | No | Label collides with already-shipped Price Object (CO.3016, different class) - no own screen |
| LINE_ITEM_TEMPLATE | Line Item Template | VERSIONED | LINE_ITEM_TEMPLATE | 93 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| MESSAGE_CONTACT | Contact | VERSIONED | COMPANY_CONTACT | 27 | Unclear | Related screens found, no exact-label match: Company Contact; Maintain Contact Group Set - needs manual title investigation |
| MESSAGE_DEFINITION | Message definition | VERSIONED | MESSAGE_DEFINITION | 8 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| METER_FREQUENCY | Meter Frequency | INVARIANT | ENUMERATION | 15 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| NOMINATION_POINT_ALLOC | Nomination Point Alloc List | VERSIONED | NOMINATION_POINT | 39 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| NOMINATION_POINT_LIST | Nomination Point List | VERSIONED | NOMINATION_POINT | 169 | Unclear | Related screens found, no exact-label match: Nomination Point Profit Centre Company List; Nomination Point Profit Centre List - needs manual title investigation |
| PRICE_GROUP | Price Group | VERSIONED | CALC_COLLECTION | 2 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| PRODUCT_COUNTRY | Product Country | VERSIONED | PRODUCT_COUNTRY | 19 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| PRODUCT_COUNTRY_BOE | Product Country | VERSIONED | PRODUCT_COUNTRY | 22 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| PRODUCT_FIELD | Product Field | VERSIONED | PRODUCT_FIELD | 19 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| PRODUCT_FIELD_BOE | Product Field | VERSIONED | PRODUCT_FIELD | 1 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| PRODUCT_NODE | Product Node | VERSIONED | PRODUCT_NODE | 19 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| PRODUCT_NODE_BOE | Product Node | VERSIONED | PRODUCT_NODE | 1 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| PRODUCT_WELL | Product Well | VERSIONED | PRODUCT_WELL | 0 | Unclear | Related screens found, no exact-label match: Daily Production Flowline and Well Status 1; Daily Production Well Forecast; Daily Production Well Hookup and Well Status 1; Daily Production Well Status 1; Daily Production Well Status 2 - needs manual title investigation |
| PRODUCT_WELL_BOE | Product Well | VERSIONED | PRODUCT_WELL | 0 | Unclear | Related screens found, no exact-label match: Daily Production Flowline and Well Status 1; Daily Production Well Forecast; Daily Production Well Hookup and Well Status 1; Daily Production Well Status 1; Daily Production Well Status 2 - needs manual title investigation |
| PROD_STREAM_GROUP | Product Stream Group | VERSIONED | CALC_COLLECTION | 3 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| PROJECT | Project | VERSIONED | CONTRACT | 1 | Unclear | Related screens found, no exact-label match: Project Data Entry; Project Data Extract; Project Data Extract Accrual; Project Data Extract By Year; Project Data Extract Connection - needs manual title investigation |
| REPORT_REFERENCE | Report Reference Object | VERSIONED | REPORT_REFERENCE | 127 | Yes | Real screen 'Report Reference' confirmed live - needs Dataset popup-picker nav, not built |
| REPORT_REF_GROUP | Report Reference Group Object | VERSIONED | REPORT_REF_GROUP | 1 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| REPORT_REF_ITEM | Report Reference Item | VERSIONED | REPORT_REF_ITEM | 2 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| REPT_CONTEXT | Reporting context | VERSIONED | REPT_CONTEXT | 5 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| REVN_CONTRACT | Revenue Contract | VERSIONED | CONTRACT | 74 | Unclear | Related screens found, no exact-label match: Revenue Contract Attributes - needs manual title investigation |
| REVN_DATA_FILTER | Data Filter | VERSIONED | REVN_DATA_FILTER | 12 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| REVN_PROD_STREAM | Revenue Stream | VERSIONED | CONTRACT | 11 | Unclear | Related screens found, no exact-label match: Revenue Stream Category; Revenue Stream Category Setup - needs manual title investigation |
| REVN_RPT_TABLE | Revenue Report Table | VERSIONED | REVN_RPT_TABLE | 0 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| REVN_RPT_TBL_SET | Revenue Table Set | VERSIONED | REVN_RPT_TBL_SET | 0 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| SALE_CONTRACT | Sale Contract | VERSIONED | CONTRACT | 62 | Unclear | Related screens found, no exact-label match: Sale Contract Attributes - needs manual title investigation |
| SCENARIO | Scenario | VERSIONED | SCENARIO | 35 | Yes | Real screen 'Scenario Manager' confirmed live - same complex forecast-manager family as shipped Cargo Planning Forecast, not built |
| SCENARIO_BATCH | Scenario Batch | VERSIONED | SCENARIO_BATCH | 10 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| SND_WELL_GROUP | Well Group | VERSIONED | SND_GROUP | 0 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| SND_WELL_GROUP_STREAM | Well Group Stream | VERSIONED | SND_GROUP_STREAM | 0 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| SOURCE_SYSTEM | Source System | VERSIONED | SOURCE_SYSTEM | 0 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| SPLIT_KEY | Split Key | VERSIONED | SPLIT_KEY | 109 | Unclear | Related screens found, no exact-label match: Company Split Key; Company Split Key Shares; Daily Split Key Company; Daily Split Key Field; Daily Split Key Other - needs manual title investigation |
| TIME_ZONE_REGION | Time zone | INVARIANT | ENUMERATION | 9 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| TRANSACTION_TEMPLATE | Transaction Template | VERSIONED | TRANSACTION_TEMPLATE | 58 | Unclear | Related screens found, no exact-label match: Transactional Inventory Template - needs manual title investigation |
| TRANSPORT_ZONE_LIST | Transport Zone List | VERSIONED | TRANSPORT_ZONE | 9 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| TRAN_CONTRACT | Transport Contracts | VERSIONED | CONTRACT | 63 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| TRAN_CONTRACT_LIST | Tran Contract List | VERSIONED | CONTRACT | 63 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
| UNIT_CONTEXT | System of Measurement | INVARIANT | ENUMERATION | 4 | Unclear | No related screens found live - likely backend/config-only, not confirmed |
