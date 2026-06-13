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
- ▶ **RESUME POINT (2026-06-13 ~22:40, window checkpoint):** Next action = **N2 allocation**: on
  HA.0002 "Daily Allocation", iterate with **Simulate ON** (no DB write) to find an allocation that
  exits **Success** — try the **"Testing allocation RUN_NO" → RUN_NO_TEST** network/job first, or a
  P1 network+date with complete input (EC_DAILY_VOLUME on P1 Dashboard/2021-10-01 exits **Failure**
  with equation errors). On a Success run, build the **conservation-oracle** verification
  (no-neg ✓ already on existing 2021-10-01 data; add sum-to-total + day→month roll-up) on
  PWEL_DAY_ALLOC / STRM_DAY_*_ALLOC. Run-mechanism is cracked (RUN CALCULATIONS = `ProdAllocButton:form:B`).
  Standing idle track = EFK deep-dive series (DeepDiveLearnings/ecpedia-efk/EFK-DEEP-DIVE-SERIES.md,
  Phase-1 domain modules next). Held for user: BPM/Process-Automation deep dive; Bitbucket cred
  rotation; Issue_1052 D/E/F. Everything committed+pushed (master=origin @ 2196704).
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
| 4 | **EC coverage track** (screen automation) | `ec-automation/docs/coverage_pluto_prioritized.md` | build N1 daily-status-grid T2 on WR.0001 (Pluto-prioritized) | 🟢 slices 1-2 done |
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
