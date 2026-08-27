# JOURNAL - Reservoir Formation (CO.0135) OV IUD

_Screen: Configuration > Assets > Well_and_Reservoir_Objects > Reservoir Formation (OV, date-effective).
View `OV_RESV_FORMATION`. This JOURNAL is backfilled 2026-08-28 (owner decision 2026-08-27 retired the
lean-deliverable waiver for Bank-/Area-pattern conversions; see `docs/lean-deliverable-backfill-workorder.md`
Batch 10). Real content pulled from PR #467's body and the pre-existing 2026-07-26 bundle - not invented._

## Built

### 2026-07-26 (original generator-scaffolded build)
- Recon (`investigation/recon.py`, read-only): DB `CLASS_TYPE=OBJECT` => OV; treeview Configuration >
  Assets > Well_and_Reservoir_Objects > Reservoir Formation. Mandatory Code/Name/Start Date; optional
  dropdowns skipped. Plain Bank-layout OV (single Date+GO nav, no mandatory dropdowns).
- Label-driven T3 (no hardcoded ids, `Fill OV Field By Label`). Playwright driver -> 7/7; RF T3 + 4-TC
  suite -> live 4/4 (no explicit Find TC, no properties-file insert/update, no grid-filter wiring).
- `verify_screen.py` -> OVERALL PASS: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4, Playwright 7/7.

### 2026-08-23 (Batch 9 full Bank-pattern conversion, PR #467)
- Rebuilt `reservoir_formation_page.resource` / `reservoir_formation_iud.robot` to mirror
  `bank_page.resource`/`berth_page.resource` exactly: properties-file-driven Insert
  (`Insert Object From Properties And Verify Code`), Update, form/grid verify; explicit
  `Find/Clear Reservoir Formation Row By Filter` wired into Update/Find/Verify-Found/Delete; dedicated
  `RESERVOIR_FORMATION_EC_USER`/`RESERVOIR_FORMATION_EC_PASS` credentials; fixed test code
  `AUTOTEST_RESVF` (replacing the earlier timestamp-suffixed unique code); expanded to 5 TCs (added
  TC04 Find).
- New `testdata/reservoir_formation_insert.properties`, `_update.properties`, `_form_verify.properties`,
  `_grid_verify.properties`.
- This **modified** the screen's existing `docs/ec_screen_registry.md` / `docs/automation-scorecard.md`
  rows (not new rows) - it already had a row from the 2026-07-26 build.

## Done well
- Full I-U-D DB-verified vs `OV_RESV_FORMATION`; live 5/5 (TC01 clean-state / TC02 insert / TC03 update /
  TC04 find / TC05 delete), self-clean 0 residual `AUTOTEST_RESVF` rows.
- Full-tree dryrun 762/762 pass at Batch 9 merge time - zero shared T1/T2 regression from the
  grid-filter wiring change.
- Filter keyword (`Find Reservoir Formation Row By Filter`) confirmed fired 7x via `output.xml` grep -
  not just assumed wired in, actually exercised.
- Fixed test code confirmed free in `OV_RESV_FORMATION` via a fresh oracledb connection before use, both
  at Batch 9 merge time and re-confirmed by this backfill's own fresh-connection check (2026-08-28,
  0 residual rows before and after the evidence-capture run).

## Done wrong / lessons
- The Batch 9 PR's shared findings doc (`tmp/batch9_shared_findings.md`) claimed the Batch 9 section
  headers in `docs/bank-pattern-conversion-checklist.md` / `docs/grid-filter-standardization-checklist.md`
  were pre-created on master via PR #464 - but PR #464 was still open/unmerged when this branch was cut
  from `origin/master`, so the headers did not actually exist yet. The worker added the header + its own
  row itself, with an explicit note flagging that the reviewer/merge step should dedupe to one header per
  file if PR #464 merged separately (same class of issue already hit once before, on Batch 7/8).
  **Lesson:** a shared cross-batch findings doc can go stale mid-flight if a sibling PR is still open;
  state the assumption explicitly in the PR body rather than trusting the doc silently.
- This bundle itself (SOW/README/JOURNAL/CHECKLIST/evidence/KB map) was NOT updated by PR #467 even
  though the automation was fully rebuilt - it stayed frozen at the 2026-07-26 build's content (4/4 RF,
  no grid-filter wiring, generated-unique test code) until this 2026-08-28 backfill. This is exactly the
  documentation debt the lean-waiver retirement (owner, 2026-08-27) exists to fix.

## Blockers -> resolution
- None new in this backfill. Per the process rule (retry-once-then-disclose), the live suite ran clean
  on the first attempt - no retry needed, no browser/timeout issue hit.
- An ad-hoc fresh-connection DB check during this backfill initially failed with a connection timeout
  because it used the wrong default DSN (`db.plutodev.woodside-pluto.tieto-og.cloud` from CLAUDE.md's
  Woodside-project reference, not this repo's local-sandbox default). Fixed by reading
  `resources/environment.py`'s actual fallback (`localhost:1521/ORCL`) instead of assuming the
  cross-project value - the second attempt (same DSN the suite itself uses) connected and returned 0
  residual rows.

## Decisions
- Playwright driver (`py/reservoir_formation_iud.py`) and its `investigation/` recon stay UNCHANGED and
  un-rebuilt by this backfill, per `docs/IUD-DELIVERABLE-CHECKLIST.md` Section H: items 4/5 remain
  permanently waived for Bank-/Area-pattern work, superseded by the Universal Screen Engine.
- This backfill only adds/refreshes documentation and evidence artifacts around the already-merged,
  already-working RF automation from PR #467 - it does not re-run the original build or touch any RF
  file.

## Evidence
- Batch 9 (PR #467, 2026-08-23): live RF 5/5, dryrun 762/762 (full-tree), filter fired 7x (output.xml
  grep), DB self-clean 0 residual (fresh oracledb connection).
- This backfill (2026-08-28): `evidence/` - dryrun 5/5 (screen-scoped) + live 5/5 (screen-scoped)
  log.html/report.html/output.xml + per-TC step screenshots (login/open_screen/action/verify/logout x5
  TCs); filter keyword re-confirmed fired 7x in this run's own output.xml; fresh-connection DB check
  0 residual `AUTOTEST_RESVF` rows in `OV_RESV_FORMATION` after the run.
