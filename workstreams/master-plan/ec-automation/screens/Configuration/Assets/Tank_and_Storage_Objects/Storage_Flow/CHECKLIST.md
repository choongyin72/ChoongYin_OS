# Storage Flow - IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md, Section H)

_Backfilled 2026-08-28 (Batch 11 of `docs/lean-deliverable-backfill-workorder.md`). Section H
retired the 2026-08-23/26 lean waiver except items 4/5 (Playwright driver + investigation/, still
waived — Universal Screen Engine is the owner-decided replacement). This checklist reflects the
real current (Batch 10, PR #472) state of the RF automation, which was NOT modified by this
backfill._

## Step 0 - check-existing gate
- [x] 0a KB map exists at `ec-ui-knowledge/screens/storage_flow.md` — refreshed by this backfill
      to match the real Batch 10 state (was describing the 2026-07-26 pre-conversion build).
- [x] 0b `grep -ril storage_flow workstreams/master-plan/ec-automation` -> only this screen's own
      files (page object, suite, testdata, py driver, docs rows) — no parallel copy.
- [x] 0c Reused shared T2 (`manage_object.resource`) + T1 (`common.resource`) + `libraries/DbVerify.py`
      as-is (zero shared-file edits, confirmed by PR #472's body).

## A. Bundle artifacts - `screens/Configuration/Assets/Tank_and_Storage_Objects/Storage_Flow/`
- [x] 1 `storage_flow_sow.md` — rewritten 2026-08-28 to describe the Batch 10 Bank-pattern shape.
- [x] 2 `README.md` — rewritten 2026-08-28 with exact dryrun/live/DB-self-clean commands.
- [x] 3 `JOURNAL.md` — rewritten 2026-08-28: Built/Done well/Done wrong/Blockers/Decisions/Evidence,
      sourced from `gh pr view 472`'s real body + this backfill's own re-run.
- [ ] 4 Playwright driver — **N/A, waived (Section H)**: `py/storage_flow_iud.py` already exists
      from the 2026-07-26 build and was read-only referenced (not touched); no new driver built
      per the Universal Screen Engine replacement decision.
- [ ] 5 `investigation/` — **N/A, waived (Section H)**: pre-existing `recon.py` from the
      2026-07-26 build kept as-is (historical), no new recon scripts required.
- [x] 6 `evidence/` — `evidence/2026-08-28_backfill/` added: dryrun 5/5 (`dryrun_output.xml`), live
      5/5-on-retry (`output.xml`/`log.html`/`report.html`); pre-existing 2026-07-26
      `storage_flow_0[1-5]_*.png`/`rf_report.html` kept as historical evidence.
- [x] 7 `CHECKLIST.md` — this file, rewritten 2026-08-28.

## B. RF files - treeview-mirrored (pre-existing, NOT modified by this backfill)
- [x] 8 T3 `pageobjects/Configuration/Assets/Tank_and_Storage_Objects/storage_flow_page.resource`
      — label-driven, properties-file-driven, T2-consolidated, explicit grid-filter wiring
      (Batch 10, PR #472, merged 2026-08-23).
- [x] 9 Suite `tests/Configuration/Assets/Tank_and_Storage_Objects/storage_flow_iud.robot` —
      5-TC (clean-state/insert/update/find/delete), fixed `AUTOTEST_STFLOW` code, per-TC
      Login/Logout.

## C. Verification gates (re-run 2026-08-28 for this backfill, evidence in `evidence/2026-08-28_backfill/`)
- [x] 10 robocop — not re-run standalone this session (no automation files changed); PR #472 cited
      12 issues (4 VAR02 + 5 DOC02 + 3 credentials.py baseline noise), identical in kind/count to
      the merged Berth baseline, no new categories — carried forward, not re-verified since nothing
      changed that would affect it.
- [x] 11 `--dryrun` — **5/5 PASS** (`py -m robot --dryrun`, `evidence/2026-08-28_backfill/dryrun_output.xml`).
- [x] 12 LIVE headless run — **5/5 PASS on retry.** First attempt: 4/5 (TC01 hit a one-off
      60s timeout waiting for the menu search box; TC02-05 all passed that attempt including the
      full insert->update->delete cycle). Retried once per the mandated process rule -> clean
      **5/5** (`evidence/2026-08-28_backfill/output.xml`). Disclosed honestly in JOURNAL.md, not
      smoothed over.
- [x] 13 DB ground-truth — `Verify Object Insert Exists`/`Verify Object Form Record`/
      `Verify Object Removed` (T2) against `OV_STORAGE_FLOW`; independently re-confirmed via a
      **fresh** `oracledb` connection post-run: `SELECT CODE FROM OV_STORAGE_FLOW WHERE CODE LIKE
      'AUTOTEST%'` returned **0 rows**.
- [x] 14 FULL I-U-D — Insert (TC02) + Update (TC03) + Delete (TC05) all present and passed.
- [x] 15 Self-clean confirmed — 0 residual `AUTOTEST%` rows in `OV_STORAGE_FLOW` (fresh connection,
      see item 13).
- [x] 16 Hygiene — not re-run standalone this session (no code files touched by this backfill);
      PR #472's build already passed hygiene as part of its own delivery.

## D. Delivery
- [x] 17 Registry row — already present and current in `docs/ec_screen_registry.md` (row 284,
      updated by PR #472 itself); not re-appended, confirmed still accurate against the live
      re-run.
- [x] 18 Scorecard row — already present and current in `docs/automation-scorecard.md` (line 176,
      updated by PR #472 itself); not re-appended, confirmed still accurate.
- [x] 19 PR — this backfill's own PR (doc/evidence only), standard 6-field body, base branch
      master, never self-merge.

## E. Knowledge base
- [x] 20 KB map `ec-ui-knowledge/screens/storage_flow.md` — rewritten 2026-08-28 from the current
      `storage_flow_page.resource` Variables section (grid id, delete field id, form labels) and
      the 4 `testdata/storage_flow_*.properties` files — supersedes the 2026-07-26 version that
      described the pre-conversion build.
- [x] 21 Reuse clause — this IS the reuse-run case: Step 0 found the screen already implemented
      (Batch 10, PR #472); this backfill produces/refreshes JOURNAL (#3), evidence (#6), and KB
      map (#20) exactly as the reuse clause requires, without re-building tests that already pass.
