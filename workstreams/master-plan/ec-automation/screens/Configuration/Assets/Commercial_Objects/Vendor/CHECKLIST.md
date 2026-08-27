# IUD Task — Deliverable Checklist — Vendor

Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md`. This is a **backfill pass** (owner decision
2026-08-27, Section H retiring the 2026-08-23/26 lean waiver) — the RF automation itself was
built and merged in PR #439 (2026-08-23, Batch 4). Items below are ticked against real
evidence: either PR #439's own cited evidence, or a fresh re-run on 2026-08-28 (this backfill),
never a guess. Items 4/5 (Playwright driver + investigation/) stay N/A per Section H — the
Universal Screen Engine is the owner-decided replacement; not rebuilt here.

---

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/vendor.md` did not exist before this backfill — created
      now (item 20 below); confirmed via `find . -iname "vendor.md" -path "*ec-ui-knowledge*"`
      returning no hits pre-backfill.
- [x] **0b.** `grep -ril "vendor" workstreams/master-plan/ec-automation/{pageobjects,tests,testdata}`
      → found: `pageobjects/.../vendor_page.resource`, `tests/.../vendor_iud.robot`,
      `testdata/vendor_*.properties` — existing impl REUSED/EXTENDED with documentation only,
      no parallel copy built.
- [x] **0c.** N/A for this backfill — no new plumbing built; the screen already uses the shared
      T2 `resources/manage_object.resource` + T1 `resources/common.resource`.

## A. Bundle artifacts — `screens/Configuration/Assets/Commercial_Objects/Vendor/`
- [x] **1. `vendor_sow.md`** — v2.0 section added: classification (plain Bank pattern, no
      navigator), mandatory fields, test data, dev story pulled from PR #439's real body.
- [x] **2. `README.md`** — updated: bundle overview + exact dryrun/live/DB-self-clean commands.
- [x] **3. `JOURNAL.md`** — created, modeled on Bank's JOURNAL.md structure, content sourced
      from PR #439's body + this backfill's own re-run.
- [ ] **4. `playwright/ec_iud_vendor.py`** — N/A, permanently waived (Section H) — Universal
      Screen Engine replaces this role. A pre-existing, pre-conversion Playwright file exists
      in this bundle's `playwright/` folder from before PR #439; left untouched, not refreshed.
- [ ] **5. `investigation/`** — N/A, permanently waived (Section H), same reasoning as #4. A
      pre-existing `investigation/commercial_objects_recon.py` predates PR #439; left untouched.
- [x] **6. `evidence/`** — `evidence/rf_backfill_2026-08-28/output.xml` + `log.html` +
      `results-summary.txt` from a real live run on 2026-08-28 (5/5 PASS, first attempt).
- [x] **7. `CHECKLIST.md`** — this file.

## B. RF files — treeview-mirrored (pre-existing, unmodified by this backfill)
- [x] **8. T3 page object** `pageobjects/Configuration/Assets/Commercial_Objects/vendor_page.resource`
      — pre-existing (PR #439), confirmed via Read: locators in `*** Variables ***`, docstring
      matches. Not modified by this backfill.
- [x] **9. Suite** `tests/Configuration/Assets/Commercial_Objects/vendor_iud.robot` — pre-existing
      (PR #439), TC01 clean → TC02 insert → TC03 update → TC04 find → TC05 delete. Not modified.

## C. Verification gates
- [x] **10. robocop clean (parity)** — `robocop check pageobjects/.../vendor_page.resource
      tests/.../vendor_iud.robot` → **7 issues** (2 VAR02 + 5 DOC02), 2026-08-28 re-run.
      Matches PR #439's own cited baseline exactly (7 issues) — no new issue classes; not a
      fresh "clean" claim, an honest parity check against the merged baseline.
- [x] **11. `--dryrun` N/N PASS** — `robot --dryrun --outputdir C:/tmp/vendor-dryrun
      tests/Configuration/Assets/Commercial_Objects/vendor_iud.robot` → **5 tests, 5 passed,
      0 failed**, run 2026-08-28.
- [x] **12. LIVE headless run N/N PASS** — `EC_HEADLESS=true robot --outputdir
      C:/tmp/vendor-live tests/Configuration/Assets/Commercial_Objects/vendor_iud.robot` →
      **5 tests, 5 passed, 0 failed**, run 2026-08-28, first attempt (no retry needed).
- [x] **13. DB ground-truth** — fresh oracledb connection (not reused from the suite run):
      `SELECT COUNT(*) FROM OV_VENDOR WHERE CODE='AUTOTEST_VEND'` → `0` after TC05's delete,
      2026-08-28. Insert/Update/Find are covered by the suite's own in-run
      `Verify Object Insert Exists`/`Verify Object Form Record`/`Verify Object Found`
      keywords (T2, `resources/manage_object.resource`), which PASSed in the same live run.
- [x] **14. FULL I-U-D scope** — TC02 Insert, TC03 Update (Name + Description), TC05 Delete
      (End Date = Start Date) — confirmed present in `vendor_iud.robot`, not I/D-only.
- [x] **15. Self-clean confirmed** — 0 residual `AUTOTEST_VEND` rows in `OV_VENDOR` via a
      fresh connection after the 2026-08-28 live run (item 13); no pre-existing Vendor data
      touched (fixed test code confirmed absent before TC01, present only during TC02-TC04,
      absent again after TC05).
- [x] **16. Hygiene PASS** — `py scripts/check_bundle_hygiene.py` (repo root) →
      `[hygiene] RESULT: PASS - no hardcoded creds (R16), pure ASCII (R20), no CHECKLIST/
      VERIFY-REPORT contradictions, doc rows match declared families`, run 2026-08-28 (one
      unrelated WARN for a different screen — Contract_Area's recon script — not Vendor).

## D. Delivery
- [x] **17. Registry row** — already present in `docs/ec_screen_registry.md` (added by PR
      #439, 2026-08-23; confirmed via grep, not re-appended by this backfill since it already
      exists and append-only means no duplicate row should be added).
- [x] **18. Scorecard row** — already present in `docs/automation-scorecard.md` (added by PR
      #439, per the PR's own file list; not re-appended for the same reason as #17).
- [x] **19. PR** — this backfill's own PR (docs/vendor-backfill-artifacts branch), 6-field
      body (What/Files/DB evidence/Self-clean/Rules applied/Base branch=master), never
      self-merged.

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/vendor.md` — created this backfill,
      pulled from `vendor_page.resource`'s `*** Variables ***` section (nav path, DB view,
      grid id, insert/update/delete selectors, mandatory-yellow fields, quirks, last-verified
      2026-08-28).
- [x] **21. Reuse clause** — Step 0 found the screen ALREADY implemented (PR #439); this
      backfill produces exactly the deliverables the reuse clause requires: JOURNAL (#3),
      evidence (#6), KB map (#20) — plus SOW/README/CHECKLIST per Section H's restored scope.

---

**Overall: all applicable items (0, 1-3, 6-21) ticked with real, cited evidence. Items 4-5
are N/A per Section H's permanent Playwright waiver — not silently skipped, explicitly
recorded as waived with the reason.**
