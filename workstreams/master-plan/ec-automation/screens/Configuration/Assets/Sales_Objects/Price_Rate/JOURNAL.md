# JOURNAL - Price Rate (CO.3024) OV-GM IUD

_Screen: Configuration > Assets > Sales_Objects > Price Rate (OV-GM groupmodel, Business-Unit-gated
via a single dropdown). View `OV_PRICE_RATE`. This JOURNAL was backfilled 2026-08-27 under the
retired-lean-waiver work order (`docs/lean-deliverable-backfill-workorder.md`, Batch 3; Section H
of `docs/IUD-DELIVERABLE-CHECKLIST.md`) - the bundle's SOW/README/evidence/investigation predated
the JOURNAL rule; PR #534 (the Area-pattern conversion) is the source of the "Built" and "Done
well" content below, pulled from its real PR body, not invented._

## Built

### Original build (2026-08-02)
- **Branch:** `feature/price-rate-iud`. Check-existing gate: 0b grep ec-automation -> only this
  build (0 other files referenced 'price_rate'); reused shared engine (`ec_object_iud.py`) + T2 +
  `DbVerify`.
- Recon (`investigation/recon.py`, read-only + `tmp/price_rate/config.json` scan): OV-GM (grid
  `manageObject:form:T_data`). Nav: Business Unit dropdown + GO. Mandatory Price Rate Code / Price
  Rate Name / Start Date + dropdown Frequency.
- Built via generator `tmp/gen_ovgm.py`: label-driven T3 (no hardcoded ids); Playwright driver
  (`py/price_rate_iud.py`) + RF T3/suite (4 TC, suite-level login, bespoke inline navigator fill).
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4 pass,
  Playwright 8/8. DB residual 0.

### Area-pattern conversion (PR #534, merged 2026-08-26)
- Converted the RF IUD suite from the OLD bespoke-navigator/4-TC/suite-level-login pattern to the
  full Area-pattern structure, mirroring `area_page.resource`/`area_iud.robot` exactly:
  properties-file-driven navigator via the shared `Apply Navigator From Properties` T2 keyword
  (`resources/manage_object.resource`, added 2026-08-26), per-TC login/logout, 5 TCs (added TC04
  Find), a fixed test code (`AUTOTEST_PRICE_RATE`, confirmed 0 rows before use, replacing the old
  timestamped code), a dedicated credentials pair (`PRICE_RATE_EC_USER`/`PRICE_RATE_EC_PASS` in
  `resources/credentials.py`), explicit grid-filter wiring (`Find/Clear Price Rate Row By
  Filter`), and zero inline DB-verify calls left in the `.robot` file - the old screen-local
  DB-verify wrapper keywords were removed, DB proof now comes solely from the shared T2 `Verify
  Object Removed` + the mandatory live-run self-clean check.
- New test-data files: `testdata/price_rate_{navigator,insert,update,form_verify,
  grid_verify}.properties`.
- The screen's genuine Business Unit navigator + GO gesture ("SS2 BU", a **single dropdown**, not
  a multi-level cascade) was KEPT unchanged - this was a structural conversion, not a
  reclassification of the screen as plain Bank-shaped.
- Registry (`docs/ec_screen_registry.md`) and scorecard (`docs/automation-scorecard.md`) rows
  MODIFIED in place (not new rows).

### This backfill (2026-08-27)
- Refreshed `price_rate_sow.md` (dev story section) and `README.md` (exact commands, DB self-clean
  query, Area-pattern facts) to reflect PR #534's conversion; both predated the JOURNAL rule and
  still described the OLD 4-TC/timestamped-code shape.
- Added this `JOURNAL.md`, `CHECKLIST.md`, and the KB selector map
  `ec-ui-knowledge/screens/price_rate.md` (refreshed - a stale 2026-08-02 version already existed,
  describing a multi-level nav cascade that PR #534's real page-object Documentation confirms is
  actually a single dropdown, C:1 only).
- Added `evidence/backfill_2026-08-27/` (fresh dryrun + live headless re-run, with per-TC
  screenshots, of the already-proven Area-pattern suite - no automation code touched).

## Done well
- Full I-U-D DB-verified vs `OV_PRICE_RATE` (insert Price Rate Code/Name, update Price Rate Name,
  delete End=Start absent); self-clean 0 residual, confirmed via a FRESH oracledb connection both
  before and after this backfill's own live re-run.
- Screen-prefixed labels confirmed live, not assumed: PR #534's page object documents that
  `objectForm`/`updateAttributes` use "Price Rate Code"/"Price Rate Name" (SCREEN-PREFIXED, like
  Area's own "Area Code"/"Area Name"), NOT the generic "Code"/"Name" Bank/Object List use.
- Robocop parity check re-run during this backfill: **7 issues** (5x `DOC02` missing test-case
  documentation + 2x `VAR02`) on the 2 changed files, cross-checked against
  `area_page.resource`/`area_iud.robot` (also 7 issues, same kind) - parity confirmed
  independently, not just cited from the PR.
- Full-tree dryrun of the Price Rate suite alone re-confirmed: 5/5 PASS.

## Done wrong / lessons
- No real regression or wrong turn was disclosed in PR #534's own body for the conversion itself.
- **Backfill-specific, real flake hit and resolved this session:** this backfill's first live
  headless re-run of the ALREADY-PROVEN suite hit `Error: Could not find active page` on TC04/TC05
  (3/5 PASS that attempt), and subsequent full-suite retries intermittently failed at Suite Setup
  itself (`Playwright process has been terminated`, then `browserContext.newPage: ... has been
  closed`). `tasklist | grep -i chrome` found a growing pile of leftover `chrome-headless-shell.exe`
  + `node.exe` processes each time (confirmed, not assumed) - this session's known cause of RF
  flakes (per the task's own standing note), not a Price Rate code defect. Cross-checked against
  the **Area** suite's own TC01 in isolation, which failed identically at the same point during the
  same window - proving the failure was environment-wide, not specific to Price Rate's automation.
  The EC web app itself was confirmed reachable and responding normally (`curl` HTTPS 302) the
  whole time, ruling out an EC-side outage. Resolution: repeated `taskkill /F /IM
  chrome-headless-shell.exe` + `taskkill /F /IM node.exe`, a short pause, then a clean full-suite
  re-run - the suite passed **5/5** on the resulting clean attempt (log/report/output archived in
  `evidence/backfill_2026-08-27/live/`). No RF automation file was touched to reach this result.

## Blockers -> resolution
- The chrome/node process pile-up above was the only blocker hit during this backfill; resolved by
  process cleanup + retry, not by any code change. No data damage: the interrupted TC02
  insert+TC03 update left one residual `AUTOTEST_PRICE_RATE` row after the first partial attempt,
  which was cleared by re-running TC05 alone (confirmed via a fresh DB re-read, 0 residual) before
  the final clean full-suite run.
- No other hard blockers during the original build, PR #534's conversion, or this backfill.

## Decisions
- Playwright bundle stays waived permanently for this backfill (owner decision 2026-08-27,
  `docs/IUD-DELIVERABLE-CHECKLIST.md` Section H) - the existing `py/price_rate_iud.py` and
  `investigation/recon.py` from the 2026-08-02 build are preserved as-is and were NOT touched,
  re-verified, or regenerated. The Universal Screen Engine is the owner-decided replacement for
  hand-written Playwright drivers going forward.
- The RF suite remains the maintained/live test; the Playwright driver is historical reference
  only (README.md updated to say so explicitly).
- Code lives in `ec-automation`; `ec-ui-knowledge/` stays MD-only.

## Evidence
- Original build (2026-08-02): `evidence/prt_0[1-5]_*.png` (5 screenshots) +
  `evidence/results.json` (`verify_screen.py` OVERALL PASS, RF 4/4, Playwright 8/8).
- PR #534 conversion (2026-08-26): live run `5 tests, 5 passed, 0 failed` (TC01-TC05), 14 `Find
  Object Row By Filter` hits in output.xml, robocop 7 issues (parity with Area), full-tree dryrun
  850/850, DB self-clean 0/0 (fresh oracledb, before+after) - all cited in the PR body.
- This backfill (2026-08-27, `evidence/backfill_2026-08-27/`): `dryrun/` (5/5 PASS,
  `log.html`/`report.html`/`output.xml`) and `live/` (5/5 PASS headless on the clean re-run, with
  a screenshot per TC step: login/open_screen/action/verify/logout x5 TCs,
  `log.html`/`report.html`/`output.xml`), a re-confirmed 15-hit filter-fired grep, a re-confirmed
  7-issue robocop parity check against Area's own baseline, a fresh-connection DB self-clean
  (`OV_PRICE_RATE`: 0 rows for `AUTOTEST_PRICE_RATE`, 0 residual `AUTOTEST%`), and `py
  scripts/check_bundle_hygiene.py` -> `RESULT: PASS`.
