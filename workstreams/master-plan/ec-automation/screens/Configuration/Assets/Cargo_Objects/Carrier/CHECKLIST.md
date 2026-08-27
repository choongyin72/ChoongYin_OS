# IUD Deliverable Checklist — Carrier

Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md`. This is a BACKFILL (Batch 11 of
`docs/lean-deliverable-backfill-workorder.md`) for a screen already converted to the Bank pattern
in PR #477 (merged 2026-08-23), under Section H's restored items (SOW/README/JOURNAL/evidence/
CHECKLIST/KB map), with items 4/5 (Playwright driver + investigation/) staying waived per Section H.

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** Read `ec-ui-knowledge/screens/carrier.md` — did not exist before this backfill;
      created as part of this task (item 20 below). No pre-existing KB entry to reuse.
- [x] **0b.** `grep -ril "carrier" workstreams/master-plan/ec-automation/{pageobjects,tests,screens,testdata}`
      → found existing implementation: `pageobjects/.../carrier_page.resource`,
      `tests/.../carrier_iud.robot`, `testdata/carrier_*.properties`,
      `screens/.../Carrier/` bundle — this task REUSES/EXTENDS it (backfill of docs/evidence only,
      per the task brief). No automation file touched.
- [x] **0c.** Shared engine already in use: `resources/manage_object.resource` (T2) +
      `resources/common.resource` (T1) via `carrier_page.resource` — confirmed untouched by this
      backfill (`git diff` scoped to docs/evidence paths only, see PR diff).

## A. Bundle artifacts — `screens/Configuration/Assets/Cargo_Objects/Carrier/`
- [x] **1. `carrier_sow.md`** — updated: added section 6 (Bank-pattern conversion, PR #477) on top
      of the original 2026-06-19 SOW; classification (OV, Bank family, plain, `OV_CARRIER`) unchanged.
- [x] **2. `README.md`** — updated: exact commands for dryrun / live headless / live headed /
      Playwright / DB self-clean re-read, reflecting the post-conversion RF suite.
- [x] **3. `JOURNAL.md`** — created (did not exist before this backfill): Built / Done well / Done
      wrong-lessons / Blockers→resolution / Decisions / Evidence, sourced from PR #477's real body.
- [ ] **4. `playwright/ec_iud_carrier.py`** — N/A / waived (Section H, `docs/IUD-DELIVERABLE-CHECKLIST.md`):
      pre-existing driver left UNCHANGED; Universal Screen Engine is the owner-decided replacement,
      no new Playwright driver built for this or any Bank-pattern conversion.
- [ ] **5. `investigation/`** — N/A / waived (Section H): pre-existing recon scripts
      (`resolve_carrier.py`, `scan_carrier.py`, `carrier_residue.py`) left UNCHANGED; reused
      `carrier_residue.py` read-only for item 15 below rather than writing a new script.
- [x] **6. `evidence/`** — added `evidence/rf-live-2026-08-28/` (this backfill's live RF re-run:
      output.xml/log.html/report.html/playwright-log.txt + 24 step screenshots, 2.3MB total, no
      single file >2MB); pre-existing `evidence/` (2026-06-19 Playwright screenshots +
      `ec_iud_carrier_result.json`) left intact.
- [x] **7. `CHECKLIST.md`** — this file.

## B. RF files (pre-existing, unchanged, reused as-is)
- [x] **8. T3 page object** `pageobjects/Configuration/Assets/Cargo_Objects/carrier_page.resource`
      — pre-existing (PR #477), NOT modified by this backfill.
- [x] **9. Suite** `tests/Configuration/Assets/Cargo_Objects/carrier_iud.robot` — pre-existing
      (PR #477), NOT modified by this backfill.

## C. Verification gates (re-run for this backfill, evidence below)
- [x] **10. robocop clean** — `py -m robocop check pageobjects/.../carrier_page.resource
      tests/.../carrier_iud.robot` → exit 1, **9 issues** (5x DOC02 missing-test-doc + 1x VAR02).
      Confirmed identical in kind/count to the already-merged `port_iud.robot` baseline (also
      exit 1, 9 issues) — pre-existing, not a regression, matches PR #477's own robocop-parity note.
- [x] **11. `--dryrun` N/N PASS** — `py -m robot --dryrun tests/Configuration/Assets/Cargo_Objects/carrier_iud.robot`
      → **5 tests, 5 passed, 0 failed** (this backfill's own re-run, 2026-08-28).
- [x] **12. LIVE headless run N/N PASS** — `EC_HEADLESS=true py -m robot
      tests/Configuration/Assets/Cargo_Objects/carrier_iud.robot` → **5 tests, 5 passed, 0 failed**
      (TC01-05, this backfill's own live re-run, 2026-08-28; artifacts in `evidence/rf-live-2026-08-28/`).
      `Find Carrier Row By Filter` grep-counted 14x, `Clear Carrier Row Filter` 5x in this run's
      `output.xml` — matches PR #477's original conversion-time count exactly.
- [x] **13. DB ground-truth** — DbVerify assertions inside the suite: `Code Should Be Present In
      View OV_CARRIER <code>` (TC02) / `Code Should Be Absent In View OV_CARRIER <code>` (TC05),
      via T2's `Insert Object From Properties And Verify Code` / `Verify Object Removed`. Both PASS
      in this backfill's live re-run.
- [x] **14. FULL I-U-D scope** — TC02 Insert / TC03 Update / TC05 Delete all present and PASS (not
      I/D only).
- [x] **15. Self-clean confirmed** — independent DB re-read via the pre-existing
      `investigation/carrier_residue.py` (read-only, run as-is, no code change):
      `py screens/Configuration/Assets/Cargo_Objects/Carrier/investigation/carrier_residue.py` →
      **"AUTOTEST residue rows in OV_CARRIER: 0"** (run 2026-08-28, after the live re-run above).
- [x] **16. Hygiene PASS** — `py scripts/check_bundle_hygiene.py` (run from repo root) →
      **"RESULT: PASS - no hardcoded creds (R16), pure ASCII (R20), no CHECKLIST/VERIFY-REPORT
      contradictions, doc rows match declared families"** (the one WARN it reports is in an
      unrelated screen, Contract_Area's investigation script — not Carrier).

## D. Delivery
- [x] **17. Registry row** — Carrier's row in `docs/ec_screen_registry.md` was already updated by
      PR #477 (MODIFIED, not appended, since it superseded the 2026-06-19 build's row) — no further
      change needed by this backfill.
- [x] **18. Scorecard row** — Carrier's row in `docs/automation-scorecard.md` was already updated
      by PR #477 — no further change needed by this backfill.
- [x] **19. PR** — this backfill's own PR, `docs/carrier-backfill-artifacts` branch, targeting
      master, standard body (What backfilled / Files added / Base branch), never self-merged.

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/carrier.md` — created (did not exist before
      this backfill), transcribed from `carrier_page.resource`'s Variables section (no re-scan).
- [x] **21. Reuse clause** — Step 0 found the screen already implemented (PR #477); this backfill
      is exactly the "reuse run" deliverable the clause requires: JOURNAL (#3) + evidence (#6) + KB
      map (#20) all produced/refreshed, not just re-confirming green tests.

**OVERALL: PASS** — all restored Section-H items (1, 2, 3, 6, 7, 20) delivered; items 4/5 correctly
N/A per the still-active Playwright waiver; items 8-19 and 21 verified with real re-run evidence
captured above, no automation file modified.
