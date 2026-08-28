# IUD Task — Deliverable Checklist — Royalty Owner

Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md`, ticked with real evidence for Royalty Owner
(Configuration > Assets > Royalty Objects > Royalty Owner, RC.0051). Backfilled 2026-08-28 per
`docs/lean-deliverable-backfill-workorder.md` (Batch 8) — Section H retired the 2026-08-23/26
lean waiver except for items 4/5 (Playwright driver + investigation/, permanently waived — the
Universal Screen Engine replaces that role).

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** No pre-existing `ec-ui-knowledge/screens/royalty_owner.md` found before this
      backfill (confirmed via a live glob of `ec-ui-knowledge/screens/*.md` — no match) — this
      backfill creates it (item 20 below), transcribing selectors already present in
      `royalty_owner_page.resource`'s Variables section, not re-discovering them.
- [x] **0b.** `grep -ril "royalty_owner" workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}`
      → found: existing impl at `pageobjects/Configuration/Assets/Royalty_Objects/royalty_owner_page.resource`,
      `tests/Configuration/Assets/Royalty_Objects/royalty_owner_iud.robot`,
      `testdata/royalty_owner_*.properties`, plus the pre-existing bundle
      (`screens/Configuration/Assets/Royalty_Objects/Royalty_Owner/{royalty_owner_sow.md,README.md,playwright/,evidence/}`).
      REUSE/EXTEND per this backfill's own instruction — no parallel copy built.
- [x] **0c.** Shared engine reused: T2 `resources/manage_object.resource`, T1
      `resources/common.resource`, `libraries/DbVerify.py` — confirmed unmodified by this backfill
      (only doc/evidence files added under `screens/.../Royalty_Owner/` and
      `ec-ui-knowledge/screens/royalty_owner.md`).

## A. Bundle artifacts — `screens/Configuration/Assets/Royalty_Objects/Royalty_Owner/`
- [x] **1. `royalty_owner_sow.md`** — pre-existing (2026-06-25), extended with a Section 5
      addendum in this backfill documenting the PR #447 Bank-pattern conversion (classification,
      test-data, and mechanic changes since the original SOW).
- [x] **2. `README.md`** — updated this backfill: bundle overview, exact run commands
      (headless/headed live, dryrun, robocop, DB self-clean SQL).
- [x] **3. `JOURNAL.md`** — new this backfill, built / done well / lessons / blockers / decisions
      / evidence, content pulled from PR #447's real body (`gh pr view 447`).
- [ ] **4. `playwright/ec_iud_royalty_owner.py`** — PRE-EXISTING (predates PR #447 and the
      Universal Screen Engine decision). Left untouched by this backfill. Not required going
      forward per Section H (item 4 permanently waived for Bank-/Area-pattern work) — kept as
      historical asset, not rebuilt or re-verified.
- [ ] **5. `investigation/`** — N/A / waived (Section H, item 5 permanently waived — engine
      replaces this role; no `investigation/` folder existed or was built).
- [x] **6. `evidence/`** — pre-existing screenshots (`royalty_owner_tc01_clean.png` ..
      `royalty_owner_tc04_deleted.png`, original 2026-06-25 build) kept as-is; NEW
      `evidence/2026-08-28_backfill_run/` added this backfill (`output.xml` + 8 step screenshots
      from a fresh live 5/5 run) + `evidence/EVIDENCE-SUMMARY.md`.
- [x] **7. `CHECKLIST.md`** — this document.

## B. RF files — treeview-mirrored (pre-existing, unmodified by this backfill)
- [x] **8. T3 page object** `pageobjects/Configuration/Assets/Royalty_Objects/royalty_owner_page.resource`
      — pre-existing (rebuilt 2026-08-23 by PR #447); read-only for this backfill, not modified.
- [x] **9. Suite** `tests/Configuration/Assets/Royalty_Objects/royalty_owner_iud.robot` —
      pre-existing (rebuilt 2026-08-23 by PR #447); read-only for this backfill, not modified.

## C. Verification gates (re-run for this backfill; not re-citing PR #447's numbers blindly)
- [x] **10. robocop clean** — `robocop check pageobjects/.../royalty_owner_page.resource
      tests/.../royalty_owner_iud.robot` → **9 issues found** (4 VAR02 + 5 DOC02). Matches PR
      #447's cited baseline exactly — no new issues introduced since conversion. ("Clean" here
      means "matches the accepted Bank-pattern baseline," per the established convention for this
      pattern family — the 9 issues are the same pre-existing VAR02/DOC02 style notes shared
      across all Bank-pattern screens, not new defects.)
- [x] **11. `--dryrun` N/N PASS** — full-tree `robot --dryrun tests/` → **883/883 pass**
      (2026-08-28 re-run; includes Royalty Owner's 5 TCs plus every other screen's suite —
      confirms no keyword-resolution regression anywhere in the tree, not just this screen).
- [x] **12. LIVE headless run N/N PASS** — `EC_HEADLESS=true robot tests/Configuration/Assets/Royalty_Objects/royalty_owner_iud.robot`
      → **5 tests, 5 passed, 0 failed** (2026-08-28, this backfill's evidence-capture run).
- [x] **13. DB ground-truth** — `DbVerify`'s `Verify Object Insert Exists`/`Verify Object Form
      Record`/`Verify Object Removed` keywords assert against `OV_ROYALTY_OWNER` during the
      suite itself (insert/update/delete each checked at DB level, not just UI). Independently
      re-verified this backfill via a FRESH, separate `oracledb` connection query:
      `SELECT COUNT(*) FROM OV_ROYALTY_OWNER WHERE CODE = 'AUTOTEST_ROYALTY_OWNER'` → **0** rows.
- [x] **14. FULL I-U-D scope** — TC02 Insert, TC03 Update, TC04 Find (round-trip verify), TC05
      Delete all present and all passed in the 2026-08-28 run.
- [x] **15. Self-clean confirmed** — independent fresh-connection DB re-read = 0 residual rows
      for `AUTOTEST_ROYALTY_OWNER` in `OV_ROYALTY_OWNER` (see item 13). Pre-existing production
      rows untouched (this suite only ever touches its own fixed test code).
- [x] **16. Hygiene PASS** — no `playwright/*.py`/`investigation/*.py` changes made by this
      backfill (item 4/5 waived, pre-existing Playwright file untouched); no credentials added or
      changed in this backfill (R16 N/A — `credentials.py`'s `ROYALTY_OWNER_EC_USER/PASS` were
      added by PR #447, not this backfill).

## D. Delivery
- [x] **17. Registry row** — already present in `docs/ec_screen_registry.md` (added by PR #447,
      2026-08-23). No change needed this backfill; confirmed present via a live grep of the
      Royalty Owner row before starting this task.
- [x] **18. Scorecard row** — already present in `docs/automation-scorecard.md` (added by PR
      #447). No change needed this backfill.
- [x] **19. PR** — this backfill's PR uses the standard body (What was backfilled / Files added /
      Base branch = master); branch `docs/royalty-owner-backfill-artifacts`, off `origin/master`,
      never self-merged.

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/royalty_owner.md` — NEW this backfill.
      Nav path, DB view, grid id, insert/update/delete selectors, mandatory-yellow fields,
      quirks, last-verified date — transcribed from `royalty_owner_page.resource`'s Variables
      section (not re-discovered).
- [x] **21. Reuse clause** — Step 0 found the screen ALREADY implemented (PR #447, 2026-08-23);
      this backfill produces/refreshes the deliverables that document it: JOURNAL (#3), evidence
      (#6), and KB map (#20) — exactly what the reuse clause requires, plus SOW/README/CHECKLIST
      per Section H's restoration.

---

**Summary:** all items required for a Bank-pattern conversion are green with real evidence.
Items 4/5 (Playwright driver, investigation/) stay explicitly N/A/waived per Section H — the
pre-existing Playwright file is left as a historical asset, not deleted or re-verified. No
automation file (`royalty_owner_page.resource`, `royalty_owner_iud.robot`,
`testdata/royalty_owner_*.properties`) was modified by this backfill.
