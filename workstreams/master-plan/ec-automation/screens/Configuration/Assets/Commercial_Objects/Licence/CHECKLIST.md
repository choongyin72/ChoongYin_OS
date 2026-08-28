# IUD Task — Deliverable Checklist (Licence)

Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md` (Sections 0, A minus 4/5, B, C, D, E per
Section H's Bank-pattern backfill scope — items 4/5, the Playwright driver +
investigation/, stay permanently waived per the owner's 2026-08-27 decision, superseded
by the Universal Screen Engine). Ticked with real evidence from this backfill
(`docs/lean-deliverable-backfill-workorder.md` Batch 6) — the RF automation itself was
NOT rebuilt or re-verified from scratch; this is documentation/evidence backfill around
already-working, already-merged automation (PR #438, 2026-08-23).

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** No `ec-ui-knowledge/screens/licence.md` existed before this backfill (only `bank.md`/`bank_account.md` existed in `ec-ui-knowledge/screens/`) — created fresh as item 20 below, sourced from the T3 page object's own Variables section.
- [x] **0b.** `grep -ril licence workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}` → found: `pageobjects/Configuration/Assets/Commercial_Objects/licence_page.resource`, `tests/Configuration/Assets/Commercial_Objects/licence_iud.robot`, `screens/Configuration/Assets/Commercial_Objects/Licence/` (existing bundle, updated not duplicated).
- [x] **0c.** No new engine/plumbing built — this task is documentation-only; existing T2 (`manage_object.resource`) + T3 (`licence_page.resource`) reused as-is, untouched.

## A. Bundle artifacts — `screens/Configuration/Assets/Commercial_Objects/Licence/`
- [x] **1. `licence_sow.md`** — updated: classification (Bank pattern, plain OV, no navigator), grid id, DB view, mandatory fields (Licence Code/Licence Name/Start Date), test data, dev story pulled from PR #438's real body.
- [x] **2. `README.md`** — updated: bundle overview + exact commands (dryrun, `EC_HEADLESS=true` live run, filter-fired grep, DB self-clean query).
- [x] **3. `JOURNAL.md`** — new: Built / Done well / Done wrong-or-lessons / Blockers→resolution / Decisions / Evidence, modeled on `screens/Configuration/Assets/Financial_Objects/Bank/JOURNAL.md`, content sourced from PR #438's real body.
- [ ] **4. Playwright driver** — N/A / permanently waived (Section H: superseded by the Universal Screen Engine; original 2026-06-12 standalone reference kept for history only, not rebuilt).
- [ ] **5. `investigation/`** — N/A / permanently waived (same reason as #4; pre-existing recon scripts from the 2026-06-12 build left untouched).
- [x] **6. `evidence/`** — added this backfill's re-run artifacts: `licence_backfill_dryrun_report.txt` (5/5 PASS), `licence_backfill_live_report.txt` (5/5 PASS), `licence_backfill_live_output.xml`, `licence_backfill_filter_fired_count.txt` (=5), `licence_backfill_selfclean.txt` (0 residual). Pre-existing 2026-06-12 Playwright screenshots + `licence_results.json` left in place, not deleted.
- [x] **7. `CHECKLIST.md`** — this file.

## B. RF files — treeview-mirrored (pre-existing, NOT modified by this backfill)
- [x] **8. T3 page object** `pageobjects/Configuration/Assets/Commercial_Objects/licence_page.resource` — pre-existing (rebuilt in PR #438, 2026-08-23), label-driven, docstring matches Variables. Not touched by this backfill (read-only confirmation).
- [x] **9. Suite** `tests/Configuration/Assets/Commercial_Objects/licence_iud.robot` — pre-existing (rebuilt in PR #438), TC01 clean-state → TC02 insert → TC03 update → TC04 find → TC05 delete/cleanup. Not touched by this backfill.

## C. Verification gates (re-run for evidence capture, 2026-08-28; automation unchanged)
- [x] **10. robocop clean** — `py -m robocop check pageobjects/.../licence_page.resource tests/.../licence_iud.robot` → 9 issues (4 VAR02 + 5 DOC02), same shape/baseline as PR #438's cited 12 (12 minus the 3 pre-existing `credentials.py` findings not re-scanned in this narrower re-run). No new issue classes.
- [x] **11. `--dryrun` N/N PASS** — `robot --dryrun tests/.../licence_iud.robot` → 5 tests, 5 passed, 0 failed (`evidence/licence_backfill_dryrun_report.txt`).
- [x] **12. LIVE headless run N/N PASS** — `EC_HEADLESS=true robot tests/.../licence_iud.robot` → 5 tests, 5 passed, 0 failed, run twice during this backfill (`evidence/licence_backfill_live_report.txt`, `evidence/licence_backfill_live_output.xml`).
- [x] **13. DB ground-truth** — `SELECT COUNT(*) FROM OV_LICENCE WHERE CODE = 'AUTOTEST_LICENCE'` via a fresh independent `oracledb` connection = 0 after the live run (`evidence/licence_backfill_selfclean.txt`). Filter keyword confirmed fired: `grep -c 'name="Find Licence Row By Filter"' output.xml` = 5 (`evidence/licence_backfill_filter_fired_count.txt`).
- [x] **14. FULL I-U-D scope** — Insert (TC02) + Update (TC03) + Find (TC04) + Delete (TC05) all present and passing.
- [x] **15. Self-clean confirmed** — independent fresh-connection re-read = 0 residual `AUTOTEST_LICENCE` rows in `OV_LICENCE`, confirmed both before and after the backfill's live runs.
- [x] **16. Hygiene PASS** — no new code files added by this backfill (docs/evidence only); robocop re-run (item 10) shows the established baseline, no regressions introduced.

## D. Delivery
- [x] **17. Registry row** — `docs/ec_screen_registry.md` row for Licence already present (line ~71, added at PR #438's merge, 2026-08-23): confirms Bank-pattern conversion, `OV_LICENCE`, manage-object nav-free, grid id, mandatory fields, grid columns. Not modified by this backfill (append-only rule — no new row needed since PR #438 already appended it).
- [x] **18. Scorecard row** — `docs/automation-scorecard.md` row already present (added at PR #438's merge). Not modified by this backfill.
- [x] **19. PR** — this backfill's own PR, 6-field body (What was backfilled / Files added / DB ground-truth evidence / Self-clean confirmed / Rules applied / Base branch = master); R8 sync before push; never self-merge.

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/licence.md` — new, nav path/DB view/grid id/insert-update-delete selectors/mandatory fields/quirks/last-verified date, transcribed from `licence_page.resource`'s own Variables section (not re-discovered).
- [x] **21. Reuse clause** — Step 0 found Licence already implemented (PR #438, merged 2026-08-23); this backfill is exactly the "reuse run" deliverable refresh the clause requires: JOURNAL (#3), evidence (#6), and KB map (#20) all produced/refreshed, not just green tests re-confirmed.
