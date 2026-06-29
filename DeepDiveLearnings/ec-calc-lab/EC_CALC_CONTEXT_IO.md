# EC Calculation — Context I/O deep trace: TRANSPORT (EC_TRAN*)

_Read-only DB trace (2026-06-29), same method as the EC_PROD trace in [[EC_CALC_ARCHITECTURE_TRACE]]. For each
context: read/write classes (`CLS_NAME` + business LABEL + key `SQL_SYNTAX` attrs) + a real equation sample.
Variable I/O mappings are CONTEXT-level (see the architecture trace). Calc outputs are stamped `CALC_RUN_NO`._

The Transport (EC Transport module) calc domain has **4 contexts**. Inferred roles from their I/O + equations:

## EC_TRAN — nomination / scheduling allocation (actuals)
The core transport calc (largest: 96- and 64-equation calcs). Allocates nominated/scheduled quantities across
services, delivery streams and paths on the transport network, honouring capacity.
- **READS:** Delivery Stream Daily Transaction (`DELSTRM_DAY_TRANSACTION`.NET_SCHEDULED_QTY); Service Daily
  Transaction [+ for-location/tiers/splits] (`SERVICE_DAY_TRANSACTION*`.PROPOSED_ALLOCATED_QTY, FROM_LOCATION_CATEGORY,
  PREV_ACCEPTED_QTY); Nomination Point Nomination Alloc (`NOMPNT_DAY_NOM_ALLOC`.ACCEPTED_QTY); Service Day Status /
  capacity (`DELSTRM_DAY_CAPACITY`.AVAILABLE_RESERVED_CAPACITY); Daily Path Nomination (`TRNP_NP_DAY_NOM_PATH`.REQUESTED_QTY).
- **WRITES:** `DELSTRM_DAY_TRANSACTION`, `SERVICE_DAY_TRANSACTION[_LOCATION/_TIERS/_SPLIT]`, `NOMPNT_DAY_NOM_ALLOC`.ACCEPTED_QTY,
  sub-day transactions, Daily Delivery Point Transaction (`DELPNT_DAY_INVENTORY_TRANSACTION`.QTY), `CALC_REF_SCHEDULE`.
- **Equation flavour:** `REMARK "Sum up proposed quantity for services"` → `gnSchedQty[SERVICE,DAY]` aggregated over
  delivery streams / paths (including inventory) → produces accepted/scheduled quantities.

## EC_TRAN_CP — forecast storage → lifting nomination generation
When forecast storage balance exceeds a threshold, generate lifting nominations.
- **READS:** Forecasted Storage Mth/Day Balance (`STOR_MTH_FCST_BAL`/`FCST_STOR_MTH_FCST_BAL`.BALANCE_QTY), Daily
  Storage Forecast (`STOR_DAY_FORECAST`/`FCST_STOR_DAY_FORECAST`), Lifting Account Daily Forecast + balances
  (`LIFT_ACC_DAY_FORECAST`, `FCST_LIFT_ACC_*`), nomination allocs (`*_STOR_LIFT_NOM_ALLOC`.NOM_QTY).
- **WRITES:** `STORAGE_LIFT_NOM_ALLOC` / `FCST_STOR_LIFT_NOM_ALLOC` (NOM_QTY) — "Nomination class used in allocation".
- **Equation flavour:** `INFO "Storage balance is above threshold, generating lifting"` → `argmax` to find the
  **largest lifting-account balance** → assign `NomQty[STORAGE,DAY,LIFTING_ACCOUNT,PARCEL_NO]` to that account.

## EC_TRAN_FC — forecast energy allocation (contract / delivery point / nomination point)
Propagates forecast volumes/mass/energy through the forecast allocation tables (+ a company-equity copy).
- **READS:** Forecast Input Contract/Delivery-Point/Nomination-Point Day Status (`FCST_{CNTR,DP,NOMPNT}_DAY_STATUS`.NET_MASS_CALC);
  Contract Parties (`CONTRACT_PARTIES`.EQUITY).
- **WRITES:** Forecast Day Alloc for Contract / Delivery Point / Nomination Point (`FCST_{CNTR,DP,NOMPNT}_DAY_ALLOC`)
  plus company copies (`FCST_{DP,NOMPNT}_DAY_CPY_ALLOC`/`_CPY_AL`) — attribute **ENERGY** (also NStdVol/NMass).
- **Equation flavour:** `INFO "Calculating series s"` → `NStdVol[DELIVERY_POINT,DAY,SERIES]` / `NMass[...]` and the
  `[CONTRACT,DAY,SERIES]` equivalents seeded from `Initial*` values → forecast standard volume / mass per series.

## EC_TRAN_TO — storage-day lifting, gross → net (the clearest example)
Named calc **`EC_GRS_TO_NET_EQN`** (16 equations) — classic oil-measurement gross-to-net conversion.
- **READS:** Storage Day Lifting Alloc (`STOR_DAY_LIFTING_ALLOC`.INITIAL_LOAD_VALUE — "Storage liftings used by
  calculations"); Storage Day Analysis Alloc (`STOR_DAY_ANALYSIS_ALLOC`.ANALYSIS_VALUE).
- **WRITES:** `STOR_DAY_LIFTING_ALLOC`.LOAD_VALUE.
- **Equation flavour:** `REMARK "Define constants for measurement codes"` → `tGrsMeasCode = TS1_GRS_VOL_BBLS`,
  `tNetMeasCode = TS1_NET_VOL_BBLS`, `tBSWAnalysisCode = TS1_BSW` → read measurement values → net = gross adjusted
  by BS&W (basic sediment & water). Net volume = Gross volume × (1 − BS&W).

## Cross-domain picture (how it chains)
- **EC_PROD** (Production Allocation) produces well/perforation allocated volumes (`PWEL_*_ALLOC`).
- **EC_TRAN** then handles network movement: nominations → scheduling → transaction allocation (accepted qtys,
  capacity) across services/delivery-streams/nomination-points.
- **EC_TRAN_TO** converts measured storage liftings gross→net (BS&W).
- **EC_TRAN_CP / EC_TRAN_FC** are the **forecast** counterparts (note the pervasive `FCST_` / `FORECAST` classes):
  forecast storage→lifting nominations, and forecast energy allocation across contract/DP/nom-point.

## Method notes (reusable for the other contexts)
- Resolve context oids: `ecdp_objects.GetObjCode` over `calc_var_{read,write}_mapping.object_id`.
- I/O by class: group `calc_var_{read,write}_mapping` by `CLS_NAME`; business name = `class_property_cnfg.LABEL`.
- Equations: `calc_equation` keyed by the calc `object_id`; `calculation.calc_context_id` filters to the context;
  strip MathML tags for a readable form.
- Scripts: `investigation/trace_tran_io.py`, `trace_tran_eq.py`, `trace_tran_labels.py` (all read-only).
