# ECSR-35236 — Issue_1052: Review PHD Validations for added TAGs ≥ 1 Dec 2025

**SOW / solution draft.** Status: recon done (read-only), build pending owner go.
**Hard constraints:** build + verify in ChoongYin_OS + COPSDEV/plutodev ONLY. **No commit to the Pluto/client repo** — final product is handed to CY for the client-repo PR.

---

## 1. Ticket
- **ECSR-35236** — Change / **Major** · labels `PLUTO_PROD`, `PUNCH_LIST` · component EC Interface · reporter Cormac Judge · **assignee Choong Yin Lee** · status **Reopen**.
- Original ask: new PHD **tags** added since 1 Dec 2025 → re-validate they land in the correct EC classes/columns, and that Check-Rule + Class validations behave. Fixed in 1.0.39.RC3, then **reopened** because **Melanie Murray** found several **check rules fire false positives** and need their **Where Formula** scoped.
- **Reopened scope (the actual work) = 8 check rules** need an extra criterion AND-ed into the Where Formula.

## 2. Critical finding — `CHECK_ID` is NOT portable across envs; use the CODE (`CHECK_NAME`)
Mel's numeric IDs are **ECAASTEST** IDs. The same ID maps to a *different* rule in plutodev. There is **no separate CODE column → `CHECK_NAME` IS the business code.** Always target by name.

| Rule (CHECK_NAME = code) | Mel's ID (ECAASTEST) | plutodev ID | Mel's criterion |
|---|---|---|---|
| `PHD_TANK_DIP_GRS_MASS_VAL1` | 1145 | **1147** | `GRS_MASS_METHOD = 'MEASURED'` |
| `PHD_TANK_DIP_STD_DENSITY_VAL1` | 1147 | **1149** | `STD_DENS_METHOD = 'MEASURED'` |
| `PHD_STRM_ANALYSIS_DENSITY_VAL1` | 1142 | **1144** | `STD_DENSITY_METHOD = 'COMP_ANALYSIS'` |
| `PHD_STRM_ANALYSIS_GCV_VAL1` | 1143 | **1145** | `GCV_METHOD = 'COMP_ANALYSIS'` |
| `PHD_PWEL_STATUS_NODATA_BHTEMP` | 1017 | 1017 | `ON_STREAM_HRS > 0` |
| `PHD_PWEL_STATUS_NODATA_WHTEMP` | 1018 | 1018 | `ON_STREAM_HRS > 0` |
| `PHD_PWEL_STATUS_NODATA_BHPRESS` | 1019 | 1019 | `ON_STREAM_HRS > 0` |
| `PHD_PWEL_STATUS_NODATA_WHPRESS` | 1020 | 1020 | `ON_STREAM_HRS > 0` |
> Trap: plutodev `1145` = the stream-GCV rule, but Mel's `1145` = the tank-gross-mass rule. Blindly applying Mel's IDs to plutodev would patch the WRONG rules.

## 3. plutodev ↔ ECAASTEST compare (by code) — read-only
- PHD family: **plutodev 65 rules, ECAASTEST 63, ZERO `WHERE_FORMULA` differences** across the 63 shared rules → the two envs are **in sync**.
- Only-in-plutodev (2): `PHD_STRM_COMP_MOL_PCT_FROZEN_V1`, `PHD_STRM_COMP_WT_PCT_FROZEN_V1` (earlier Issue_1052 frozen rules). Only-in-ECAASTEST: none.
- **Mel's fix is applied in NEITHER env** → ECAASTEST is not a reference; we author it.

## 4. Mechanic (how a check rule works here)
- `TV_CTRL_CHECK_RULES`: `CHECK_NAME` (code), `WHERE_FORMULA` (human formula, `${Var}` tokens), `WHERE_CLAUSE` (compiled SQL — may be null/regenerated), `SELECT_CLAUSE`=`Count(*)`, `SEVERITY_LEVEL`. The check FAILS when the WHERE_FORMULA selects ≥1 row (i.e. a bad row exists).
- `TV_CTRL_CHECK_RULE_VARIABLE`: one row per `${Var}` → `VARIABLE_TYPE='ATTRIBUTE'`, `VARIABLE_VALUE=<class attribute>`. e.g. rule 1147 `GrsMass → ZWP_GRS_MASS_TONNES`.
- Current variable→attribute map (plutodev): `GrsMass→ZWP_GRS_MASS_TONNES` · `StdDensity→MEAS_STD_DENSITY_KGPERSM3` · `Density→DENSITY` · `Gcv→GCV_MJPERSM3` · `AvgBHTemp→AVG_BH_TEMP_C` · `AvgWHTemp→AVG_WH_TEMP_C` · `AvgBHPress→AVG_BH_PRESS_KPA` · `AvgWHPress→AVG_WH_PRESS_KPA`.
- Method attribute values confirmed live: stream `STD_DENSITY_METHOD`/`GCV_METHOD` ∈ {`REF_VALUE`,`COMP_ANALYSIS`}; PWEL class has `ON_STREAM_HRS`; tank `GRS_MASS_METHOD` seen = `MEASURED`.

## 5. Proposed change (current → target)
For each rule: (a) **add one ATTRIBUTE variable** for the method/on-stream attribute, (b) **AND-append it** to `WHERE_FORMULA`.

| Rule | current WHERE_FORMULA | + new variable | target WHERE_FORMULA |
|---|---|---|---|
| TANK_DIP_GRS_MASS | `(${GrsMass} IS NULL OR ${GrsMass} < 0)` | `GrsMassMethod → GRS_MASS_METHOD` | `(${GrsMass} IS NULL OR ${GrsMass} < 0) AND ${GrsMassMethod} = 'MEASURED'` |
| TANK_DIP_STD_DENSITY | `(${StdDensity} IS NULL OR ${StdDensity} < 0)` | `StdDensMethod → STD_DENS_METHOD` | `… AND ${StdDensMethod} = 'MEASURED'` |
| STRM_ANALYSIS_DENSITY | `(${Density} IS NULL OR ${Density} < 0)` | `DensityMethod → STD_DENSITY_METHOD` | `… AND ${DensityMethod} = 'COMP_ANALYSIS'` |
| STRM_ANALYSIS_GCV | `(${Gcv} IS NULL OR ${Gcv} < 0)` | `GcvMethod → GCV_METHOD` | `… AND ${GcvMethod} = 'COMP_ANALYSIS'` |
| PWEL_NODATA_BHTEMP | `(${AvgBHTemp} IS NULL OR ${AvgBHTemp} < 0)` | `OnStreamHrs → ON_STREAM_HRS` | `… AND ${OnStreamHrs} > 0` |
| PWEL_NODATA_WHTEMP | `(${AvgWHTemp} IS NULL OR …)` | `OnStreamHrs → ON_STREAM_HRS` | `… AND ${OnStreamHrs} > 0` |
| PWEL_NODATA_BHPRESS | `(${AvgBHPress} IS NULL OR …)` | `OnStreamHrs → ON_STREAM_HRS` | `… AND ${OnStreamHrs} > 0` |
| PWEL_NODATA_WHPRESS | `(${AvgWHPress} IS NULL OR …)` | `OnStreamHrs → ON_STREAM_HRS` | `… AND ${OnStreamHrs} > 0` |

**Semantics:** a null/negative value is only a violation when the value was *supposed* to be real — i.e. measured (tank), comp-analysis-derived (stream), or the well was on stream (PWEL). `REF_VALUE`/defaulted/off-stream rows stop false-failing.

## 6. Build approach (ChoongYin_OS)
- **Idempotent, re-runnable SQL** (`ec-sql-script-builder` house style), **targeting by `CHECK_NAME`** (resolve the per-env `CHECK_ID` at runtime — do NOT hardcode Mel's IDs):
  1. `UPDATE TV_CTRL_CHECK_RULES SET WHERE_FORMULA = <target>` where `CHECK_NAME = …` **and the criterion isn't already present** (guard against double-append → re-runnable).
  2. **Upsert the method/on-stream variable** into `TV_CTRL_CHECK_RULE_VARIABLE` (update-if-exists else insert) for that `CHECK_ID`.
  3. `REV_TEXT = 'ECSR-35236'` on every write; **no DELETE**.
- **Rollback script** restoring the captured original `WHERE_FORMULA` + removing the added variable.
- **Open build questions to resolve first (Phase-0b recon / confirm):**
  1. **`WHERE_CLAUSE` regeneration** — is it derived from `WHERE_FORMULA` at run time, or stored compiled? If stored, the DB edit must also refresh it (or do the edit via the **Check Rule screen** Save, which recompiles). ⟵ key.
  2. **Tank method attribute exact names** (`GRS_MASS_METHOD` / `STD_DENS_METHOD`) on the tank-dip class — confirm (stream view confirmed; tank class TBC).
  3. **TV_ versioning** — these are versioned TV tables; confirm the supported write path (screen vs direct DB vs Flyway) so the change is approved/effective.
  4. Whether the value comparison should be `= 'COMP_ANALYSIS'` only, or `IN (...)` (any other "real" methods that should still validate, e.g. `MEASURED`). Confirm with Mel/Grant.

## 7. Verify (COPSDEV/plutodev only)
- Apply on COPSDEV → re-run the relevant Check Group / Validation Overview on a date the rule previously false-fired → confirm it **no longer fires** AND still fires on a genuine null/negative with the right method. DB ground-truth via `TV_CTRL_CHECK_LOG`.
- UT evidence doc: Check Rule screen before/after Where Formula + Validation Overview before/after + DB before/after.

## 8. Deliver
- ChoongYin_OS PR (`feature/ecsr-35236-phd-check-rules`) for review → hand the final SQL + evidence to CY for the **client-repo** PR (I never commit there). Update the Jira ticket (→ retest) with what changed, on owner OK.

## Appendix — env access (read-only recon)
- COPSDEV/plutodev: `db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev` ECKERNEL_EC.
- ECAASTEST: `test.db.non-prod.plp.wde.ecaas.cloud:1521/QDB` ECKERNEL_EC (pwd in /c/tmp scratch only, never committed).
- Rule table `TV_CTRL_CHECK_RULES`; variables `TV_CTRL_CHECK_RULE_VARIABLE`; run log `TV_CTRL_CHECK_LOG`; group link `TV_CTRL_CHECK_COMBINATION`.
