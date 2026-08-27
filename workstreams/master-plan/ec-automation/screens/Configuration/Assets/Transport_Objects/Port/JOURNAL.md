# JOURNAL — Port (CO.2003) OV IUD

_Screen: Configuration > Assets > Transport Objects > Port (OV, date-effective). View `OV_PORT`._
_This JOURNAL covers TWO builds: the original 2026-07-26 build (superseded) and the Batch-9
Bank-pattern conversion (PR #465, 2026-08-23, current live shape). The Built/Lessons sections below
retain the original 2026-07-26 entries verbatim; the sections after that were added 2026-08-28 per
`docs/lean-deliverable-backfill-workorder.md` Batch 10 — real content pulled from PR #465's actual
body, not invented._

## Built

### 2026-07-26 (original build, superseded — kept verbatim)
- **Branch:** `feature/port-iud` off master. Check-existing gate: NONE covered (uncovered target from
  `docs/ov-reuse-targets.md`); reused shared engine + DbVerify + T2, no parallel copy.
- **Recon** (`investigation/recon.py`, read-only): DB `CLASS_TYPE=OBJECT` => OV; treeview
  Configuration > Assets > Transport Objects > Port. Form: Port Code / Port Name / Start Date mandatory;
  Country/Canal/Time Zone/Carrier dropdowns all **optional** => no dropdown-fill needed. Grid has real
  ports (never touched).
- **Label-driven from the start** — no hardcoded `R:n:C:n` ids in the T3; fields resolved by label via
  T2. Nice side-effect: no separate update-tab id recon needed (labels stable across the three form
  tabs).
- **Bug found by the driver (not hidden):** first headless run FAILED insert grid-check — row
  persisted to `OV_PORT` (DB confirmed True) but absent from the rendered grid at check-instant. Root
  cause = **async redraw on a paginated grid** (Port = 2 pages). Probe confirmed the row lands on
  page 1 alpha-sorted once redraw completes.
- **Generic fix in the shared engine** (per owner: "build generic py code to cater most cases"):
  `row_exists` walks all paginator pages + resets to page 1; `wait_for_row` polls the current page
  then does a full paginated sweep; `select_row` navigates to the page holding the code before
  clicking. Backed up to `.keyword_backups/ec_object_iud.py.pre-pagination.bak`. **Bank canary re-run
  7/7** (backward-compatible). Port driver -> **7/7 ALL PASS + self-clean**.
- **RF** T3 + suite (label-driven). `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0,
  dryrun 4/4, **LIVE RF 4/4**, **Playwright 7/7**.

### 2026-08-23 (Batch 9, PR #465 — current live shape, pulled from the merged PR's real body)
- Upgraded Port from the older arg-based/no-filter page object to the full Bank-pattern shape:
  label-driven, properties-file-driven Insert/Update/Verify, and explicit grid-filter wiring
  (`Find Port Row By Filter`/`Clear Port Row Filter` -> shared T2), matching
  `bank_page.resource`/`berth_page.resource` exactly.
- Files: `port_page.resource` (rebuilt), `port_iud.robot` (rebuilt: 5 TCs, per-TC login/logout,
  fixed test code), new `testdata/port_{insert,update,form_verify,grid_verify}.properties`,
  additive `PORT_EC_USER`/`PORT_EC_PASS` in `resources/credentials.py`.
- Port's grid is paginated (2 pages) — confirmed the shared engine's existing pager-walking behavior
  in the T2 filter/row-locate keywords still worked correctly for the new grid-filter wiring; no
  engine change needed this time.
- Live RF run (`EC_HEADLESS=true`): **5/5 pass** (TC01 Verify Clean State, TC02 Insert, TC03 Update,
  TC04 Find, TC05 Delete). Full-tree `tests/` dryrun: 762/762 pass. robocop: 9 issues (4 VAR02 + 5
  DOC02-style), same count/kind as the established baseline (`berth_iud.robot` also shows 9 issues
  of the same kind) — not a regression.
- DB self-clean: fresh `oracledb` connection, `SELECT COUNT(*) FROM OV_PORT WHERE CODE LIKE
  'AUTOTEST%'` = 0, both before and after the live run. Filter keyword `Find Port Row By Filter`
  confirmed 15x via `output.xml` grep.
- Playwright driver `py/port_iud.py` left **unchanged** (out of scope for this conversion).

### 2026-08-28 (this backfill — documentation/evidence only, no automation touched)
- Discovered the pre-existing `screens/.../Port/` bundle (SOW/README/CHECKLIST/VERIFY-REPORT/
  evidence) documented only the 2026-07-26 build and had NOT been refreshed when PR #465 landed —
  it still described 4 TCs, no properties files, no grid-filter wiring, even though the live RF
  files had already moved on. Refreshed SOW/README/CHECKLIST/JOURNAL/KB map to reflect PR #465's
  real, current shape; left the original evidence/VERIFY-REPORT as an explicitly-labeled historical
  record rather than deleting it.
- Re-ran the live suite once for fresh evidence (see Evidence below) — 5/5 pass, no retry needed,
  no regression vs #465's own citation.

## Done well
- Port's grid is **paginated (2 pages)** — PR #465 confirmed the shared engine's existing
  pager-walking behavior in the T2 filter/row-locate keywords still worked correctly for the new
  grid-filter wiring, with **no engine change needed**.
- Full I-U-D DB-verified vs `OV_PORT` (insert Port Name, update Port Name, delete End=Start absent);
  self-clean 0 residual, confirmed via a fresh `oracledb` connection both before and after the live
  run (both at #465's merge and again by this backfill's own re-run).
- Live RF 5/5 (PR #465, 2026-08-23) and re-confirmed live RF 5/5 by this backfill's own re-run
  (2026-08-28) — no regression between the two runs, same `Find Port Row By Filter` hit count (15),
  same robocop issue count (9).
- Label-driven T3s are both no-hardcode AND simpler to build (skip update-tab id recon) — carried
  forward from the original build into the Batch-9 conversion.

## Done wrong / lessons
- The **original 2026-07-26 build's first headless run FAILED** the insert grid-check: the row had
  persisted to `OV_PORT` (DB confirmed True) but was absent from the rendered grid at check-instant.
  Root cause: **async redraw on a paginated grid** (Port = 2 pages). Fixed generically in the shared
  engine (per owner: "build generic py code to cater most cases") rather than as a Port-specific
  patch — `row_exists` now walks all paginator pages + resets to page 1, `wait_for_row` polls then
  sweeps all pages, `select_row` navigates to the page holding the code. Bank canary re-run 7/7
  confirmed backward-compatible.
- **This backfill task itself is a lesson in bundle staleness:** the pre-existing doc bundle
  documented the 2026-07-26 build only — PR #465 (2026-08-23) upgraded the live RF files but never
  touched the doc bundle, leaving it silently out of date. This is exactly the gap Section H of
  `docs/IUD-DELIVERABLE-CHECKLIST.md` and the backfill work order exist to close.

## Blockers -> resolution
- No hard blockers in either the original build (paginated-grid bug self-resolved generically, see
  above) or this backfill (live RF suite ran 5/5 pass on the first attempt, no retry needed, per the
  process rule to retry once on failure before disclosing).

## Decisions
- Paginated OV grids need all-page membership + page navigation on select — handled once,
  generically, for every OV screen (unchanged decision from the original build).
- Playwright driver (`py/port_iud.py`) stays unchanged/unrebuilt — per owner decision 2026-08-27
  (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H), the Playwright bundle stays permanently waived for
  Bank-/Area-pattern conversions; the Universal Screen Engine is the replacement going forward.
- Both the 2026-07-26 evidence (Playwright 7/7, RF 4/4) and this backfill's fresh 2026-08-28
  evidence (RF 5/5, current Batch-9 shape) are kept side-by-side in `evidence/` — the old evidence is
  a historical record of the pre-conversion state, not deleted or overwritten.
- `VERIFY-REPORT.md` is left as the ORIGINAL 2026-07-26 auto-generated report (predates the Batch-9
  conversion) rather than re-run, since this backfill's scope is documentation/evidence, not
  re-verification via that specific tool; the fresh gate evidence (robocop 9 / dryrun 5-5 / live 5-5
  / hygiene PASS / DB self-clean 0) is recorded directly in README.md/CHECKLIST.md instead, each
  citing the actual command run.

## Evidence
- Playwright (2026-07-26, historical): `evidence/port_0[1-5]_*.png` + `rf_report.html`, 7/7 ALL PASS.
- RF (2026-08-23, PR #465, cited from the merged PR body): live 5/5 pass, `output.xml` grep 15x
  `Find Port Row By Filter`, DB self-clean 0 residual, full-tree dryrun 762/762 pass, robocop 9
  issues (baseline parity with Berth).
- RF (2026-08-28, this backfill's fresh re-run): `evidence/TC0[1-5] *.png` + `log.html`/`output.xml`/
  `report.html`, live 5/5 pass, `output.xml` grep 15x `Find Port Row By Filter` (same count as
  #465), robocop 9 issues (same count/kind, re-confirmed), hygiene PASS, DB self-clean via fresh
  connection = 0 residual `AUTOTEST%` rows in `OV_PORT`.
