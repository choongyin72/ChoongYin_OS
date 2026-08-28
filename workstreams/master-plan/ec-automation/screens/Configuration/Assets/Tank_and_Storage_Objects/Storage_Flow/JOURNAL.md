# JOURNAL - Storage Flow (CO.2091) OV IUD

## 2026-07-26 - initial build
- **Branch:** `feature/storage_flow-iud` (own branch, stacked so the shared-engine helpers are present).
  Check-existing gate: only this build; reused shared engine + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only): DB `CLASS_TYPE=OBJECT` ⇒ OV; treeview
  Configuration > Assets > Tank_and_Storage_Objects > Storage Flow. Mandatory Code/Name/Start Date;
  optional dropdowns skipped. Plain Bank-layout OV (single Date+GO nav, no mandatory dropdowns
  identified at that time).
- **Label-driven** T3 (no hardcoded ids). Playwright driver -> 7/7; RF T3+suite -> live 4/4.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4, Playwright 7/7.
- Used a **unique-timestamped** test code (`AUTOTEST_SF_<timestamp>`) and a single suite-level
  login (no per-TC Login/Logout), no explicit grid-filter wiring.

## 2026-08-23 - Batch 10 Bank-pattern conversion (PR #472)

**Built** — brought Storage Flow up to the full Bank-pattern shape via `ec-bank-pattern-converter`,
matching `bank_page.resource`/`berth_page.resource`: properties-file-driven insert/update, form/grid
verify, and explicit grid-filter wiring, replacing the screen's older unique-timestamped-code/
single-login/no-filter approach.

**Files touched (real, from PR #472's body):**
- `pageobjects/.../storage_flow_page.resource` (rebuilt)
- `tests/.../storage_flow_iud.robot` (rebuilt: 5-TC, fixed code, per-TC Login/Logout)
- `resources/credentials.py` (additive: `STORAGE_FLOW_EC_USER`/`STORAGE_FLOW_EC_PASS`)
- `testdata/storage_flow_insert.properties`, `_update.properties`, `_form_verify.properties`,
  `_grid_verify.properties` (all new)
- `docs/ec_screen_registry.md` — MODIFIED existing row (was the 2026-07-26 generator-scaffolded text)
- `docs/automation-scorecard.md` — MODIFIED existing row
- `docs/bank-pattern-conversion-checklist.md` / `docs/grid-filter-standardization-checklist.md` —
  appended rows under the pre-merged Batch 10 header
- `py/storage_flow_iud.py` (Playwright driver) — **read but NOT modified**; used as the source of
  truth for the mandatory `Flow Direction`/`Storage` dropdowns

**Done well:**
- Kept the existing proven mandatory dropdowns (`Flow Direction`/`Storage` = `__FIRST__`) from the
  already-proven page object + Playwright driver, rather than re-deriving from a static CSS
  mandatory-field scan (Batch-9 Process Train lesson: a static scan can miss a de-facto-mandatory
  field that only shows up as a failed Save).
- No shared T1/T2 (`manage_object.resource`/`common.resource`) changes — reused as-is per the
  Batch 10 critical rule.
- Isolated sparse-checkout clone under `Workplaces/storage_flow/` (gitignored), own feature branch;
  explicit-path staging only (no `git add -A`); synced with `origin/master` before push.

**Done wrong / lessons carried into this backfill:**
- The pre-conversion (2026-07-26) SOW/README/JOURNAL/CHECKLIST/KB were left describing the OLD
  build (unique-timestamped code, single login, no filter, "plain, no mandatory dropdowns") and
  were never refreshed when PR #472 landed — the classic doc-drift gap this backfill project
  exists to close. This 2026-08-28 backfill rewrites SOW/README/JOURNAL/CHECKLIST/KB to match the
  real current state.

**Evidence cited in PR #472's body:**
- Live headless run: 5/5 pass
- Full `tests/` dryrun: 767/767 pass
- robocop: 12 issues (4 VAR02 + 5 DOC02 + 3 credentials.py baseline noise) — identical in kind/count
  to the merged Berth baseline, no new categories
- Grid-filter keyword fired 15x (output.xml grep)
- DB self-clean: 0 residual `AUTOTEST%` rows in `OV_STORAGE_FLOW`, fresh `oracledb` connection
  before and after

## 2026-08-28 - documentation/evidence backfill (Batch 11, this task)

**Built** — SOW/README/JOURNAL/CHECKLIST.md rewritten to describe the real Batch 10 state (sourced
from `gh pr view 472`'s body, the current `storage_flow_page.resource`/`storage_flow_iud.robot`,
and the 4 `testdata/storage_flow_*.properties` files); KB map `ec-ui-knowledge/screens/storage_flow.md`
refreshed with the current selectors/mandatory fields; new evidence captured.

**Done well:**
- Re-ran the existing, already-proven suite exactly as-is (no automation edits) to capture fresh
  evidence: dryrun 5/5, live 5/5 on retry, DB self-clean re-confirmed via an independent fresh
  connection.

**Done wrong / lessons (disclosed honestly, per the process rule):**
- The FIRST live attempt this session got **4/5** — `TC01 Verify Clean State` failed on
  `TimeoutError: locator.waitFor: Timeout 60000ms exceeded` waiting for the menu search box
  (`[id="menu:searchForm:searchTxt"]`) to become visible. TC02-05 (the actual insert/update/find/
  delete cycle) all passed on that same attempt. This reads as a one-off slow-page-load flake on
  the very first login of the run, not a defect in the suite or a regression from PR #472 — a
  retry (one retry only, per the mandated process rule) came back clean 5/5. Not chased further
  (no grinding, no process-kill) since it was non-reproducible on retry and the underlying
  mechanism (login -> nav -> IUD -> DB-verify -> self-clean) is otherwise proven correct.

**Blockers -> resolution:**
- None beyond the one flaky TC01 attempt above, resolved by the single permitted retry.

**Decisions:**
- Kept `investigation/recon.py` and the 2026-07-26 `evidence/*.png`/`rf_report.html` as historical
  artifacts rather than deleting them — they document the pre-conversion build faithfully; new
  evidence from this backfill lives alongside them in `evidence/2026-08-28_backfill/`.
- Did not touch `VERIFY-REPORT.md` (still reflects the 2026-07-26 pre-conversion `verify_screen.py`
  run) — regenerating it would require re-running `verify_screen.py` with `--driver`, which targets
  the now-superseded Playwright-driver-centric flow; the CHECKLIST.md and this JOURNAL now carry
  the real Batch 10 + backfill evidence instead.

**Evidence:** `evidence/2026-08-28_backfill/` (dryrun_output.xml, output.xml, log.html, report.html
from the successful retry run).
