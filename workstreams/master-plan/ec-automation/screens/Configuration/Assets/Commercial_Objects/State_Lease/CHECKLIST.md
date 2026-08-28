# IUD Task — Deliverable Checklist — State Lease

Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md`. This is a **lean-deliverable backfill** (owner
decision 2026-08-27, Section H) — items 4/5 (Playwright driver + `investigation/`) stay waived
permanently per Section H (Universal Screen Engine replaces that role for Bank-pattern screens).
Items 8-19/21 were already delivered and merged in PR #440 (2026-08-23, Batch 4) and are cited
below from that PR's body; this backfill re-ran the suite live once (2026-08-28) for fresh evidence
and added items 1/2/3/6/7/20.

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/state_lease.md` did not exist before this backfill — created
      now (item 20). No pre-existing KB map to reuse.
- [x] **0b.** `grep -ril "state_lease" workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}`
      → found existing impl: `pageobjects/.../state_lease_page.resource`,
      `tests/.../state_lease_iud.robot`, `screens/.../State_Lease/` (pre-existing bundle with
      SOW/README/evidence/playwright/investigation from 2026-06-12). This task REUSED/EXTENDED
      that bundle — did not build a parallel copy.
- [x] **0c.** Shared engine reused: RF suite delegates to T2 `resources/manage_object.resource` +
      T1 `resources/common.resource` + `libraries/DbVerify.py` + `libraries/PropertiesReader.py`.
      No new plumbing added.

## A. Bundle artifacts — `screens/Configuration/Assets/Commercial_Objects/State_Lease/`
- [x] **1. `state_lease_sow.md`** — refreshed 2026-08-28 with classification (plain Bank-pattern OV,
      no navigator), grid id, mandatory fields, test data, dev story pulled from PR #440's real body.
- [x] **2. `README.md`** — refreshed 2026-08-28 with bundle overview + exact run commands (dryrun,
      live headless, DB self-clean query).
- [x] **3. `JOURNAL.md`** — new, modeled on Bank's JOURNAL.md structure, content pulled from PR #440's
      real body/commit history (see `JOURNAL.md` in this bundle).
- [ ] **4. `playwright/ec_iud_state_lease.py`** — N/A / waived (Section H: Playwright driver stays
      waived for Bank-pattern conversions; a pre-existing 2026-06-12 legacy copy is kept for
      history only, not rebuilt or extended).
- [ ] **5. `investigation/`** — N/A / waived (Section H, same reason as #4; pre-existing 2026-06-12
      recon scripts kept for history only).
- [x] **6. `evidence/`** — `evidence/backfill_2026-08-28/` added: live-run `output.xml`/`log.html`/
      `report.html` + 25 step screenshots + `results_summary.md` (this backfill, 2026-08-28).
      Pre-existing 2026-06-12 Playwright evidence (`state_lease_0[1-8]_*.png` +
      `state_lease_results.json`) retained unchanged.
- [x] **7. `CHECKLIST.md`** — this file.

## B. RF files — treeview-mirrored (pre-existing, PR #440, NOT modified by this backfill)
- [x] **8. T3 page object**
      `pageobjects/Configuration/Assets/Commercial_Objects/state_lease_page.resource` — merged
      PR #440, 2026-08-23. Not touched by this backfill task.
- [x] **9. Suite** `tests/Configuration/Assets/Commercial_Objects/state_lease_iud.robot` — TC
      structure: TC01 clean-state -> TC02 insert -> TC03 update -> TC04 find -> TC05 delete
      (cleanup via true delete). Merged PR #440, 2026-08-23. Not touched by this backfill task.

## C. Verification gates
- [x] **10. robocop clean (relative to baseline)** — per PR #440 body: 7 issues (2 VAR02 + 5 DOC02),
      fewer than the 9-issue baseline for the batch. (Historical citation; not re-run standalone in
      this backfill — see item 16 for this backfill's own hygiene evidence.)
- [x] **11. `--dryrun` N/N PASS** — PR #440: full-tree dryrun 740/740 PASS. **This backfill
      (2026-08-28), re-run standalone:** `robot --dryrun tests/Configuration/Assets/Commercial_Objects/state_lease_iud.robot`
      → **5 tests, 5 passed, 0 failed** (`evidence/backfill_2026-08-28/results_summary.md`).
- [x] **12. LIVE headless run N/N PASS** — PR #440: live 5/5 PASS, 2026-08-23. **This backfill
      (2026-08-28), re-run:** `EC_HEADLESS=true robot tests/Configuration/Assets/Commercial_Objects/state_lease_iud.robot`
      → **5 tests, 5 passed, 0 failed** on first attempt (no retry needed). Artifacts in
      `evidence/backfill_2026-08-28/`.
- [x] **13. DB ground-truth** — `libraries/DbVerify.py::code_should_be_absent_in_view("OV_STATE_LEASE", ...)`
      / `Verify Object Removed` (delete), `Verify Object Insert Exists` (insert), `Verify Object Found`
      (find) all assert against `OV_STATE_LEASE` directly. **This backfill's own fresh-connection
      check** (`Workplaces/state-lease-backfill/dbcheck.py`, using `DbVerify._connect()` /
      `_code_present`): `AUTOTEST_STL present in OV_STATE_LEASE (fresh connection): False` — 0
      residual rows confirmed post-run, 2026-08-28.
- [x] **14. FULL I-U-D scope** — Insert (TC02) + Update (TC03) + Delete (TC05) all present, plus
      Find (TC04) and a clean-state check (TC01).
- [x] **15. Self-clean confirmed** — independent DB re-read = 0 residual `AUTOTEST_STL` rows
      (item 13 above, this backfill's own fresh connection, 2026-08-28). PR #440 also cited this at
      merge time (2026-08-23) with a stray `RECON_STL` row cleanup noted in `JOURNAL.md`.
- [x] **16. Hygiene PASS** — not independently re-run in this doc-only backfill (no code changed);
      relying on PR #440's own hygiene pass at merge (no R16/R20 findings reported in that PR's
      body). No `playwright/*.py`/`investigation/*.py` files were added or modified by this task.

## D. Delivery
- [x] **17. Registry row** — already present, `docs/ec_screen_registry.md` line: "State Lease |
      Configuration > Assets > Commercial Objects > State Lease | OV | `OV_STATE_LEASE` |
      manage-object (plain...) | ... Bank-pattern conversion ... 2026-08-23, Batch 4 ...". Not
      re-appended by this backfill (append-only, no duplicate needed — row already documents the
      conversion).
- [x] **18. Scorecard row** — already present per PR #440's file list
      (`docs/automation-scorecard.md` modified in that PR). Not re-appended by this backfill.
- [x] **19. PR** — this backfill's own PR (docs/state-lease-backfill-artifacts branch) uses the
      standard 6-field body (What was backfilled / Files added / Base branch = master); R8 sync
      done before push; never self-merged.

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/state_lease.md` — new, created 2026-08-28,
      transcribed from `state_lease_page.resource`'s Variables section (nav path, DB view, grid id,
      Code label, delete field id, mandatory/optional fields, quirks), last-verified 2026-08-28.
- [x] **21. Reuse clause** — Step 0 found the screen already implemented (RF suite live-merged);
      this backfill produces exactly the deliverables the reuse clause requires: JOURNAL (#3),
      evidence (#6), and KB map (#20) — plus the additionally-restored SOW/README/CHECKLIST per
      Section H.

## Overall
**Items 1/2/3/6/7/20/21 (this backfill's scope): DONE, evidenced above.**
**Items 8-19 (RF automation + original verification gates): pre-existing, merged PR #440,
2026-08-23 — cited, not rebuilt.**
**Items 4/5: N/A, waived permanently per Section H.**
No RF automation, page object, or properties files were modified by this backfill task.
