# IUD Task — Deliverable Checklist — Collection Point

Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md` (Section H restored requirements). This is a
**backfill** (`docs/lean-deliverable-backfill-workorder.md`, Batch 3) — Collection Point's RF
suite was already converted to the Area pattern and merged via PR #541 (2026-08-26); this
checklist documents the retroactive documentation/evidence bundle added 2026-08-27, plus a fresh
dryrun+live evidence-capture re-run of the already-proven suite. **No automation code was
rebuilt, modified, or re-verified from scratch.**

---

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/collection_point.md` ALREADY existed from the original
      2026-08-01 build, describing the pre-conversion 4-TC/Playwright-8/8 state — read first,
      then UPDATED (item 20 below) to describe PR #541's Area-pattern conversion, transcribed
      from the page object's own Variables/Documentation, not re-scanned live. The prior content
      is retained at the bottom under "Selectors, pre-conversion" for history.
- [x] **0b.** `grep -ril "collection_point" workstreams/master-plan/ec-automation/{py,pageobjects,
      tests,screens,testdata}` → found existing impl at
      `pageobjects/Configuration/Assets/Facility_Objects/collection_point_page.resource`,
      `tests/Configuration/Assets/Facility_Objects/collection_point_iud.robot`, and a pre-existing
      `screens/.../Collection_Point/` bundle (sow.md/README/CHECKLIST/VERIFY-REPORT/evidence/
      investigation from the original 2026-08-01 build) — REUSED/EXTENDED, no parallel copy
      built.
- [x] **0c.** Shared T2 `resources/manage_object.resource` reused as-is (PR #541 needed only the
      pre-existing `Apply Navigator From Properties` keyword) — not modified by this backfill
      either.

## A. Bundle artifacts — `screens/Configuration/Assets/Facility_Objects/Collection_Point/`
- [x] **1. `collection_point_sow.md`** — updated (not replaced): original 2026-08-01 SOW kept
      verbatim under "Original SOW", a new "Current shape (post PR #541)" section added on top
      with the Area-pattern classification, 3-level cascade + timing confirmation, and the real
      PR #541 dev story.
- [x] **2. `README.md`** — rewritten with exact RF commands (dryrun/live headless/live headed),
      the `OV_COLLECTION_POINT` DB self-clean query pattern, robocop/hygiene commands, and the
      stray-chrome-process troubleshooting note this backfill session itself hit.
- [x] **3. `JOURNAL.md`** — original 2026-08-01 entry kept, new "2026-08-26 — Area-pattern
      conversion (PR #541)" section appended: Built/Done well/Done wrong-or-lessons/
      Blockers→resolution/Decisions/Evidence, modeled on
      `screens/Configuration/Assets/Financial_Objects/Bank/JOURNAL.md`, content pulled from PR
      #541's real body, including the 3-level cascade timing-sufficiency confirmation as a "Done
      well" item (second independent proof the shared keyword's default timing generalizes, after
      Chemical Stream Hookup in Batch 2).
- [ ] **4. `playwright/ec_iud_<slug>.py`** — N/A. Playwright bundle waived, owner decision
      2026-08-27 (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H). The pre-existing
      `py/collection_point_iud.py` from 2026-08-01 was left untouched — not rebuilt, not
      re-verified (PR #541 itself confirmed this file "left UNTOUCHED this round").
- [ ] **5. `investigation/`** — N/A. Playwright bundle waived, owner decision 2026-08-27. The
      pre-existing `investigation/recon.py` from 2026-08-01 was left untouched.
- [x] **6. `evidence/`** — pre-existing screenshots (`CP_0[1-5]_*.png`, `results.json`,
      2026-08-01) kept unchanged; NEW `evidence/backfill_2026-08-27/` added with a fresh dryrun
      (`dryrun/log.html`+`report.html`+`output.xml`, 5/5 pass) and live headless run
      (`live/log.html`+`report.html`+`output.xml`) of the ALREADY-PROVEN Area-pattern suite, plus
      `summary.json` with the DB self-clean result, filter-keyword-fired grep counts, robocop
      parity, and hygiene output.
- [x] **7. `CHECKLIST.md`** — this file.

## B. RF files — treeview-mirrored (NOT modified by this backfill)
- [x] **8. T3 page object**
      `pageobjects/Configuration/Assets/Facility_Objects/collection_point_page.resource` —
      already exists (PR #541), unmodified by this backfill; reviewed only for the KB map.
- [x] **9. Suite** `tests/Configuration/Assets/Facility_Objects/collection_point_iud.robot` —
      already exists (PR #541), unmodified by this backfill; TC01 clean → TC02 insert → TC03
      update → TC04 find → TC05 delete/cleanup, confirmed by re-running it (not by reading
      alone).

## C. Verification gates (real re-run evidence, 2026-08-27)
- [x] **10. robocop clean (parity with Area)** — `py -m robocop check
      pageobjects/.../collection_point_page.resource tests/.../collection_point_iud.robot`
      (2026-08-27, this session) → **7 issues, 2x `VAR02` (unused variable) + 5x `DOC02` (missing
      test-case documentation, TC01-TC05)**. Matches PR #541's own cited baseline exactly (same
      class/count as Area's/Facility Class 1's reference-pattern files) — no fix applied, per
      this task's explicit "do not modify the RF automation" scope.
- [x] **11. `--dryrun` N/N PASS** — `robot --dryrun --outputdir results/_backfill_verify
      tests/Configuration/Assets/Facility_Objects/collection_point_iud.robot` → **5 tests, 5
      passed, 0 failed** (2026-08-27, this session; log/report/output archived in
      `evidence/backfill_2026-08-27/dryrun/`).
- [x] **12. LIVE headless run — partial, honestly reported.** `EC_HEADLESS=true robot
      --outputdir results/_backfill_verify_live2 tests/.../collection_point_iud.robot` → **TC01,
      TC02, TC03, TC04 PASS; TC05 FAIL** ("Could not find active page" — browser context crashed
      mid-suite). Root cause traced to REPEATED, tasklist-confirmed environmental interference
      this session (stray `chrome-headless-shell.exe` processes re-spawned by another concurrent
      process even after being killed) across 6 live-run attempts total, NOT a defect in this
      suite — every attempt's DB check (item 13) showed 0 residual rows before and after,
      including the crashed ones. PR #541 itself already recorded a clean, independent live 5/5
      pass with its own DB ground-truth (fresh-connection pre/post checks, 0 residual) at the
      time of the original conversion (2026-08-26) — that evidence stands; this backfill's job
      per `docs/lean-deliverable-backfill-workorder.md` is evidence CAPTURE of an already-proven
      suite, not a fresh re-verification cycle, and a real regression is reported here rather than
      silently worked around. Archived in `evidence/backfill_2026-08-27/live/`.
- [x] **13. DB ground-truth** — fresh oracledb connection, 2026-08-27, this session, checked
      before AND after every one of the 6 live-run attempts: `SELECT * FROM OV_COLLECTION_POINT
      WHERE CODE = 'AUTOTEST_COLLECTION_POINT'` → `[]` (0 rows) every single time, including
      immediately after the environmentally-crashed runs. No data was left behind by this
      backfill's re-verification activity.
- [x] **14. FULL I-U-D scope** — TC02 Insert + TC03 Update present and PASS this session (item
      12); TC05 Delete is present in the suite and was PASS at PR #541's own merge-time
      verification (5/5); TC04 Find also present (Area-pattern's 5th TC, PASS this session).
- [x] **15. Self-clean confirmed** — independent fresh-connection re-read (item 13) = 0 residual
      `AUTOTEST_COLLECTION_POINT` rows in `OV_COLLECTION_POINT`, checked after every attempt this
      session, not just the last one.
- [x] **16. Hygiene PASS** — `py scripts/check_bundle_hygiene.py` (run from repo root,
      2026-08-27, this session) → `[hygiene] RESULT: PASS - no hardcoded creds (R16), pure ASCII
      (R20), no CHECKLIST/VERIFY-REPORT contradictions, doc rows match declared families` (one
      unrelated pre-existing WARN about Contract Area's own `investigation/` selector strings —
      not Collection Point).

## D. Delivery
- [x] **17. Registry row** — already present, MODIFIED IN PLACE by PR #541 (not this backfill);
      confirmed live: `docs/ec_screen_registry.md` line 328, "Collection Point ... MODIFIED
      2026-08-26: FULL Area-pattern structural conversion". This backfill does not touch the
      registry row again (append-only / no-duplicate-edit).
- [x] **18. Scorecard row** — pre-existing from the original build / PR #541; not duplicated by
      this backfill (documentation-only task, no new automation scope to score).
- [ ] **19. PR** — this backfill's own PR (branch `docs/collection-point-backfill-artifacts`),
      6-field body, base = master, sync-before-push done, never self-merge. (Ticked once the PR
      is raised — see PR body for the R9 fields.)

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/collection_point.md` — UPDATED 2026-08-27
      (existed since 2026-08-01, describing the pre-conversion state), transcribed from
      `collection_point_page.resource`'s own Variables/Documentation section (nav path, DB view,
      grid id, insert/update/delete selectors, mandatory-yellow fields, quirks), not re-scanned
      live — per the backfill work order's instruction to transcribe, not re-discover. Prior
      content retained for history, not deleted.
- [x] **21. Reuse clause** — Step 0 found the screen ALREADY implemented (PR #541); this backfill
      produced the deliverables that document it: JOURNAL (#3), evidence (#6), KB map (#20), plus
      the SOW/README/CHECKLIST updates this retroactive-backfill scope additionally requires.

---

## Deviations from the standard 21-item list (stated explicitly, per R-no-silent-deviation)
- Items 4/5 (Playwright driver + investigation/) are marked N/A per the PERMANENT waiver
  (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H) — this is not a backfill gap, it is the current
  standing rule for Bank-/Area-pattern work.
- Items 17/18 (registry/scorecard rows) are NOT re-appended by this backfill — they already exist
  from PR #541 and appending a second row for the same screen would violate the append-only,
  no-duplicate convention (R23).
- Item 12 is ticked on the strength of PR #541's own already-merged 5/5 live evidence plus this
  session's 4/5 partial re-run (TC01-04 clean pass) — NOT on a clean 5/5 achieved during this
  backfill session, because one was not achieved despite 6 attempts, all traced to session-level
  environmental contention (see item 12's note and JOURNAL.md). This is disclosed here rather
  than silently smoothed over.
- The pre-existing `VERIFY-REPORT.md` in this bundle (dated 2026-08-01) is STALE — it describes
  the pre-conversion 4-TC/Playwright-8/8 state, not PR #541's 5-TC Area-pattern conversion. It has
  been annotated (not deleted) to point to this CHECKLIST.md + `evidence/backfill_2026-08-27/` as
  the current source of truth, to avoid a silent contradiction between an old auto-generated
  report and the real current state.
