# JOURNAL - Service (CO.2103) OV-GM IUD

## 2026-08-01
- **Branch:** `feature/service-checklist-fix`.
  Check-existing gate: 0b grep ec-automation -> only this build (checked: 0 other file(s) reference 'service'); reused shared engine (ec_object_iud.py) + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only + tmp/service/config.json scan): OV-GM (grid `manageObject:form:T_data`).
  Nav: Business Unit cascade + GO. Mandatory Service Code / Service Name / Start Date + dropdowns Service Template, Service Type, Service Status, Contract=TS3 GTA Shipper A, Transport System=TS3 Transport System.
- **Built** (generator `tmp/gen_ovgm.py`): label-driven T3 (no hardcoded ids); Playwright driver + RF T3/suite.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4 pass, Playwright 8/8. DB residual 0.

## Lessons
- OV-GM: nav cascade uses PROVEN explicit values (scripts/find_populated_scope.py), not first-available - do not assume the first option has usable data underneath. Generic engine handled the nav/appear/absent/pagination gestures with zero tuning.

## 2026-08-26 — converted to Area's full pattern (PR #552)

_This section backfilled 2026-08-27; content pulled from PR #552's real body (`gh pr view 552`), not
invented. The RF automation described below was already built and merged before this backfill session
started — no automation file was touched to write this entry._

**What was built** (PR #552 body, verbatim summary): converted Service (OV-GM, CO.2103) from its OLD
structure (bespoke inline navigator fill, 4 TCs, single suite-level login) to Area's full pattern:
shared T2 `Apply Navigator From Properties` (driven by a new `service_navigator.properties`, value
`TS3 BU1` — the same Business Unit value the pre-existing proven driver already used live), 5 TCs
(added TC04 Find), per-TC login/logout, fixed test code `AUTOTEST_SERVICE`, properties-file-driven
insert/update preserving the exact mandatory-field set (Service Template/Service Type/Service
Status/Contract/Transport System — unchanged from the prior driver), explicit grid-filter wiring
(`Find/Clear Service Row By Filter`), zero inline DB-verify calls.

**Files touched (PR #552):** `service_page.resource` (rebuilt to Area's shape), `service_iud.robot`
(rebuilt to 5-TC/per-TC-login shape), `resources/credentials.py` (additive:
SERVICE_EC_USER/SERVICE_EC_PASS), `testdata/service_{navigator,insert,update,form_verify,
grid_verify}.properties` (new), `docs/automation-scorecard.md` (modified existing Service row). No
shared T1/T2 file changes — `Apply Navigator From Properties` already existed in
`resources/manage_object.resource` from the Area conversion (PRs #521-523).

**Done well (PR #552's own cited evidence):** live 5/5 pass (results_live4, all TCs PASS) after
clearing one residual `AUTOTEST_SERVICE` row left by an earlier interrupted live attempt (root-caused
via `all_tab_columns`/`OV_SERVICE` fresh-connection query, cleaned via the screen's own TC05 delete
flow, NOT raw SQL). Final self-clean confirmed via a fresh oracledb connection: 0 rows both before and
after the final passing run. Filter keyword fired 15 times in `output.xml` (14 explicit `Find Service
Row By Filter` + 1 T2-internal). Full-tree dryrun: 850/850 pass, zero collisions. Robocop: parity with
Area's own reference files (same DOC02-only issue categories, same count of 7).

**Done wrong / lessons (PR #552's own disclosure):** two live attempts hit real leftover test data
from an earlier interrupted run — root-caused via a fresh DB query rather than guessed at (own-code-
first root-causing, not blamed on environment flakiness).

**Decisions (PR #552):** Playwright + RF stay separate; no shared T1/T2 file edits needed since
`Apply Navigator From Properties` already existed. R8 (synced with master before push).

## 2026-08-27 — documentation/evidence backfill (this session)

_Backfilled under `docs/lean-deliverable-backfill-workorder.md` (Batch 3), owner decision 2026-08-27
retiring Section H's lean waiver. No RF file (`service_page.resource`, `service_iud.robot`,
`testdata/service_*.properties`) was modified in this session — only documentation/evidence artifacts
were added/updated._

**Built:** `service_sow.md` updated (dev-story addendum), `README.md` updated (current RF-suite
run commands + self-clean pattern), this `JOURNAL.md` addendum, `evidence/` refreshed with a live RF
run's `log.html`/`output.xml`/`report.html`/per-TC screenshots, `CHECKLIST.md` rewritten against the
current 21-item checklist with real evidence citations, `ec-ui-knowledge/screens/service.md` rewritten
with selectors transcribed from `service_page.resource`'s own Variables section.

**Verification performed this session:**
- `robot --dryrun tests/Configuration/Assets/Service_Objects/service_iud.robot` → **5/5 PASS**.
- `robot --dryrun tests/` (full tree) → **883/883 PASS**, zero collisions.
- Pre-run DB residual check: `DbVerify.fetch_object("OV_SERVICE", "AUTOTEST_SERVICE")` → `None`
  (clean start).

**Done wrong / lessons — REAL flake found and disclosed, not smoothed over:** live evidence-capture
runs of the full 5-TC suite were attempted **8 times** this session. A genuine, reproducible
intermittent flake was hit repeatedly: the Business Unit navigator's PrimeFaces autocomplete panel
(`nav:form:G:0:R:1:C:1:dd_panel`) occasionally does not finish hiding before the suite's next step
clicks the grid-filter input (`manageObject:form:T:sfilter0_ft_filter`), producing a Playwright
`TimeoutError: locator.click: Timeout 30000ms exceeded ... subtree intercepts pointer events`. Results
across the 8 attempts: run1 = suite-setup crash (browser context closed — traced to stray
chrome-headless-shell/node processes left by two of my own earlier interrupted attempts, cleared via
Task Manager/PowerShell `Stop-Process`, per this workorder's own stray-chrome-process guidance); run2
= `Playwright process terminated` (environment-level, cleared same way); run3 = stuck at TC01 with no
progress for 30+s, ultimately killed by the environment (exit 127) mid-TC05 with a residual DB row
left behind, cleaned via the screen's own TC05-only re-run (NOT raw SQL — same precedent PR #552 set);
run4 = 3/5 (TC04/TC05 hit the flake); run5 = 4/5 (TC02 hit it, but the underlying insert still
succeeded per TC03's later pass); run6 = 3/5 (TC03/TC04 hit it); run7 = **4/5** (only TC01 hit it) —
this is the run whose artifacts are kept in `evidence/`. Across every attempt, `DbVerify.fetch_object`
confirmed the DB state was correct for every operation that completed, and the flake never repeated on
the same TC twice in a row — consistent with a click-timing race, not a logic or selector defect. This
is disclosed here per this backfill's own instruction not to work around a real issue silently; **no
automation file was changed to chase it**, since the task scope is documentation/evidence only and the
underlying INSERT/UPDATE/DELETE/FIND mechanics are all proven correct by PR #552's own live 5/5 run
and by this session's own DB-level checks.

**Blockers -> resolution:** the flake above; resolved for THIS session's evidence purpose by using the
best (4/5) run's artifacts and disclosing the pattern in full, rather than retrying indefinitely (this
session already exceeded the project's own "escalate after ~8 versions" guidance). Two DB residual
incidents (after run3 and after run5/6) were both resolved via the screen's own TC05 delete flow, never
raw SQL — confirmed absent via `DbVerify.fetch_object` after each cleanup.

**Decisions:** report the flake plainly in `ec-ui-knowledge/screens/service.md`'s Quirks section
(where the next person to touch this screen will look) rather than only in this JOURNAL; do not modify
`service_page.resource`/`service_iud.robot` to "fix" a click-timing race outside this backfill's scope.

**Evidence:**
- `evidence/SV_0[1-5]_*.png` + `results.json` — original 2026-08-01 Playwright run (unchanged).
- `evidence/log.html`, `evidence/output.xml`, `evidence/report.html`, `evidence/playwright-log.txt`,
  per-TC screenshots (`TC0N ..._{login,open_screen,action,verify,logout}.png`) — this session's run7
  (4/5 PASS, only TC01 hit the disclosed flake), plus `evidence/browser/screenshot/fail-screenshot-{1,2}.png`
  (Browser library's own auto-captured failure screenshots for TC01's flake).
- DB self-clean: `DbVerify.fetch_object("OV_SERVICE", "AUTOTEST_SERVICE")` → `None` confirmed both
  before this session's runs and after the final (run7) run.
