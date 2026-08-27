# IUD Task — Deliverable Checklist — Chemical Stream (CO.0258)

_Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md`. This is a **documentation/evidence backfill**
(`docs/lean-deliverable-backfill-workorder.md`, owner decision 2026-08-27, Section H) around
already-merged, already-live-tested RF automation — the Area-pattern conversion in PR #545 (merged
2026-08-26). No RF file (`chemical_stream_page.resource`, `chemical_stream_iud.robot`,
`testdata/chemical_stream_*.properties`) was modified to produce this checklist. Items 4/5
(Playwright driver + `investigation/`) stay permanently waived per Section H — the pre-existing
Playwright bundle from the screen's original 2026-07-30 build is kept in this bundle unchanged,
not rebuilt. This file SUPERSEDES the pre-existing `CHECKLIST.md`, which described the
pre-conversion 4-TC/Playwright-8/8 state._

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/chemical_stream.md` already existed (from the 2026-07-30
      build, last corrected 2026-08-16) — updated in this PR (see item 20) to describe the current
      post-PR-#545 Area-pattern RF shape, not re-scanned live from scratch.
- [x] **0b.** `grep -rli chemical_stream workstreams/master-plan/ec-automation --include="*.robot"
      --include="*.resource" --include="*.py"` (excluding `chemical_stream_hookup`/`chemical_tank`
      matches) → existing impl found: `pageobjects/Configuration/Assets/Chemical_Objects/
      chemical_stream_page.resource`, `tests/Configuration/Assets/Chemical_Objects/
      chemical_stream_iud.robot`, `py/chemical_stream_iud.py`,
      `screens/Configuration/Assets/Chemical_Objects/Chemical_Stream/` (SOW/README/JOURNAL/
      CHECKLIST/VERIFY-REPORT/evidence/investigation pre-existed from the 2026-07-30 build).
      REUSED/EXTENDED — no parallel copy built.
- [x] **0c.** Shared engine reused: RF suite calls the shared T2 `resources/manage_object.resource`
      (`Apply Navigator From Properties`, `Insert/Update/Verify Object *`) + `libraries/DbVerify.py`
      for this backfill's own evidence-capture DB reads (via new `investigation/
      check_autotest_residual.py`). No new plumbing added.

## A. Bundle artifacts — `screens/Configuration/Assets/Chemical_Objects/Chemical_Stream/`
- [x] **1. `chemical_stream_sow.md`** — updated (Addendum 2026-08-27) with the current OV-GM
      classification, the genuine 3-level Production Unit → Area → Facility Class 1 navigator
      cascade, the mandatory From Connection popup mechanism (preserved unchanged), test data used,
      and the dev story pulled from PR #545's real body.
- [x] **2. `README.md`** — updated with the post-PR-#545 bundle overview + exact run commands
      (dryrun, live headless run, DB self-clean check via new `investigation/
      check_autotest_residual.py`).
- [x] **3. `JOURNAL.md`** — appended (dated 2026-08-26 entry, Built/Done well/Done wrong-or-lessons/
      Blockers→resolution/Decisions/Evidence), pulled from PR #545's real body + this session's own
      live-run evidence. Prior 2026-07-30/2026-08-16 entries left untouched.
- [ ] **4. Playwright driver** — N/A. Playwright bundle waived, owner decision 2026-08-27 (Section H
      of `docs/IUD-DELIVERABLE-CHECKLIST.md`); the pre-existing `py/chemical_stream_iud.py` from the
      2026-07-30 build is kept unchanged, not rebuilt.
- [ ] **5. `investigation/`** — mostly N/A per the same Section H waiver; the pre-existing recon
      scripts (`recon.py`, `recon_chs_popup*.py`, `chs_find_real_code.py`, `chs_structural_recon.py`,
      `chs_pacing_sweep.py`, `chs_modal_repro.py`) are kept unchanged. One new, additive script was
      added for this backfill's own evidence capture: `check_autotest_residual.py` (self-clean
      re-check, not a re-investigation of the screen).
- [x] **6. `evidence/`** — captured in this session: `evidence/2026-08-27_area_pattern_backfill/`
      (`log.html`, `output.xml`, `report.html`, `playwright-log.txt`, per-TC screenshots from a live
      5/5 RF run against the CURRENT converted suite, `robocop_output.txt`), alongside the
      pre-existing 2026-07-30 evidence (`chs_0[1-5]_*.png`, `chs_insert_ui_FAIL.png`, `results.json`
      — kept unchanged, predates the conversion).
- [x] **7. `CHECKLIST.md`** — this file (rewritten; the pre-existing version described the
      pre-conversion 4-TC/Playwright-8/8 state and is superseded by this update).

## B. RF files — treeview-mirrored (pre-existing, unmodified by this backfill)
- [x] **8. T3 page object**
      `pageobjects/Configuration/Assets/Chemical_Objects/chemical_stream_page.resource` —
      pre-existing, converted to the Area pattern in PR #545 (merged 2026-08-26), not touched by
      this backfill.
- [x] **9. Suite** `tests/Configuration/Assets/Chemical_Objects/chemical_stream_iud.robot` —
      pre-existing, converted in PR #545, not touched by this backfill.

## C. Verification gates (re-run for evidence, not re-verification of a defect)
- [x] **10. robocop clean** — `py -m robocop check pageobjects/.../chemical_stream_page.resource
      tests/.../chemical_stream_iud.robot` (this session, 2026-08-27) → **7 issues** (VAR02 x2 +
      DOC02 x5) — same shape (kind/count of finding categories) as Area's own current baseline and
      Chemical Stream Hookup's; PR #545 cited 10 issues at its own merge time, this session
      re-measured 7 on the identical two files — a robocop/config-drift difference across sessions,
      not a new finding category or a regression introduced by this backfill (no RF file touched).
- [x] **11. `--dryrun` N/N PASS** — `robot --dryrun
      tests/Configuration/Assets/Chemical_Objects/chemical_stream_iud.robot` (this session) →
      **5/5 PASS**. Full-tree `robot --dryrun tests/` (this session) → **883/883 PASS**, no
      collisions/regressions.
- [x] **12. LIVE headed/headless run N/N PASS** — `EC_HEADLESS=true robot --outputdir
      screens/Configuration/Assets/Chemical_Objects/Chemical_Stream/evidence/
      2026-08-27_area_pattern_backfill tests/.../chemical_stream_iud.robot` (this session) →
      **5/5 PASS**, first attempt, no flake.
- [x] **13. DB ground-truth** — `investigation/check_autotest_residual.py`
      (`SELECT CODE FROM OV_CHEM_STREAM WHERE CODE LIKE 'AUTOTEST%'`) → `[]` (0 residual rows),
      verified via a fresh oracledb connection both before and after the live run in this session.
- [x] **14. FULL I-U-D scope** — TC02 Insert / TC03 Update / TC05 Delete all present and passing
      (plus TC01 Verify Clean State, TC04 Find) — confirmed by reading `chemical_stream_iud.robot`'s
      5 test cases and by this session's own live 5/5 run.
- [x] **15. Self-clean confirmed** — independent DB re-read (fresh connection, this session) = 0
      residual `AUTOTEST%` rows in `OV_CHEM_STREAM` after the live run.
- [x] **16. Hygiene PASS** — `py scripts/check_bundle_hygiene.py` (repo root, this session) →
      `[hygiene] RESULT: PASS - no hardcoded creds (R16), pure ASCII (R20), no CHECKLIST/
      VERIFY-REPORT contradictions, doc rows match declared families` (167 bundles + 271 recon
      scripts scanned; the one WARN in the output is a pre-existing, unrelated Contract Area recon
      script, not this screen).

## D. Delivery
- [ ] **17. Registry row** — N/A for this backfill. Chemical Stream's row in
      `docs/ec_screen_registry.md` already exists and already documents the PR #545 conversion
      (append-only edit made at merge time of that PR, not this backfill).
- [ ] **18. Scorecard row** — N/A for this backfill, same reasoning as item 17 —
      `docs/automation-scorecard.md`'s Chemical Stream row already reflects the merged conversion.
- [x] **19. PR** — this backfill's own PR, with the standard body (What was backfilled / Files
      added / Base branch = master); never self-merged.

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/chemical_stream.md` — updated in this
      backfill: the Automation section now describes the current post-PR-#545 shape (5 TCs, per-TC
      login, shared T2 `Apply Navigator From Properties`, properties-file-driven testdata), the
      From Connection popup mechanism (unchanged), mandatory-yellow fields, quirks, last-verified
      date updated to 2026-08-27.
- [x] **21. Reuse clause.** Step 0 found Chemical Stream's RF automation ALREADY implemented,
      converted, and merged — this backfill produces exactly the deliverables the reuse clause
      requires: #1/#2/#3 refreshed, #6 fresh evidence, #7 rewritten CHECKLIST, #20 KB map updated.
