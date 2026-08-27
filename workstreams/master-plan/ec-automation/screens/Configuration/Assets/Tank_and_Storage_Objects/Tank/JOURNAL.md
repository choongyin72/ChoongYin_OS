# JOURNAL — Tank IUD

_Screen: Configuration > Assets > Tank and Storage Objects > Tank (OV-GM groupmodel manage-object,
navigator-gated). View `OV_TANK`. This JOURNAL was backfilled 2026-08-27 under the retired-lean-
waiver work order (`docs/lean-deliverable-backfill-workorder.md`, Batch 3; Section H of
`docs/IUD-DELIVERABLE-CHECKLIST.md`) — Tank was a brand-new build (PR #553, 2026-08-26) that never
had ANY prior automation or bundle, so this JOURNAL is built from PR #553's real body, not
invented, and this backfill is the FIRST bundle this screen has ever had, not a refresh of an
existing one._

## Built

### Original build (PR #553, merged 2026-08-26)
- Brand-new Robot Framework IUD suite for Tank (`OV_TANK`) — no prior automation existed for plain
  Tank before this PR (confirmed via a fresh repo grep; Chemical_Tank/Chemical_Transport_Tank/
  Storage/Storage_Flow/`daily_tank_status_vcf` are unrelated siblings).
- Built via the `ec-area-pattern-new-screen` skill after a live DOM scan confirmed the navigator is
  Area-pattern-shaped: single row, increasing-column cascade (`nav:form:G:0:R:1:C:0..3`) where C:0
  is a Date field with a working default (left untouched) and C:1/C:2/C:3 are a genuine Production
  Unit -> Area -> Facility Class 1 cascade — the SAME shape and SAME "P1 Production Unit"/"P1
  Area"/"P1 Facility 1" values already proven on Well's navigator.
- 5-TC/per-TC-login/pure-screen-verify structure, properties-file-driven, T2-consolidated,
  mirroring `area_page.resource`/`area_iud.robot` exactly.
- Files: `pageobjects/.../tank_page.resource` (T3), `tests/.../tank_iud.robot` (5 TCs),
  `testdata/tank_{insert,update,form_verify,grid_verify,navigator}.properties` (5 files),
  additive-only `TANK_EC_USER`/`TANK_EC_PASS` in `resources/credentials.py`,
  `investigation/{recon.py,dbcheck_selfclean.py}` (consolidated live-recon evidence), new registry
  row and scorecard row (append-only).

### This backfill (2026-08-27)
- Added `tank_sow.md`, this `JOURNAL.md`, `CHECKLIST.md`, the KB selector map
  `ec-ui-knowledge/screens/tank.md`, and `evidence/backfill_2026-08-27/` (fresh dryrun + live
  re-run captured as evidence of the already-proven suite — no automation code touched).
  Since Tank never had a `screens/` bundle before, this is the bundle's FIRST creation, not a
  refresh — the `investigation/` folder already existed from PR #553 and was left untouched.

## Done well
- Full I-U-D DB-verified vs `OV_TANK` (insert Tank Code/Name, update Tank Name, delete End=Start
  absent); self-clean 0 residual, confirmed via a FRESH oracledb connection (PR #553 body: pre-run
  check found the fixed test code free, independent post-run self-clean check found 0 residual
  `AUTOTEST%` rows).
- Screen-prefixed labels confirmed live, not assumed: `tank_page.resource` documents that
  `objectForm`/`updateAttributes` use "Tank Code"/"Tank Name" (SCREEN-PREFIXED, like Area's own
  "Area Code"/"Area Name"), NOT the generic "Code"/"Name" that Bank/Object List use.
- Full recon before any locator was written: navigator shape, mandatory fields (yellow-background
  scan on the pristine New-Object row), the Op Production Unit/Op Area/Op Facility Class 1
  scope-matching requirement (confirmed via a self-cleaning probe insert/update/delete,
  `AUTOTEST_TANK_RECON`, never the real fixed test code), the objectdates Delete field id, the grid
  column headers, and the real treeview path (live expand of Configuration > Assets > "Tank and
  Storage Objects") — all done live, not extrapolated from a sibling screen.
- Full-tree dryrun 854/854 PASS (per PR #553 body); this backfill's own fresh dryrun re-confirmed
  the Tank suite alone: 5/5 PASS.
- Robocop parity check performed and passed: 7 issues (2x VAR02 + 5x DOC02) on the 2 built files,
  identical count/kind to Area's own established baseline — confirmed independently again during
  this backfill.

## Done wrong / lessons
- No regressions or wrong turns disclosed in PR #553's body for the original build.
- **Backfill-specific real flake, disclosed here, not smoothed over:** the first FOUR live-run
  attempts during this backfill session failed with a mix of `Error: Could not find active page`,
  `ConnectionError: Playwright process has been terminated with code 1`, and
  `WSAGetOverlappedResult: Connection reset` errors — all transport/process-level, at different
  points in the run each time (once mid-navigator-cascade, once at suite setup). `tasklist`
  confirmed an accumulating pile of stray `chrome-headless-shell.exe`/`node.exe`/`robot.exe`
  processes left behind by each failed attempt (the exact cause flagged in this task's own
  instructions from earlier in the session). One of those partial attempts got far enough to
  insert `AUTOTEST_TANK` into `OV_TANK` before dying (TC02 completed, TC05 never reached), leaving
  a residual row — confirmed via `investigation/dbcheck_selfclean.py` (1 row, `AUTOTEST_TANK` /
  `Automation Test Tank`). Fix: ran TC05 alone to clean it up (confirmed 0 residual afterward), did
  a full `taskkill` sweep of the stray processes, then re-ran the full suite once more — 5/5 PASS,
  clean, first try after the sweep. This was an environment/process-hygiene issue in this session,
  not a Tank suite defect: the dryrun stayed 5/5 throughout, an isolated TC01+TC02-only run passed
  cleanly mid-investigation, and the final full run passed cleanly once the stray processes were
  cleared.
- No automation code was touched to work around this — the suite itself was never modified; only
  the environment (stray processes) and the residual test data were cleaned up.

## Blockers -> resolution
- Stray-process resource exhaustion (see above) -> resolved via `taskkill` on
  `chrome-headless-shell.exe`/`node.exe`/`robot.exe`, confirmed clear via `tasklist`, then a clean
  re-run.
- Residual `AUTOTEST_TANK` row from a partial crashed attempt -> resolved by running TC05 alone
  (the suite's own Delete Object Via End Date keyword), confirmed 0 residual via a fresh
  `oracledb` connection.
- No other hard blockers during the original build or this backfill; no data damage — the residual
  row was this backfill's own test artifact, never a pre-existing production row.

## Decisions
- Playwright bundle stays permanently waived for this screen (owner decision 2026-08-27,
  `docs/IUD-DELIVERABLE-CHECKLIST.md` Section H) — Tank never had one; none is built now. The
  Universal Screen Engine is the owner-decided replacement for hand-written Playwright drivers
  going forward.
- The RF suite is the ONLY and maintained test for this screen (there was never a Playwright
  alternative to compare against, unlike converted screens with a historical reference driver).
- Code lives in `ec-automation`; `ec-ui-knowledge/` stays MD-only.

## Evidence
- Original build (PR #553, 2026-08-26): live run `5 tests, 5 passed, 0 failed` (TC01-TC05), fresh
  `oracledb` post-run check 0 residual `AUTOTEST%` rows, `grep -c "Find Object Row By Filter"` = 15,
  full-tree dryrun 854/854, robocop 7 issues (parity with Area) — all cited in the PR body.
- This backfill (2026-08-27): `evidence/backfill_2026-08-27/` — `dryrun/` (5/5 PASS,
  `log.html`/`report.html`/`output.xml`) and `live/` (5/5 PASS headless,
  `log.html`/`report.html`/`output.xml`, reached after clearing the stray-process flake described
  above), plus `summary.json` documenting the full flake timeline, the DB self-clean result
  (`OV_TANK`: 0 rows for `AUTOTEST_TANK`, 0 residual `AUTOTEST%`, fresh connection, both before and
  after the final run), a re-confirmed 15-hit filter-fired grep, a re-confirmed 7-issue robocop
  parity check against Area's own baseline, and `py scripts/check_bundle_hygiene.py` -> `RESULT:
  PASS`.
