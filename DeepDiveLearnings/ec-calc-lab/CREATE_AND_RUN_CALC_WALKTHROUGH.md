# EC Calculation — Create → Connect → Run (VERIFIED demo walkthrough)

_Proven end-to-end on the local sandbox 2026-06-29 (web sysadmin; DB localhost:1521/ORCL ECKERNEL_EC). Every
step DB/fact-verified. Object: `AUTOTEST_CALC_TEST` (EQUATIONS/MAIN/EC_PROD/DAY), run on network `P1_DAY_ALLOC`._

This is the disposable-test recipe for "build my own calc and run it". Refer to
[[EC_CALC_SCREENS_REFERENCE.md]] for the exact element ids of each screen.

## Outcome proven
Created my own calc → connected it as a job → ran it via Daily Allocation Simulate → **Exit Status =
"Simulate Success"**, log line **INFO "Test: 3"** (my calc's own equation `INFO = 'Test: ' +
engineParameter('run_no')`). Simulate = dry-run, no real allocation data written. Evidence:
`evidence/calc_10..12_*.png`.

## Step 1 — Create the calc  (screen: Create Calculation)
- Date + Calculation Context = **Production Allocation** (EC_PROD) + GO.
- Create = **Copy-To-New** from a donor (VERSIONS area): New Code `AUTOTEST_CALC_TEST`, New Name, New Start
  Date → **"Copy To New Calculation"**. Donor `RUN_NO_TEST` (EQUATIONS) → inherits a valid logging equation.
- DB-verify: row in `CALCULATION` (object_code=AUTOTEST_CALC_TEST, calc_type=EQUATIONS).

## Step 2 — Equation  (screen: Maintain Calculation)
- The copy already carries a valid equation (`INFO = 'Test: ' + engineParameter('run_no')`), so no authoring
  needed for the demo. (Authoring from scratch needs the canvas math-editor — not headless-typable.)

## Step 3 — Connect the calc as a job  (screen: Calculation Group Setup)  ← the hard part, now solved
1. Date + **Calculation Group Context = "Allocation Network Calculation"** + GO.
2. Click the **P1_DAY_ALLOC** network row → bottom tabs appear.
3. Open the **CALCULATION JOB CONNECTION** tab (shows existing jobs: Calculation Test, Daily Well Volume).
4. **Insert (+) → "Calculation Job"** adds a new blank row.
5. **CRITICAL — the Insert drops the new blank row in the MIDDLE and pushes existing rows down.** Do NOT
   assume the new row is the last index. **Find the row that is actually empty** (read each row's Start Date)
   and fill THAT one: Start Date `2011-01-01` + Calculation Job dropdown = **AUTOTEST Calc Test**.
6. Confirm **no row is left empty** (EC validates every row on Save; a blank row → silent reject with banner
   "Required fields are empty … on row N").
7. **Click Save** (EC never auto-saves). DB-verify in **`tv_alloc_network_job_conn`** (NOT DEPENDENT_CALC_JOB):
   AUTOTEST_CALC_TEST present, and existing connections (CALC_TEST, EC_DAILY_VOLUME) retained.

## Step 4 — Run it  (screen: Daily Allocation)
1. From Date + To Date (e.g. 2026-06-27) · Allocation Network Group = **P1 Day Allocation** · **Calculation
   Job = AUTOTEST Calc Test** (now offered because Step 3 connected it) · GO.
2. (Optional) Log Level = Full · **tick Simulate** (safe dry-run) — verify it's ticked before running.
3. **Run Calculations** → OK → GO/refresh to load the result grid.
4. Verify: result row **Exit Status = "Simulate Success"**, and the log shows my calc's INFO line.

## Step 5 — Self-clean (leave sandbox as found)
- Calculation Group Setup → P1_DAY_ALLOC → CALCULATION JOB CONNECTION → select the AUTOTEST row → Delete →
  Save → DB-verify gone from `tv_alloc_network_job_conn` (CALC_TEST + EC_DAILY_VOLUME remain).
- Create Calculation → select AUTOTEST_CALC_TEST → **Delete Calculation → Yes** → DB-verify 0 rows + 0 orphan
  equations.

## Gotchas that cost time (so the next run is fast)
- **Read the on-screen error first** — it names the exact failing field/row.
- **EC never auto-saves** — explicit Save click, then DB-verify (a click ≠ persisted).
- **Insert adds the new row in the MIDDLE** — fill the actually-empty row, not a fixed index.
- **Correct backing table = `tv_alloc_network_job_conn`** (DEPENDENT_CALC_JOB is the wrong table).
- A lingering autocomplete dropdown panel can invisibly intercept clicks — dismiss/hide it (or force-click).
- Network-job eligibility is NOT limited to PROCESS calcs — EQUATIONS calcs connect fine (11 exist).
