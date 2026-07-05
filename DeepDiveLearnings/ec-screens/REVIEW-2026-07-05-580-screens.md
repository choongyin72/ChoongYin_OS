# Periodic Deep-Dive Review — the +400 new notes (580/1,457, 2026-07-05)

_Second milestone review: the ~400 notes added since the 180-screen merge (two 200-batch runs). Includes the quality audit that drove today's runner fixes._

## What the +400 covered

| Block | Count | What it is |
|---|---|---|
| CO.1xxx | 73 | **Platform admin + the calculation framework** |
| CO.2xxx | 101 | **Lifting / cargo / marine / contract commercial layer** |
| CO.3xxx | 25 | **Pricing & finance configuration** |
| PO.* | ~142 new | **Production Operations — the daily/monthly data-entry surface** |
| GD.* | 63 | **Gas Dispatching — transport nominations & balancing** |

### CO.1xxx — the platform's own control room (2 sub-worlds)
1. **The metamodel screens** — Class Configuration / Class Attribute Config / Class Property Codes / Business Function (CO.1097, class `BUSINESS_FUNCTION`!) / Maintain Treeview / Form Designer / EC Codes / System Attributes / Group Model / Units & Unit Conversion / Production Day Table. These are the screens that *define* everything the runner has been cataloguing — EC configuring EC.
2. **The calculation framework** — Database/Simple Object Types (CO.1037/1038), Variable Definitions (CO.1039), **Maintain/Create Calculation (CO.1040/1042, class `CALCULATION`)**, Global Attributes (CO.1041), Calculation Context (CO.1059, `CALC_CONTEXT`), Calculation Library (CO.1060–1062), Calc Log Profiles (CO.1047). This is precisely the territory of the calc-SME goal and the earlier calc-lab recon — now mapped as screens.
   Plus ops/integration: ECIS Agent Log, Event Route/Endpoint Config, User Exit Package Config, Extensions Manager, App Server Health/Performance, Data Purging, Configuration Export.

### CO.2xxx — the commercial/logistics layer
Port, Berth, Lifting Account (+measurement/analysis/document satellites), Cargo document templates & status mappings, Laytime/Delay codes, **Contract (CO.2016) + Contract Parties + Copy Contract (CO.2019 = `CONTRACT_PREPARE`)**, Nomination/Delivery Point, Business Unit, Contract Area, Currency. The Copy-Contract screen CLP's ULSD CR relies on lives here.

### CO.3xxx — pricing & finance config
**Price Index (CO.3009 = `PRICE_INDEX`)**, Price Concept/Element, Price Object, Price Index Factor, Price Rate, Cargo Price Element Setup, Contract Account (+List/Template), Sale Contract Attributes (CO.3001), Service Accounts, Spot Opportunity. **Direct overlap with the live CLP ULSD work** (TCADI00 goes into CO.3009; the 5 new attributes into CO.3001/CO.2020).

### PO — Production Operations (the N1/daily world)
Daily/Monthly Stream Status screens (oil/gas/water/mass variants), Tank/Chemical-Tank status, Equipment Status, Personnel Onboard, Marine Logistics, Alarms, Environmental Events, component analyses, batch/LACT/totalizer screens. Type profile flips here: **74 N1 daily grids + DATA/DAY/MTH/1HR classes dominate** — the operational data-entry surface that feeds allocation.

### GD — Gas Dispatching
Nomination lifecycle as classes: `TRNP_DAY_NOM_INPUT` → Nomination Matrix → Location Matching/Confirmation → Balancing → `CNTR_DAY_LOC_INVENTORY` (+ contract/location swaps) → Delivery Point Targets (`TRDP_`), Operational Nominations (`TCTR_`), sub-daily variants throughout. A `.1` twin-screen convention (grid/alternate view of the same class).

## Quality audit verdict (the "validate its quality" ask)

**Sound:** 380/580 classes resolved with provenance; 0 partials; 90% carry corpus Help images (59 without ≈ corpus gap, expected); ambiguous labels honestly left unresolved (10) rather than guessed.

**⚠ Main defect found: "process/config" over-claiming (190/580).** The no-class⇒process/config rule (correct for the original CO.0076–0086 cluster) was silently absorbing **data screens whose class resolution failed** — e.g. *Daily Output Nomination*, *Daily Tank Status – Mass*, *Daily Weather Status*, many GD/PO screens. Completeness stayed honest (terminal, no loop) but the type label was wrong and the failure invisible.

**Fixes shipped today (runner `f2ddb71` + `d075025`):**
1. Resolver strengthened — also strips `DAILY_/SUB_DAILY_/MONTHLY_` prefixes and `_STATUS/_OVERVIEW` suffixes from URL tokens (still guarded by `class_cnfg` existence — no guessing).
2. Honest no-class label — "no class resolved — process/config OR underivable data screen" instead of claiming process/config.
3. New CHECKLIST flag `no class resolved` — every such screen is now greppable for a targeted enrichment pass.
4. The 4 legacy '?'-name notes (PO.0001/0002/0003/0005) reset for regeneration in the current format.

**Remaining improvement backlog (post-completion enrichment pass, in priority order):**
- Re-resolve the ~190 flagged no-class screens with the stronger resolver + sibling/twin inference (`GD.xxxx` ↔ `GD.xxxx.1`) + DV_/TV_ view-name search.
- Config-table linkage for the *genuine* process/config screens (PROSTY_CODES / CTRL_CHECK_* / STRM_FORMULA / SCHEDULE…).
- Cross-link notes ↔ IUD bundles/registry; preserve manual `## Deep-dive` sections across re-runs.
- The `.1`/variant twins could reference their base note instead of duplicating.

## Milestone meaning

With CO complete and PO/GD swept, the notes now cover **the platform's own configuration machinery, the calc framework, the commercial/pricing layer (CLP-relevant), the daily operations surface, and gas transport nominations** — the map now spans config → operations → commercial. Remaining ~877: the deeper functional modules (allocation, sales/revenue, reporting et al.) — at 3×200/day, completion lands within ~2 days.

— End of review —
