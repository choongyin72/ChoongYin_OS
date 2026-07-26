# OV Reuse Targets — Bank-layout screens (`manage_object_nav`)

**Purpose:** track the EC OV object-config screens that share **Bank's exact layout/controller**
(`manage_object_nav`: navigator = single **Date + GO**, one **object-list grid**, one **NEW VERSION
detail form**). These reuse the shared engine `py/ec_object_iud.py` (thin driver = copy `py/bank_iud.py`,
swap `SCREEN`/`GRID_DATA_ID`/`VIEW`/field_maps) + `libraries/DbVerify.py`. Tick as covered.

- **Source:** the 947 deep-dive notes (`DeepDiveLearnings/ec-screens/notes/*.md`); Bank = `CD.0021`.
- **Signature:** URL controller `manage_object_nav/CLASS_NAME`. OV-GM (BU/PU cascade nav) use a different
  controller and are NOT in this set. Navigator confirmed Date+GO on a 5-screen visual spot-check (CD/CO/SP/IN).
- **Coverage key:** the `OV_<view>` name referenced (word-boundary) in `pageobjects/` + `tests/`.
- **Totals:** 71 screens = **43 covered · 28 uncovered** (updated 2026-07-26: +Disposition Type CO.0208, +Report Area RP.0017, +Choke CO.0185, +Choke Model CO.0217, +Port CO.2003, +Berth CO.2012, +Canal CO.2069).
- **Caveat:** navigator is uniform, but each screen's **detail-form fields differ** — some have mandatory
  reference dropdowns (e.g. Bank Account: Bank/Customer/Currency). Recon each form before building; if it has
  mandatory ref dropdowns the generic engine needs dropdown-fill support (not yet built) or a standalone bundle.

## Uncovered — reuse targets (28 remaining; done ones ticked [x] below)
### CD (9)
- [ ] Document Template — `CD.0013` — `OV_DOC_TEMPLATE`
- [ ] Revenue Stream Category — `CD.0015` — `OV_STREAM_CATEGORY`
- [ ] Stream Item Category — `CD.0016` — `OV_STREAM_ITEM_CATEGORY`
- [ ] Split Item Other — `CD.0017` — `OV_SPLIT_ITEM_OTHER`
- [ ] Input List — `CD.0035` — `OV_STREAM_ITEM_COLLECTION`
- [ ] HCB System — `CD.0097` — `OV_BALANCE`
- [ ] UOP Key — `CD.0099` — `OV_FIN_UOP_DEPR_KEY`
- [ ] Inventory Area — `CD.0115` — `OV_INVENTORY_AREA`
- [ ] EC Code Object — `CD.0135` — `OV_EC_CODE_OBJECT`
### CO (20)
- [ ] Chemical Product — `CO.0072` — `OV_CHEM_PRODUCT`
- [ ] Orifice Plate — `CO.0089` — `OV_ORIFICE_PLATE`
- [ ] Meter Run — `CO.0091` — `OV_METER_RUN`
- [ ] Process Train — `CO.0120` — `OV_PROCESS_TRAIN`
- [ ] Reservoir Block — `CO.0133` — `OV_RESV_BLOCK`
- [ ] Reservoir Formation — `CO.0135` — `OV_RESV_FORMATION`
- [ ] Reservoir Block Formation — `CO.0137` — `OV_RESV_BLOCK_FORMATION`
- [ ] Deferment Group — `CO.0149` — `OV_DEFERMENT_GROUP`
- [x] Choke — `CO.0185` — `OV_CHOKE` (done 2026-07-25)
- [x] Disposition Type — `CO.0208` — `OV_DISPOSITION_TYPE` (done 2026-07-25)
- [x] Choke Model — `CO.0217` — `OV_CHOKE_MODEL` (done 2026-07-26)
- [ ] Blend — `CO.0219` — `OV_BLEND`
- [ ] Calculation Group Context — `CO.0245` — `OV_CALC_GRP_CONTEXT`
- [ ] Chemical Transport Tank — `CO.0257` — `OV_CHEM_TRANS_TANK`
- [ ] Calculation Context — `CO.1059` — `OV_CALC_CONTEXT`
- [ ] Dummy Tag Event Object — `CO.1063` — `OV_DUMMY_TAG_EVENT`
- [x] Port — `CO.2003` — `OV_PORT` (done 2026-07-26)
- [x] Berth — `CO.2012` — `OV_BERTH` (done 2026-07-26)
- [x] Canal — `CO.2069` — `OV_CANAL` (done 2026-07-26)
- [ ] Storage Flow — `CO.2091` — `OV_STORAGE_FLOW`
### IN / RP / SP (6)
- [ ] Transactional Inventory Properties — `IN.0023` — `OV_TRANS_INVENTORY`
- [ ] Config Variable — `IN.0031` — `OV_CONFIG_VARIABLE`
- [ ] Transactional Inventory Layout Set — `IN.0033` — `OV_TRANS_INV_TMPL_SET`
- [x] Report Area — `RP.0017` — `OV_REPORT_AREA` (done 2026-07-25)
- [ ] Data Extract Setup — `SP.0043` — `OV_SUMMARY_SETUP`
- [ ] Data Extract Set — `SP.0049` — `OV_SUMMARY_SET`

## Covered — already have an RF suite (36)
Stream-All `CD.0007` · Product Description `CD.0012` · Customer `CD.0019` · Vendor `CD.0020` ·
Bank `CD.0021` · Bank Account `CD.0022` · Payment Term `CD.0023` · VAT Code `CD.0029` ·
Sales Order `CD.0033` · Cost Object Mapping `CD.0089` · Field Group `CD.0091` · Document Date Term `CD.0107` ·
Document Received Term `CD.0108` · Exchange Rate Source `CD.0111` · Payment Scheme `CD.0113` ·
Object List `CD.0131` · DOA Credit Limit `CD.1059` · Production Unit `CO.0001` · Country `CO.0005` ·
Product `CO.0007` · Licence `CO.0011` · Company `CO.0013` · Carrier `CO.0098` · Region `CO.0118` ·
Functional Area `CO.0145` · County `CO.0213` · MMS Lease `CO.0214` · State Lease `CO.0215` ·
Operator Lease `CO.0216` · State `CO.0243` · Currency `CO.2028` · Business Unit `CO.2034` ·
Royalty Owner `RC.0051` · Royalty Depositor `RC.0052` · Product Group `RC.0053` · Unit Agreement `RC.0055`
