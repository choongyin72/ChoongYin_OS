# Service (CO.2103) - recon COMPLETE, build not started. Resume point for item 2.

Everything below is executed-command output or a file read, not inference. Nothing has been written to the
sandbox for this screen - all recon was read-only.

## Identity
| fact | value | source |
|---|---|---|
| BF code | `CO.2103` | `docs/ov-non-bank-targets.md:61` (step-0 check) |
| view | `OV_SERVICE` (58 columns, 43 rows) | DB |
| class | `SERVICE`, `CLASS_TYPE=OBJECT` -> OV | `class_cnfg` via scanner |
| treeview | `Configuration > Assets > Service Objects > Service` | scanner |
| folder | `Configuration/Assets/Service_Objects` (3 segments -> import depth 4) | treeview |
| family | **OV-GM**, grid `manageObject:form:T_data` | scanner, stable 3/3 runs |

## Navigator (gated)
`Date` | `Business Unit` C:1 (16 options, **the only mandatory one**) | `Contract Area` C:2 | `Contract` C:3

- ⚠ **Do NOT call `apply_ovgm_navigator` with the default `levels=4`** - C:3 exists but has ZERO options for
  the first-available BU, and the engine raises `RuntimeError: dropdown has no options`. Only C:1 is
  mandatory; the grid renders with C:1 alone.
- ⚠ **Do NOT use first-available for the BU.** `EC LNG Norway` (alphabetically first) owns NO contract areas
  or contracts - its cascade children are empty, so a Service row could never list under it.

## The scope trap (this is what would have wasted a live run)
`OV_SERVICE` has **no business-unit column**. A row's scope comes from `CONTRACT_ID`. All 43 existing rows
use contracts under contract area `TS3_FIRM`, which belongs to Business Unit `TS3_BU1`. So with
first-available everywhere, the navigator would sit on `EC LNG Norway` while the form's Contract dropdown
(88 unscoped options) picked `Albritton 15H-1 Division Order` - the row saves fine and NEVER lists.
That is exactly how Message Group failed.

## Values to use - labels resolved from codes (dropdowns show NAMES, the DB stores CODES)
| field | label to select | code in DB | source |
|---|---|---|---|
| nav Business Unit | `TS3 BU1` | `TS3_BU1` | `OV_BUSINESS_UNIT` |
| Contract (form) | `TS3 GTA Shipper A` | `TS3_GTA_SHP_A` | `OV_CONTRACT` |
| Transport System (form) | `TS3 Transport System` | `TS3_SYSTEM` | `OV_TRANSPORT_SYSTEM` |

Mirror row: `TS3_SHIPPER_A_P2P` -> template `TS3_ALLOC_SERVICE_TEMPLATE`, type `P2P` /
`POINT_TO_POINT`, status NULL, contract `TS3_GTA_SHP_A`, transport system `TS3_SYSTEM`.

## Insert form - 8 mandatory fields (scanner, live)
`Service Code` (text) | `Service Name` (text) | `Start Date` (date) | `Service Template` (dd) |
`Service Type` (dd) | `Service Status` (dd) | `Contract` (dd) | `Transport System` (dd)
Optional: End Date, Start/End Segment, Chargeable, Use Tolerance, Revenue Attribution x2, Comments,
Description, Enable Supplementary.

- All 8 have options under the applied scope - verified, so the screen IS insertable.
- Template / Type / Status are NOT scope-relevant -> `__FIRST__` is acceptable for them. Contract and
  Transport System MUST be the explicit values above.
- ⚠ Use start date **2003-01-01** (`TEST_START_DATE_REFDD`), not 2000-01-01: reference dropdowns only offer
  objects effective at the form's start date. This cost me a false "engine defect" on Area today.
- Noted, not chased: `STATUS_CODE` is NULL in every existing row although the UI marks Service Status
  mandatory.

## What the generator still needs (the actual remaining work)
`gen_ovgm.py` forces `__FIRST__` everywhere and always calls `apply_ovgm_navigator(page)` with `levels=4`.
Two opt-in capabilities are needed, in BOTH layers (Playwright driver AND RF T3/suite):
1. `nav_value` - select an explicit value in nav C:1 instead of first-available, plus `nav_levels` to stop
   the cascade at level 1.
2. explicit values in `extra_dropdowns` - accept `["Label", "Value"]` pairs as well as plain labels.
Then: generate -> `verify_screen` live -> package -> no-loss diff -> PR with every touched file listed.

## Recon scripts (all read-only, committed)
`tmp/recon_service_dds.py` (nav labels + every mandatory dd's options under scope),
`tmp/recon_service_scope.py` (existing row shape + columns), `tmp/recon_service_bu.py` (contract -> area ->
BU chain), `tmp/resolve_service_labels.py` + `_labels2.py` + `tmp/find_views.py` (code -> label resolution),
`tmp/scan_service_thrice.py` (scanner stability).
