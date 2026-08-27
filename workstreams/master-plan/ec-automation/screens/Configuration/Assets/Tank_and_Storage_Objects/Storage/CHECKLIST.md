# Storage — IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md, 21 gates)

_Backfilled 2026-08-28 per `docs/lean-deliverable-backfill-workorder.md` (Batch 4) — Storage was
converted to the full Area pattern in PR #537 (merged 2026-08-26) under the 2026-08-23/26 lean
waiver, which skipped items 1/3/6/7/20 below. Section H (2026-08-27) retired that waiver except
for items 4/5 (Playwright driver + investigation/), which stay permanently waived — the Universal
Screen Engine replaces that role. This checklist backfills the restored items; it does not
re-build or re-verify the RF automation itself (already proven at PR #537's merge)._

## Step 0 — check-existing gate
- [x] 0a. KB map exists (`ec-ui-knowledge/screens/storage.md`, refreshed by this backfill).
- [x] 0b. `grep -ril "storage_page.resource" workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}`
      → existing impl found: `pageobjects/Configuration/Assets/Tank_and_Storage_Objects/
      storage_page.resource`, `tests/Configuration/Assets/Tank_and_Storage_Objects/
      storage_iud.robot`, `docs/ec_screen_registry.md` row. Reused/updated in PR #537, NOT
      duplicated. This backfill adds documentation only, no code path was re-derived.
- [x] 0c. Shared engine reused — RF suite calls the shared T2 `resources/manage_object.resource`
      keywords (`Apply Navigator From Properties`, `Insert/Update/Find Object...`,
      `Verify Object Removed`) + `libraries/DbVerify.py`; no per-screen plumbing added.

## A. Bundle artifacts
- [x] **1.** `storage_sow.md` — refreshed this backfill (was describing the pre-#537 4-TC/
      first-available shape; now reflects PR #537's Area-pattern conversion).
- [x] **2.** `README.md` — refreshed this backfill with exact dryrun/live/DB-self-clean commands.
- [x] **3.** `JOURNAL.md` — refreshed this backfill: 2026-07-30 original build entry kept,
      2026-08-26 PR #537 conversion entry added from the real PR body, plus this backfill's own
      2026-08-28 entry (including the live-run flake, disclosed not smoothed over).
- [ ] **4.** Playwright driver — **N/A / permanently waived** (owner decision 2026-08-27, Universal
      Screen Engine replaces this role). Pre-existing `py/storage_iud.py` from the 2026-07-30
      build is untouched by this backfill and by PR #537.
- [ ] **5.** `investigation/` — **N/A / permanently waived**, same reason as item 4. The
      pre-existing `investigation/` folder (recon.py from 2026-07-30) is left as-is.
- [x] **6.** `evidence/` — this backfill added `dryrun_output.xml` (5/5 pass), `live_attempt1_
      output.xml` (4/5 pass, TC05 grid-redraw flake, disclosed in JOURNAL.md), `live_output.xml`
      + `live_report.html` + `live_log.html` (retry, 5/5 pass — the cited live evidence). The
      pre-existing `stg_0[1-5]_*.png` + `results.json` from the 2026-07-30 Playwright run are
      kept as historical evidence, not removed.
- [x] **7.** `CHECKLIST.md` — this file.

## B. RF files (pre-existing, verified not re-verified from scratch — already proven at PR #537)
- [x] **8.** T3 `pageobjects/Configuration/Assets/Tank_and_Storage_Objects/storage_page.resource`
      (label-driven, no hardcoded ids except the documented `objectdates` End Date constant —
      confirmed by reading the file, not touched by this backfill).
- [x] **9.** Suite `tests/Configuration/Assets/Tank_and_Storage_Objects/storage_iud.robot` (5 TCs,
      per-TC login/logout — confirmed by reading the file, not touched by this backfill).

## C. Verification gates (re-run once for this backfill's evidence capture, not a fresh build cycle)
- [x] **10.** robocop — `robocop check pageobjects/.../storage_page.resource tests/.../
      storage_iud.robot` → **7 issues, all DOC02** (missing `[Documentation]` on TC02-05, same
      baseline-noise class the PR #537 body cites for Area itself — no new issue class).
- [x] **11.** `--dryrun` — **5/5 PASS** (`evidence/dryrun_output.xml`, 2026-08-28).
- [x] **12.** LIVE headless run — first attempt **4/5 pass** (TC05 grid-redraw flake,
      `evidence/live_attempt1_output.xml`); retry **5/5 PASS**
      (`evidence/live_output.xml`/`live_report.html`, 2026-08-28) — cited as this backfill's
      live evidence, per the one-retry process rule.
- [x] **13.** DB ground-truth — TC05's DB check is the shared T2 `Verify Object Removed`
      (`OV_STORAGE`, code `AUTOTEST_STG`); independently confirmed via a fresh `oracledb`
      connection: `SELECT CODE, OBJECT_START_DATE, OBJECT_END_DATE FROM OV_STORAGE WHERE CODE
      LIKE 'AUTOTEST%'` → empty result set, both before and after the retry run.
- [x] **14.** FULL I-U-D scope — Insert (TC02) + Update (TC03) + Delete (TC05) all present and
      passed in the retry run.
- [x] **15.** Self-clean confirmed — fresh-connection query above returned 0 residual rows after
      the retry run.
- [x] **16.** Hygiene PASS — `py scripts/check_bundle_hygiene.py` → `RESULT: PASS` (no hardcoded
      creds / R16, pure ASCII / R20, no CHECKLIST/VERIFY-REPORT contradiction). The 2 WARN lines
      it reports belong to an unrelated screen (Contract_Area), not Storage.

## D. Delivery
- [x] **17.** Registry row — `docs/ec_screen_registry.md` Storage row already updated at PR
      #537's merge (2026-08-26); unchanged by this backfill.
- [x] **18.** Scorecard row — `docs/automation-scorecard.md` Storage row already updated at PR
      #537's merge; unchanged by this backfill.
- [x] **19.** PR — this backfill's own PR (docs/storage-backfill-artifacts), 6-field body,
      base = master, never self-merged.

## E. Knowledge base
- [x] **20.** KB selector map `ec-ui-knowledge/screens/storage.md` — refreshed this backfill from
      the pre-#537 shape (4-TC first-available) to reflect PR #537's fixed-code/per-TC-login/
      explicit-navigator-values shape, pulled from `storage_page.resource`'s own Variables
      section.
- [x] **21.** Reuse clause — this IS a reuse/refresh run (screen already implemented, converted
      under PR #537): JOURNAL, evidence, and KB map are all refreshed/produced by this backfill,
      per the reuse-clause requirement — not just passing tests.
