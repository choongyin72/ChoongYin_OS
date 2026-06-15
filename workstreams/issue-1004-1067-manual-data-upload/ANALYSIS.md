# Issue 1004 + 1067 — PLP ECaaS Manual Data Upload — Analysis & Uplift Plan

_Deep-dive of the request + the AOPA baseline (`ACTR-3098 Data_Upload_V4.xlsx` + ECIS mapping SQL).
Source (read-only): `C:\Projects\Woodside\jiras\Issue-1004 & 1067  - PLP ECaaS Manual data upload template\`._
_Author: Claude Opus 4.8 · 2026-06-16 · for Woodside **Pluto (PLP)** hub._

## 1. What is being asked (the two issues combine cleanly)

| | Issue **1004** (PLP manual upload template) | Issue **1067** (Bulk update — J. Foleti) |
|---|---|---|
| Essence | An Excel template (one **tab per EC daily screen**) + ECIS interface + scheduler that ingests it into EC | The **semantics** of that bulk update — per-class key vs updatable attributes, mandatory comment, numeric-only, role-respecting |
| Scope | Daily well (all input vol/mass), Daily Gas/Liquid/Water/Electrical streams (M/V/E), Stream compositions, Daily Tank VCF | `STRM_DAY_STREAM_MEAS_*` (WAT/GAS/OIL/ELE), `TANK_DAY_DIP_STATUS`, `STRM_COMP_ANALYSIS`, `PWEL_DAY_STATUS`/`_2`, ~maybe `SCTR_ACC_*` (contract accounts) |
| Rules | facility/stream dropdowns; multi-day per stream OR all inputs for one day; REV_TEXT traceability; **5-min automated processing**; validations (negative, locked month, status ≤ Verified) | non-blank **comment mandatory**; **numeric-only** (ignore blank, error if non-numeric); **respect user role** (don't run as root); `LAST_UPDATED_BY` = uploader; `REV_TEXT` = "Upload File <n>"; column headings = class attributes |

**They are one feature:** 1004 = the *delivery vehicle* (template + ECIS + schedule, AOPA baseline); 1067 = the
*rules* the vehicle must enforce. Build as a single ECIS "Data Upload Interface", uplifted for Pluto.

## 2. AOPA baseline — how it actually works (verified from the SQL)

AOPA's `ZWA_WELL_THEOR` interface uses EC's **ECIS Advanced-Excel source-mapping** engine — 4 config tables:

| Config table | Role |
|---|---|
| `OV_IMP_SOURCE_INTERFACE` | the interface (`CODE=ZWA_WELL_THEOR`, `SOURCE_TYPE=EXCEL`, `TRANSACTION_TYPE=ROW`, `INTERFACE_TYPE=INSERT_UPDATE`) |
| `OV_IMP_SOURCE_MAPPING` | each Excel **tab.cell → staging column** (e.g. `PATH_ORIGIN='WellTheor.D5'`, `EC_KEY='ZWT.ON_STRM_HRS'`, `KEY_1='ROWS:WELL_CODE'`, `KEY_2='ROWS:DAYTIME'`) |
| `OV_IMP_SOURCE_PATH` | cell-navigation (UPPER_LEFT/LOWER_RIGHT find-bounds → reads a variable number of rows per tab) |
| `OV_IMP_TARGET_MAPPING` | staging **EC_KEY → target EC `CLASS.ATTRIBUTE`** (+ optional `FROM_UNIT/TO_UNIT` conversion) |

**Run path:** scheduler job `ZWA_ProcessWellTheorUpload` → `ECISAction` → `AdvancedExcelJobAction` (read) →
`StagingJobActionTarget` (stage/validate) → `TargetMappingJobAction` (write to EC class). **DB-based file drop.**
**Schedule type = `ONCE` (manual/on-demand) — NOT 5-minute recurring.**

**Transforms seen:** `PCT→FRAC` for `STRM_DAY_STREAM_MEAS_OIL.BS_W` and `TANK_DAY_INV_OIL.DILUENT_CUT`;
`TONNES→KG` for `STRM_MTH_LIQ.GRS_MASS`; `DELETE_WR_FUNCTION` on `OIL_SG` so the uploaded value overrides
its derivation. Traceability today = `REV_TEXT` carries the *migration ticket* (e.g. `25-01043222`), and the
staging prefix (ZWT/ZSG/…) anchors source→target. **No per-upload "Upload File <n>" and no `ZWA_ACTR_REF`.**

## 3. Tab ↔ EC class ↔ Pluto screen map

| AOPA tab | EC class (target) | Pluto screen (screenshot provided) | In Pluto scope? |
|---|---|---|---|
| WellTheor | `PWEL_DAY_STATUS` | Daily Production Well Status 1 (PLU) | ✅ (also needs **`PWEL_DAY_STATUS_2`** per 1067) |
| StreamGas | `STRM_DAY_STREAM_MEAS_GAS` | Daily Gas Stream Status | ✅ |
| StreamOil | `STRM_DAY_STREAM_MEAS_OIL` | Daily Liquid Stream Status | ✅ |
| StreamWater | `STRM_DAY_STREAM_MEAS_WAT` | Daily Water Stream Status | ✅ |
| StreamElectrical | `STRM_DAY_STREAM_MEAS_ELE` | Daily Electrical Stream Status | ✅ |
| DailyTank | `TANK_DAY_INV_OIL` | Daily Tank Status - VCF Calc | ✅ (confirm class — Pluto may use `TANK_DAY_DIP_STATUS`/VCF variant) |
| WellInjectionGas | `IWEL_DAY_STATUS_GAS` | — (no Pluto screenshot) | ❓ likely **EXCLUDE** |
| WellInjectionWater | `IWEL_DAY_STATUS_WATER` | — (no Pluto screenshot) | ❓ likely **EXCLUDE** |
| MonthLiquid | `STRM_MTH_LIQ` | — | ❓ confirm |
| **— (not in AOPA) —** | `STRM_COMP_ANALYSIS` | **Stream Gas Component Analysis** | ➕ **ADD** |
| **— (not in AOPA) —** | well-composition class (confirm) | **Well Gas Component Analysis** | ➕ **ADD** |
| **— (not in AOPA) —** | `SCTR_ACC_DAY_STATUS` | **Daily Contract Account Status** | ➕ ADD (1067 "~maybe") |
| **— (not in AOPA) —** | `SCTR_ACC_DAY_CPY_STATUS` | **Daily Contract Account Result - Company** | ➕ ADD (1067 "~maybe") |
| **— (not in AOPA) —** | `SCTR_ACC_MTH_STATUS` | **Monthly Contract Account Status** | ➕ ADD (1067 "~maybe") |
| **— (not in AOPA) —** | `SCTR_ACC_MTH_CPY_STATUS` | **Monthly Contract Account Company Status** | ➕ ADD (1067 "~maybe") |

## 4. Gap analysis — AOPA baseline vs Pluto requirement

**Reusable as-is (mechanism):** the whole ECIS Advanced-Excel engine + the 4 config tables + the staging→target
pattern + unit-conversion approach. This is the big win — no new PL/SQL engine, it's **configuration**.

**Missing from the AOPA template — must be ADDED for Pluto (6 tabs):**
1. **Stream Gas Component Analysis** (`STRM_COMP_ANALYSIS`) — wide, multi-component layout (C1…nC5, CO2, N2…).
2. **Well Gas Component Analysis** (well-comp class — confirm) — same shape.
3. **Daily Contract Account Status** (`SCTR_ACC_DAY_STATUS`).
4. **Daily Contract Account Result - Company** (`SCTR_ACC_DAY_CPY_STATUS`).
5. **Monthly Contract Account Status** (`SCTR_ACC_MTH_STATUS`).
6. **Monthly Contract Account Company Status** (`SCTR_ACC_MTH_CPY_STATUS`).
   _(Composition tabs are a different shape from the simple value tabs — needs its own column design.
   Contract-account tabs are marked "~maybe" in 1067 — scope must be confirmed.)_

**In AOPA, probably NOT Pluto scope — confirm EXCLUDE:** WellInjectionGas, WellInjectionWater (no Pluto
screenshot), MonthLiquid (no screenshot).

**Pluto uplift checklist (config + behaviour):**
- [ ] Rename AOPA identifiers → Pluto: interface code, job name, staging prefixes `ZWA/ZWT/ZSG…` → Pluto (`ZWP…`).
- [ ] **Facility/stream dropdowns** = Pluto assets (NOT Ngujima-Yin/Pyrenees/Macedon).
- [ ] **5-minute recurring schedule** (AOPA is `ONCE`) — change schedule type to a 5-min interval (1004).
- [ ] **Traceability (1067):** `REV_TEXT` = "Upload File <file-number>" per upload; `LAST_UPDATED_BY` = the
      uploading user (not sysadmin/root); add Pluto's **`ZWP_ACTR_REF`** column to the mapped attributes.
- [ ] **Validations (1004+1067):** reject negative inputs; block locked month; only write rows whose record
      status is **≤ Verified** (never overwrite Approved); **numeric-only** (ignore blank cells, error on
      non-numeric except Comments); **mandatory non-blank Comment**; **respect the uploading user's role**
      (don't run as system root — a Surveillance user must not update beyond their permission).
- [ ] **`PWEL_DAY_STATUS_2`** — AOPA WellTheor maps only `PWEL_DAY_STATUS`; Pluto needs the 2nd well class too.
- [ ] Confirm Pluto tank class (`TANK_DAY_INV_OIL` vs a VCF-calc variant) + which unit conversions apply.

## 5. My read (recommendation)
- **Adopt the AOPA ECIS Advanced-Excel engine wholesale** — it's mature, config-driven, and already does
  staging + unit conversion + insert/update-by-row. Don't rebuild; re-point it at Pluto classes.
- **Two clear workstreams:** (A) the 6 AOPA-covered tabs = mostly *config + rename + Pluto dropdowns* (fast);
  (B) the 6 net-new tabs (2 compositions + 4 contract-accounts) = need column design + class confirmation
  (slower; compositions are the hardest due to the wide multi-component layout).
- **Biggest open scope question:** the 4 Contract-Account screens are "~maybe" in 1067 — get an explicit
  in/out decision before sizing.
- **Behavioural gaps to design, not inherited from AOPA:** the 5-min recurring schedule, the per-upload
  REV_TEXT/`ZWP_ACTR_REF`, the role-respecting write, and the status-≤-Verified guard.

## 6. Open questions → see `VALIDATION-EMAIL.md` (to be sent to the business for sign-off)
The template/column validation + scope confirmation is captured as a ready-to-send email in this folder.
