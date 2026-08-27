# Production Separator - IUD Deliverable Checklist (vs `docs/IUD-DELIVERABLE-CHECKLIST.md`, Section H)

_Backfilled 2026-08-27 (`docs/lean-deliverable-backfill-workorder.md`, Batch 2) for the Area-pattern
conversion in PR #551 (merged 2026-08-26). Items 4/5 (Playwright driver + investigation/) stay
waived per Section H — the pre-existing driver is unchanged and not rebuilt. This replaces the
prior checklist, which described the pre-conversion 2026-07-30 build only._

## Step 0 — check-existing gate
- [x] 0a. `ec-ui-knowledge/screens/production_separator.md` did not exist before this backfill —
      created as part of this task (item 20 below).
- [x] 0b. `grep -ril "production_separator" workstreams/master-plan/ec-automation/{py,pageobjects,
      tests,screens}` -> found: `py/production_separator_iud.py`,
      `pageobjects/.../production_separator_page.resource`,
      `tests/.../production_separator_iud.robot`, `screens/.../Production_Separator/`. REUSED/
      EXTENDED (PR #551 converted the existing RF; this backfill adds docs only) — no parallel copy.
- [x] 0c. Shared engine reused: `resources/manage_object.resource` (T2, `Apply Navigator From
      Properties`, `Insert/Update/Verify Object *`), `libraries/DbVerify.py` (single DB-verify),
      `libraries/PropertiesReader.py`. No new plumbing added.

## A. Bundle artifacts — `screens/Configuration/Assets/Facility_Objects/Production_Separator/`
- [x] 1. `production_separator_sow.md` — rewritten this backfill to reflect the Area-pattern shape
      (was still describing the pre-conversion 4-TC shape).
- [x] 2. `README.md` — rewritten this backfill with exact dryrun/live/DB-self-clean commands.
- [x] 3. `JOURNAL.md` — rewritten this backfill, modeled on
      `screens/Configuration/Assets/Financial_Objects/Bank/JOURNAL.md`, real content pulled from
      PR #551's body (including the `__FIRST__` gotcha in "Done wrong / lessons").
- [ ] 4. `playwright/ec_iud_<slug>.py` — N/A, waived per Section H (Universal Screen Engine
      replaces this role). Pre-existing `py/production_separator_iud.py` untouched.
- [ ] 5. `investigation/` — N/A, waived per Section H (existing `investigation/recon.py` from the
      2026-07-30 build untouched, not rebuilt).
- [x] 6. `evidence/` — pre-existing `evidence/psep_0[1-5]_*.png` + `results.json` kept (2026-07-30
      build); this backfill ADDS `evidence/backfill_2026-08-27/` (fresh dryrun + live 5/5 re-run +
      DB self-clean result, of the CURRENT PR #551 suite).
- [x] 7. `CHECKLIST.md` — this file.

## B. RF files (pre-existing, unchanged by this backfill)
- [x] 8. T3 `pageobjects/Configuration/Assets/Facility_Objects/production_separator_page.resource`
      — label-driven, no hardcoded ids (Delete End Date field is the one documented hardcoded
      exception, same rationale as Area's own).
- [x] 9. Suite `tests/Configuration/Assets/Facility_Objects/production_separator_iud.robot` — 5 TCs
      (Clean State/Insert/Update/Find/Delete), per-TC Login/Logout.

## C. Verification gates — re-run this backfill (2026-08-27), evidence in `evidence/backfill_2026-08-27/`
- [x] 10. robocop on the RF files: **7 issues, all `DOC02`** (missing TC `[Documentation]`) —
      re-checked Area's own current baseline the same session: also 7 `DOC02` issues -> parity,
      not a regression.
- [x] 11. `--dryrun`: **5/5 PASS** (`evidence/backfill_2026-08-27/dryrun/log.html`+`output.xml`).
- [x] 12. LIVE headless run: **5/5 PASS**
      (`EC_HEADLESS=true py -m robot tests/Configuration/Assets/Facility_Objects/
      production_separator_iud.robot`, `evidence/backfill_2026-08-27/live/log.html`+`output.xml`).
      No stray `chrome.exe` processes found before the run (`tasklist | grep -i chrome` checked
      clean).
- [x] 13. DB ground-truth — shared T2 `Verify Object Removed` (`OV_PRODSEPARATOR`, code column)
      inside TC05; independently re-confirmed this backfill via a fresh oracledb connection:
      `SELECT COUNT(*) FROM OV_PRODSEPARATOR WHERE CODE = 'AUTOTEST_PSEP'` -> 0,
      `... WHERE CODE LIKE 'AUTOTEST%'` -> 0.
- [x] 14. FULL I-U-D scope — Insert + Update + Delete all present (TC02/TC03/TC05).
- [x] 15. Self-clean confirmed — see item 13; both counts 0 after the live re-run
      (`evidence/backfill_2026-08-27/db_self_clean_result.txt`).
- [x] 16. Hygiene PASS — `py scripts/check_bundle_hygiene.py` -> `RESULT: PASS` (no hardcoded
      creds, pure ASCII, no CHECKLIST/VERIFY-REPORT contradictions for this bundle).

## D. Delivery
- [x] 17. Registry row — `docs/ec_screen_registry.md` already reflects the Area-pattern shape
      (modified in place by PR #551; not re-touched by this backfill, no duplicate row added).
- [x] 18. Scorecard row — `docs/automation-scorecard.md` already updated by PR #551 (not a new
      row); not re-touched by this backfill.
- [x] 19. PR — this backfill's own PR (docs-only, standard body: What was backfilled / Files added
      / Base branch = master), never self-merged.

## E. Knowledge base
- [x] 20. KB selector map `ec-ui-knowledge/screens/production_separator.md` — created this
      backfill (did not exist before), transcribed from `production_separator_page.resource`'s
      Variables section, modeled on `ec-ui-knowledge/screens/area.md`.
- [x] 21. Reuse clause — this IS the reuse-run deliverable: JOURNAL (#3), evidence (#6), and KB map
      (#20) all produced/refreshed this backfill, not just re-confirmed green tests.
