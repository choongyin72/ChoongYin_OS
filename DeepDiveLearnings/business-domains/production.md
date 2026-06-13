# EC Production — domain dive 1 (2026-06-13, local sandbox)

Sources: live menu walk (`tmp/biz_domains/ec_production_branch.txt`, 371 nodes) ·
DB row counts · DOC-04 KB chapter · live scheduler history. Goal: enough business
understanding to design **business test-case suites** ([[project_ec_coverage_goal]] phase 2).

## 1. The menu (what the business actually works with daily)
EC Production branch sections:
| Section | What it is | Sandbox data? |
|---|---|---|
| Daily/Deferment Dashboards, Production Efficiency | KPI widgets (CTRL_DASHBOARD, fed by allocation results) | after alloc runs |
| **Well and Reservoir** | per-WELL data entry/view: Event / Sub Daily / **Daily** / Period / Monthly + Well Finder | ✅ PWEL_DAY_STATUS **84.5k rows** |
| **Production Operations** | same rhythm for Equipment / Stream / Tank / Test Device | ✅ EQPM_DAY_STATUS 39.5k, STRM_DAY_STREAM 66k, TANK_MEASUREMENT 16k |
| Production Testing | well-test workflow PT.0005→0009→0010→0011→0025 + perf/decline curves | ✅ PWEL_RESULT 220, PWEL_SAMPLE 25k |
| Production Deferment | PD.0020 events, loss accounting, corrective actions | ✅ DEFERMENT_EVENT 59, DEFER_LOSS_* 444 |
| Planning and Forecasting | Forecast / Plan | FCST_* (ZWP_PROD_TARGET precedent feeds FCST_FCTY1_DAY_STATUS) |
| **Hydrocarbon Accounting** | Daily/Monthly Data Status Processes (P→V→A), Month Locking, **Allocation** | ✅ PWEL_DAY_ALLOC 120, STRM_DAY_ALLOC 8 |
| Cargo Administration / Chemicals | cargo + chemical inventory views | partial |

## 2. THE core daily business flow (live-evidenced on this sandbox)
```
InitiateDay (scheduler, ran 2026-05-29 OK)
  └─ instantiates the new production day's empty status rows (SYSTEM_DAYS 5.7k)
Operators / interfaces fill DAILY STATUSES
  └─ PWEL_DAY_STATUS (wells), EQPM_DAY_STATUS, STRM_DAY_STREAM, TANK_MEASUREMENT
     (ECIS uploads land here too — my CLAUDE_WELL_TEST wrote PWEL_DAY_STATUS!)
Well tests refresh allocation basis
  └─ PT.lifecycle → PWEL_RESULT (theoretical rates per well)
Deferments recorded when production misses plan
  └─ PD.0020 → DEFERMENT_EVENT (+ loss split into DEFER_LOSS_*)
DailyProductionAllocation (scheduler, ran 2026-05-29 OK)
  └─ reconciles delivery-point measurements back to wells over the allocation network
     → PWEL_DAY_ALLOC / STRM_DAY_ALLOC (+ dashboards light up)
Record Status Processes (CO.0076)
  └─ P → V (daily verify) → A (monthly approve) → Month Lock (no further writes)
```
Everything in Production hangs off this loop; monthly is the same loop at month grain.

## 3. Where our existing work already touches this domain
- **ECIS upload** (CLAUDE_WELL_TEST) writes PWEL_DAY_STATUS = the "operators/interfaces
  fill daily statuses" step. The PHD-backup task = exactly this step's emergency path.
- **Issue_1052 validations** (frozen/sum checks) = quality gates on these same daily
  statuses before verification.
- **Dispatching/Assets objects** we automate = the master data this flow runs on.
- Record status P (Provisional) on everything we insert = first state of this lifecycle.

## 4. Candidate BUSINESS TEST CASES (for the phase-2 suites — to propose to Choong-Yin)
1. **Daily-cycle smoke**: InitiateDay (Run Now) → assert new day's PWEL_DAY_STATUS rows
   exist for active wells → enter one well's day data → run DailyProductionAllocation →
   assert PWEL_DAY_ALLOC row + dashboard value. (One E2E thread through the whole loop.)
2. **Status lifecycle**: insert P data → run Verify status process → assert V → attempt
   edit (expect restriction per validation level) → approve → month lock → assert write
   rejected. (Tests the governance spine.)
3. **Deferment loss math**: create PD.0020 Down event with loss rate × downtime → run
   Calculate Deferment → assert event loss + day allocation impact.
4. **Well test → allocation basis**: enter PT single test → accept → assert PWEL_RESULT
   feeds next allocation differently.
5. **ECIS backup path** (ties to the real task): upload day data via Excel when "PHD down"
   → staging review → promote → allocation consumes it identically.
All five are DB-verifiable (counts/values in *_DAY_STATUS / *_DAY_ALLOC) = our proof style.

## 5. HANDS-ON exercise log (2026-06-13 ~00:39 local)
Attempted the daily-cycle hands-on: RUN NOW on InitiateDay (enabled, pinned EC-Cluster:ECDS).
**What I learned about the scheduler internals (deep dive while debugging):**
- RUN NOW creates a one-shot Quartz trigger named `<name>--!##RERUN##!<UTC-stamp>` in the
  QRTZ_* clustered job store; EC's TV_* config sits ON TOP of plain Quartz.
- Scheduler instance = `ECDS` (container id.ECDS), check-in every 7.5s
  (QRTZ_SCHEDULER_STATE); job class = BusinessControllerInvokerJob.
- **FINDING: trigger acquisition is STALLED on the sandbox since ~2026-06-12 15:00** —
  my CLAUDE trigger (due 18:00) AND the InitiateDay rerun trigger sit WAITING past their
  fire times; QRTZ_FIRED_TRIGGERS empty; no paused groups; locks normal; instance checks
  in fine. Quartz layer healthy ⇒ the EC app's scheduler executor is stuck (likely needs
  an app/container restart). All scheduler runs earlier on 2026-06-12 (incl. my ECIS runs
  at 14:24/14:55) worked.
- ⚠️ CONSEQUENCE for the ECIS RE-TEST with Choong-Yin (2026-06-14): RUN NOW will NOT
  execute until the EC app is restarted. Flag this first.
- InitiateDay exercise itself = PENDING until scheduler revives (then: expect SYSTEM_DAYS
  + ~360 PWEL_DAY_STATUS rows for the new day, then DailyProductionAllocation).

## 5b. Open questions for Choong-Yin (domain truths I can't infer)
- Which of these flows does WOODSIDE actually run on Pluto (As-Built scope)? e.g. is
  deferment in scope? which allocation networks?
- Safe to run InitiateDay / DailyProductionAllocation on the LOCAL sandbox for test #1?
  (They ran 2026-05-29, so the config exists; but blast radius of a new day?)
- Month-lock state on sandbox — which months are locked (affects what tests can write)?
