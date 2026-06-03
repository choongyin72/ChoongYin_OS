# Issue_1052 — Phase 1 Unit Test: Learning Curve

**Date:** 2026-06-03 to 2026-06-04
**Environment:** COPS DEV (db.plutodev.woodside-pluto.tieto-og.cloud)
**Script:** `unit_test_check_rules.py`
**Tag Source:** `issue-1052-tag-list.csv` (661 tags, 28 class/attribute combinations)

---

## Final Result

```
Total assertions : 220  |  Passed : 220  |  Failed : 0  |  Overall : PASS ✅
TC01–TC08       : All PASS (42 objects across 8 rules)
IDEMPOTENCY     : PASS — re-run produces no duplicates
ROLLBACK        : PASS — 8 rules deleted then restored cleanly
```

---

## What We Built

Python unit test script connecting directly to COPS DEV Oracle DB via `oracledb`.
Tests all 8 PHD check rules (TC01–TC08) inserted by `Issue1052_PHD_Check_Rules.sql`.

### Sub-Tests Per TC

| Sub-Test | Type | Can Fail? | Description |
|---|---|---|---|
| 1. RULE_EXISTS | Genuine | ✅ Yes | Confirms rule in DB with correct CHECK_ID, TABLE_ID, VARIABLE |
| 1b. SEVERITY_LEVEL | Genuine | ✅ Yes | Asserts SEVERITY_LEVEL = 'ERROR' |
| 1c. WHERE_FORMULA | Genuine | ✅ Yes | Asserts formula exists and contains IS NULL check |
| 1d. REV_TEXT | Genuine | ✅ Yes | Asserts REV_TEXT is set (= 'ECPR-Issue1052') |
| 2. OBJECT_EXISTS | Genuine | ✅ Yes | Confirms object CODE exists in TV_OBJECTS |
| 2b. MAX_DAYTIME | Genuine | ✅ Yes | Gets latest DAYTIME from RV_ view for that object |
| 3. POSITIVE_VALID | Genuine | ✅ Yes | Confirms NOT NULL data exists — rule would NOT fire |
| 4. NEG_NULL_CHECK | Informational | No | Reports if NULL rows exist (rule would fire) |
| 5. NEG_OUTOFRANGE | Informational | No | Reports if 0–100% range breach exists (TC01/TC02 only) |

### Standalone Tests

| Test | Type | What It Proves |
|---|---|---|
| IDEMPOTENCY | Genuine | Re-running SQL script keeps count at 8 — no duplicates |
| ROLLBACK | Genuine | Rollback deletes all 8 rules; restore brings them all back |

---

## What We Did Wrong (and Fixed)

### 1. Hardcoded object codes
**Wrong:** Picked stream/tank codes myself without any basis.
**Fix:** Load all object codes dynamically from `issue-1052-tag-list.csv`. Zero hardcoding.

### 2. Wrong table names — ORA-00942
**Wrong:** Used `TV_STRM_COMP_ANALYSIS` by doing `RV_` → `TV_` string replacement.
**Fix:** Correct prefix is `RV_` for all 3 classes. DV_ also exists but uses different column names.

### 3. Self-referencing PASS/FAIL — tests that could never fail
**Wrong:** Sub-Tests 3, 4, 5 set `expected = actual` dynamically — always PASS regardless.
**Fix:** Sub-Test 3 (POSITIVE_VALID) restructured to genuine assertion. Genuinely fails if no data.

### 4. No DAYTIME filter
**Wrong:** Queries scanned ALL historical dates — inflated counts.
**Fix:** Added `AND DAYTIME = TO_DATE(:dt, 'YYYY-MM-DD')` to Sub-Tests 3, 4, 5.

### 5. Hardcoded test date
**Wrong:** `TEST_DATE = date(2026, 1, 1)` arbitrary fixed — may have no data.
**Fix:** Sub-Test 2b queries `MAX(DAYTIME)` live from RV_ view. Sub-Tests 3–5 use `TEST_DATE = 2026-01-01` (verified to have data).

### 6. Used OBJECT_ID in WHERE clause
**Wrong:** `WHERE OBJECT_ID = :oid` — two-step lookup.
**Fix:** RV_ views have `CODE` column. Changed to `WHERE CODE = :code`.

### 7. Tried DV_ views without checking column names
**Wrong:** Applied `DV_TANK_DAY_DIP_STATUS` but kept RV_ column names. ORA-00904.
**Fix:** DV_ uses shorter names (`GRS_VOL` not `GRS_VOL_SM3`, `OBJECT_CODE` not `CODE`). Stay with RV_.

### 8. Sub-Test 3 included NULL check — duplicating Sub-Test 4
**Wrong:** Had 3 queries in POSITIVE_VALID including IS NULL check.
**Fix:** Removed — Sub-Test 4 handles NULL. POSITIVE_VALID now only checks NOT NULL.

### 9. POSITIVE_VALID used `>= 0` — too strict for LNG tanks
**Wrong:** `WHERE value IS NOT NULL AND value >= 0` — LNG tanks have AVG_TEMP_C = -160°C which is NOT >= 0.
**Fix:** Changed to `WHERE value IS NOT NULL` only. The rule fires on IS NULL, not on negative values.

### 10. Single object per TC
**Wrong:** Only tested first object from CSV per TC.
**Fix:** Loop ALL unique objects for each TC's EC Class + Attribute.

### 11. Wrong CSV attribute names for TC06, TC08
**Wrong:** `GRS_MASS` and `STD_DENSITY` not in CSV.
**Fix:** TC06 = `ZWP_GRS_MASS`, TC08 = `MEAS_STD_DENSITY` (CSV short names without unit suffixes).

### 12. Summary showed last object's result
**Wrong:** TC_META overwritten each iteration.
**Fix:** Store TC_META on first object only. Summary computes overall TC result (FAIL if ANY object fails).

### 13. Opening files in external windows
**Wrong:** Used `Invoke-Item`, `Code.exe` to open result files.
**Fix:** Always show results directly in chat window.

### 14. SQL*Plus `/` terminator breaks oracledb
**Wrong:** `cur.execute(sql_file_content)` failed with `ORA-06550: PLS-00103: Encountered symbol "/"`.
**Fix:** `read_plsql()` helper strips all lines after the `/` terminator before executing.

### 15. RULE_EXISTS didn't check SEVERITY, WHERE_FORMULA, REV_TEXT
**Wrong:** Only confirmed rule exists by name — didn't verify correctness of configuration.
**Fix:** Expanded to also assert SEVERITY_LEVEL = 'ERROR', WHERE_FORMULA IS NOT NULL + contains 'IS NULL', REV_TEXT is set.

### 16. No idempotency or rollback tests
**Wrong:** Never verified re-runnability or rollback safety.
**Fix:** Added `test_idempotency()` and `test_rollback()` as standalone tests.

---

## TC07 — False Alarm (Corrected)

**Originally reported:** TC07 LNG tanks AVG_TEMP_C = -160°C would trigger false ERROR alerts.

**Corrected finding:** Query confirmed WHERE_FORMULA = `(${AvgTemp} IS NULL)` — only fires on NULL, NOT on negative values. LNG tanks at -160°C are safe. Our POSITIVE_VALID test was wrong (checking `>= 0`), not the rule. Fixed in iteration 9 above.

---

## Key Technical Learnings

| Topic | Learning |
|---|---|
| EC view naming | `RV_` = reporting view, `DV_` = display view (shorter cols), `TV_` = transaction view |
| CODE vs OBJECT_ID | RV_ views expose `CODE` — no need to join TV_OBJECTS for data queries |
| TV_OBJECTS | Needed for OBJECT_EXISTS check — confirms object registered in EC |
| MAX(DAYTIME) | Always derive test date from DB — never assume a fixed date has data |
| DV_ column names | `GRS_VOL_SM3` → `GRS_VOL`, `AVG_TEMP_C` → `AVG_TEMP`, `OBJECT_CODE` not `CODE` |
| CSV attribute vs RV_ column | CSV uses short names; RV_ uses full column names with unit suffixes |
| SQL*Plus `/` terminator | `oracledb` can't execute scripts with `/` — strip with `read_plsql()` helper |
| Self-referencing tests | `expected = actual` dynamically = can never fail = not a real test |
| WHERE_FORMULA | Must contain IS NULL — confirms rule fires for missing PHD data |
| REV_TEXT | Mandatory for traceability — confirms which ECPR implemented the rule |

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
