# Canal - IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md)

_Refreshed 2026-08-28 (Batch 9 backfill). Section H (2026-08-27) retired the lean waiver that let
PR #458 (2026-08-23) skip items 1/3/6/7/20 — this checklist restores them with real evidence.
Items 4/5 (Playwright driver + investigation/) stay waived permanently per Section H (Universal
Screen Engine is the replacement) — marked N/A below, not built new._

## Step 0 - check-existing gate
- [x] 0a. `ec-ui-knowledge/screens/canal.md` already existed from the 2026-07-26 original build
      (described the old 4-TC argument-driven shape) — refreshed in place (item 20 below) to
      describe the current Bank-pattern (PR #458) shape, not duplicated.
- [x] 0b. `grep -ril canal workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}`
      -> existing impl found: `pageobjects/.../canal_page.resource`,
      `tests/.../canal_iud.robot`, `py/canal_iud.py` (Playwright, pre-existing, unchanged),
      `screens/.../Canal/` (this bundle, pre-existing from 2026-07-26, refreshed not duplicated).
- [x] 0c. Reused the shared engine/T2/T1 — zero shared-file (`manage_object.resource`/
      `common.resource`) changes needed for PR #458's conversion; this backfill made none either.

## A. Bundle artifacts - `screens/Configuration/Assets/Transport_Objects/Canal/`
- [x] 1. `canal_sow.md` - refreshed 2026-08-28 to describe the CURRENT (Bank-pattern, PR #458)
      shape; classification/mandatory fields/dev story pulled from PR #458's real body + the
      screen's actual `canal_page.resource`.
- [x] 2. `README.md` - refreshed with exact dryrun/live/robocop/hygiene/DB-self-clean commands.
- [x] 3. `JOURNAL.md` - refreshed; both the 2026-07-26 original build and the 2026-08-23 PR #458
      conversion documented with real content (Built/Done well/Done wrong/Blockers/Decisions/
      Evidence), plus this backfill's own 2026-08-28 entry.
- [x] 4. Playwright driver - **waived permanently** (Section H) - `py/canal_iud.py` pre-exists,
      unchanged, not rebuilt.
- [x] 5. `investigation/` - **waived permanently** (Section H) - pre-existing `recon.py` kept as
      historical artifact, not extended; no new recon script required.
- [x] 6. `evidence/` - fresh run captured 2026-08-28: `evidence/rf_batch9_2026-08-28/`
      (`dryrun_output.xml`, `output.xml`, `log.html`, `report.html`, all <400KB). Pre-existing
      `canal_0[1-5]_*.png`/`rf_report.html` (2026-07-26, pre-conversion) kept for history.
- [x] 7. `CHECKLIST.md` - this file, refreshed and ticked with real evidence below.

## B. RF files - treeview-mirrored (UNCHANGED by this backfill)
- [x] 8. T3 `pageobjects/Configuration/Assets/Transport_Objects/canal_page.resource` -
      pre-existing (PR #458), label-driven, explicit grid-filter wiring. Not modified.
- [x] 9. Suite `tests/Configuration/Assets/Transport_Objects/canal_iud.robot` - pre-existing
      (PR #458), 5-TC Bank shape. Not modified.

## C. Verification gates (re-run live for this backfill, 2026-08-28 - not hand-typed)
- [x] 10. robocop clean (baseline) - `robocop check pageobjects/.../canal_page.resource
      tests/.../canal_iud.robot` -> 9 issues, all DOC02/style baseline (same category/count PR
      #458 cited as matching Bank's own accepted baseline - no new categories).
- [x] 11. `--dryrun` N/N PASS - `robot --dryrun tests/.../canal_iud.robot` -> **5/5 PASS**.
- [x] 12. LIVE headless run N/N PASS - `EC_HEADLESS=true robot tests/.../canal_iud.robot` ->
      **5/5 PASS**, first attempt, no retry needed.
- [x] 13. DB ground-truth - fresh `oracledb` connection (2026-08-28, this backfill's own check):
      `SELECT CODE FROM OV_CANAL` -> `[SUEZ, PANAMA]` only; `CANAL_KIEL` absent both before and
      after the run. Suite's own in-run assertion: `Code Should Be Absent In View OV_CANAL
      CANAL_KIEL` (T2 `Verify Object Removed`, TC05).
- [x] 14. FULL I-U-D scope - TC02 Insert / TC03 Update / TC05 Delete all present and passing
      (plus TC01 clean-state, TC04 find).
- [x] 15. Self-clean confirmed - independent fresh-connection DB re-read (above) = 0 residual
      `CANAL_KIEL` rows; pre-existing `SUEZ`/`PANAMA` rows verified intact/unaffected.
- [x] 16. Hygiene PASS - `py scripts/check_bundle_hygiene.py` (from repo root) -> exit 0, RESULT:
      PASS (no hardcoded creds, pure ASCII, no CHECKLIST/VERIFY-REPORT contradiction).

## D. Delivery
- [x] 17. Registry row - already present, `docs/ec_screen_registry.md` Canal row (cites PR #458,
      Batch 7, full Bank-pattern). Not re-appended (already correct).
- [x] 18. Scorecard row - already present, `docs/automation-scorecard.md` (updated by PR #458).
      Not re-appended (already correct).
- [x] 19. PR - this backfill's own PR, docs-only, standard 6-field body, base = master, never
      self-merged.

## E. Knowledge base
- [x] 20. KB selector map `ec-ui-knowledge/screens/canal.md` - **refreshed** (pre-existed from
      2026-07-26, described the old 4-TC shape); selectors re-transcribed from the CURRENT
      `canal_page.resource`'s own Variables section, not re-discovered live.
- [x] 21. Reuse clause - this screen's Step 0 found an EXISTING bundle (predating the lean rule);
      per the reuse clause, JOURNAL + evidence + KB map were all refreshed/produced, not just
      green tests alone.
