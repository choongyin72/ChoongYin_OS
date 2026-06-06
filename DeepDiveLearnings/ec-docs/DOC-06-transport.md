# DOC-06 — EC Transport
**Source:** EC 14.2.4 `transport` (12 pages) · **Read:** 2026-06-06

> Transport of hydrocarbons by pipeline or vessel — terminals, LNG/NGL, off-take. Completes the Woodside business trio (Production + Revenue/Sales + Transport).

## Business areas
**CA** (Cargo Administration = tanker scheduling/shipment planning) with sub-areas **CP** (Cargo Planning), **TO** (Terminal Operation — irregularities, cargo documents), **LA** (Lifting Account). Plus **OD** (Oil Delivery), **GD** (Gas Dispatching/Delivery), **FC** (Forecast — match field forecast vs plant capacity).

## 🔑 Cargo Status (dedicated workflow on top of record status)
Beyond P/V/A, cargo has its own status: **T** Tentative → **R** Ready for Harbour → **C** Closed → **A** Approved; **D** Cancelled (must be code D). Customer statuses map to system statuses in **Cargo Status Mapping (CO.2006)**. Set via Nomination Entry (CP.0001, creates as Tentative), Cargo Info (CP.0003), Lifting Instruction (CP.0005 → Ready), BL/MR Info (TO.0005 → Closed).
- **Status drives record status**: Closed → sets `RECORD_STATUS=V` on CARGO_TRANSPORT / STORAGE_LIFT_NOMINATION / STORAGE_LIFTING (locks edits); Approved → sets `A` on those + CARGO_ACTIVITY / CARGO_ANALYSIS / CARRIER_INSPECTION etc.
- Transition matrix governs allowed changes (e.g. Approved→Closed blockable via system setting).

## 🔑 The EC Contract Concept (shared Transport + Sales + Revenue)
Models contracts simple→complex:
- **Contract** (period, year/day offsets) · **Contract Parties** (vendor + customer, multi-company equity split) · **Contract Template** (attribute set for a contract type, e.g. GSA) · **Contract Attributes** (effective-dated — can change over contract life) · **Contract Accounts** (transactional-quantity obligations: Monthly Sales Gas Qty, Take-or-Pay, Off-Spec — volume/mass/energy).
- Access can be limited per module (Transport/Sales/etc.). *(This is the backbone of Sales Allocation in DOC-05.)*

## EC Revenue Interface
Cargo info replicated to EC Revenue for invoicing via **Interface Functions**. Cargo Liftings (per parcel) replicated at Bill-of-Lading value; CIF cargoes also replicate expected-unload/unload. Quantity types: **LOAD** (BL/MR Info TO.0005), **EXP_UNLOAD**, **UNLOAD** (Unload Info TO.0010). Configured in **Product Measurement Setup (CO.2002)**. Preconditions: contract 'Available in Revenue' + Incoterm set. Cargo Quantities replicated monthly after month close.

## Screen/config features
- **Screen Configurability (Gas Dispatching):** URL params reuse one screen def — `NAV_MODEL`, `FORCE_NAV_CLASS`, `CLASS`, `BF_PROFILE` (CO.1025), `TARGET`.
- **Demurrage form layout** (TO.0007/TO.0015): `FormLabelLayoutTransformer` reads class-attr props `viewgroup`/`viewcol`/`viewrow` (dynamic per demurrage type). 🔑 **Toolbar Insert disabled — replaced by "Create" buttons** (dynamic layout props only evaluate on persisted records). *(Another Manage-Object-style insert variation, like Bank/Equipment's disabled toolbar buttons.)*
- **Gantt chart transformers** (perf): `DataModelFilterTransformer` (eq/between/in — moves DB filtering to app layer), `GanttChartTooltipTransformer`, `GanttChartConflictDetector` for Berth/Carrier Utilization (CP.0068 Forecast Manager, CP.0072).
- **Cargo Administration context menus**: `GenericCargoAction` + `ue_cargo_action.execute()`, configured via `BF_COMPONENT`/`CNTX_MENU_ITEM`/`CNTX_MENU_ITEM_PARAM` tables.

## Contract end-dating & calendars
- **End Dating of Contracts (CO.2086)**: shortening a contract is hard (data dependencies). New BF finds/resolves dependencies (Dependency Sets → Summary → Class Data), then allows new End Date. Backed by `ecdp_object_dependency.generateDependencyPackage('CONTRACT')` → `eced_<CLASS>` package. *(Generalizes the object-relation date integrity from DOC-02 ENFORCE_DATE_CHECK.)*
- **Berth Slot Calendar (CP.0078/0079)**: calendar screenlet from STORAGE_LIFT_NOM_INFO + BERTH_PERIOD_RESTRICTION; cell colour/tooltip/duration configured via Maintain System Settings props; EC Codes `CARGO_CALENDAR_DETAIL` (detail + colour).

## New Cargo Planning data model (EC-13.2.0)
Separates **commercial nominations** from **physical execution**. Explicit **nomination type** (lifting/delivery) decoupled from storage type (import/export). One cargo = many lifting + delivery nominations. Physical tables e.g. `VOY_CARGO_ACT` (load/unload activities). Old model deprecated but still supported via DB logic; upgrade scripts migrate.

---

## Cross-links
- **EC Contract Concept** is shared with Sales Allocation (DOC-05) and Revenue.
- Cargo status → record status V/A linkage extends the P/V/A model (DOC-01/04).
- Demurrage "Create buttons" (toolbar insert disabled) = another Manage-Object insert variation → relevant to IUD automation.
- Contract end-dating dependency resolution generalizes ENFORCE_DATE_CHECK (DOC-02).
- Next: **DOC-07 ECIS + Events** (integration — high priority).
