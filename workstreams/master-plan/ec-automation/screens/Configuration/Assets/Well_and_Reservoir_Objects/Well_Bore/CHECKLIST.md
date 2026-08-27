# IUD Task — Deliverable Checklist (Well Bore, CO.0054)

_Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md`. This screen was converted to the full
Area-pattern in PR #564 (merged 2026-08-27) under the then-current Section G lean waiver. Section
H (owner decision 2026-08-27) retired that waiver except for items 4/5 (Playwright driver +
investigation/, permanently superseded by the Universal Screen Engine). This CHECKLIST is the
2026-08-28 backfill of the items Section G had waived — ticked against real evidence gathered in
this backfill session, per `docs/lean-deliverable-backfill-workorder.md` Batch 5._

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/well_bore.md` did not exist before this backfill — created
      in this session (see item 20).
- [x] **0b.** `grep -ril "well_bore" workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}`
      → found existing implementation: `py/well_bore_iud.py`, `pageobjects/.../well_bore_page.resource`,
      `tests/.../well_bore_iud.robot`, `screens/.../Well_Bore/` (pre-existing bundle from
      2026-07-31). REUSED/EXTENDED — no parallel copy built.
- [x] **0c.** Shared engine already in use by the pre-existing driver; not re-plumbed.

## A. Bundle artifacts — `screens/Configuration/Assets/Well_and_Reservoir_Objects/Well_Bore/`
- [x] **1. `well_bore_sow.md`** — updated this session with the real Area-pattern classification,
      per-field navigator shape, mandatory fields, test data, and the dev story pulled from PR
      #564's body (bespoke T3 keyword rationale + the mid-task registry-collision incident).
- [x] **2. `README.md`** — updated this session: bundle overview + exact dryrun/live/robocop/
      DB-self-clean/hygiene commands.
- [x] **3. `JOURNAL.md`** — updated this session, modeled on Bank's JOURNAL.md structure (Built /
      Done well / Done wrong-or-lessons / Blockers→resolution / Decisions / Evidence), with real
      content from PR #564's body and the follow-up commit `c35b909b`.
- [ ] **4. Playwright driver** — N/A, permanently waived (Section H): the Universal Screen Engine
      replaces this role going forward. Pre-existing `py/well_bore_iud.py` left UNCHANGED.
- [ ] **5. `investigation/`** — N/A, permanently waived (Section H), same reasoning as item 4.
      Pre-existing `investigation/recon*.py` scripts left UNCHANGED.
- [x] **6. `evidence/`** — `evidence/backfill_2026-08-28/` added this session: `log.html`,
      `output.xml`, `report.html` from a fresh live headless run (5/5 PASS, first attempt, no
      retry needed), `robocop_output.txt` (7 issues, parity with Area's baseline), `summary.md`
      (DB self-clean + filter-hit-count evidence). Pre-existing `evidence/wb_0[1-5]_*.png` (2026-07-31)
      left in place, not overwritten.
- [x] **7. `CHECKLIST.md`** — this file.

## B. RF files (pre-existing, UNCHANGED by this backfill)
- [x] **8. T3 page object** `pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/well_bore_page.resource`
      — bespoke `Apply Well Bore Navigator From Properties` keyword confirmed present (read, not modified).
- [x] **9. Suite** `tests/Configuration/Assets/Well_and_Reservoir_Objects/well_bore_iud.robot` —
      5 TCs (Verify Clean State / Insert / Update / Find / Delete) confirmed present (read, not modified).

## C. Verification gates (re-run this session for evidence capture only — automation not modified)
- [x] **10. robocop clean** — exit=1, **7 issues** (5x DOC02, 2x VAR02), matching Area's own
      documented baseline (parity, not a regression). See `evidence/backfill_2026-08-28/robocop_output.txt`.
- [x] **11. `--dryrun` N/N PASS** — `robot --dryrun tests/Configuration/Assets/Well_and_Reservoir_Objects/well_bore_iud.robot`
      → **5/5 PASS, 0 fail** (this backfill session, 2026-08-28).
- [x] **12. LIVE headless run N/N PASS** — `EC_HEADLESS=true robot tests/Configuration/Assets/Well_and_Reservoir_Objects/well_bore_iud.robot`
      → **5/5 PASS, 0 fail**, first attempt (2026-08-28). See `evidence/backfill_2026-08-28/log.html`.
- [x] **13. DB ground-truth** — fresh independent `oracledb` connection (`localhost:1521/ORCL`,
      `ECKERNEL_EC`): `SELECT COUNT(*) FROM OV_WELL_BORE WHERE UPPER(CODE) LIKE 'AUTOTEST%'` → 0.
      `Verify Object Removed` (shared T2 keyword) performs the in-suite DB check on TC05.
- [x] **14. FULL I-U-D scope** — TC02 Insert, TC03 Update, TC05 Delete all present and PASS in the
      2026-08-28 live run.
- [x] **15. Self-clean confirmed** — same fresh connection above: `SELECT COUNT(*) FROM OV_WELL_BORE`
      → **158** (pre-existing rows intact, unchanged from the 2026-07-31/2026-08-27 counts); 0
      residual `AUTOTEST%` rows.
- [x] **16. Hygiene PASS** — `py scripts/check_bundle_hygiene.py` (repo root) → RESULT: PASS (no
      hardcoded creds R16, pure ASCII R20, no CHECKLIST/VERIFY-REPORT contradiction). One unrelated
      pre-existing WARN for a different screen's (Contract Area) investigation script.

## D. Delivery
- [x] **17. Registry row** — already present in `docs/ec_screen_registry.md` (line ~317, added by
      PR #564; the duplicate "keep-both" row created by the mid-task collision was already removed
      by follow-up commit `c35b909b` before this backfill started). No change needed this session.
- [x] **18. Scorecard row** — already present in `docs/automation-scorecard.md` (added by PR #564).
      No change needed this session.
- [x] **19. PR** — this backfill's own PR, standard 6-field body, targets `master`, never self-merged.

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/well_bore.md` — created this session (did
      not exist before), transcribed from `well_bore_page.resource`'s own Variables/Keywords
      sections — see that file for the selectors, including the bespoke navigator keyword's group
      sequence.
- [x] **21. Reuse clause** — this IS a reuse/backfill run (Step 0 found the screen already fully
      implemented). This CHECKLIST + the refreshed JOURNAL/SOW/README + the new evidence/KB map
      satisfy the reuse clause — "Done" is not claimed on green tests alone.

---
_Backfilled 2026-08-28 per `docs/lean-deliverable-backfill-workorder.md` (Batch 5, final Area-pattern
wave). Automation files (`py/well_bore_iud.py`, `well_bore_page.resource`, `well_bore_iud.robot`,
`testdata/well_bore_*.properties`, `investigation/*`) were read but NOT modified in this session._
