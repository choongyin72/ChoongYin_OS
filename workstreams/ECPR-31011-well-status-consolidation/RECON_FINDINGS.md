# ECPR-31011 — Remove "Daily Production Well Status 2 (SCA)" screen
## Item 1: Read-only recon findings (2026-06-10)

**Ticket:** https://energycomponents.atlassian.net/browse/ECPR-31011
**Status in Jira:** New, unassigned (idle since 2026-05-28) | Epic: ECPR-31002 (WS A&G Allocation) | Label: PLU_WS_A
**Recon scripts:** `db_recon_31011.py` / `db_recon_31011_v2.py` (outputs: `db_recon_output*.txt`) — both 100% read-only against plutodev.
**Repo scanned:** `C:\DEV\GIT\woodside_impl_pluto_12839` (source only; `target/` build artifacts excluded below).

---

## Finding 1 — "Status 2" is a DATA CLASS, not a separate table (changes the whole plan)

There is **one** physical table `PWEL_DAY_STATUS` (285 columns) with a `DATA_CLASS_NAME`
discriminator column. `PWEL_DAY_STATUS_2` exists only as:
- class definition: `Pluto_Base/.../common/classes/R__0800_PWEL_DAY_STATUS_2.xml`
- generated views `DV_/RV_/TV_DT_PWEL_DAY_STATUS_2` + `IUD_PWEL_DAY_STATUS_2` trigger
- report layer: `ZWP_V_REP_PWEL_DAY_STATUS_2` view + `ZWP_R_PWEL_DAY_STATUS_2` report class

So "merge the screens" = **re-point SCA wells to data class PWEL_DAY_STATUS** + expose the
missing attributes on class 1. No table migration. Historical rows keep their
`DATA_CLASS_NAME='PWEL_DAY_STATUS_2'` tag unless we also update them (open question #3).

## Finding 2 — Both classes are LIVE (cutover must be coordinated)

| Data class | Wells | Rows | Daytime range | Rows last 30d |
|---|---|---|---|---|
| PWEL_DAY_STATUS (PLU) | 12 (PLA-01..08, PL-PYA-02, PYA-01, XNA-01/02) | 2,148 | 2025-12-11 → 2026-06-09 | 336 |
| PWEL_DAY_STATUS_2 (SCA) | 13 (SCA_01 .. SCA_13) | 884 | 2026-04-01 → 2026-06-09 | 364 |

Both landed data **yesterday**. SCA data on DEV comes from
`Pluto_Testdata/.../V1.0.0.0010.0560__SCA_WELL_TEST_DATA.sql` (403 refs — seeds class 2 directly).

## Finding 3 — Attribute gap is small and well-defined

DV view diff: class 1 = 107 cols, class 2 = 60 cols.

**Class 2 has only 12 columns class 1 lacks:**
- 7 standard attrs that already exist physically in the base table, just not exposed on
  class 1: `AVG_FLOW_RATE, AVG_MPM_GAS_MASS_RATE, AVG_MPM_GAS_RATE, DRIVE_CURRENT,
  DRIVE_FREQUENCY, PUMP_DISCHARGE_PRESS, PUMP_PRESSURE` → pure class-config addition.
- The 5 ZWP_* attrs from Cato's comment, which live in different places:
  - `ZWP_ALLOC_GAS_ENERGY`, `ZWP_MEAS_GAS_ENERGY` → physical cols in extension table
    `ZWP_T_PWEL_DAY_STATUS` (shared by both classes) → config-only to expose on class 1.
  - `ZWP_MEAS_EV_RATIO`, `ZWP_MEAS_MV_RATIO` → only in DV_2/RV_2 → likely computed/
    expression attrs; need class-XML inspection to replicate on class 1.
  - `ZWP_THEOR_GAS_ENERGY` → only in DV_2 → likely FUNCTION-type attr; same.
- Note: class 1 already has `ZWP_THEOR_GAS_VOL` (the one using
  `zwp_prod_well_theoretical.getGasStdRateDay`); class 2 does not. Simon's calc-vs-screen
  theo discrepancy (`ecbp_well_theoretical` vs `zwp_prod_well_theoretical`) remains an open
  business question, not a recon question.

Class 1 has 59 columns class 2 lacks (alloc results, ZWT_* well-test attrs, etc.) —
no obstacle; SCA wells simply gain unused attrs.

## Finding 4 — Definitive consumer list (what must be re-pointed/retired)

**DB-side dependents of class-2 views:** only cross-schema synonyms
(ENERGYX_EC, TRANSFER_EC, REPORTING_EC, QUORUM_SUPPORT_RO) + the class's own triggers.
**No PL/SQL package or other view reads class 2** → all real consumers are config in the repo:

| Consumer | File (Pluto_Config unless noted) | Refs |
|---|---|---|
| Class definition | Pluto_Base `R__0800_PWEL_DAY_STATUS_2.xml` | 8 |
| Report view + class | Pluto_Base `R__0810_ZWP_V_REP_...sql`, `R__0820_ZWP_R_...XML` | 2+1 |
| Screen/class access | `1.0.0/.../0060__T_BASIS_ACCESS.sql`, `1.0.12/.../0008__ECPR-30603_ACCESS.sql` | 14+22 |
| Check rules | `1.0.0/.../0550__CHECK_RULES.sql` | 17 |
| Status process tasks | `1.0.0/.../1360__TV_STATUS_PROCESS_TASK.sql` | 7 |
| Calc variables (read/key) | `0693/0695__CALC_VAR_*` (1.0.0) + `0620/0630` (1.0.12) | 4+8 each |
| RnA report config | ECPR-30651 series (1.0.17/19/22) + ECPR-30737/30741 (1.0.24) | 22 each / 2 each |
| **Daily Asset Report template** | Pluto_Reports `excelreport/r_plu_sca_daily_asset.xls` | 3 |
| Test data seed | Pluto_Testdata `0560__SCA_WELL_TEST_DATA.sql` | 403 |
| Class export | `json/PWEL_DAY_STATUS_2.json` | 8 |

This **confirms Simon's May-11 warning**: `r_plu_sca_daily_asset.xls` (R_PLU_SCA_DAILY_ASSET,
a June-priority report) references PWEL_DAY_STATUS_2 directly. The other two June reports
(R_BLP_DAILY_PROD_ALLOC_SCARBOROUGH, R_SCA_DAILY_PARTNER) did not hit on the grep — verify
their data classes when slicing.

**OFM interface:** staging classes `ZWP_OFM_WELL_DAY` / `ZWP_OFM_WELL_MTH` exist in
Pluto_Base; ~30 allocation calc scripts reference OFM. Which target class the OFM loader
writes well data into was NOT determined in this pass → follow-up before Slice C.

## Open questions (need humans before execution)

1. **Grant:** preferred mechanism to hide screen + remove access (his governance approach,
   per Cato's May-12 comment — likely via T_BASIS_ACCESS-style script).
2. **Cato/Simon:** theo-value function mismatch — when SCA wells move to class 1, should
   `ZWP_THEOR_GAS_VOL` (zwp_ function) become their screen theo value, and is the allocation
   calc (`ecbp_` function) expected to agree?
3. **Data history:** re-tag existing 884 class-2 rows to `PWEL_DAY_STATUS` (history visible
   in merged screen + class-1 reports) or leave them (history only via retired class)?
   Recommendation: re-tag, else the Daily Asset Report loses SCA history pre-cutover.
4. **Cutover date** for SCA wells' class change (date-effective config).
5. Confirm ECSR-35100 ("SCA data in Wells screen is not consistent", reopened 2026-06-10)
   is a symptom of this dual-class split — if so, link the tickets.

## Proposed slices (unchanged from proposal, now evidence-based)

- **A.** Add 12 missing attrs to class PWEL_DAY_STATUS (7 standard = config; 5 ZWP_* =
  replicate class-2 XML definitions). Edit `R__0800_PWEL_DAY_STATUS.xml` equivalent +
  Flyway migration. Additive, zero risk.
- **B.** Re-point 13 SCA wells to class PWEL_DAY_STATUS from cutover date (+ optional
  history re-tag per Q3). Update testdata seed.
- **C.** Re-point consumers: r_plu_sca_daily_asset.xls, calc variable mappings, check
  rules, status-process tasks, RnA config; verify OFM loader target.
- **D.** Hide "Daily Production Well Status 2 (SCA)", remove access, rename screen 1 →
  "Daily Production Well Status" (mechanism per Q1). Retire class-2 check rules/access.
- Release via **both PROD and PCI swimlanes** (Simon, May-28).

## Verification plan (when execution is approved)

- L1 DB: post-cutover SCA rows land with `DATA_CLASS_NAME='PWEL_DAY_STATUS'`; zero new
  class-2 rows; ZWP attr values populated; theo sample reconciliation (zwp_ vs ecbp_).
- L2 UI (Robot Framework): merged screen shows 25 wells, SCA attrs visible; old screen
  absent from treeview & inaccessible.
- L3 Reports: run the 3 June-priority SCA reports for a post-cutover date, reconcile vs DB.
- Negative: repo grep for PWEL_DAY_STATUS_2 returns only the retired class definition.

---

## Addendum (2026-06-10): full DV-view + class-XML deep dive

Artifacts: `dv_view_diff.py` → `dv_view_diff.csv` (full 119-row machine table),
`DV_VIEW_DIFF.md` (grouped markdown), `view_DV_PWEL_DAY_STATUS*.sql` (raw view text).
Class config sources read: `Pluto_Base/.../R__0800_PWEL_DAY_STATUS.xml` (186 attr entries)
and `R__0800_PWEL_DAY_STATUS_2.xml`.

**Headline: the real attribute gap is 4, not 12.**

Of the 12 columns only in DV_2:
- 3 are DUPLICATES of attrs class 1 already exposes (same source expression, different
  name/label): ZWP_ALLOC_GAS_ENERGY ≡ ALLOC_GAS_ENERGY (pwelDayAlloc.alloc_gas_energy),
  ZWP_MEAS_GAS_ENERGY ≡ AVG_GAS_ENERGY (base col), ZWP_THEOR_GAS_ENERGY ≡ THEOR_GAS_ENERGY
  (EcBp_Well_Theoretical.getGasEnergyDay). → Decision: relabel class-1 attrs vs add ZWP dupes.
- 5 standard cols are marked IGNORE_IND=Y in class-2 XML (AVG_FLOW_RATE, DRIVE_CURRENT,
  DRIVE_FREQUENCY, PUMP_DISCHARGE_PRESS, PUMP_PRESSURE) — in the view but HIDDEN on the
  screen. Likely config noise; probably nothing to migrate.
- **4 genuinely needed:** AVG_MPM_GAS_RATE + AVG_MPM_GAS_MASS_RATE (visible "Multiphase
  Meter" fields with zwp_p_validation.isMultiphaseMeterNonEditable editability), and
  ZWP_MEAS_EV_RATIO + ZWP_MEAS_MV_RATIO (read-only FUNCTION attrs: alloc_gas_energy/vol and
  alloc_gas_mass/vol with fallback to last non-zero alloc day; full CASE SQL in class-2 XML
  lines 9–17, directly copyable).

**Customization symmetry (good news):** both class XMLs carry the identical ON_STREAM_HRS
rounding trigger action, and both wire zwp_p_tooltip.getValidations verificationStatus/
verificationText (class 1 on MORE attrs than class 2). The Issue_1052/ECPR-31074 validation
framework is the same one — consolidation interacts with that work (check-rule object lists).

**Shared-but-different expressions (3) — need business decision:**
- WELL_STATUS: class 1 = EcDp_Well.getWellStatus(... 'EVENT','PWEL_DAY_STATUS'); class 2 =
  ec_well_period_status.well_status(... production-day-start local). Merged screen keeps
  class-1 behavior — confirm acceptable for SCA wells.
- CHOKE_UOM: class 1 reads OA.CHOKE_UOM; class 2 derives via ec_well_version.CHOKE_UOM().
  Both IGNORE'd on class-2 screen → low risk.
- CLASS_NAME: literal, no action.

**Slice A is now precisely scoped:** add 2 standard attrs + 2 FUNCTION ratio attrs (copy
XML blocks) to R__0800_PWEL_DAY_STATUS.xml, plus label/group-header decisions for the 3
dupes ("SPFM Measured Gas" / "Ratios" / "Theoretical Gas" headers per WDE spec).

*Recon performed by Claude (read-only). No data, config, or Jira state was changed.*

---

## STATUS (2026-06-10 evening): ⛔ ON HOLD — scripts prepared, NOT deployed

Chosen hide mechanism (per Choong-Yin, with Object Maintenance screenshot): revoke ALL
role access on the screen URL object
`/com.ec.prod.wr.screens/daily_well_status/GROUPMODEL/WELL/TARGET/WELL/CLASS_NAME/PWEL_DAY_STATUS_2`
(T_BASIS_OBJECT object_id 5097 on plutodev) by **DELETING all 18 TV_T_BASIS_ACCESS rows**.

Prepared and verified-by-review, awaiting explicit go:
- `deploy_revoke_PWEL_DAY_STATUS_2_access.sql` — DELETE + pre/post checks (18 → 0; screens 1/3 untouched)
- `rollback_restore_PWEL_DAY_STATUS_2_access.sql` — idempotent restore of all 18 rows at original levels
- `access_backup_PWEL_DAY_STATUS_2.csv` — live pre-change snapshot (2026-06-10)

**RULE: do NOT run the deploy script against plutodev/COPS DEV (or any environment)
without Choong-Yin's explicit OK in that session.**
