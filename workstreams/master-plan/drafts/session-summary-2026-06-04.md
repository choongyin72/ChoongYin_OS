# Session Summary — 4 June 2026

**Date:** 2026-06-04
**Main Focus:** Issue_1052 — Evidence Document refinement + WHERE_FORMULA corrections

---

## Key Accomplishments Today

### 1. Evidence Document — v1.3 (Final)
File: `workstreams/production-stability/sql-scripts/Issue1052_Evidence_COPS_DEV.docx`

**Section 5.3 restructured:**
- Table 1: Check Rule Configuration (TC, Rule, ID, RV Table)
- Table 2: Split into 8 separate tables — one per TC
- TC01 & TC02: 7 columns with Component No (STRM_COMP_ANALYSIS has component dimension)
- TC03–TC08: 6 columns (no component)
- Each row = one object (or object+component) with MAX(DAYTIME) and actual DB value

**Section 5.3.2 added:** WHERE_FORMULA correction note (TC03/TC04/TC08 fixed from `<= 0` to `< 0`)

**Document History:** v1.0 → v1.1 → v1.2 → v1.3

### 2. WHERE_FORMULA Corrections — Critical Fix

**Problem found:** SQL script had `<= 0` for 3 rules. Incorrect — system initialises data to 0.0 waiting for PHD, so 0.0 is a valid state. Existing EC pattern uses `< 0`.

**Rules corrected:**
| Rule | Before | After |
|---|---|---|
| PHD_STRM_ANALYSIS_DENSITY_VAL1 | `<= 0` | `< 0` |
| PHD_STRM_ANALYSIS_GCV_VAL1 | `<= 0` | `< 0` |
| PHD_TANK_DIP_STD_DENSITY_VAL1 | `<= 0` | `< 0` |

**COPS DEV DB updated.** All 3 rules confirmed in DB with correct `< 0` formula.

### 3. Unit Test Script — Final State
File: `workstreams/production-stability/test-scripts/unit_test_check_rules.py`

**Parameters added:**
- `strict_positive=True` — for rules firing on `<= 0`, positive check uses `> 0`
- `null_only=True` — for TC07 AVG_TEMP_C (IS NULL only rule), any NOT NULL value valid
- `strict_positive` removed from TC03/TC04/TC08 after correction to `< 0`

**Final run: 220/220 PASS ✅**

### 4. Key Learning — NEVER Make Assumptions on Spec
**Feedback saved to memory.** If spec condition unclear → always ask user first. Never use "engineering judgement" as substitute for spec reference.

---

## Current WHERE_FORMULA for All 8 Rules (COPS DEV — Confirmed)

| CHECK_ID | Rule | WHERE_FORMULA |
|---|---|---|
| 1142 | PHD_STRM_COMP_MOL_PCT_VAL1 | `(${MolPct} IS NULL OR ${MolPct} < 0 OR ${MolPct} > 100)` |
| 1143 | PHD_STRM_COMP_WT_PCT_VAL1 | `(${WtPct} IS NULL OR ${WtPct} < 0 OR ${WtPct} > 100)` |
| 1144 | PHD_STRM_ANALYSIS_DENSITY_VAL1 | `(${Density} IS NULL OR ${Density} < 0)` |
| 1145 | PHD_STRM_ANALYSIS_GCV_VAL1 | `(${Gcv} IS NULL OR ${Gcv} < 0)` |
| 1146 | PHD_TANK_DIP_GRS_VOL_VAL1 | `(${GrsVol} IS NULL OR ${GrsVol} < 0)` |
| 1147 | PHD_TANK_DIP_GRS_MASS_VAL1 | `(${GrsMass} IS NULL OR ${GrsMass} < 0)` |
| 1148 | PHD_TANK_DIP_AVG_TEMP_VAL1 | `(${AvgTemp} IS NULL)` |
| 1149 | PHD_TANK_DIP_STD_DENSITY_VAL1 | `(${StdDensity} IS NULL OR ${StdDensity} < 0)` |

---

## Test Data Analysis — Final Verdict

All 8 check rules aligned with spec:
- TC01/TC02: 0.0 for component percentages is valid (rule uses < 0 OR > 100)
- TC03/TC04: 0.0 is valid initialised state (rule uses < 0, not <= 0)
- TC05/TC06: 0.0 volume/mass is valid (empty tank scenario)
- TC07: -160°C LNG is valid (rule IS NULL only)
- TC08: 454 kg/Sm3 valid (rule uses < 0)
- TC01 `1C1401_TO_E1405AB / N2` = NULL — FAIL (no data ever received from PHD — expected)

---

## Pending Tasks (EOD 4 June 2026)

| # | Task | Status |
|---|---|---|
| 1 | Rebase ECPR-31030/31/32/34 | 🟡 Monitor — release team |
| 2 | Verify 1.0.37-RC1 ECaaS TEST | 🔴 Pending |
| 3 | BLP Offtake Report | 🔴 Overdue (was 5 Jun) |
| 4 | Raise ECPR for R_BLP_MONTHLY_ALLOC_PLUTO | 🟡 Pending |
| 5 | Merge PRs #603–606 | 🟡 Monitor — release team |
| 6 | Issue_1052: Reply to Grant | 🟡 Ready — Phase 1 done |
| 7 | Daniel Perez UAT blockers | 🔴 Overdue |
| 8 | Issue_1052: 6 ECPR drafts A–F | ⏳ Waiting Grant |

---

## Next Steps

**Phase 2:** EC Web App System Test via Robot Framework — plan to be enhanced
- Sandbox was down earlier today, now back up (with restarts)
- Robot Framework suite ready at `tests/validation/issue_1052_check_rules.robot`
- plutodev.yaml environment config confirmed working

**Issue_1052 SQL script** — needs ECPR number before moving to Woodside project
- Current REV_TEXT = 'ECPR-Issue1052' (placeholder)
- Must get real ECPR number from Grant before Woodside deployment
