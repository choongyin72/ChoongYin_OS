# IUD Task — Deliverable Checklist (Field)

Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md`. This is a **backfill** (owner decision
2026-08-27, `docs/lean-deliverable-backfill-workorder.md`) for a screen already converted to
the full Area pattern (PR #525 + PR #529, merged/landed 2026-08-26) under the now-retired
Section G lean waiver. Items 4/5 (Playwright driver + investigation/) remain waived per
Section H — the Universal Screen Engine replaces that role. All other items are ticked with
real evidence gathered by re-running the already-merged, already-live-tested suite ONE time
during this backfill session (2026-08-27), not by re-verifying or rebuilding the automation.

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** Read `ec-ui-knowledge/screens/field.md` — did not exist before this backfill;
      created it as part of this task (item 20 below), using `field_page.resource`'s own
      Variables section as source, not re-scanning the live screen.
- [x] **0b.** `grep -ril "field" workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}`
      → found existing implementation at `pageobjects/Configuration/Assets/Commercial_Objects/
      field_page.resource` + `tests/Configuration/Assets/Commercial_Objects/field_iud.robot`
      (merged, live, PR #525/#529). This task REUSES/DOCUMENTS it — no parallel copy built.
- [x] **0c.** N/A for this backfill — no new OV IUD driver is being built; the shared T2
      `resources/manage_object.resource` keywords are already in use by the existing suite.

## A. Bundle artifacts — `screens/Configuration/Assets/Commercial_Objects/Field/`
- [x] **1. `field_sow.md`** — updated (v2.0) with classification, nav/grid/cell shape, test
      data, and the real dev story pulled from PR #525/#529 bodies.
- [x] **2. `README.md`** — updated with bundle overview + exact `robot --dryrun`/live-run/
      DB self-clean commands.
- [x] **3. `JOURNAL.md`** — new, modeled on `screens/Configuration/Assets/Financial_Objects/
      Bank/JOURNAL.md`, built from PR #525/#529's real bodies including the honest
      missing-import defect caught by the mandatory dryrun.
- [ ] **4. `playwright/ec_iud_<slug>.py`** — N/A, permanently waived for Bank-/Area-pattern
      work (Section H) — the existing 2026-06-12 legacy Playwright driver is kept unchanged as
      historical reference, not updated/rebuilt.
- [ ] **5. `investigation/`** — N/A, same waiver as item 4. Existing legacy recon scripts kept
      unchanged.
- [x] **6. `evidence/`** — new `evidence/backfill-2026-08-27/` subfolder added with this
      session's live run artifacts (`live_log.html`, `live_output.xml`, `live_report.html`,
      `results_summary.md`); legacy 2026-06-12 screenshots + `field_results.json` kept
      unchanged in the existing `evidence/` folder.
- [x] **7. `CHECKLIST.md`** — this file.

## B. RF files — treeview-mirrored
- [x] **8. T3 page object** `pageobjects/Configuration/Assets/Commercial_Objects/
      field_page.resource` — already merged (PR #525/#529), NOT modified by this backfill.
- [x] **9. Suite** `tests/Configuration/Assets/Commercial_Objects/field_iud.robot` — already
      merged, 5-TC structure (Verify Clean State/Insert/Update/Find/Delete), NOT modified by
      this backfill.

## C. Verification gates (re-run once for backfill evidence, not a rebuild)
- [x] **10. robocop clean** — re-run this session: `py -m robocop check
      pageobjects/.../field_page.resource tests/.../field_iud.robot` → **7 issues** (2 VAR02 +
      5 DOC02), matching PR #529's cited parity with Area's own baseline (also 7 issues, same
      shape) — confirmed again independently, not a regression.
- [x] **11. `--dryrun` N/N PASS** — re-run this session: `py -m robot --dryrun tests/` →
      **883 tests, 883 passed, 0 failed** (full tree, includes Field's 5 TCs).
- [x] **12. LIVE headless run N/N PASS** — re-run this session:
      `EC_HEADLESS=true py -m robot tests/Configuration/Assets/Commercial_Objects/field_iud.robot`
      → **5 tests, 5 passed, 0 failed** (TC01–TC05).
- [x] **13. DB ground-truth** — exact assertion re-run this session via a fresh `oracledb`
      connection (`localhost:1521/ORCL`, `ECKERNEL_EC`):
      `SELECT COUNT(*) FROM OV_FIELD WHERE CODE LIKE 'AUTOTEST%'` → **0** (before and after the
      live run). Each op (insert/update/find/delete) verified at DB level via the shared T2
      `Verify Object Removed` keyword inside TC05 (confirmed by grep: zero inline DB-verify
      calls remain in `field_iud.robot`).
- [x] **14. FULL I-U-D scope** — Insert (TC02) + Update (TC03) + Find (TC04) + Delete (TC05)
      all present and passing.
- [x] **15. Self-clean confirmed** — independent fresh-connection DB re-read after this
      session's live run = 0 residual `AUTOTEST%` rows in `OV_FIELD`.
- [x] **16. Hygiene PASS** — re-run this session: `py scripts/check_bundle_hygiene.py` (repo
      root) → **RESULT: PASS** (167 bundles + 271 recon scripts scanned; no hardcoded creds,
      ASCII-clean, no CHECKLIST/VERIFY-REPORT contradictions, doc rows match declared
      families). One unrelated WARN for Contract Area's own investigation script — not a
      Field finding.

## D. Delivery
- [x] **17. Registry row** — already present in `docs/ec_screen_registry.md` (Field row,
      describes the full 2026-08-26 conversion in detail); not modified by this backfill
      beyond what PR #525/#529 already appended.
- [x] **18. Scorecard row** — already present in `docs/automation-scorecard.md` (added by
      PR #529, per that PR's own "Files touched" list).
- [x] **19. PR** — this backfill's own PR, standard 6-field body (What was backfilled / Files
      added / Base branch = master; per the backfill workorder's format, adapted from the
      standard body since no new automation/DB-write is being made).

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/field.md` — new, transcribed from
      `field_page.resource`'s own Variables section (nav path, DB view, grid id, mandatory
      fields, quirks), last-verified date 2026-08-27.
- [x] **21. Reuse clause** — Step 0 found the screen already implemented; this backfill
      produces/refreshes the required deliverables around it (JOURNAL, evidence, KB map, plus
      the SOW/README/CHECKLIST restored by Section H) rather than declaring "done" on green
      tests alone.

---

**OVERALL: PASS** — all non-waived items (1,2,3,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21)
ticked with real evidence gathered in this backfill session; items 4/5 correctly left N/A per
the permanent Section H waiver. No RF automation file was modified to produce this bundle.
