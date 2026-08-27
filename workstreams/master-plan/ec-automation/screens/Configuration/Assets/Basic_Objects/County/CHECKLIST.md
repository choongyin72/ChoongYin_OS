# IUD Task — Deliverable Checklist — County

Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md`. County is a Bank-pattern conversion (PR #429,
2026-08-23) with a targeted alignment fix (PR #489, 2026-08-24). Per Section H (owner decision
2026-08-27), the lean waiver for Bank-/Area-pattern work is RETIRED except items 4/5 (Playwright
driver + investigation/, permanently waived — superseded by the Universal Screen Engine). This
CHECKLIST is a **backfill** (2026-08-28) — the RF automation was NOT re-built or re-verified from
scratch; it was re-run once for evidence.

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/county.md` did not exist before this backfill — created now
      (this task). No prior KB map existed to reuse.
- [x] **0b.** `grep -ril county` confirms existing impl: `pageobjects/Configuration/Assets/Basic_Objects/county_page.resource`
      (T3) + `tests/Configuration/Assets/Basic_Objects/county_iud.robot` (suite) — REUSED, not rebuilt.
- [x] **0c.** Shared engine confirmed in use: T3 delegates to `resources/manage_object.resource` (T2) +
      `resources/common.resource` (T1); no new plumbing added.

## A. Bundle artifacts — `screens/Configuration/Assets/Basic_Objects/County/`
- [x] **1. `county_sow.md`** — updated: v2.0 classification (Bank pattern, no navigator, `OV_COUNTY`,
      mandatory fields, dev story pulled from PR #429/#489), v1.0 (2026-06-11) kept as history.
- [x] **2. `README.md`** — updated: bundle overview + exact dryrun/live/DB-self-clean commands for the
      current RF suite; original Playwright-only framing corrected.
- [x] **3. `JOURNAL.md`** — created: Built/Done well/Done wrong-or-lessons/Blockers→resolution/Decisions/
      Evidence, sourced from PR #429 and #489 bodies + commit messages.
- [ ] **4. `playwright/ec_iud_county.py`** — N/A, permanently waived (Section H) — Universal Screen
      Engine supersedes hand-written Playwright drivers. Original 2026-06-11 file kept as history only,
      not touched.
- [ ] **5. `investigation/`** — N/A, permanently waived (Section H), same reason. Original files kept
      as history only, not touched.
- [x] **6. `evidence/`** — created `evidence/2026-08-28_backfill_live_run/` with `output.xml`, `log.html`,
      20 step screenshots (TC01-05 × login/open_screen/action/verify/logout), and `RESULTS-SUMMARY.md`.
      Folder size 1.5MB total, largest single file `log.html` ~332KB — well under the 2MB single-file
      guidance, nothing truncated.
- [x] **7. `CHECKLIST.md`** — this file.

## B. RF files — treeview-mirrored (pre-existing, NOT modified by this task)
- [x] **8. T3 page object** `pageobjects/Configuration/Assets/Basic_Objects/county_page.resource` —
      pre-existing (PR #429/#489), read-only for this task.
- [x] **9. Suite** `tests/Configuration/Assets/Basic_Objects/county_iud.robot` — pre-existing
      (PR #429/#489), read-only for this task.

## C. Verification gates (re-run for evidence, 2026-08-28; automation itself unchanged)
- [x] **10. robocop clean-parity** — `py -m robocop check county_page.resource county_iud.robot` →
      **11 issues** (all DOC02/VAR02, same classes as Bank's own 13-issue baseline on
      `bank_page.resource`/`bank_iud.robot` run the same way) — parity confirmed, no new issue classes,
      not a regression.
- [x] **11. `--dryrun` N/N PASS** — County-only: `robot --dryrun tests/.../county_iud.robot` →
      **5 tests, 5 passed, 0 failed**. Full-tree: `robot --dryrun tests` → **883 tests, 883 passed,
      0 failed** (no collisions).
- [x] **12. LIVE headless run N/N PASS** — `EC_HEADLESS=true robot tests/.../county_iud.robot` →
      **5 tests, 5 passed, 0 failed** (TC01 Verify Clean State, TC02 Insert, TC03 Update, TC04 Find,
      TC05 Delete). Output: `results/_live_county/output.xml` (copied into `evidence/`).
- [x] **13. DB ground-truth** — pure-screen-verify pattern (PR #489): in-suite verification is via
      shared T2 keywords (`Verify Object Insert Exists`/`Verify Object Form Record`/`Verify Object
      Removed`, each comparing live screen values to `testdata/county_*.properties`), NOT an inline
      `DbVerify` call in the suite itself (deliberately removed to match `bank_iud.robot`). Out-of-suite
      DB ground truth for THIS backfill: fresh oracledb connection,
      `SELECT CODE FROM OV_COUNTY WHERE CODE LIKE 'AUTOTEST%'` → **0 rows** after the live run above
      (script: `Workplaces/county-backfill/selfclean_check.py`, gitignored scratch).
- [x] **14. FULL I-U-D scope** — TC02 Insert, TC03 Update, TC05 Delete all present and passed (TC04
      Find is additional, not a substitute for any of the three).
- [x] **15. Self-clean confirmed** — see item 13: 0 residual `AUTOTEST%` rows in `OV_COUNTY` on an
      independent fresh-connection re-read after the full live run.
- [x] **16. Hygiene** — no new/changed code files produced by this backfill (docs/evidence only);
      `check_bundle_hygiene.py`'s R16/R20 checks target `playwright/*.py`/`investigation/*.py`, both of
      which are untouched, pre-existing files from the original 2026-06-11 build (not created by this
      task, so not re-audited here).

## D. Delivery
- [x] **17. Registry row** — already present, PR #429/#489 era (`docs/ec_screen_registry.md` line 45,
      "County | ... OV ✅ rebuilt live 5/5 (2026-08-23) ..."). Append-only; this backfill did not need to
      add a new row (one already exists and accurately reflects the current automation).
- [x] **18. Scorecard row** — already present (`docs/automation-scorecard.md` line 85, Basic Objects
      section, "County (OV, manage-object) — Bank-pattern conversion ... ✅ Rebuilt live 5/5"). Append-only;
      no new row needed.
- [x] **19. PR** — this backfill's own PR, standard 6-field body, base branch master, never self-merged.

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/county.md` — created (did not exist before this
      backfill); nav path, DB view, grid id, delete-field id, mandatory-yellow fields, quirks
      (screen-prefixed labels, no dates on updateAttributes, pure-screen-verify convention), last-verified
      date 2026-08-28.
- [x] **21. Reuse clause** — Step 0 found the screen already implemented (RF suite live since 2026-08-23);
      per the reuse clause this backfill produced/refreshed JOURNAL (#3), evidence (#6), and KB map (#20)
      — not tests-passing alone.

## F / G — not applicable
Section F (engine-only bundle variant) does not apply — County has a full RF T3/suite, not an
engine-only build. Section G's lean-RF-only waiver is the ORIGIN of the gap this backfill closes, now
superseded by Section H for this screen's category.

## H — this backfill's own scope
Section H restored items 1/2/3/6/7/20 for Bank-/Area-pattern work; items 4/5 stay waived permanently.
This CHECKLIST reflects exactly that split. Items 8-19/21 were never waived and are ticked above with
real re-run evidence from 2026-08-28.
