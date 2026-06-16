# Pluto Sales Contract Accounts (SCTR_ACC) — screen scoping + data model

_Deep-dive 2026-06-16, COPSDEV (read-only DB + live screen recon). Complements [sales.md](sales.md)
(which covers the sales menu/flow on the local sandbox's `CNTRACC_*`); this note is the **Pluto/COPSDEV
`SCTR_ACC_*`** contract-account layer and the **navigator-scoping** that the daily/monthly
contract-account upload tabs (Issues 1004/1067) need. Triggered by a real gap: the contract-account
screens wouldn't load data under first-option navigation._

## 1. The screens (4) and their data views
| Screen | Data view (ECKERNEL_EC) | Grain | Keys | Value cols |
|---|---|---|---|---|
| Daily Contract Account Status | `DV_SCTR_ACC_DAY_STATUS` (4,863) | day | Contract Account, Date | Volume/Mass/Energy Qty, Extra 1 Qty, UOM |
| Daily Contract Account Result – Company | `DV_SCTR_ACC_DAY_CPY_STATUS` (14,355) | day×company | Account, Company, Date | Vol/Mass/Energy Qty, Extra 1 Qty, UOM |
| Monthly Contract Account Status | `DV_SCTR_ACC_MTH_STATUS` | month | Account, Month | Vol/Mass/Energy Qty, Extra 1, UOM + YTD + TTD |
| Monthly Contract Account Company Status | `DV_SCTR_ACC_MTH_CPY_STATUS` (650) | month×company | Account, Company, Month | as above + YTD + TTD |

All keyed by `OBJECT_CODE` (the contract-account object, e.g. `UG_PLU`/`UG_SCA`/`C_PLU_CUFSA`) +
`ACCOUNT_CODE` (+ `COMPANY_CODE` for the company variants) + `DAYTIME`. `TIME_SPAN` = DAY/MTH.
Monthly company view adds `ZWP_*_QTY_YTD` / `ZWP_*_QTY_TTD` (year-to-date / total-to-date roll-ups).

## 2. The navigator is an OWNERSHIP cascade — NOT the facility cascade
Daily/monthly status **stream/well/tank** screens scope by the **physical** hierarchy
`Production Unit → Area → Facility Class 1 (→ Well Hookup)`. Contract-account screens scope by a
**commercial/ownership** cascade instead:

```
Business Unit → Contract Area → Contract → Contract Account → Profit Centre → Data Set → Company
(Woodside Energy Ltd) (Owner Group) (Burrup Facilities Co) ("Cold dry…")   (PL-PYA 02) (*Official) (8 cos)
```

- **Business Unit** has a single option here (`Woodside Energy Ltd.`); the deeper levels **cascade**
  and are empty until the level above is picked (a recon that opens them without cascading sees `[]`).
- **Company** options (the 8 Pluto offtakers): JERA Scarborough, Kansai Electric Power Australia,
  LJ Scarborough, **Midocean Pluto**, Woodside Burrup, Woodside Energy (Australia), Woodside Energy
  (Domestic Gas), Woodside Energy Scarborough.
- **Data Set** = `*Official` / `Estimate`.

> This is why first-option navigation returns **"No records found"**: the first option at each deep
> level rarely co-occurs with data on the chosen date.

## 3. Data is SPARSE and date-specific (the real blocker)
Unlike the dense daily-status grids (16–47 rows/day), contract-account rows are **1–2 per
(account, company, date)** and only on specific dates. Confirmed data-bearing combos (from the DV
views, read-only):

| View | DAYTIME | Account | Company |
|---|---|---|---|
| `DV_SCTR_ACC_DAY_CPY_STATUS` | 2026-05-23 | "Pluto Export LNG product made available at the LNG Delivery Point" | Midocean Pluto Pty Ltd |
| `DV_SCTR_ACC_DAY_STATUS` | 2025-12-21 | LIQUID_FEED (object UG_PLU) | — |
| `DV_SCTR_ACC_MTH_CPY_STATUS` | 2026-04-01 | "Pluto Export LNG product…" | Midocean Pluto Pty Ltd |

Daily contract data spans **Dec 2025 – May 2026** (latest 2026-05-26); monthly is 1st-of-month
(latest 2026-04-01). EC's grid **"Copy to clipboard" refuses an empty grid** ("No data found to be
copied"), so a data-bearing scope is mandatory to capture sample rows — the column **headers** still
render on an empty grid (captured for the V2 template; rows pending a confirmed example).

## 4. Recipe — how to load a contract-account screen with data
1. **Pick the date from the DV view first** (the densest `(DAYTIME, account, company)` combo), not a
   guess — mirrors the Finder/DB-first lesson from the stream screens.
2. Set the navigator **top-down** (each level cascades from the one above): Business Unit → … →
   **Contract Account = the data account name** → Data Set `*Official` → **Company = Midocean Pluto**
   (or whichever company the DV row shows).
3. GO. If still empty, the chosen account isn't under the picked Contract — walk the Contract/Contract
   Area level to the one that lists that account.
4. **Open question / next step:** confirm whether a **"Contract Account Finder"** exists (analogous to
   Stream/Well/Tank Finder) — it would resolve an account/object code → its full navigator path in one
   step, the cleanest recipe. Not yet verified.

## 5. Structural (config) tables seen on COPSDEV
`CNTRACC_PER_CPY_STATUS` (15,005), `CNTR_ACC_PERIOD_STATUS` (5,416), `CNTR_ACCOUNT_EVENT` (456),
`CNTR_ACC_EVENT_TYPE` (162), `CNTR_DAY_DP_CPY_CP_ALLOC` (11,781). The `CNTR_*`/`CNTRACC_*` family is
the contract structure + period/event results; the `SCTR_ACC_*` classes are the per-account day/month
**status** rows the screens edit (and the upload would write).

## 6. Ties to Issues 1004/1067
- The contract-account upload tabs need **keys = Account (+Company) + Date**, **updatable = Vol/Mass/
  Energy Qty + Extra 1 Qty + UOM** (+ Comments/ACTR Ref). YTD/TTD on the monthly views are **derived**.
- Whether all four contract screens are in scope is still a business decision ("~maybe" in 1067) — the
  validation email asks for a confirmed representative example (account + company + date) to finalise.
