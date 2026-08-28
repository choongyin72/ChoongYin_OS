# JOURNAL — Transport Zone IUD

_Screen: Configuration > Assets > Dispatching Objects > Transport Zone (OV-GM,
Business-Unit-gated). View `OV_TRANSPORT_ZONE`. This JOURNAL was backfilled 2026-08-28 under the
retired-lean-waiver work order (`docs/lean-deliverable-backfill-workorder.md`, Batch 5; Section H
of `docs/IUD-DELIVERABLE-CHECKLIST.md`) — this screen never had a `screens/` bundle at all before
this backfill. PR #557 (the Area-pattern conversion) is the source of the "Built" and "Done well"
content below, pulled from its real PR body and `docs/ec_screen_registry.md`'s row, not invented._

## Built

### Original build (pre-existing, older pattern)
- RF page object + suite (4-TC/suite-level-login/generated-code/inline-DB-verify pattern) —
  `transport_zone_page.resource` + `transport_zone_iud.robot`. No `screens/` documentation bundle
  was ever created for this build.

### Area-pattern conversion (PR #557, merged 2026-08-26)
- Live recon (read-only, no Save/Insert/Delete) confirmed the navigator group `nav:form:G:0` has
  THREE columns: C:0 Date (mandatory:true but already defaulted/filled on load, no fill needed),
  C:1 Business Unit dropdown (mandatory:true, genuinely empty/`MandatoryCellStyle` — the ONLY
  field needing a fill), C:2 a second dropdown (mandatory:false, optional filter — GO succeeds
  with C:2 left empty once C:1 is set). This is exactly the single-dropdown/same-row-cascade shape
  Area's pattern supports — FITS, no shared-file change needed (defaults row=1/group G:0/
  start_col=C:1 already match).
- Converted the RF IUD suite from the OLD bespoke shape to the full Area-pattern structure: 5 TCs
  (incl. TC04 Find), per-TC Login/Logout, fixed test code `AUTOTEST_TRANSPORT_ZONE`,
  properties-file-driven insert/update/verify, the genuine Business Unit navigator delegated to
  the shared T2 `Apply Navigator From Properties` keyword, explicit `Find/Clear Transport Zone Row
  By Filter` grid-filter wiring, zero inline DB-verify calls (pure-screen verification).
- New test-data files: `testdata/transport_zone_{navigator,insert,update,form_verify,
  grid_verify}.properties`.
- Dedicated credentials pair `TRANSPORT_ZONE_EC_USER`/`TRANSPORT_ZONE_EC_PASS` added to
  `resources/credentials.py` (additive only).
- Registry (`docs/ec_screen_registry.md`) and scorecard (`docs/automation-scorecard.md`) rows
  MODIFIED in place; new R38 sections added to `docs/bank-pattern-conversion-checklist.md` and
  `docs/grid-filter-standardization-checklist.md`.
- No shared T1/T2 file changes — `resources/manage_object.resource` untouched, the existing
  `Apply Navigator From Properties` defaults already fit this screen's shape.

### This backfill (2026-08-28)
- Added the entire `screens/Configuration/Assets/Dispatching_Objects/Transport_Zone/` bundle from
  scratch (it never existed before): `transport_zone_sow.md`, this `JOURNAL.md`, `README.md`,
  `CHECKLIST.md`, the KB selector map `ec-ui-knowledge/screens/transport_zone.md`, and
  `evidence/backfill_2026-08-28/` (fresh dryrun + live re-run captured as evidence of the
  already-proven suite — no automation code touched).

## Done well
- Full I-U-D DB-verified vs `OV_TRANSPORT_ZONE` (insert Transport Zone Code/Name, update Transport
  Zone Name, delete End=Start absent); self-clean 0 residual, confirmed via a FRESH oracledb
  connection both before and after PR #557's live run (per its own body), and re-confirmed via a
  fresh connection again after this backfill's own passing live re-run.
- Screen-prefixed labels confirmed live, not assumed: PR #557's page object documents that
  `objectForm`/`updateAttributes` use "Transport Zone Code"/"Transport Zone Name"
  (SCREEN-PREFIXED, like Area's own "Area Code"/"Area Name"), NOT the generic "Code"/"Name" that
  Bank/Object List use.
- Full-tree dryrun stayed 100% pass (875/875) at conversion time (per PR #557 body); this
  backfill's own fresh dryrun re-confirmed the Transport Zone suite alone: 5/5 PASS.
- Robocop parity check performed and passed: 7 issues (VAR02 + DOC02 kinds) on the 2 changed
  files, identical count to Area's own established baseline — confirmed independently again during
  this backfill by running robocop directly against `area_page.resource`/`area_iud.robot` (also 7
  issues).
- Filter keyword fired 15 times (`grep -c "Find Object Row By Filter" output.xml`), matching PR
  #557's cited count exactly, on this backfill's own passing retry run.

## Done wrong / lessons
- No regressions or wrong turns disclosed in PR #557's own body for the conversion itself — the
  navigator mandatory/optional classification was confirmed live via DOM class inspection
  (`MandatoryCellStyle` vs `mandatory:false`), not assumed from the pre-existing registry note.
- **Backfill-specific: one real live-run timeout, disclosed not hidden.** The FIRST evidence-capture
  attempt of `EC_HEADLESS=true robot ...` produced `4 tests, 4 passed, 1 failed` — TC01 "Verify
  Clean State" failed with `TimeoutError: locator.waitFor: Timeout 60000ms exceeded` waiting for
  `[id="menu:searchForm:searchTxt"]` to become visible (a page-load/menu-render timing issue on
  first login of the run, not a Transport Zone screen defect — TC02-TC05 all passed cleanly in the
  same run once the browser session was past that point). Per this task's process rule (retry ONCE,
  do not kill any chrome/node process by name in this shared environment), an immediate retry of
  the identical, unmodified command was run. It passed clean: 5/5 PASS. Reported here as a real
  flake candidate that self-resolved on retry, not silently smoothed over.

## Blockers -> resolution
- **Live-run timeout on TC01** (this backfill, 2026-08-28) — resolved by an immediate single retry
  (no process kill), per the task's process rule; the retry passed 5/5 with no code change. The
  failing first attempt's artifacts are preserved at
  `evidence/backfill_2026-08-28/live_attempt1_fail/` for disclosure.
- No other blockers during this backfill.

## Decisions
- Playwright bundle stays waived permanently for Area-pattern work (owner decision 2026-08-27,
  `docs/IUD-DELIVERABLE-CHECKLIST.md` Section H) — no Playwright bundle is built for this screen;
  the Universal Screen Engine is the owner-decided replacement going forward.
- The RF suite is the maintained/live test for this screen.
- Code lives in `ec-automation`; `ec-ui-knowledge/` stays MD-only.

## Evidence
- PR #557 conversion (2026-08-26): live run `5 tests, 5 passed, 0 failed` (TC01-TC05), 15 `Find
  Object Row By Filter` hits in output.xml, robocop 10 issues total (7 on the 2 changed screen
  files = parity with Area, +3 pre-existing unrelated `credentials.py` findings), full-tree dryrun
  875/875 — all cited in the PR body.
- This backfill (2026-08-28): `evidence/backfill_2026-08-28/` — `dryrun/` (5/5 PASS,
  `log.html`/`report.html`/`output.xml`), `live_attempt1_fail/` (the disclosed first attempt,
  4/5 pass — TC01 timeout, `log.html`/`report.html`/`output.xml` preserved), and `live/` (the
  PASSING RETRY, 5/5 PASS headless, `log.html`/`report.html`/`output.xml`), plus a DB self-clean
  result (`OV_TRANSPORT_ZONE`: 0 rows for `AUTOTEST_TRANSPORT_ZONE`, 0 residual `AUTOTEST%`, fresh
  connection, run after the passing retry), a re-confirmed 15-hit filter-fired grep, a
  re-confirmed 7-issue robocop parity check against Area's own baseline, and
  `py scripts/check_bundle_hygiene.py` → `RESULT: PASS`.
