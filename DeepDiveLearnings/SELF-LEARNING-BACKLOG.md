# Self-Directed Deep-Dive Learning — Master Backlog
Standing protocol (user, 2026-06-13): **when idle and no one is pinging me, I draft/continue a
deep-dive self-learning plan and kick it off autonomously. On any blocker: stop → rethink →
deeper dive (alternative source/angle) → retry → resolve** ([[feedback_blocker_rethink_cycle]],
[[feedback_never_idle_deep_dive]]). This file is the single prioritized queue — pick the top
unblocked item, do it, leave an artifact, check it off, repeat.

## Blocker handling (user-confirmed 2026-06-13)
On a blocker: **pause → reassess → try to resolve independently** (rethink, alternative
source/angle). **If still unresolvable, do NOT get stuck — move to the next planned topic and
continue learning.** Log the blocker + outcome (resolved / skipped) in the Blocker Log below.

## Worklog for next user review (append every block; user reviews when back)
- 2026-06-13: Dispatching slice 2 (Nomination Cycle + Meter live 4/4, popup-picker T1; Pipeline
  parked) — committed 156c1ff. · Business-domain curriculum (5 domains + glossary + test backlog
  + As-Built index) — committed a3e6057.
- 2026-06-13: As-Built 14 (daily allocation + monthly + GHG/PRRT) + As-Built 05 (interfaces;
  reframed ECIS task) → notes; ECIS memory updated. NOT committed yet.
- 2026-06-13: ECpedia EFK Phase A done — TAF (stub), Calc Framework (allocation recipe), ECIS
  (pluggable adapters), Environment (redirect). NOT committed yet.
- 2026-06-13: As-Built 09 Validations (xlsx) READ — full Issue_1052 rule catalog w/ Check Rule
  IDs → ASBUILT09-VALIDATIONS.md; Issue_1052 memory updated. Confirms rules 1156/1157 + pins the
  2 missed layers (V_DAILY_MISSING_DATA 1058-1074 + SCREEN/Class layer). NOT committed yet.
- 2026-06-13: As-Built 06 Calculations (105pp docx) READ — calc inventory (ZWP_ALLOC_*, C_PRRT,
  ZWPC_EMISSION_DISCHARGE 11-step, component set C1-nC5), engine variable<->class.column model,
  + the full PHD->validations->massbalance->allocation->emissions/CO2e->contract-accounts->PRRT
  data-flow chain → ASBUILT06-CALCULATIONS.md. NOT committed yet.
- 2026-06-13: EFK Phase B sampled (HCA, Sales Allocation, industry page) — EFK domain pages are
  thin intros linking to RD130 release-docs; depth already held. Captured allocation rationale
  (custody-transfer / fiscal metering / reconciliation factor) + PRRT/RAU/CO2e/component-set/
  lifting-year into GLOSSARY. EFK deep dive effectively complete; RD130 = future product source.
- 2026-06-13: COMMITTED be9d537 (15 files) — all As-Built syntheses + EFK notes + backlog, pushed. Standing PK auto-commit grant now active for my deep-dive work.
- 2026-06-13: As-Built 07 Reports READ → ASBUILT07-REPORTS.md (35-report catalog; NOPTA/PRRT/Petroleum-Statistics/NGER/NPI/Safeguard regulatory theme) + CAPSTONE tying the whole As-Built chain. As-Built deep dive substantively complete.
- 2026-06-13: Produced Pluto-PRIORITIZED coverage backlog (ec-automation/docs/coverage_pluto_prioritized.md)
  by cross-ref As-Built 02 screen catalog x automated registry. Finding: master-data layer largely
  done; the real Pluto value is the daily/monthly STATUS data-entry grids (new T2 pattern N1) +
  RUN/status-process screens. Next slice = build N1 "daily-status grid" T2 on WR.0001. Committed.
- 2026-06-13: Wrote EC Web App Internals field guide (ec-automation/docs/ec_webapp_internals.md) —
  consolidated reverse-engineered framework/PrimeFaces/DOM knowledge (id grammar, screen types,
  the working gestures incl. popup/dd/save, config layers, SI units, DB-verify). Accelerates every
  future screen build. Committed. Also: standing-autonomy+coaching grant saved to memory.
- 2026-06-13: As-Built 11 Notification/MHM READ → ASBUILT11-NOTIFICATION.md (committed c06653c).
  The human-in-the-loop signalling layer: Email (MHM: Actor MHM.0012 / Distribution List MHM.0001 /
  Message Distribution MHM.0004 / Message Journal MHM.0007 = test oracle; SMTP via Remote Endpoint
  Config) + Todo (bell/TODO screen). KEY: only **N_R_D_VALIDATION_REVIEW** is live <new scope> (ties
  to Issue_1052); the 14 <Phase 2> notifications ARE the spec for the future monthly approval
  workflow (verify→approve provisional→approve final by QMI/Topside/Wells→lock). 8 Pluto DLs map
  the role taxonomy. As-Built reference now: only 01 SystemConfig + 03 ObjectConfig (both xlsx) left.
- 2026-06-13: Self-improvement health check — verified T3 popup delegation (meter_page delegates
  cleanly to shared `Pick From EC Object Popup`, no inlined duplication) + screen-registry audit
  (all Dispatching screens incl. Meter/Pipeline-parked/Nomination Cycle current with hard-won facts).
  Framework + registry confirmed healthy; no refactor needed. (No code change → nothing to commit.)
- 2026-06-13: N1 daily-status-grid pattern — wrote design doc (committed c914e72) THEN live+DB recon
  of WR.0001 Daily Production Well Status 1 (committed c63d1ab). Answered 6/7 unknowns: iframe nav
  Date+PU+(Well Hookup|Facility Class 1)→GO `button:form:B`; GROUPMODEL/WELL; table PWEL_DAY_STATUS
  (+WELL_HOOKUP_DAY_STATUS) key (OBJECT_ID,DAYTIME); **rows pre-instantiated → edit-in-place, NO IUD**;
  RECORD_STATUS/APPROVAL per-row (P→V→A) + on-screen VALIDATION tab. Registry row added. **Open #4**:
  grid cell ids need a data-bearing PU (generic sandbox P1 has no wells; 84,914 PWEL rows exist under
  other PUs — one well→facility-class→PU join finds a usable scope to finish the grid capture).
- 2026-06-13: WR.0001 recon now COMPLETE (7/7). Cracked #4: the navigator is a 4-level cascade
  PU→Area→Facility Class 1→**Well Hookup** (FC1/WH cascade from AREA, not PU — earlier scan gave
  false zeros). Full scope @ seed date 2003-01-01 (113 filled wells; default ~today empty — confirms
  version-filter rule) renders the grid: **`daily_well_status:form:T_data`**, cells
  **`daily_well_status:form:T:{r}:C{c}_in`** (+`_dd_input` dd cols), grouped headers Well/Choke/
  WellHead/Downhole/GasLift/MeasuredRates/MultiphaseMeter/Theoretical/Override/Allocated/ESP. Working
  scope: AS2 EC Exploration Norway / AS2_Onshore Area / AS2_Production Facility no 1 / AS2_Lift Gas
  Manifold 1. Design doc + registry updated. **N1 build now fully unblocked** — next = T2
  daily_status_grid.resource + T3 wr0001 page + DbVerify.value_in_day_status, dryrun→live→DB-verify.
- 2026-06-13: N1 BUILD (dryrun-green). Settled the frame question — the screen IS the main frame
  (top-level locators work, no iframe piercing; earlier "nested iframe" was a Playwright detach
  artifact). Built: T1 DbVerify day-status helpers (self-tested vs live DB, 4b8e96f); T2
  resources/daily_status_grid.resource (reusable N1 edit-in-place layer on existing T1); T3
  pageobjects/Production/wr0001_daily_well_status_page.resource (cascade + scope); suite
  tests/Production/daily_well_status_edit.robot (self-reverting edit→Save→UI+DB verify→revert).
  **Robocop clean + --dryrun 3/3 PASS; re-dryran nomination_cycle (DbVerify consumer) PASS (no
  breakage).** Remaining = first LIVE run (headed): pin ROW0_WELL_NAME + ROW0_CELL↔ROW0_DB_COLUMN
  (edit→Save→diff PWEL_DAY_STATUS), then it proves N1 end-to-end + generalizes to PO.0002.
- 2026-06-13: N1 LIVE run — honest result. TC01 PASS (cascade+GO renders rows LIVE → nav/read path
  fully proven). TC02/03 FAIL: inline-grid EDIT does NOT persist; DB-verify correctly caught it (no
  false pass). Two findings: (1) toolbar Save (`screenToolbar:form:menuB…`, onclick EC.forceChange)
  stays DISABLED after a cell edit — the OV/TV Save gesture doesn't commit this grid; Ctrl+s also no.
  (2) CORRECTION of earlier overconfidence: the grid is NOT 1:1 with PWEL_DAY_STATUS raw cols — only
  C4=24=ON_STREAM_HRS lined up; the rate cols (791/4822/2186/187 in DB) ≠ grid cells (644/5081/2356/
  239), so the grid shows derived/blended values; true cell↔col map needs a real edit→commit→diff.
  DATA INTEGRITY VERIFIED INTACT (no PWEL_DAY_STATUS col=21; phantom 21 = unsaved view-state).
  Next genuine blocker = crack the inline edit→commit gesture (what enables that Save / edit-mode /
  row action / status gate), then establish the column map. Coaching note logged below.
- 2026-06-13: 🎉 N1 WRITE SOLVED + suite GREEN 3/3 LIVE (DB-verified, self-cleaning). Cracked via a
  HEADED capture of the USER's real save: the working gesture = (1) edit cell with real keystrokes +
  Tab → fires the cell `change` behavior (POST source=...C{c}_in event=change) which STAGES the value;
  (2) toolbar Save (`screenToolbar:form:menuBar`, execute=@all) → COMMITS. My 14 fails = step 1 never
  fired (fill() doesn't; or value==phantom=no-op). Automated replica DB-verified 24→22→24. Fixed T3 to
  resolve well BY NAME (Well no 2 = row 1, not 0) + reload-before-revert for edit→save→edit chaining.
  Updated T2 daily_status_grid (Daily Status Row Index For + gesture docs), T3, suite, registry, scorecard.
  N1 rung C→A. Next: generalize to PO.0002 Daily Gas Stream Status (reuse the pattern).
- 2026-06-13: PO.0002 Daily Gas Stream Status recon — N1 pattern GENERALIZES (proven, not a one-off).
  Same nav cascade one level shorter (Date→PU→Area→Facility Class 1; no Well Hookup), same GO, same
  save gesture (transfers from WR.0001). Two grids: editable `measured:form:T_data` (cells
  measured:form:T:{r}:C{c}_in) + read-only `derived:form:T_data`. Physical table = STRM_DAY_STREAM
  (the URL CLASS_NAMEs _MEAS_GAS/_DER_GAS are view projections — lesson: class≠table here). T2
  `daily_status_grid` reuses verbatim (keywords take grid_id/cell_id/table as args). Registry row +
  design-doc generalization section added. Build pending = thin PO.0002 T3 + suite + a stream→OID
  DbVerify helper + pin C{c}↔STRM_DAY_STREAM column, then live edit→save→DB-verify→revert (mechanical).
- 2026-06-13: 🎉 PO.0002 Daily Gas Stream Status BUILT + live 3/3 (DB-verified, self-cleaning) — the
  N1 pattern GENERALIZES (2 proven screens now). Post-restart clean slate; mapped C7=STRM_DAY_STREAM.
  GRS_VOL via edit→save→diff; stream resolved by name via OV_STREAM. Refactored T2 DB-verify to a
  generic `Object Id By Name` (DbVerify) + comma-tolerant `Daily Status Cell Should Show` / `Read
  Daily Status Cell` (gas rates formatted 2,949.9). WR.0001 re-tested 3/3 (no regression from the
  shared-keyword change). Robocop clean. NOTE: running 2 N1 suites in ONE robot invocation is flaky
  (2nd suite's grid load races — "object not found"); run N1 suites individually OR add inter-suite
  session reset (known limitation, logged). Next: extend to liquid/water/electrical/well-comp.
- 2026-06-13: N2 recon — HA.0002 Daily Allocation (`/com.ec.prod.ha.screens/edit_daily_alloc`): RUN
  screen, nav = From Date + To Date + Allocation Network Group/Network + Calculation Job, GO=button:form:B
  (no edit grid until run). Writes PWEL_DAY_ALLOC / STRM_DAY_*_ALLOC. (Did NOT run a calc — pending
  user's view on what to verify + safe test day.)
- 2026-06-13: ECpedia/EFK DEEP-DIVE SERIES set up (user-directed) → DeepDiveLearnings/ecpedia-efk/
  EFK-DEEP-DIVE-SERIES.md. Enumerated all 33 EFK home children (CQL parent=1835010), categorized +
  phased by value (P1 domain modules → P2 calc/framework → P3 reference → P4 ops-on-demand → P5 skip).
  Kicked off: read Hydrocarbon Accounting (allocation network) + the calc-engine critique → GOLD
  (calc-engine-insights.md: variable-cache/dimensioned-variable model + the allocation TEST ORACLE
  for N2). EC Production parent = thin diagram (children later). Series runs during idle going fwd.
  NOTE (user 2026-06-13): commit ONLY inside C:\Projects\ChoongYin_OS; external writes (incl Confluence)
  need explicit permission, never silent.
- 2026-06-13: N2 allocation (HA.0002) deep recon + run attempt → pattern_n2_allocation_run_design.md.
  Mapped screen/nav/networks (AS2_Onshore etc.)/result tables (PWEL_DAY_ALLOC ALLOC_*_VOL per well;
  STRM_DAY_*_ALLOC at PC/company/component grains). ⛔ HONEST BLOCKER: the allocation RUN is NOT
  executable in this sandbox — G3/G4 dds empty after network pick, GO surfaces no Run control, no
  row created, and toolbar shows "Process automation not available" (the calc executor; separate
  from the Quartz scheduler the user restarted). NOT cracked (unlike N1) — needs PA enabled or a
  known run path (SME). ✅ Doable now: the VERIFY half — conservation oracle on EXISTING results;
  no-negatives invariant VERIFIED on 2021-10-01 (0 negative ALLOC_* values). Next: DbVerify
  allocation-conservation helper + read-only suite on existing data (no run needed). OPEN Q for user:
  can Process Automation be enabled locally / what's the supported allocation-run path?
- 2026-06-13: N2 RUN MECHANISM CRACKED (corrects 2 wrong conclusions). HA.0002 runs allocations
  SYNCHRONOUSLY via green "RUN CALCULATIONS" button (`ProdAllocButton:form:B`) — NOT BPM ("process
  automation not available" = BPM bell red herring; PA=BPM, skip per SME). Flow: date + Network
  (must have a calc job in ALLOC_NETWORK_JOB_CONN — AS2_Onshore has none; P1 Dashboard/Resv/Testing
  do) + Calc Job (EC_DAILY_VOLUME="Daily Well Volume" etc.) → RUN → job runs ~1-2s → result in
  log_list (Success/Failure + downloadable log). Simulate checkbox = run flow but NEVER write DB
  (SME; safe iteration). Ran EC_DAILY_VOLUME/P1 Dashboard/2021-10-01 → **Failure** (equation errors:
  "Failed to execute equation step / evaluate iteration / calculate-assign") = real finding (calc
  errors, doesn't complete). Next: find a Success case (try RUN_NO_TEST test network, or a P1 date
  with complete input) via Simulate, then verify conservation oracle. CALIBRATION: I was wrong twice
  — (1) "PA blocks the run" (it doesn't; found RUN CALCULATIONS); (2) implied executor dead (jobs DO
  run, in 1-2s). DB-as-truth + reading the log_list corrected both.
- 2026-06-13 ~22:55: N2 SUCCESS exit achieved — "Testing allocation RUN_NO" + "01 Run No .test"
  @2003-01-01, Simulate ON → log_list = **"Simulate Success"** (executor: WAITING→ACQUIRED→Success,
  ~1s). Confirms the full run path works; the P1 EC_DAILY_VOLUME Failure is that calc's own equation
  defect, not the mechanism. Run path FULLY PROVEN.
- 2026-06-13: 🎉 N2 RUN-verify suite BUILT + live 3/3 (DB-verified, no DB write). HA.0002 Daily
  Allocation, layered T1→T3: T2 `resources/allocation_run.resource` (set date range / network(G:2) /
  calc job(G:4) / Simulate / RUN CALCULATIONS `ProdAllocButton:form:B` / poll `log_list` Exit Status),
  T3 `pageobjects/Production/ha0002_daily_allocation_page.resource` (scope), suite
  `tests/Production/daily_allocation_run.robot`, + DbVerify conservation oracle
  (`allocation_conservation_should_hold` = no-neg + rows-exist). **TC01 positive** "Testing allocation
  RUN_NO"/"01 Run No .test"@2003-01-01 → **Success**; **TC02 negative** "P1 Dashboard"/"Daily Well
  Volume"@2021-10-01 → **Failure** (real calc-engine equation defect); **TC03** conservation oracle on
  PWEL_DAY_ALLOC@2021-10-01 (22 wells, 0 neg). All runs **Simulate ON = no DB write — VERIFIED**
  (22 rows/0 neg unchanged after). Build calibration: the Simulate checkbox is the `:cb` *input*
  itself (id `dateStartJob:form:G:0:R:1:C:2:cb`, native input styled ECCheckboxCell) — there is NO
  `...C:2` container; the live `Click` hung until I JS-clicked the input. log_list cell map:
  NETWORK=4, EXIT STATUS=7, newest=top. Non-simulate path stalls in the Quartz executor (ACQUIRED) —
  functional tests use Simulate. Robocop clean; full-suite --dryrun 235/235; N1 canary (WR.0001) still
  live 3/3 (additive DbVerify edit safe). Design doc + registry (HA.0002 row + N2 type pattern) +
  scorecard updated. Recon scripts: `tmp/scripts/n2_*`.
- 2026-06-14: EFK series CLOSED for value (Phases 1–3: Production→Revenue chain, VCF, Database Sanity,
  Extensions Matrix; notes in `ecpedia-efk/`). N2 sum-to-total extension attempted → BLOCKED (sandbox
  data sparse: only ALLOC_GAS_VOL populated, no co-present STRM totals; logged in N2 design doc).
  Post-change re-test habit honoured (random suite nomination_point flaked then 4/4).
- 2026-06-14: **N3 RECON DONE → build is a GO** (user empowered me to self-plan). N3 = **HA.0001 Daily
  Data Status Processes** (P→V→A record-status engine). Found it's an **N2-analog** (same RUN
  scaffolding: From/To date + GO `button:form:B`, `dateStartJob:form`, `statusProcess:form`,
  `RunningJobs:form:T_data`) → reuse `allocation_run.resource` as the T2 template. DB: all
  PWEL_DAY_STATUS = 'P' (liftable); chosen positive process **`P3_VERIFY_FCTY`** (P→V); oracle =
  RECORD_STATUS P→V + `STAT_PROCESS_STATUS.ROWS_UPDATED`; self-clean via reverse process (`P1_RevUpd`).
  Full ready-to-execute plan → `ec-automation/docs/pattern_n3_status_process_design.md`. Recon:
  `tmp/scripts/n3_*.py`. ⚠️ One open risk: status processes may run via the BPM executor (could stall
  like N2 non-simulate) — first live run on HA.0001's RUN button resolves it.
- 2026-06-14: N3 run path CRACKED + fired live → ⛔ **BLOCKED by BPM/Process-Automation executor**
  (same infra blocker as N2 non-simulate). Run path proven: dates + process-in-G:2 dd + GO +
  `RunProcessButton:form:B`; result grid `statusProcess:form:T_data` (# Rows Updated). But "P1 Forward
  Status Update" @2003-01-01 went RunningJobs=**WAITING** and never executed — DB unchanged (all P,
  STAT_PROCESS_STATUS empty). Status processes have NO synchronous Simulate, so every run needs the
  executor. Clean (no data mutated). **Decision for user (see N3 design doc):** (a) enable Process
  Automation/BPM executor (also unblocks N2 non-simulate) → I finish N3 fully; (b) build partial
  N3 (submit + read-only oracle, completion-pending-PA); (c) park + move on. This is the recurring
  held "BPM/Process-Automation" item now on the critical path for N3.
- ▶ **RESUME POINT (2026-06-14, N3 recon done — BUILD NEXT):** Execute the N3 build per
  `docs/pattern_n3_status_process_design.md` §"Build steps": (1) live-crack `statusProcess:form` post-GO
  (process-select control + RUN button id + any Simulate + the completed-run/log grid id), on a tiny
  one-facility/day scope; (2) DbVerify `record_status_count` + `status_should_lift` + ROWS_UPDATED;
  (3) T2 `status_process_run.resource` (fork of `allocation_run.resource`); (4) T3
  `ha0001_daily_status_process_page.resource` (P3_VERIFY_FCTY + scope + reverse-process cleanup);
  (5) suite `daily_status_process_run.robot` (TC01 P→V + ROWS_UPDATED; TC02 reverse→P); dryrun→live
  (headed)→DB-verify→robocop→commit+push; (6) re-test habit + registry row + scorecard. Held for user:
  BPM/Process-Automation deep dive; Bitbucket cred rotation; Issue_1052 D/E/F; Chemistry-module licensing.
- 2026-06-14 (unattended autonomy window): (a) Traced the recurring scheduler "name is null" to its
  root — `BUSINESS_ACTION 'Daily Offshore Process'` has NULL `ACTION_CLASS_NAME` + `JBPM_DEPLOYMENT_ID
  ='dummy'` (a never-deployed jBPM process on an ENABLED schedule); config defect, not infra. Memory
  + N3 design doc + [[reference_ec_daily_offshore_process_broken]]. (b) Deep-dived EC BPM from the SDK
  working examples + EC source → `DeepDiveLearnings/ec-bpm/ec-bpm-deep-dive.md` (process→deploy(GAV)→
  template→instance; building blocks; ties to N1/N2/N3) + EC scheduler internals (EFK Phase-4
  schedule-job recipe). (c) **Diagnosed the deployment**: `run_EC_14_2_4.bat` was missing
  `12-docker-compose.ec-worker.yml` → ec-worker (background scheduler node) not up → status/BPM runs
  sit WAITING; fix = add overlay 12 (script now updated). (d) Coverage track: **3rd N1 screen recon'd
  + build-ready** — "Daily Water Injection Well Status" (IWEL_DAY_STATUS), same WR.0001 template,
  C4=ON_STREAM_HRS DB-proven, non-iframed, scope AS2_Water Injection Manifold 1 @2026-02-13; registry
  row added; build pending a null-original self-clean decision.
- 2026-06-14: ✅ **N1 #3 BUILT + live 3/3** — "Daily Water Injection Well Status" (IWEL_DAY_STATUS).
  edit→save→DB-verify(ON_STREAM_HRS=18)→DB-restore-null self-clean; chose DB-restore teardown (added
  `reset_day_status_value` to DbVerify; null cells make UI-clear unreliable — pops a save-confirm modal).
  Fixed a latent shared-helper bug: `day_status_value_should_be` failed None==None → added a null
  branch (WR.0001 canary re-verified 3/3, so safe). N1 now generalizes across 3 object types:
  PWEL (WR.0001) / STRM (PO.0002) / IWEL (this). Files: tests/Production/daily_water_injection_well_
  status_edit.robot + pageobjects/Production/iwel_water_injection_status_page.resource.
- ▶ **RESUME POINT (2026-06-14):** N3 status-process LIVE still blocked on **ec-worker not running**
  (run script fixed with overlay 12 — awaits redeploy; "name is null" is a separate broken-config red
  herring). No-blocker next items: (1) **Daily Equipment Status** N1 #4 — VIABILITY CONFIRMED
  (`tmp/scripts/n1_eqpm_viability.py` + `n1_eqpm_scope.py`): N1 grid (Date + 3-level nav, no
  well-hookup), `EQPM_DAY_STATUS` (ON_STREAM_HRS/AVG_RPM/AVG_PRESS/POWER_*), name source `OV_EQPM`,
  equipment e.g. "Offshore Gas Injection Compressor A" on 2024-02-06 (129 rows). Remaining: map nav
  scope names (OV_EQPM OP_FCTY_1/OP_AREA → the PU/Area/Facility cascade), confirm grid+cells, edit→diff
  the cell↔column, then fork the IWEL T3 (different object class = stronger N1 generalization). (2) other
  injection/stream siblings (CO2/steam/liquid), data-confirmed via `n1_daystatus_data_scan.py`. (3) When
  ec-worker is up: finish N3 live (P→V + ROWS_UPDATED + reverse) per `pattern_n3_status_process_design.md`.
  Held for user: redeploy with ec-worker (overlay 12); disable the broken "Daily Offshore Process" schedule.
- (next blocks append here…)

## Operating rules (always)
- Read-only EC sandbox unless a hands-on exercise is justified + low-risk; clean up any test data.
- No deletes outside `C:\Projects\ChoongYin_OS`; **no commits/pushes to remote without explicit
  user OK** (accumulate notes; fold into one docs commit when asked).
- Token-aware: synthesize, never transcribe; one section per block; checkpoint status in the
  track's own plan file.
- Confluence: search-first / fetch pages individually ([[feedback_atlassian_confluence_pattern]]).
- Every block leaves a written artifact (notes doc + memory pointer if durable).
- Pause a track at a clean checkpoint when budget runs low; never abandon mid-page.

## Active tracks (priority order; each has its own detailed plan file)
| # | Track | Plan file | Next item | State |
|---|---|---|---|---|
| 1 | **ECpedia EFK deep dive** (user-directed) | `ecpedia-efk/EFK-DEEP-DIVE-PLAN.md` | DONE for value (thin hub → RD130 for depth) | ✅ A+B done |
| 2 | **Pluto As-Built series** | `business-domains/PLUTO-ASBUILT-INDEX.md` | finish As-Built 14 monthly detail; lower-pri vols 01/02/03/07/11 [05,06,09,14 DONE] | 🔵 14+05 done |
| 3 | **Business-domain syntheses** (deepen) | `business-domains/PLAN.md` | fold EFK/As-Built findings into production/sales/revenue deep passes | 🔵 drafts done |
| 4 | **EC coverage track** (screen automation) | `ec-automation/docs/coverage_pluto_prioritized.md` | N1 done (WR.0001+PO.0002), N2 done (HA.0002); next = N3 status-process P→V→A | 🟢 N1+N2 live |
| 5 | **Industry grounding** | (feeds `business-domains/GLOSSARY.md`) | EFK "Learn more about the Oil & Gas Industry" + allocation/lifting/royalty concepts | ☐ |

## Pull-from-here when idle (self-pick logic)
1. (EFK done) If a user-directed track is open → continue it first.
2. Else pick the track with highest live-task payoff (As-Built 09 Validations = Issue_1052;
   As-Built 06 = allocation/ECIS).
3. Else advance the coverage track (build the next screen pattern).
4. Always prefer finishing a started section over opening a new one.

## Blocker log (rethink-resolve outcomes — append as they happen)
- 2026-06-13 EFK TAF pages = empty stubs → didn't churn; logged the architectural signal from
  titles, pivoted to A2. (Resolution: recognize low-yield source, extract meta-signal, move on.)
- 2026-06-13 EFK calc pages = thin slide-wrappers → cross-checked against DOC-12 (already deep),
  captured only the new concrete recipe, moved on.
- 2026-06-12 sandbox scheduler executor stalled (RUN NOW never fires) → diagnosed to app layer
  (Quartz healthy); flagged needs EC app restart; parked hands-on that depend on it.

## Parked (need user / external)
- ECIS re-test (needs EC app restart + user review).
- Pipeline screen (PIPELINE operational groupmodel question for user).
- Issue_1052 D/E/F (Grant discussion); ECPR-31011 (deploy OK).
- COPSDEV anything (Flyway only, never hand-config).
