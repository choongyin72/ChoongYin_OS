# IUD Task — Deliverable Checklist — Price Object (CO.3016)

_Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md`. This is a **documentation/evidence backfill**
(`docs/lean-deliverable-backfill-workorder.md`, owner decision 2026-08-27, Section H) around
already-merged, already-live-tested RF automation (PR #536, merged 2026-08-26). No RF file
(`price_object_page.resource`, `price_object_iud.robot`, `testdata/price_object_*.properties`) was
modified to produce this checklist. Items 4/5 (Playwright driver + investigation/) stay permanently
waived per Section H — the pre-existing Playwright bundle from the screen's original 2026-08-03 build is
kept in this bundle unchanged, not rebuilt._

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/price_object.md` already existed before this backfill (from the
      2026-08-03 build) — refreshed in this PR to reflect the PR #536 Area-pattern conversion. Selectors
      transcribed from `price_object_page.resource`'s own Variables section, not re-scanned live.
- [x] **0b.** `grep -ril price_object workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}`
      (filtering out `product_price_object` hits) → existing impl found:
      `pageobjects/Configuration/Assets/Sales_Objects/price_object_page.resource`,
      `tests/Configuration/Assets/Sales_Objects/price_object_iud.robot`, `py/price_object_iud.py`,
      `screens/Configuration/Assets/Sales_Objects/Price_Object/` (SOW/README/JOURNAL/CHECKLIST/
      VERIFY-REPORT/evidence/investigation pre-existed from the 2026-08-03 build). REUSED/EXTENDED — no
      parallel copy built, and confirmed distinct from "Product Price Object" (CD.0011, PR #502).
- [x] **0c.** Shared engine reused: RF suite calls the shared T2 `resources/manage_object.resource`
      (`Insert/Update/Verify Object *`, `Apply Navigator From Properties`) + `libraries/DbVerify.py`
      for this backfill's own evidence-capture DB reads. No new plumbing added.

## A. Bundle artifacts — `screens/Configuration/Assets/Sales_Objects/Price_Object/`
- [x] **1. `price_object_sow.md`** — updated with the current Area-pattern nav/grid/cell shape, test
      data, and the dev story pulled from PR #536's body (including the real Business Unit gotcha),
      layered on top of the original 2026-08-03 build's own dev story.
- [x] **2. `README.md`** — updated with the bundle overview + exact run commands (dryrun/live/DB
      self-clean pattern), disambiguated from Product Price Object.
- [x] **3. `JOURNAL.md`** — updated: PR #536's Built/Done well/Done wrong-or-lessons/Blockers→resolution/
      Decisions/Evidence sections added, pulled from the PR body + this session's own live-run evidence;
      the original 2026-08-03 entry is kept unchanged above it.
- [ ] **4. Playwright driver** — N/A. Playwright bundle waived, owner decision 2026-08-27 (Section H of
      `docs/IUD-DELIVERABLE-CHECKLIST.md`); the pre-existing `py/price_object_iud.py` from the 2026-08-03
      build is kept unchanged, not rebuilt.
- [ ] **5. `investigation/`** — N/A, same waiver as item 4; the pre-existing
      `investigation/gen_ovgm_config.json` from the 2026-08-03 build is kept unchanged.
- [x] **6. `evidence/`** — captured in this session: `log.html`, `output.xml`, `report.html` from a live
      5/5 RF run (2026-08-27), alongside the pre-existing 2026-08-03 Playwright evidence
      (`po_0[1-5]_*.png`, unchanged).
- [x] **7. `CHECKLIST.md`** — this file.

## B. RF files — treeview-mirrored (pre-existing, unmodified by this backfill)
- [x] **8. T3 page object** `pageobjects/Configuration/Assets/Sales_Objects/price_object_page.resource`
      — pre-existing, merged in PR #536 (Area-pattern conversion), not touched by this backfill.
- [x] **9. Suite** `tests/Configuration/Assets/Sales_Objects/price_object_iud.robot` — pre-existing,
      merged in PR #536, not touched by this backfill.

## C. Verification gates (re-run for evidence, not re-verification of a defect)
- [x] **10. robocop clean** — `py -m robocop check pageobjects/.../price_object_page.resource
      tests/.../price_object_iud.robot` (this session, 2026-08-27) → **7 issues** (DOC02 missing
      `[Documentation]` on TC03-05) — matches PR #536's own cited parity with Area's baseline (7
      DOC02-only issues both sides). No drift, no new issue category.
- [x] **11. `--dryrun` N/N PASS** — `robot --dryrun tests/Configuration/Assets/Sales_Objects/
      price_object_iud.robot` (this session) → **5/5 PASS**.
- [x] **12. LIVE headless run N/N PASS** — `EC_HEADLESS=true robot --outputdir
      screens/Configuration/Assets/Sales_Objects/Price_Object/evidence tests/.../price_object_iud.robot`
      (this session) → **5/5 PASS** clean, first attempt (no flake). `tasklist` checked for stray
      chrome processes before the run per this backfill's own instruction; several pre-existing stray
      `chrome-headless-shell.exe` processes were present, unrelated to this suite, not interfering.
- [x] **13. DB ground-truth** — `libraries.DbVerify.fetch_object("OV_PRICE_OBJECT",
      "AUTOTEST_PRICE_OBJECT")` → `None` (absent) verified via a fresh oracledb connection after the
      live run in this session.
- [x] **14. FULL I-U-D scope** — TC02 Insert / TC03 Update / TC05 Delete all present and passing (plus
      TC01 Clean State, TC04 Find) — confirmed by reading `price_object_iud.robot`'s 5 test cases.
- [x] **15. Self-clean confirmed** — independent DB re-read (fresh connection, this session) = 0
      residual `AUTOTEST_PRICE_OBJECT` rows in `OV_PRICE_OBJECT` after the clean run.
- [x] **16. Hygiene PASS** — `py scripts/check_bundle_hygiene.py` (repo root, this session) →
      `[hygiene] RESULT: PASS - no hardcoded creds (R16), pure ASCII (R20), no CHECKLIST/VERIFY-REPORT
      contradictions, doc rows match declared families` (167 bundles + 271 recon scripts scanned; the
      one WARN reported belongs to Contract Area's `investigation/`, unrelated to this screen).

## D. Delivery
- [ ] **17. Registry row** — N/A for this backfill. Price Object's row in
      `workstreams/master-plan/ec-automation/docs/ec_screen_registry.md` (line 342) already exists and
      already documents the PR #536 conversion (edited in place at merge time of that PR, not this
      backfill).
- [ ] **18. Scorecard row** — N/A for this backfill, same reasoning as item 17 —
      `docs/automation-scorecard.md`'s Price Object row already reflects the merged conversion.
- [x] **19. PR** — this backfill's own PR, with the standard body (What was backfilled / Files added /
      Base branch = master); never self-merged.

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/price_object.md` — refreshed in this backfill:
      nav path, DB view, grid id, insert/update/delete selectors (transcribed from
      `price_object_page.resource`'s Variables section), mandatory-yellow fields, quirks (including the
      real "EC LNG Norway" vs "Royalty Canada" gotcha), last-verified date 2026-08-26/27.
- [x] **21. Reuse clause.** Step 0 found Price Object's RF automation ALREADY implemented and merged —
      this backfill produces exactly the deliverables the reuse clause requires: #3 JOURNAL, #6 evidence,
      #20 KB map (plus #1/#2/#7 restored per Section H).
