# IUD Task — Deliverable Checklist (Royalty Depositor)

Copy of `docs/IUD-DELIVERABLE-CHECKLIST.md`, ticked for **Royalty Depositor**
(Configuration > Assets > Royalty Objects > Royalty Depositor, RC.0052).

**Context:** the RF automation (T3 + suite + testdata) was built by PR #448 (merged 2026-08-23,
Batch 5 of the Bank-pattern conversion project) under Section G's lean-RF-only waiver. This
CHECKLIST backfills the documentation/evidence items that Section G waived and Section H
(owner decision 2026-08-27) restored — SOW, README, JOURNAL, evidence, this CHECKLIST, KB map.
Items 4/5 (Playwright driver + investigation/) stay waived per Section H (Universal Screen Engine
replaces that role). **No RF/automation file was modified to produce this bundle** — only
documentation/evidence artifacts were added or updated.

---

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/royalty_depositor.md` did not exist before this task —
      added as part of this backfill (item 20 below), transcribed from the existing
      `royalty_depositor_page.resource` Variables section, not re-scanned live.
- [x] **0b.** `grep -ril "royalty_depositor" workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}`
      → found existing impl: `pageobjects/Configuration/Assets/Royalty_Objects/royalty_depositor_page.resource`,
      `tests/Configuration/Assets/Royalty_Objects/royalty_depositor_iud.robot`,
      `testdata/royalty_depositor_*.properties`, and a pre-existing bundle at
      `screens/Configuration/Assets/Royalty_Objects/Royalty_Depositor/` (SOW/README/playwright/evidence
      predating PR #448). REUSED/EXTENDED — no parallel copy built.
- [x] **0c.** N/A for this backfill task (no new OV IUD engine build) — the existing RF suite
      already reuses the shared T2 `resources/manage_object.resource` + T1 `resources/common.resource`.

## A. Bundle artifacts — `screens/Configuration/Assets/Royalty_Objects/Royalty_Depositor/`
- [x] **1. `royalty_depositor_sow.md`** — updated 2026-08-28 with the real PR #448 dev story
      (Section 0 "UPDATE NOTE"), current Bank-pattern classification (Section 2.4/2.5), and known
      risks (Section 3). Source: `gh pr view 448` body (verbatim facts).
- [x] **2. `README.md`** — updated 2026-08-28 with exact dryrun/live/DB self-clean commands.
- [x] **3. `JOURNAL.md`** — added 2026-08-28, modeled on
      `screens/Configuration/Assets/Financial_Objects/Bank/JOURNAL.md`'s structure, content pulled
      from PR #448's real body (Built / Done well / Done wrong-lessons / Blockers→resolution /
      Decisions / Evidence).
- [ ] **4. Playwright driver** — N/A, waived (Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`:
      Universal Screen Engine replaces hand-written Playwright drivers going forward). A legacy
      pre-PR#448 Playwright bundle (`playwright/ec_iud_royalty_depositor.py`) already exists and
      is kept as historical reference, untouched by this task.
- [ ] **5. `investigation/`** — N/A, waived (same Section H reason as item 4). No new recon
      scripts were needed — all facts came from the existing `_page.resource`, the registry row,
      and PR #448's body/commit history.
- [x] **6. `evidence/`** — added `evidence/2026-08-28-live-run/` (log.html, report.html,
      output.xml, Browser-library playwright log, one screenshot per TC login/open_screen/action/
      verify/logout step) from a real live run executed as part of this backfill (see item 12).
      Pre-existing screenshots directly under `evidence/` (pre-dating PR #448) are left in place
      as historical reference, untouched.
- [x] **7. `CHECKLIST.md`** — this document.

## B. RF files — treeview-mirrored (pre-existing, PR #448 — NOT modified by this backfill)
- [x] **8. T3 page object** `pageobjects/Configuration/Assets/Royalty_Objects/royalty_depositor_page.resource` —
      pre-existing (PR #448); confirmed present, read for KB-map transcription, NOT edited.
- [x] **9. Suite** `tests/Configuration/Assets/Royalty_Objects/royalty_depositor_iud.robot` —
      pre-existing (PR #448); TC01 clean-state → TC02 insert → TC03 update → TC04 find → TC05
      delete/cleanup; confirmed present, NOT edited.

## C. Verification gates — re-confirmed by this backfill (fresh runs, no automation changes)
- [x] **10. robocop clean (baseline)** — `py -m robocop check pageobjects/.../royalty_depositor_page.resource tests/.../royalty_depositor_iud.robot`
      → **9 issues** (4 VAR02 + 5 DOC02 at time of this backfill run, 2026-08-28) — at/near the
      established Bank-pattern baseline (8 at PR #448 time); no new files changed by this task so
      this is a fresh measurement of pre-existing code, not a new regression introduced here.
- [x] **11. `--dryrun` N/N PASS** — screen suite: `robot --dryrun tests/Configuration/Assets/Royalty_Objects/royalty_depositor_iud.robot`
      → **5/5 PASS** (2026-08-28). Full-tree: `robot --dryrun tests/` → **883/883 PASS** (2026-08-28).
- [x] **12. LIVE headless run N/N PASS** — `EC_HEADLESS=true robot --outputdir <out> tests/Configuration/Assets/Royalty_Objects/royalty_depositor_iud.robot`
      → **5/5 PASS** (2026-08-28, this backfill's confirmation run). Artifacts in
      `evidence/2026-08-28-live-run/`.
- [x] **13. DB ground-truth** — exact assertions already wired into the pre-existing suite:
      `Verify Object Insert Exists` (TC02, backed by `Code Should Be Present In View`),
      `Verify Object Found` (TC04), `Verify Object Removed` (TC05, backed by
      `Verify Object Removed ${RD_TABLE} ov_royalty_depositor ${code}`), all against
      `OV_ROYALTY_DEPOSITOR`. Re-confirmed passing on the 2026-08-28 live run.
- [x] **14. FULL I-U-D scope** — Insert (TC02) + Update (TC03) + Find (TC04) + Delete (TC05) all
      present and passing on the 2026-08-28 live run.
- [x] **15. Self-clean confirmed** — fresh oracledb connection after the 2026-08-28 live run:
      `SELECT COUNT(*) FROM OV_ROYALTY_DEPOSITOR WHERE CODE = 'AUTOTEST_ROYALTY_DEP'` → **0**.
- [x] **16. Hygiene PASS** — N/A for new code (this backfill added only Markdown docs + evidence
      artifacts under `screens/` and `ec-ui-knowledge/`, no `playwright/*.py` or
      `investigation/*.py` files were added/changed) — `check_bundle_hygiene.py`'s R16/R20 scope
      (env-creds, ASCII in Playwright/investigation scripts) does not apply to this backfill's
      changes. Pre-existing hygiene from PR #448 is unaffected (no automation files touched).

## D. Delivery
- [x] **17. Registry row** — already present at `docs/ec_screen_registry.md` (PR #448 row,
      updated again 2026-08-25 for the alignment fix). **Not re-appended by this backfill** —
      the row already documents the current state; this task only adds the docs bundle it points
      to via `screens/.../Royalty_Depositor/`.
- [x] **18. Scorecard row** — already present at `docs/automation-scorecard.md` (PR #448). Not
      re-appended by this backfill (same reasoning as item 17).
- [x] **19. PR** — this backfill's own PR uses the standard 6-field body (What was backfilled /
      Files added / Base branch = master, etc.), branch `docs/royalty-depositor-backfill-artifacts`,
      synced with master before push, never self-merged.

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/royalty_depositor.md` — added 2026-08-28,
      transcribed from `royalty_depositor_page.resource`'s Variables section (nav path, DB view,
      grid id, insert/update/delete selectors, mandatory-yellow fields, quirks), last-verified
      2026-08-28.
- [x] **21. Reuse clause.** Step 0 found the screen already implemented (PR #448) — this backfill
      is exactly the "reuse run" the clause describes: it produces/refreshes JOURNAL (#3),
      evidence (#6), and KB map (#20) rather than declaring done on green tests alone.
