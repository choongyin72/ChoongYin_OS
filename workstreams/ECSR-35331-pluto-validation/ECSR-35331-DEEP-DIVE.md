# ECSR-35331 — PLP Downstream: Validation Rules Not Applied (Deep Dive)

> Jira: https://energycomponents.atlassian.net/browse/ECSR-35331 · **Critical Bug** · assignee **Choong Yin Lee**
> Labels: `PLUTO_UAT` `PLU_DOWNSTREAM` `UAT_Wave_03` · Component: EC Allocation/Calculations · Status: New
> Reporter: Murali Viswanathan (2026-06-17). This doc = working analysis; no client-repo changes made.

## ★ FINAL FINDINGS — 2026-06-18 (review before commit; supersedes §5 below)

### Screen-validation mechanism — the core discovery
EC "screen validation" on these Pluto screens is **display-only, not a save-time block**:
- **`PCK_GEN_CHECK.run_check` / `run_day_check`** = the BATCH engine that runs the check rules and **writes
  violations to `CTRL_CHECK_LOG`** (line 341 INSERT).
- **`ZWP_P_TOOLTIP.getValidations`** = **reads** `CTRL_CHECK_LOG` and shows the cell's verification
  status/text (only for rules with `ZWP_SCREEN_VAL='Y'`). It does **0 inserts** — pure display.
- So: **no batch run → no log row → no on-screen error; and a bad value is NEVER blocked on save.**
- Proven live: set `Train 1 LNG Rundown` Grs Mass = **−8.5** (method=MEASURED). Rule 1040's exact condition
  matches the row, but `CTRL_CHECK_LOG` has **0 rows for 2026-05-12** → no error shown. Rule 1040 itself
  works (319 historical logs, incl. this same stream on 2025-12-17).

### As-built confirms the requirement (item 1)
`WSPLU_EC_AsBuilt09_Validations_v1.0.xlsx` (Pluto As-Built, DDS 09): **Daily Gas Stream Status · `GRS_MASS` ·
"All measured values must be >= 0" · type `SCREEN, CHECK_RULE` · ERROR · Check Rule 1040 · Validated By
Screen = YES.** Spec'd + implemented (rule 1040, `ZWP_SCREEN_VAL='Y'`), but not enforced at runtime.

### Defect groupings
- **Group A — negatives accepted (same root cause):** items **1, 2, 3, 5, 8, 12** (+ item 4 tanks). The ≥0
  check rules exist (`ZWP_SCREEN_VAL='Y'`, ERROR) but are display-from-log, need the batch run, never block
  save. Attribute per stream: item1 `GRS_MASS`(1040), item12 energy(1041), item5 `POWER_CONSUMPTION`(1057),
  gas vol/mass/energy(1039/40/41), oil(1051/52). Item 4 tanks: `TANK_INVENTORY` group **unbound + 0 rules**.
- **Group C — allocation output not generated (different domain):** items **7, 9, 10, 11**. `02 Onshore
  Daily Allocation` runs *Success* but doesn't produce expected mass/vol/energy for Pluto Inlet Gas / BOG —
  likely **"No theoretical mass found"** (seen in the alloc run log). NOT a validation issue → investigate next.
- **Item 6 — remove defunct calc job:** the "Calculation Job" dropdown is sourced from EC Calculation objects
  (`OV_CALCULATION`). Defunct = **`Daily BLP Allocation <OBSOLETE>`** (Daily Allocation) + **`Monthly BLP
  Allocation <OBSOLETE>`** (Monthly). Remove = end-date (End=Start) the Calculation object(s) via the
  Calculation screen or a `Pluto_Config` Flyway migration.

### Status / cleanup
Item 1 fully root-caused; Group A grouped (others share item-1 mechanism — individual confirm pending);
item 6 traced; Group C re-framed, investigation pending (tomorrow). **No client-env writes by me (all
read-only).** ⚠️ The **−8.5 test value on `Train 1 LNG Rundown` / 2026-05-12 should be reverted to 0.**

---

## 1. Problem
On Pluto (Burrup) downstream daily screens, **screen validation is not applied**: the app accepts
**negative measured/override values** and **missing mandatory values** (mass / volume / energy), and
allocations still "succeed" on the bad data. 12 reported sub-items, in 3 themes:
- **A — negatives wrongly accepted:** items 1, 2, 3, 4, 5, 8, 12
- **B — missing-data, allocation still succeeds:** items 7, 9, 10, 11
- **C — UI cleanup:** item 6 (remove a defunct calculation option on the Daily Allocation screen)

## 2. Environment (ECAASDEV — the UAT env)
| | |
|---|---|
| Web app | https://dev.non-prod.plp.wde.ecaas.cloud/ |
| Web login | **`quorum` / `<redacted — held securely, not in repo>`** (the earlier `sysadmin/Sysadmin@01` was wrong) |
| DB | `dev.db.non-prod.plp.wde.ecaas.cloud:1521/QDB` · `ECKERNEL_EC` / `<redacted — held securely, not in repo>` |
| Client repo | `C:\DEV\GIT\woodside_impl_pluto_12839` (branch `PCI`, v1.1.6) — **READ-ONLY** unless explicit OK + feature branch; fixes ship via `Pluto_Config` Flyway → Bitbucket PR |

## 3. Full navigator recipe (all confirmed live, read-only)
**Constant for every stream-status item:** Date `2026-05-12` · Production Unit `Pluto Scarborough` ·
Area `Burrup LNG Park` · GO `button:form:B`. Navigator = Date (G:0) + PU (G:1) + Area (G:2) + Facility Class 1 (G:3).

| # | Defect | Screen | Facility Class 1 | Stream(s) |
|---|---|---|---|---|
| 1 | LNG rundown — negative | Daily Gas Stream Status | **LNG Train 1** | `Train 1 LNG Rundown` |
| 2 | Cold dry vapour flare — negative | Daily Gas Stream Status | **Flare** | `Cold Dry Vapour` |
| 3 | Condensate rundown — negative | Daily Liquid Stream Status | **Condensate** | `Condensate Rundown ex 1U-2000`, `…ex 2U-2000`, `Total Condensate Rundown` (also LNG Train 1 → `Condensate Rundown from Train 1 Fractionation`) |
| 4 | LNG & Condensate tanks — negative | Daily Gas + Daily Liquid (+ Daily Tank Status) | **Storage and Loading** | LNG: `LNG Tank 3101`, `LNG Tank 3102`; Condensate: `Condensate Tank 3301/3302/3303` |
| 5 | Daily electrical — negative | Daily Electrical Stream Status | **LNG Park** / **Fuel** / **Condensate** | `Total Plant Electricity`, `Electricity produced from GT4001–4004`, `LNG Loading Pump T3101 A/B/C`, `Condensate Loading Pump A/B/C` |
| 7 | Pluto inlet gas — missing mass | Daily Gas Stream Status | **Pluto Onshore** | `Pluto Inlet Gas` |
| 8 | Pluto inlet gas — negative | Daily Gas Stream Status | **Pluto Onshore** | `Pluto Inlet Gas` |
| 9 | Pluto inlet gas — missing vol+energy | Daily Gas Stream Status | **Pluto Onshore** | `Pluto Inlet Gas` |
| 10 | BOG — mass ok, energy missing | Daily Gas Stream Status | **Pluto Onshore** / Fuel / LNG | `Total BOG Return` (or `BOG to Common Fuel Gas System`, `LNG Ship BOG`, `T1 LNG Tanks BOG`) |
| 11 | BOG — missing energy | Daily Gas Stream Status | same as 10 | same |
| 12 | BOG — negative | Daily Gas Stream Status | same as 10 | same |
| 6 | Remove defunct calc option | Daily Allocation (`edit_daily_alloc`) | — | — |

*Items 5 and 10–12 have several candidate streams; screen + facility are confirmed, exact stream to be
pinned against the per-item screenshot.*

**Treeview path** (stream-status screens): EC Production → Production Operations → Stream Routes →
Group Model - by Day → (Daily Gas / Liquid / Electrical Stream Status; Daily Tank Status - VCF Calc).

Item 1 verified live: `Train 1 LNG Rundown` row present; the original UAT negative (`-15,167.16`) is no
longer in the data (currently 0.00 — env data changed since 2026-06-17), so a live defect repro needs a
**write** (enter negative → Save → confirm no validation), gated on explicit OK + self-clean.

## 4. How EC validation should work (mechanism)
Validation = **check rules** (`CTRL_CHECK_RULES`) linked to **check groups** (`CTRL_CHECK_GROUP`) bound to a
screen via `EC_USER_OBJECT`; a rule enforces on-screen only when its group is screen-bound **and**
`ZWP_SCREEN_VAL='Y'`. Live on ECAASDEV: **120 rules; 70 carry `< 0` / `IS NULL` checks, all `ZWP_SCREEN_VAL=
'Y'`.** Screen-bound groups exist for standard classes (GAS/OIL/WATER/ELEC/STEAM/MASS → `daily_stream_status`,
tanks → `daily_tank_dip_status`, wells, equipment) + `V_MD_*` missing-data groups.

## 5. Root cause — CONFIRMED from the live check-rule formulas (read-only DB)
The actual deployed rules (CTRL_CHECK_RULES + CTRL_CHECK_RULE_VARIABLE on ECAASDEV):
```
GAS negatives (ZWP_SCREEN_VAL=Y, ERROR):
  1039: (GRS_VOL_GAS_M3 < 0 OR NULL) AND GROSS_VOLUME_METHOD = MEASURED
  1040: (GRS_MASS_GAS_TONNES < 0 OR NULL) AND GRS_MASS_METHOD = MEASURED
  1041: (MEAS_ENERGY_GJ < 0 OR NULL) AND ENERGY_METHOD = MEASURED
ELEC 1057: (POWER_CONSUMPTION_KWH < 0 OR NULL) AND ENERGY_METHOD = MEASURED
MISSING-DATA gas 1058: GRS_MASS_GAS_KG IS NULL AND method=MEASURED   [ZWP_SCREEN_VAL = N]
TANK 1074: GRS_VOL_SM3 IS NULL AND method=MEASURED  [ZWP_SCREEN_VAL = N];  TANK_INVENTORY group = 0 rules + unbound
```
**Three root causes:**
1. **Negatives (items 1,2,3,5,8,12):** every negative/null ERROR check is gated on `… METHOD = MEASURED`.
   A manual OVERRIDE sets a non-MEASURED method, so the clause is false and the rule **skips → negative saved**
   (matches "negative override accepted"). Rules 1039/1040/1041 (gas), 1057 (elec), 1051/1052 (liquid).
2. **Missing-data (items 7,9,10,11):** the missing-data rules are `ZWP_SCREEN_VAL=N` (don't block on the entry
   screen) AND cover only ONE attribute (gas = mass only; **no missing volume/energy** rule). So missing
   vol/energy passes and allocation succeeds.
3. **Tanks (item 4):** `TANK_INVENTORY` group has **zero rules + EC_USER_OBJECT=NULL** (unbound); the only
   tank rule (1074) is missing-volume, screenVal=N, **no negative check** → tank negatives never validated.

**Fix direction (one Pluto_Config Flyway migration, mirroring v1.1.3):**
(a) drop/relax the `AND method=MEASURED` gate (or add the override method) so `<0` is blocked regardless of
method; (b) add volume+energy missing-data rules with `ZWP_SCREEN_VAL=Y`; (c) add tank negative/null rules +
bind `TANK_INVENTORY` to the daily tank screen.
**To confirm before drafting:** item 1 says "measured negative" — a write-repro (override negative + a
measured negative) would pin method-gate vs an attribute/unit nuance (`GRS_VOL_GAS_M3` vs the screen's `Sm³`).
(DB dive: `tmp/scripts/ecsr_rule_dive.py`.)

## 6. Blockers / open
- The 22 Jira attachment screenshots can't be auto-downloaded (no tool retrieves the binaries) — using the
  live env instead.
- Live defect repro (negative accepted) requires a write to UAT → gated on explicit OK + self-clean.

## 7. Next steps
1. Pull the live check-rule formulas for these streams → pinpoint exactly why negatives/missing values pass.
2. Pin the exact BOG + electrical streams (items 5, 10–12) against the item screenshots.
3. Propose fix per theme (Pluto_Config Flyway migration) → feature branch → propose→confirm → client Bitbucket PR.

## 8. Recon artifacts (read-only; no writes to client env)
- DB: `tmp/scripts/ecsr35331_recon.py` (check-rule config) · `tmp/scripts/ecsr_drive.py` (item-1 live drive)
- UI sweep: `tmp/scripts/ecsr_nav_map.py` (gas) + `ecsr_nav_map2.py` (liquid/electrical/tank)
- Outputs: `tmp/ecsr_recon/*.png`, `tmp/ecsr_recon/nav_map*_out.txt`
