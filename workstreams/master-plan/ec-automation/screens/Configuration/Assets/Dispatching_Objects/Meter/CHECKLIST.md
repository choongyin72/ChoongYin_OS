# IUD Task — Deliverable Checklist — Meter

_Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md`. Backfill (2026-08-27, Batch 3,
`docs/lean-deliverable-backfill-workorder.md`) for a screen already converted to the Area pattern
(PR #554, merged 2026-08-26). Items 4/5 (Playwright driver + investigation/) stay waived per
Section H — the Universal Screen Engine replaces that role. RF automation was NOT rebuilt or
re-verified from scratch for this backfill; the evidence below is a fresh re-run of the
already-proven suite plus real-fact citations pulled from PR #554._

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/meter.md` did not exist before this backfill — created as
      part of item 20 below (KB map was one of the items this backfill restores).
- [x] **0b.** `grep -ril meter_page.resource workstreams/master-plan/ec-automation` → found at
      `pageobjects/Configuration/Assets/Dispatching_Objects/meter_page.resource` (existing impl,
      reused/documented, not rebuilt).
- [x] **0c.** Confirmed the screen uses the shared T2 engine (`resources/manage_object.resource`'s
      `Apply Navigator From Properties`, `Insert/Update Object From Properties`, etc.) and the
      generic T1 popup gesture (`resources/popup.resource`'s `Pick From EC Object Popup`) — no new
      plumbing, per PR #554's own body.

## A. Bundle artifacts — `screens/Configuration/Assets/Dispatching_Objects/Meter/`
- [x] **1. `meter_sow.md`** — classification, nav/grid/cell shape, test data, dev story, lessons
      (including the wrong-then-corrected classification).
- [x] **2. `README.md`** — bundle overview + exact run commands.
- [x] **3. `JOURNAL.md`** — built/done-well/done-wrong/blockers/decisions/evidence, modeled on
      Bank's JOURNAL.md, pulled from PR #554's real body + the registry row's detailed narrative.
- [ ] **4. Playwright driver** — WAIVED (Section H, owner decision 2026-08-27) — Universal Screen
      Engine replaces this role; not built.
- [ ] **5. `investigation/`** — WAIVED (Section H) — same reason as item 4.
- [x] **6. `evidence/`** — step screenshots + `output.xml`/`log.html`/`report.html`/
      `results-summary.md` from a real live run captured 2026-08-27.
- [x] **7. `CHECKLIST.md`** — this file.

## B. RF files — treeview-mirrored (pre-existing, unchanged by this backfill)
- [x] **8. T3 page object** `pageobjects/Configuration/Assets/Dispatching_Objects/meter_page.resource`
      (pre-existing, PR #554; locators in Variables, docstring matches — confirmed by reading it
      for this backfill).
- [x] **9. Suite** `tests/Configuration/Assets/Dispatching_Objects/meter_iud.robot` (pre-existing,
      PR #554; 5-TC clean→insert→update→find→delete structure).

## C. Verification gates (fresh evidence captured 2026-08-27 for this backfill)
- [x] **10. robocop clean/parity** — `py -m robocop check meter_page.resource meter_iud.robot` =
      7 issues (2 VAR02 + 5 DOC02), exact parity with `area_page.resource`/`area_iud.robot`'s own
      7-issue baseline (re-run 2026-08-27, matches PR #554's original citation).
- [x] **11. `--dryrun` N/N PASS** — screen suite 5/5 pass; full `tests/` tree 883/883 pass
      (`results/meter_backfill_dryrun*`, re-run 2026-08-27).
- [x] **12. LIVE headless run N/N PASS** — 5/5 pass, `results/meter_backfill_live/`
      (`EC_HEADLESS=true`, re-run 2026-08-27; two earlier attempts hit a transient stray-Chrome
      Browser-library flake, resolved by killing stale `chrome-headless-shell.exe` processes and
      re-running — see `evidence/results-summary.md`).
- [x] **13. DB ground-truth** — `SELECT COUNT(*) FROM OV_METER WHERE CODE LIKE 'AUTOTEST_METER%'`
      = 0 before insert / present during the run / 0 after delete, via `Verify Object Removed`
      (T2, `libraries/DbVerify.py`) inside TC05, and independently re-checked via a fresh
      `oracledb` connection after the run (`Workplaces/meter-backfill/check_selfclean.py`, output:
      "OV_METER AUTOTEST_METER% residual count (fresh connection): 0").
- [x] **14. FULL I-U-D scope** — Insert (TC02) + Update (TC03) + Delete (TC05) all present and
      passing.
- [x] **15. Self-clean confirmed** — 0 residual `AUTOTEST_METER%` rows via fresh connection
      (2026-08-27 re-run); no pre-existing rows touched.
- [x] **16. Hygiene PASS** — `py scripts/check_bundle_hygiene.py` → "RESULT: PASS - no hardcoded
      creds (R16), pure ASCII (R20), no CHECKLIST/VERIFY-REPORT contradictions, doc rows match
      declared families" (re-run 2026-08-27; the one WARN it emits concerns an unrelated screen,
      Contract Area's `investigation/` recon script, not Meter).

## D. Delivery
- [x] **17. Registry row** — already present (starred ⭐, `docs/ec_screen_registry.md` line 89),
      appended by PR #554; this backfill did not modify it.
- [x] **18. Scorecard row** — already present (`docs/automation-scorecard.md`, "Dispatching
      Objects — slice 2" row), appended by PR #554; this backfill did not modify it.
- [x] **19. PR** — this backfill's own PR follows the standard 6-field body (What/Files/DB
      ground-truth/Self-clean/Rules applied/Base branch=master); never self-merged.

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/meter.md` — created by this backfill (did
      not exist before), transcribed from `meter_page.resource`'s own Variables section and
      `docs/meter_popup_notes.md`.
- [x] **21. Reuse clause** — Step 0 found the screen already implemented (PR #554); this backfill
      produces the JOURNAL, evidence, and KB map that a reuse run still requires, per this item's
      own rule.

**OVERALL: PASS** — all non-waived items (1,2,3,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21)
backed by real evidence cited above; items 4/5 explicitly waived per Section H.
