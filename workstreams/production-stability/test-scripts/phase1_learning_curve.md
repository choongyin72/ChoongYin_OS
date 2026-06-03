# Issue_1052 — Phase 1 Unit Test: Learning Curve

**Date:** 2026-06-03 to 2026-06-04
**Environment:** COPS DEV (db.plutodev.woodside-pluto.tieto-og.cloud)
**Script:** `unit_test_check_rules.py`
**Tag Source:** `issue-1052-tag-list.csv` (661 tags, 28 class/attribute combinations)

---

## Final Result

```
Total assertions : 189  |  Passed : 187  |  Failed : 2  |  Overall : FAIL
TC01–TC06, TC08 : PASS
TC07            : FAIL — LNG tank AVG_TEMP_C is negative (physically correct for LNG ~-162°C)
```

---

## What We Built

Python unit test script connecting directly to COPS DEV Oracle DB via `oracledb`.
Tests all 8 PHD check rules (TC01–TC08) inserted by `Issue1052_PHD_Check_Rules.sql`.

### Sub-Tests Per TC

| Sub-Test | Type | Can Fail? | Description |
|---|---|---|---|
| RULE_EXISTS | Genuine | ✅ Yes | Confirms rule in DB with correct CHECK_ID, TABLE_ID, VARIABLE |
| OBJECT_EXISTS | Genuine | ✅ Yes | Confirms object CODE exists in TV_OBJECTS |
| MAX_DAYTIME | Genuine | ✅ Yes | Gets latest DAYTIME from RV_ view for that object |
| POSITIVE_VALID | Genuine | ✅ Yes | 2-query check: Q1=valid data exists, Q2=negative value exists |
| NEG_NULL_CHECK | Informational | No | Reports if NULL rows exist (rule would fire) |
| NEG_OUTOFRANGE | Informational | No | Reports if 0–100% range breach exists (TC01/TC02 only) |

---

## What We Did Wrong (and Fixed)

### 1. Hardcoded object codes
**Wrong:** Picked stream/tank codes myself without any basis.
**Fix:** Load all object codes dynamically from `issue-1052-tag-list.csv` filtered by EC Class + Attribute. Zero hardcoding.

### 2. Wrong table names — ORA-00942
**Wrong:** Used `TV_STRM_COMP_ANALYSIS` by doing `RV_` → `TV_` string replacement.
**Fix:** Queried `ALL_OBJECTS` to discover actual accessible views. Correct prefix is `RV_` for all 3 classes.

### 3. Self-referencing PASS/FAIL — tests that could never fail
**Wrong:** Sub-Tests 3, 4, 5 set `expected = actual` dynamically — always PASS regardless.
**Fix:** Sub-Test 3 (POSITIVE_VALID) restructured to 2 real queries with fixed expected = `PASS`. Genuinely fails if no valid data or negative value found.

### 4. No DAYTIME filter
**Wrong:** Queries scanned ALL historical dates — mixing results, counts inflated.
**Fix:** Added `AND DAYTIME = TO_DATE(:dt, 'YYYY-MM-DD')` to Sub-Tests 3, 4, 5.

### 5. Hardcoded test date
**Wrong:** Used `TEST_DATE = date(2026, 1, 1)` as arbitrary fixed date — may have no data.
**Fix:** Sub-Test 2b queries `MAX(DAYTIME)` live from RV_ view per object. Sub-Tests 3–5 use `TEST_DATE = 2026-01-01` (verified to have data). `MAX(DAYTIME)` shown for reference.

### 6. Used OBJECT_ID in WHERE clause
**Wrong:** Sub-Tests 3, 4, 5 used `WHERE OBJECT_ID = :oid` — two-step lookup.
**Fix:** RV_ views expose `CODE` column directly. Changed to `WHERE CODE = :code`.

### 7. Tried DV_ views without checking column names
**Wrong:** Applied `DV_TANK_DAY_DIP_STATUS` but kept RV_ column names (`GRS_VOL_SM3`). ORA-00904.
**Finding:** DV_ views use shorter column names without unit suffixes (`GRS_VOL` not `GRS_VOL_SM3`, `OBJECT_CODE` not `CODE`).
**Decision:** Stay with `RV_` views — check rules reference RV_ table IDs, column names match exactly.

### 8. Sub-Test 3 included NULL check — duplicating Sub-Test 4
**Wrong:** Had 3 queries in POSITIVE_VALID including IS NULL check.
**Fix:** Removed NULL query from Sub-Test 3. Now only: Q1=valid data, Q2=negative value.

### 9. Single object per TC
**Wrong:** Only tested the first object from CSV per TC.
**Fix:** Loop ALL unique objects for each TC's EC Class + Attribute. Sub-Test 1 (RULE_EXISTS) runs once; Sub-Tests 2–5 run per object.

### 10. Wrong CSV attribute names for TC06, TC08
**Wrong:** Used `GRS_MASS` and `STD_DENSITY` as attribute lookup keys — not in CSV.
**Fix:**
- TC06: CSV attribute = `ZWP_GRS_MASS`, RV_ column = `ZWP_GRS_MASS_TONNES`
- TC08: CSV attribute = `MEAS_STD_DENSITY`, RV_ column = `MEAS_STD_DENSITY_KGPERSM3`
- CSV uses short names without unit suffixes; RV_ uses full names with units.

### 11. Summary showed last object's result instead of overall TC result
**Wrong:** `TC_META` overwritten on each object iteration → summary showed last object only.
**Fix:** Store `TC_META` on first object only. Summary computes overall TC result: FAIL if ANY object failed.

### 12. Opening files in external windows
**Wrong:** Used `Invoke-Item`, `Code.exe` to open result files.
**Fix:** Always show results directly in chat window. Never open external windows unless user explicitly asks.

---

## Key Technical Learnings

| Topic | Learning |
|---|---|
| EC view naming | `RV_` = reporting view (read), `DV_` = display view (shorter col names), `TV_` = transaction view (DML) |
| CODE vs OBJECT_ID | RV_ views expose `CODE` column — no need to join TV_OBJECTS for data queries |
| TV_OBJECTS | Still needed for Sub-Test 2 (OBJECT_EXISTS) — confirms object registered in EC |
| MAX(DAYTIME) | Always derive test date from DB — never assume a fixed date has data |
| DV_ column names | DV_ strips unit suffixes: `GRS_VOL_SM3` → `GRS_VOL`, `AVG_TEMP_C` → `AVG_TEMP`, `OBJECT_CODE` not `CODE` |
| CSV attribute vs RV_ column | CSV uses short attribute names; RV_ uses full column names with unit suffixes. Map them separately. |
| Self-referencing tests | A test that sets `expected = actual` dynamically can never fail — not a real test |
| Sub-test responsibility | Each sub-test must have one clear responsibility. No overlap between POSITIVE_VALID and NEG_NULL |

---

## Real Finding from TC07

**LNG tank AVG_TEMP_C is negative — physically correct but rule flags it as invalid.**

| Object | AVG_TEMP_C | Issue |
|---|---|---|
| T_LNG_T3101 | -160.6°C | LNG stored at ~-162°C — negative is correct |
| T_LNG_T3102 | -160.4°C | LNG stored at ~-162°C — negative is correct |

**Check rule `PHD_TANK_DIP_AVG_TEMP_VAL1` fires when `AVG_TEMP_C IS NULL OR AVG_TEMP_C <= 0`**

This will produce false ERROR alerts for LNG tanks. Rule needs to be reviewed — either:
- Exclude LNG tanks from this check rule
- Change condition to only fire when `AVG_TEMP_C IS NULL` (not `<= 0`)

**Action:** Raise to Grant before deploying to production.

---

## Object Coverage per TC

| TC | EC Class | Attribute (CSV) | RV_ Column | Objects Tested |
|---|---|---|---|---|
| TC01 | STRM_COMP_ANALYSIS | MOL_PCT | MOL_PCT | 10 |
| TC02 | STRM_COMP_ANALYSIS | WT_PCT | WT_PCT | 3 |
| TC03 | STRM_ANALYSIS | DENSITY | DENSITY | 6 |
| TC04 | STRM_ANALYSIS | GCV | GCV_MJPERSM3 | 9 |
| TC05 | TANK_DAY_DIP_STATUS | GRS_VOL | GRS_VOL_SM3 | 5 |
| TC06 | TANK_DAY_DIP_STATUS | ZWP_GRS_MASS | ZWP_GRS_MASS_TONNES | 2 |
| TC07 | TANK_DAY_DIP_STATUS | AVG_TEMP | AVG_TEMP_C | 5 |
| TC08 | TANK_DAY_DIP_STATUS | MEAS_STD_DENSITY | MEAS_STD_DENSITY_KGPERSM3 | 2 |
