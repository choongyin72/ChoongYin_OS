# Berth — IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md)

_Refreshed 2026-08-28 — lean-deliverable backfill (Batch 8 of `docs/lean-deliverable-backfill-workorder.md`),
per Section H (owner decision 2026-08-27: the 2026-08-23/26 lean waiver is retired except items 4/5, the
Playwright driver + investigation/, which stay permanently waived going forward). The original 2026-07-26
checklist below described the pre-PR#454 4-TC build; this refresh re-ticks against the CURRENT (post-#454,
5-TC) automation. Berth is one of the two exemplar screens (with Bank) the Bank-pattern initiative is
modeled on — no automation file was touched by this backfill._

## Step 0 — check-existing gate
- [x] **0a.** `ec-ui-knowledge/screens/berth.md` existed and was read first (refreshed in this backfill, not re-scanned from scratch).
- [x] **0b.** `grep -ril berth workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}` → found — existing impl reused/extended (PR #454 rebuilt in place, this backfill adds docs only).
- [x] **0c.** Shared engine reused: RF suite uses shared T2 `resources/manage_object.resource` + T1 `resources/common.resource`; Playwright driver reuses `py/ec_object_iud.py` + `libraries/DbVerify.py` — no parallel copy.

## A. Bundle artifacts — `screens/Configuration/Assets/Transport_Objects/Berth/`
- [x] **1.** `berth_sow.md` — refreshed 2026-08-28 to describe the post-PR#454 shape (classification, nav/grid/cell shape incl. grid-filter wiring, test data, dev story pulled from PR #454's real body).
- [x] **2.** `README.md` — refreshed 2026-08-28 with exact dryrun/live/DB self-clean commands.
- [x] **3.** `JOURNAL.md` — refreshed 2026-08-28: original 2026-07-26 entry kept, 2026-08-23 PR #454 entry added (pulled from the real PR body), this backfill's own 2026-08-28 entry added (including the disclosed DSN mistake, not smoothed over).
- [x] **4.** Playwright flow → `py/berth_iud.py` — **pre-existing, untouched by this backfill** (predates the lean rule; item 4 is permanently waived for NEW Bank-pattern work per Section H, but this screen already has one from 2026-07-26 and it was not re-verified or modified here).
- [x] **5.** `investigation/recon.py` — **pre-existing, untouched by this backfill** (same status as item 4 — predates the lean rule, permanently waived going forward, not re-run here).
- [x] **6.** `evidence/` — pre-existing 2026-07-26 Playwright screenshots + `rf_report.html` kept; this backfill added `evidence/backfill_2026-08-28/` (dryrun_output.xml, live_output.xml/log.html/report.html, per-TC screenshots, robocop_output.txt, hygiene_output.txt) from a fresh real run.
- [x] **7.** `CHECKLIST.md` — this file, refreshed with real evidence citations.

## B. RF files — treeview-mirrored
- [x] **8.** T3 `pageobjects/Configuration/Assets/Transport_Objects/berth_page.resource` — rebuilt PR #454 (label-driven, properties-file-driven, grid-filter wired, NO hardcoded ids). NOT modified by this backfill.
- [x] **9.** Suite `tests/Configuration/Assets/Transport_Objects/berth_iud.robot` — rebuilt PR #454 (5-TC: clean-state/insert/update/find/delete, per-TC Login/Logout, fixed test code `AUTOTEST_BERTH`). NOT modified by this backfill.

## C. Verification gates (real evidence, this backfill's own re-run 2026-08-28)
- [x] **10.** robocop — `py -m robocop check pageobjects/.../berth_page.resource tests/.../berth_iud.robot` → **9 issues**, all DOC02/COM04/DOC03/MISC06 (missing `[Documentation]` on TC03-05 etc.) — cross-checked against Bank's own robocop run (13 issues, same category) to confirm this is the pre-existing baseline PR #454's body already disclosed, not a new defect class. NOT "clean" — disclosed honestly (see `evidence/backfill_2026-08-28/robocop_output.txt`).
- [x] **11.** `robot --dryrun` — **5/5 PASS, 0 failed** (`evidence/backfill_2026-08-28/dryrun_output.xml`).
- [x] **12.** LIVE run — `EC_HEADLESS=true robot ...` → **5/5 PASS, 0 failed**, first attempt, no retry needed (`evidence/backfill_2026-08-28/live_output.xml`/`live_report.html`/`live_log.html` + 20 per-TC screenshots).
- [x] **13.** DB ground-truth — in-suite: `Verify Object Insert Exists`/`Verify Object Form Record`/`Verify Object Found`/`Verify Object Removed` (T2, backed by `libraries/DbVerify.py` against `OV_BERTH`). Independent re-check this backfill: fresh `oracledb` connection (`localhost:1521/ORCL` alias, matching the repo's own default) — `SELECT code, name, object_end_date FROM OV_BERTH WHERE code = 'AUTOTEST_BERTH'` → 0 rows.
- [x] **14.** FULL I-U-D — TC02 Insert, TC03 Update, TC05 Delete all present and passing (TC01 clean-state + TC04 Find round out the 5-TC suite).
- [x] **15.** Self-clean confirmed — independent fresh-connection re-read: 0 residual `AUTOTEST_BERTH` rows; `SELECT COUNT(*) FROM OV_BERTH` = 11, matching the SOW's long-standing real-row count (pre-existing production data confirmed untouched).
- [x] **16.** Hygiene — `py scripts/check_bundle_hygiene.py` → **RESULT: PASS** — no hardcoded creds (R16), pure ASCII (R20), no CHECKLIST/VERIFY-REPORT contradiction (`evidence/backfill_2026-08-28/hygiene_output.txt`).

## D. Delivery
- [x] **17.** Registry row — already present (`docs/ec_screen_registry.md`, updated by PR #454); not reopened by this backfill (doc-only refresh doesn't change the registry claim).
- [x] **18.** Scorecard row — already present (`docs/automation-scorecard.md`, updated by PR #454); not reopened by this backfill.
- [x] **19.** PR — this backfill's own PR uses the standard body (What was backfilled / Files added / Base branch = master); never self-merge.

## E. Knowledge base
- [x] **20.** KB map `ec-ui-knowledge/screens/berth.md` — refreshed 2026-08-28 to the post-PR#454 shape (5-TC, fixed test code, grid-filter wiring, dedicated credentials, last-verified date updated).
- [x] **21.** Reuse clause — satisfied: this is a reuse/refresh run (Step 0 found the screen already implemented), and it produced/refreshed JOURNAL (#3), evidence (#6), and KB map (#20) as required — not just a "tests still pass" claim.

_Items 4/5 note: PERMANENTLY WAIVED for new Bank-pattern work going forward (Section H), but this screen
already has a Playwright driver + investigation/ predating the lean rule — kept as pre-existing/untouched,
not re-verified or expanded by this backfill._
