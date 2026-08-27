# IUD Task — Deliverable Checklist — Field Group

_Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md`. This is a **documentation/evidence backfill**
(`docs/lean-deliverable-backfill-workorder.md`, owner decision 2026-08-27, Section H) around
already-merged, already-live-tested RF automation (PR #434, merged 2026-08-23). No RF file
(`field_group_page.resource`, `field_group_iud.robot`, `testdata/field_group_*.properties`) was
modified to produce this checklist. Items 4/5 (Playwright driver + investigation/) stay
permanently waived per Section H — a pre-existing Playwright bundle from the screen's original
2026-06-12 build is kept in this bundle unchanged, not rebuilt._

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/field_group.md` did not exist before this backfill —
      created in this PR (see item 20). Selectors transcribed from `field_group_page.resource`'s
      own Variables section, not re-scanned live.
- [x] **0b.** `grep -ril field_group workstreams/master-plan/ec-automation/{py,pageobjects,
      tests,screens,testdata}` -> existing impl found:
      `pageobjects/Configuration/Assets/Commercial_Objects/field_group_page.resource`,
      `tests/Configuration/Assets/Commercial_Objects/field_group_iud.robot`,
      `testdata/field_group_{insert,update,form_verify,grid_verify}.properties`,
      `screens/Configuration/Assets/Commercial_Objects/Field_Group/` (SOW/README/playwright/
      investigation/evidence pre-existed from the 2026-06-12 build, converted to Bank pattern
      by PR #434 on 2026-08-23). REUSED/EXTENDED — no parallel copy built. Disambiguated from
      `field_page.resource`/`field_iud.robot` (a DIFFERENT screen, the Area-pattern "Field",
      already backfilled in Batch 1) by exact grep on `field_group_page.resource`.
- [x] **0c.** Shared engine reused: RF suite calls the shared T2 `resources/manage_object.resource`
      (`Insert/Update/Verify Object *`, `Find/Clear Object Row By Filter`) + T1
      `resources/common.resource` (`Login/Open EC Screen`). No new plumbing added by this
      backfill.

## A. Bundle artifacts — `screens/Configuration/Assets/Commercial_Objects/Field_Group/`
- [x] **1. `field_group_sow.md`** — updated (Section 6 addendum) with current classification
      (plain Bank-pattern OV, no navigator), current grid/DOM shape, current test data, and the
      dev story pulled from PR #434's real body.
- [x] **2. `README.md`** — updated with the bundle overview + exact dryrun/live/DB self-clean
      commands.
- [x] **3. `JOURNAL.md`** — created: Built/Done well/Done wrong-or-lessons/Blockers->resolution/
      Decisions/Evidence, pulled from PR #434's real body + this session's own live-run evidence.
- [ ] **4. Playwright driver** — N/A. Playwright bundle waived, owner decision 2026-08-27
      (Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`); the pre-existing
      `playwright/ec_iud_field_group.py` from the 2026-06-12 build is kept unchanged, not
      rebuilt.
- [ ] **5. `investigation/`** — N/A, same waiver as item 4; the pre-existing `investigation/`
      scripts from the 2026-06-12 build are kept unchanged.
- [x] **6. `evidence/`** — captured in this session: `log.html`, `output.xml`, `report.html`
      from a live 5/5 RF run (2026-08-28) in `evidence/backfill_2026-08-28/`, alongside the
      pre-existing 2026-06-12 evidence (screenshots + `field_group_results.json`, unchanged).
- [x] **7. `CHECKLIST.md`** — this file.

## B. RF files — treeview-mirrored (pre-existing, unmodified by this backfill)
- [x] **8. T3 page object**
      `pageobjects/Configuration/Assets/Commercial_Objects/field_group_page.resource` —
      pre-existing, merged in PR #434 (2026-08-23), not touched by this backfill.
- [x] **9. Suite** `tests/Configuration/Assets/Commercial_Objects/field_group_iud.robot` —
      pre-existing, merged in PR #434, not touched by this backfill.

## C. Verification gates (re-run for evidence, not re-verification of a defect)
- [x] **10. robocop clean** — `py -m robocop check pageobjects/.../field_group_page.resource
      tests/.../field_group_iud.robot` (this session, 2026-08-28) -> **9 issues** (4 VAR02 + 5
      DOC02) — matches PR #434's own cited 9-issue baseline exactly. No drift, no new issue
      category.
- [x] **11. `--dryrun` N/N PASS** — `robot --dryrun tests/` (full tree, this session) ->
      **883/883 PASS**.
- [x] **12. LIVE headless run N/N PASS** — `EC_HEADLESS=true robot --outputdir
      screens/Configuration/Assets/Commercial_Objects/Field_Group/evidence/backfill_2026-08-28
      tests/.../field_group_iud.robot` (this session, 2026-08-28) -> **5/5 PASS**, first
      attempt, no retry needed. Artifacts in `evidence/backfill_2026-08-28/`.
- [x] **13. DB ground-truth** — fresh `oracledb` connection (`localhost:1521/ORCL`,
      `ECKERNEL_EC`), run after the live pass: `SELECT COUNT(*) FROM OV_FIELD_GROUP WHERE
      CODE = 'AUTOTEST_FIELD_GROUP'` -> `0`; `SELECT CODE FROM OV_FIELD_GROUP WHERE CODE LIKE
      'AUTOTEST%'` -> no rows.
- [x] **14. FULL I-U-D scope** — TC02 Insert / TC03 Update / TC05 Delete all present and
      passing (plus TC01 Clean State, TC04 Find) — confirmed by reading
      `field_group_iud.robot`'s 5 test cases.
- [x] **15. Self-clean confirmed** — independent DB re-read (fresh connection, this session) =
      0 residual `AUTOTEST_FIELD_GROUP`/`AUTOTEST%` rows in `OV_FIELD_GROUP` after the live run.
- [x] **16. Hygiene PASS** — `py scripts/check_bundle_hygiene.py` (repo root, this session) ->
      `[hygiene] RESULT: PASS - no hardcoded creds (R16), pure ASCII (R20), no CHECKLIST/
      VERIFY-REPORT contradictions, doc rows match declared families` (167 bundles + 272 recon
      scripts scanned; one pre-existing unrelated WARN on a different screen's recon script,
      Contract Area — not this screen).

## D. Delivery
- [ ] **17. Registry row** — N/A for this backfill. Field Group's row in
      `workstreams/master-plan/ec-automation/docs/ec_screen_registry.md` already exists and
      already documents the PR #434 conversion (append-only edit made at merge time of that
      PR, not this backfill).
- [ ] **18. Scorecard row** — N/A for this backfill, same reasoning as item 17 —
      `docs/automation-scorecard.md`'s Field Group row already reflects the merged conversion.
- [x] **19. PR** — this backfill's own PR, with the standard body (What was backfilled / Files
      added / Base branch = master); never self-merged.

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/field_group.md` — created in this
      backfill: nav path, DB view, grid id, insert/update/delete selectors (transcribed from
      `field_group_page.resource`'s Variables section), mandatory-yellow fields, quirks, last
      verified date 2026-08-28.
- [x] **21. Reuse clause.** Step 0 found Field Group's RF automation ALREADY implemented and
      merged — this backfill produces exactly the deliverables the reuse clause requires: #3
      JOURNAL, #6 evidence, #20 KB map (plus #1/#2/#7 restored per Section H).
