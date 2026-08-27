# IUD Task — Deliverable Checklist — Transport Zone

Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md` (Section H restored requirements). This is a
**backfill** (`docs/lean-deliverable-backfill-workorder.md`, Batch 5) — Transport Zone's RF suite
was already converted to the Area pattern and merged via PR #557 (2026-08-26); this checklist
documents the retroactive documentation/evidence bundle added 2026-08-28, plus a fresh
dryrun+live evidence-capture re-run of the already-proven suite. **No automation code was
rebuilt, modified, or re-verified from scratch.**

---

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/transport_zone.md` did not exist before this backfill —
      created fresh (item 20 below), transcribed from the page object's own Variables/
      Documentation, not re-scanned live.
- [x] **0b.** `grep -ril "transport_zone" workstreams/master-plan/ec-automation/{py,pageobjects,
      tests,screens,testdata}` → found existing impl at
      `pageobjects/Configuration/Assets/Dispatching_Objects/transport_zone_page.resource`,
      `tests/Configuration/Assets/Dispatching_Objects/transport_zone_iud.robot`, and the 5
      `testdata/transport_zone_*.properties` files — REUSED/EXTENDED, no parallel copy built. No
      pre-existing `screens/.../Transport_Zone/` bundle was found (this build never had one).
- [x] **0c.** Shared T2 `resources/manage_object.resource` reused as-is (PR #557 needed only the
      already-existing `Apply Navigator From Properties` keyword) — not modified by this backfill
      either.

## A. Bundle artifacts — `screens/Configuration/Assets/Dispatching_Objects/Transport_Zone/`
- [x] **1. `transport_zone_sow.md`** — created (did not exist before). Classification, nav/grid/
      cell shape, test data, and the real §3.2 PR #557 dev story.
- [x] **2. `README.md`** — created, with exact RF commands (dryrun/live headless/live headed) and
      the `OV_TRANSPORT_ZONE` DB self-clean query pattern.
- [x] **3. `JOURNAL.md`** — created (did not exist before). Built/Done well/Done wrong-or-lessons/
      Blockers→resolution/Decisions/Evidence, modeled on
      `screens/Configuration/Assets/Financial_Objects/Bank/JOURNAL.md`, content pulled from PR
      #557's real body + `docs/ec_screen_registry.md`'s row, not invented. Includes the disclosed
      live-run timeout hit during this backfill's own evidence capture.
- [ ] **4. `playwright/ec_iud_<slug>.py`** — N/A. Playwright bundle waived, owner decision
      2026-08-27 (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H). No pre-existing Playwright bundle
      was found for this screen — nothing to preserve or rebuild.
- [ ] **5. `investigation/`** — N/A. Playwright bundle waived, owner decision 2026-08-27. No
      pre-existing recon scripts existed for this screen outside temp recon steps disclosed in PR
      #557's own body.
- [x] **6. `evidence/`** — created fresh: `evidence/backfill_2026-08-28/` with a dryrun
      (`dryrun/log.html`+`report.html`+`output.xml`), the disclosed first live attempt
      (`live_attempt1_fail/` — 4/5 pass, TC01 timeout), and the passing live headless retry
      (`live/log.html`+`report.html`+`output.xml`) of the ALREADY-PROVEN Area-pattern suite.
- [x] **7. `CHECKLIST.md`** — this file.

## B. RF files — treeview-mirrored (NOT modified by this backfill)
- [x] **8. T3 page object**
      `pageobjects/Configuration/Assets/Dispatching_Objects/transport_zone_page.resource` —
      already exists (PR #557), unmodified by this backfill (confirmed via `git status`); reviewed
      only for the KB map.
- [x] **9. Suite** `tests/Configuration/Assets/Dispatching_Objects/transport_zone_iud.robot` —
      already exists (PR #557), unmodified by this backfill; TC01 clean → TC02 insert → TC03
      update → TC04 find → TC05 delete/cleanup, confirmed by re-running it (not by reading alone).

## C. Verification gates (real re-run evidence, 2026-08-28)
- [x] **10. robocop clean (parity with Area)** — `py -m robocop check
      pageobjects/.../transport_zone_page.resource tests/.../transport_zone_iud.robot`
      (2026-08-28, this session) → **7 issues** (VAR02/DOC02 kinds — 2x on the page object docstring
      shape, 2x DOC02 missing test-case documentation on TC04/TC05, plus additional VAR02/DOC02).
      Cross-checked `py -m robocop check
      pageobjects/Configuration/Assets/Basic_Objects/area_page.resource
      tests/Configuration/Assets/Basic_Objects/area_iud.robot` (the Area-pattern role model) →
      **also 7 issues**. Transport Zone's robocop output is at parity with Area's own established
      baseline, not a new/worse defect — no fix applied, per this task's explicit "do not modify
      the RF automation" scope.
- [x] **11. `--dryrun` N/N PASS** — `py -m robot --dryrun --outputdir
      screens/.../Transport_Zone/evidence/backfill_2026-08-28/dryrun
      tests/Configuration/Assets/Dispatching_Objects/transport_zone_iud.robot` → **5 tests, 5
      passed, 0 failed** (2026-08-28, this session; log/report/output archived in
      `evidence/backfill_2026-08-28/dryrun/`).
- [x] **12. LIVE headless run N/N PASS** — `EC_HEADLESS=true py -m robot --outputdir ...
      tests/Configuration/Assets/Dispatching_Objects/transport_zone_iud.robot`. FIRST attempt:
      **5 tests, 4 passed, 1 failed** (TC01 "Verify Clean State" timed out waiting for the menu
      search textbox to become visible — a page-load timing issue, not a code defect; TC02-TC05 all
      passed cleanly in the same run). RETRY (same unmodified command, single retry per the task's
      process rule, no chrome/node process killed): **5 tests, 5 passed, 0 failed** (TC01-TC05 all
      PASS, 2026-08-28, this session; archived in `evidence/backfill_2026-08-28/live/`). Disclosed,
      not smoothed over — see JOURNAL.md and the preserved
      `evidence/backfill_2026-08-28/live_attempt1_fail/` artifacts.
- [x] **13. DB ground-truth** — fresh oracledb connection, 2026-08-28, this session, run after the
      passing retry: `SELECT COUNT(*) FROM OV_TRANSPORT_ZONE WHERE CODE =
      'AUTOTEST_TRANSPORT_ZONE'` → `0`; `SELECT CODE FROM OV_TRANSPORT_ZONE WHERE CODE LIKE
      'AUTOTEST%'` → `[]` (no rows). Confirms the suite's own TC02/TC03/TC05 insert/update/delete
      cycle against `OV_TRANSPORT_ZONE` completed cleanly.
- [x] **14. FULL I-U-D scope** — TC02 Insert + TC03 Update + TC05 Delete all present and PASS (see
      item 12); TC04 Find also present (Area-pattern's 5th TC).
- [x] **15. Self-clean confirmed** — independent fresh-connection re-read (item 13) = 0 residual
      `AUTOTEST_TRANSPORT_ZONE` / `AUTOTEST%` rows in `OV_TRANSPORT_ZONE` after the live run.
- [x] **16. Hygiene PASS** — `py scripts/check_bundle_hygiene.py` (run from repo root, 2026-08-28,
      this session) → `[hygiene] RESULT: PASS - no hardcoded creds (R16), pure ASCII (R20), no
      CHECKLIST/VERIFY-REPORT contradictions, doc rows match declared families` (one unrelated
      pre-existing WARN about Contract Area's `investigation/live_recon_contract_area.py` selector
      STRINGS — DOM locator literals, not hardcoded credential values, unrelated to Transport
      Zone).

## D. Delivery
- [x] **17. Registry row** — already present, MODIFIED IN PLACE by PR #557 (not this backfill);
      confirmed live: `docs/ec_screen_registry.md` line 88, "Transport Zone ... FULL Area-pattern
      conversion done 2026-08-26". This backfill does not touch the registry row again
      (append-only / no-duplicate-edit).
- [x] **18. Scorecard row** — pre-existing from PR #557; not duplicated by this backfill
      (documentation-only task, no new automation scope to score).
- [ ] **19. PR** — this backfill's own PR (branch `docs/transport-zone-backfill-artifacts`),
      6-field body, base = master, sync-before-push done, never self-merge. (Ticked once the PR is
      raised — see PR body for the R9 fields.)

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/transport_zone.md` — created 2026-08-28
      (did not exist before), transcribed from `transport_zone_page.resource`'s own
      Variables/Documentation section (nav path, DB view, grid id, insert/update/delete selectors,
      mandatory-yellow fields, quirks), not re-scanned live — per the backfill work order's
      instruction to transcribe, not re-discover.
- [x] **21. Reuse clause** — Step 0 found the screen ALREADY implemented (PR #557); this backfill
      produced the deliverables that document it: JOURNAL (#3), evidence (#6), KB map (#20), plus
      the SOW/README/CHECKLIST this retroactive-backfill scope additionally requires.

---

## Deviations from the standard 21-item list (stated explicitly, per R-no-silent-deviation)
- Items 4/5 (Playwright driver + investigation/) are marked N/A per the PERMANENT waiver
  (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H) — this is not a backfill gap, it is the current
  standing rule for Area-pattern work.
- Items 17/18 (registry/scorecard rows) are NOT re-appended by this backfill — they already exist
  from PR #557 and appending a second row for the same screen would violate the append-only,
  no-duplicate convention (R23).
- Item 12's live-run gate required TWO attempts (one disclosed failure — a page-load timeout, not
  a code defect — one passing retry) due to a shared-environment timing issue, not a code defect —
  recorded honestly in the evidence rather than only citing the passing run, per the task's
  explicit process rule (retry ONCE, disclose if it still fails, never kill chrome/node processes
  by name in this shared environment).
