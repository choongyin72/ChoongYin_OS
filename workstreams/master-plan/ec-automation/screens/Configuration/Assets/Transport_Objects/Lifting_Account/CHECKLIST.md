# IUD Task — Deliverable Checklist — Lifting Account (CO.2004)

Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md`. This bundle predates the 2026-08-23/26 lean
waiver (Section G) — the checklist below was refreshed on 2026-08-28 per
`docs/lean-deliverable-backfill-workorder.md` Batch 5 to reflect the current (PR #562, 2026-08-27)
Area-pattern automation, restoring items 1/2/3/6/7/20 per Section H. Items 4/5 (Playwright driver +
investigation/) are marked pre-existing/untouched — the driver exists from the original 2026-07-30
build and was deliberately left unmodified by PR #562's RF-only conversion and by this backfill.

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/lifting_account.md` existed (from the 2026-07-30 build);
      refreshed in this session with the row2 addressing + regression note rather than re-scanned
      from zero.
- [x] **0b.** `grep -ril "lifting_account" workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}`
      → existing impl found: `py/lifting_account_iud.py`, `pageobjects/.../lifting_account_page.resource`,
      `tests/.../lifting_account_iud.robot`, this `screens/.../Lifting_Account/` bundle. REUSED/
      REFRESHED, not duplicated.
- [x] **0c.** Shared T2 `Apply Navigator From Properties` (`resources/manage_object.resource`)
      reused (extended in PR #562, not touched by this backfill task).

## A. Bundle artifacts — `screens/Configuration/Assets/Transport_Objects/Lifting_Account/`
- [x] **1. `lifting_account_sow.md`** — refreshed 2026-08-28; classification, navigator shape (one
      G:0 group, cascade spanning R:1/R:3), grid id, mandatory fields, test data, dev story, the
      shared-keyword regression, lessons. See file.
- [x] **2. `README.md`** — refreshed 2026-08-28; bundle overview + exact commands (dryrun, live
      headless, robocop, DB self-clean query).
- [x] **3. `JOURNAL.md`** — refreshed 2026-08-28; original 2026-07-30 entry preserved + new
      2026-08-27 (PR #562 conversion + regression, caught pre-merge by the live-canary gate) +
      2026-08-28 (this backfill) entries appended, each in Built/Done-well/Done-wrong/Blockers→
      resolution/Decisions/Evidence shape.
- [ ] **4. Playwright driver** — N/A for this backfill: `py/lifting_account_iud.py` pre-exists
      (2026-07-30 build) and was deliberately left untouched by both PR #562 and this task, per the
      owner's 2026-08-27 decision that item 4 stays permanently waived for Bank-/Area-pattern
      conversions (the Universal Screen Engine is the forward replacement).
- [ ] **5. `investigation/`** — N/A for this backfill, same reason as #4; a pre-existing
      `investigation/recon.py` from the 2026-07-30 build is present untouched, not refreshed (no new
      recon was needed for this documentation-only task).
- [x] **6. `evidence/`** — original `la_0[1-5]_*.png` + `results.json` (2026-07-30, Playwright 8/8)
      kept; added `output.xml`/`log.html`/`report.html`/`results-summary.md` from this backfill
      task's own one-time live confirmation run (2026-08-28, RF 5/5).
- [x] **7. `CHECKLIST.md`** — this file, refreshed with real evidence.

## B. RF files (pre-existing, unmodified by this backfill)
- [x] **8. T3 page object** `pageobjects/Configuration/Assets/Transport_Objects/lifting_account_page.resource`
      — built in PR #562; locators in Variables; docstring matches Variables.
- [x] **9. Suite** `tests/Configuration/Assets/Transport_Objects/lifting_account_iud.robot` — 5 TCs,
      clean → insert → update → find → delete, per-TC login/logout.

## C. Verification gates (re-confirmed live by this backfill task, 2026-08-28)
- [x] **10. robocop clean (relative to baseline)** — `robocop check` on the T3 + suite returns
      **7 issues**, all DOC02 (missing `[Documentation]` on test cases). Confirmed exact parity
      against Area's own baseline (`area_page.resource`/`area_iud.robot` also 7 issues via the same
      rule, checked directly this session) — not a regression, matches the registry's note.
- [x] **11. `--dryrun` N/N PASS** — `robot --dryrun tests/.../lifting_account_iud.robot`: **5 tests,
      5 passed, 0 failed** (this session, 2026-08-28).
- [x] **12. LIVE headless run N/N PASS** — `EC_HEADLESS=true robot tests/.../lifting_account_iud.robot`:
      **5 tests, 5 passed, 0 failed**, first attempt, no retry needed (this session, 2026-08-28).
      Artifacts in `evidence/output.xml`, `evidence/log.html`, `evidence/report.html`.
- [x] **13. DB ground-truth** — fresh independent oracledb connection (localhost:1521/ORCL,
      ECKERNEL_EC), `SELECT COUNT(*) FROM OV_LIFTING_ACCOUNT WHERE CODE LIKE 'AUTOTEST%'` = **0**
      after the live run (this session). Original PR #562 also cites the same query = 0 before AND
      after its own live run.
- [x] **14. FULL I-U-D scope** — TC02 Insert, TC03 Update, TC05 Delete all present (plus TC01 clean
      state, TC04 Find) — confirmed by reading `lifting_account_iud.robot`.
- [x] **15. Self-clean confirmed** — independent DB re-read = 0 residual `AUTOTEST%` rows (see #13).
- [x] **16. Hygiene PASS** — no new automation files created or modified by this backfill task
      (SOW/README/JOURNAL/CHECKLIST/evidence/KB map are documentation, not `playwright/*.py` or
      `investigation/*.py` subject to R16/R20); the pre-existing automation files were not touched.

## D. Delivery
- [x] **17. Registry row** — `docs/ec_screen_registry.md` Lifting Account row already exists
      (dated 2026-08-27, PR #562) and already documents the full row2 shape + regression; no new
      row needed for a documentation-only backfill (append-only rule — nothing to append, the row is
      current).
- [x] **18. Scorecard row** — same as #17; `docs/automation-scorecard.md` row already current from
      PR #562, no change needed for this backfill.
- [x] **19. PR** — this backfill's own PR, 6-field body (What/Files/DB ground-truth evidence/
      Self-clean/Rules applied/Base branch), base = master, never self-merge.

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/lifting_account.md` — refreshed 2026-08-28
      with the row2 navigator addressing, the actual current keyword-fix code shape (transcribed
      from the live file, not memory), the regression-history note as a documented gotcha, and
      today's last-verified date.
- [x] **21. Reuse clause** — this IS a "screen already implemented" case (Step 0 found existing
      automation); the refresh produced/refreshed JOURNAL (#3), evidence (#6), and KB map (#20) as
      required, not just re-confirmed passing tests.

---

**OVERALL for this backfill task: documentation/evidence artifacts restored per Section H; items
4/5 stay N/A per the permanent Playwright-driver waiver; all other items ticked with real evidence
gathered 2026-08-28 (dryrun 5/5, live 5/5, robocop 7-issue parity with Area, DB self-clean 0
residual). No automation file was created, modified, or re-verified from scratch beyond re-running
the already-proven suite once.**
