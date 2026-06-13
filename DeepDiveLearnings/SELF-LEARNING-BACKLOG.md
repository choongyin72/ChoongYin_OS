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
| 4 | **EC coverage track** (screen automation) | `ec-automation/docs/ec_screen_registry.md` | next treeview section after Dispatching; dependency-screen setup-chains | 🟢 slices 1-2 done |
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
