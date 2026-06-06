# DOC-05 — EC Revenue + EC Sales
**Source:** EC 14.2.4 `revn` (13) + `sale` (5) = 18 pages · **Read:** 2026-06-06

## A. EC SALES

### Business areas
**GS** (Gas Sales) with sub-areas: **SD** Sales Dispatching (capacity booking, nominations, delivery follow-up), **PR** Price Determination, **SA** Sales Allocation, **TR** Trading (portfolio/risk/deal capture). Plus **GP** Gas Purchase, **OS** Oil Sales.

### Sales Allocation (SA)
Follows up **contractual commitments on quantities**. Built on the **EC Contract Concept**: Contract → **Sales Calculation Rule Sets** → **Contract Accounts** → results stored as **Contract Account Quantities** (daily/monthly/yearly). Rules configured as **equations** (calc framework) referencing contract attributes. E.g. "Monthly Off Spec Qty" account computed from delivery quantities + off-spec events.

### Price Determination (PR)
Unit prices from **price indices** + contractual rules. **Price Object** (based on a **Price Concept** = named set of **price elements**, e.g. CIF = Cost+Insurance+Freight) → **Price Calculation Rule Sets** → results to **Contract Price List** / **Product Price List**. Price objects point to a product or product+contract, with currency/UOM/timespan/calc-rule/seq.

### Config
- System attr `ALLOW_SALE_CALC_LOCK_MTH` (N) — block sales calc on locked months.
- Many `Instantiate *` system properties (in `ctrl_property_meta`, default Y) — pre-create empty daily/monthly/yearly records (deliveries, price index/rate, contract status).
- "Allow re-running of approved Sales calculation" (N).

## B. EC REVENUE

### Document validation lifecycle 🔑
**OPEN → VALID1 → VALID2 → TRANSFER → BOOKED.** Booking Period set when moved to TRANSFER. Must get all docs to BOOKED before closing a booking period. (Analogous to the P/V/A status model but for financial docs.)

### Key system attributes (CO.1012)
`ACNT_LOGIC_DATE_METHOD` (DOC_DATE vs TRANS_DATE — which version of fin_account mappings to use) · `ALIGN_REPORTING_BOOKING` · `ALLOW_BATCH_OPTION` (Batch/Now prompt on transfer) · `CASCADE_BOE_FACT_CHANGE` (AUTO/MANUAL/NONE — recalc Stream Items on BOE conversion-factor change) · `DEFAULT_BOOKING_PERIOD` (BY_DOC_DATE) · `ACC_REV_INTERFACE_IND` (ERP accrual reversals).

### Sales → Revenue interface 🔑
`EcBp_Replicate_Sales_Qty` package moves **Contract Account data → `IFAC_SALES_QTY`** tables. Requires `ec_contract.revn_ind=Y` + `ec_contract_account.interface_to_revenue=Y`. Three levels: Contract-Account (`DV_SCTR_ACC_MTH/YR_STATUS`), +Profit-Centre (`_PC_`), +Company (`_PC_CPY`). **Daily not supported** — aggregate to monthly. Full User-Exit support (`ue_Replicate_Sales_Qty`).

### Quantity module (Stream Items)
- **Stream Item** = the unit of quantity tracked; values daily/monthly via the **Quantity** screens (Daily/Monthly List/Node/Quantity Input/Overview — VO.* screens).
- **Stream Item Calculations**: use the calc framework (Calculation Context = "Stream Item Volumes"), executed via **Allocation Networks** + Nodes (Stream Items → Streams → Nodes). Daily/Monthly Quantity Allocation screens.
- **Month-by-Day / Year-by-Month tabs**: manage a whole month/year of a Stream Item across day/month sub-tabs.
- **Accruals**: RUN ACCRUAL (last actual / month-avg / manual) → status `ACCRUAL` → "ACCRUAL TO FINAL" → `FINAL`.
- **Client-Side Data Validation (CSDV)** 🔑: set `INCLUDE_IN_VALIDATION=Y` on the Stream Item object + data class, **regenerate** via `ecdp_viewlayer.BUILDVIEWLAYER`/`BUILDREPORTLAYER` (DOC-02 view generator!), set limits in **Object Validation – Default**. Zones: green (ok) / orange (warning, yellow underline) / red (error — blocks save unless Conditional flag set). ⚠️ **Direct DB insert bypasses validation** (e.g. `update stim_mth_value …`) — *consistent with how my DB IUD operated below the UI validation layer.*

### Other Revenue features
- **Financial Item (FI)**: store monetary/quantity values against **any** EC object (Field/Well/Stream/Facility/Tank/Pipeline/Company/Cost-object/Financial-Account/Contract-Area); daily/monthly/yearly; via templates or calculation engine.
- **Calendar / Calendar Collection**: business-day/holiday sets for Document/Received/Payment dates. Collection = union of linked Calendars (holiday in any = holiday). New BFs handle recurring/moving holidays (Easter-relative, "first Monday of May").
- **Visual Tracing**: visualize linked data entities for a month (per Property, Actual/Accrual); Year Status icons (all booked / partial / none); `EcDp_Visual_Tracing.UpdateYearStatus()`.
- **Interfacing 'Other' Line Items** (EC-11.1-SP02+): Fixed Value, Free Unit Price Object, Interest, Percentage (All/Qty/Manual) — beyond just quantities.
- **Consolidation**: Financial-Transaction Process screens folded into **PDG/CDG** (Period/Cargo Document Generation) screens; Inventory screens → **Inventory Configuration** + **Inventory Processing Year-to-Month** (tabs: Properties/Rate Definition/Selection/Values/Item Selection/Historic Layer; hides unused sections).
- **Dashboards** (`REVN_*`, views `V_DASH_*`): document-validation-level counts + monetary roll-ups, by Company/Area/Business Unit.
- **LOCALE** config: week-start weekday via Regional Settings (`/com/ec/eccore/locale/language` + `/country`).

---

## Cross-links
- Document lifecycle (OPEN→BOOKED) parallels record status P/V/A (DOC-01/04).
- Sales Allocation + Price + Stream Item calcs all use the **Calculation Framework** (DOC-01) + Allocation Networks (DOC-04).
- **CSDV** uses `BUILDVIEWLAYER` regen (DOC-02 view generator) + validation zones (cell colours, DOC-01); direct-DB-insert bypasses it (matches my DB IUD).
- `IFAC_SALES_QTY` = Sales→Revenue handoff table.
- Next: **DOC-06 Transport**.
