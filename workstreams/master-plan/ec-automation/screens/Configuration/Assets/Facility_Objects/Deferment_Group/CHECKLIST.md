# Deferment Group — IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md)

_Backfilled 2026-08-28 per `docs/lean-deliverable-backfill-workorder.md` (Batch 11, last screen) —
Section H retired the 2026-08-23/26 lean waiver for Bank-/Area-pattern conversions. Items 4/5
(Playwright driver + investigation/) stay permanently waived (Universal Screen Engine supersedes
them). This checklist documents the ALREADY-MERGED PR #479 rebuild plus this session's honest
re-verification attempt — it does NOT re-tick items on a fresh "PASS" that didn't actually happen
today._

## Step 0 — check-existing gate
- [x] **0a.** KB map existed (`ec-ui-knowledge/screens/deferment_group.md`, pre-dating this backfill)
      and was read before touching anything.
- [x] **0b.** `grep -ril deferment_group workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}`
      → found: existing RF T3/suite/testdata from PR #479 (merged 2026-08-23) + a pre-Batch-8
      Playwright driver `py/deferment_group_iud.py`. REUSED/documented, not rebuilt.
- [x] **0c.** Confirmed the existing automation already uses the shared T2 (`manage_object.resource`)
      and `DbVerify.py` — no new plumbing added by this backfill.

## A. Bundle artifacts — `screens/Configuration/Assets/Facility_Objects/Deferment_Group/`
- [x] **1.** `deferment_group_sow.md` — rewritten 2026-08-28 to reflect the Batch 8/PR #479 shape +
      this session's access-regression finding.
- [x] **2.** `README.md` — rewritten 2026-08-28 with exact dryrun/live/DB-self-clean commands.
- [x] **3.** `JOURNAL.md` — rewritten 2026-08-28, modeled on Bank's JOURNAL.md (Built / Done well /
      Done wrong-or-lessons / Blockers -> resolution / Decisions / Evidence), sourced from PR #479's
      real body.
- **4.** Playwright driver — **N/A, permanently waived** (Section H of the deliverable checklist —
      Universal Screen Engine replaces hand-written drivers going forward). The pre-existing
      `py/deferment_group_iud.py` from before the waiver was left untouched, not deleted.
- **5.** `investigation/` — **N/A, permanently waived** (same Section H clause). Not built/refreshed.
- [x] **6.** `evidence/` — real artifacts added 2026-08-28: two live-attempt `log.html`/`output.xml`/
      screenshot sets (both FAILED, disclosed honestly), one dryrun `log.html`/`output.xml` (PASSED),
      `backfill_2026-08-28_access_check.txt` (the DB query that root-caused the failure), and — after
      the owner granted access the same day — `2026-08-28_access_regranted/` (live 5/5 PASS
      `log.html`/`output.xml`/`report.html`) + `2026-08-28_access_regranted_check.txt` (the before/after
      access grant + self-clean query). Pre-existing 2026-07-26 screenshots
      (`deferment_group_0[1-5]_*.png`, `rf_report.html`) kept as historical evidence of the
      pre-Batch-8 shape, not deleted.
- [x] **7.** `CHECKLIST.md` — this file.

## B. RF files (pre-existing, from PR #479 — NOT modified by this backfill)
- [x] **8.** T3 `pageobjects/Configuration/Assets/Facility_Objects/deferment_group_page.resource` —
      label-driven, properties-file-driven, T2-consolidated, grid-filter-wired (verified by reading
      the file 2026-08-28; unchanged from PR #479).
- [x] **9.** Suite `tests/Configuration/Assets/Facility_Objects/deferment_group_iud.robot` — TC01-05
      (clean-state / insert / update / find / delete), per-TC Login/Logout (verified by reading the
      file 2026-08-28; unchanged from PR #479).

## C. Verification gates
- [x] **10. robocop clean** — re-run 2026-08-28: page object `robocop check pageobjects/.../deferment_group_page.resource`
      → "No issues found" (exit 0). Suite → 9 issues (4 VAR02 + 5 DOC02), same baseline-noise class
      already accepted on every other Batch 7-11 suite per PR #479's own body — not a regression.
- [x] **11. `--dryrun` N/N PASS** — re-run 2026-08-28: `robot --dryrun tests/.../deferment_group_iud.robot`
      → **5/5 PASS, 0 failed** (`evidence/backfill_2026-08-28_dryrun/`). This is a static structure
      check only — does not require live EC access, so it is unaffected by item 12's failure below.
- [x] **12. LIVE headed/headless run N/N PASS** — **RE-VERIFIED 2026-08-28, PASS.** The owner granted
      the `SYST.ADM` role (the sandbox login role) access on `OBJECT_ID=1087` — confirmed live via a
      fresh `oracledb` connection: `SYST.ADM` = `LEVEL_ID 60` (was `0` at the time item 12 was first
      logged as blocked; the other 4 roles remain `0`, unaffected since they're not the sandbox login
      role). Re-ran the suite immediately after: `EC_HEADLESS=true robot tests/.../deferment_group_iud.robot`
      → **5/5 PASS**, all TCs (Clean State / Insert / Update / Find / Delete). See
      `evidence/2026-08-28_access_regranted/{log.html,output.xml,report.html}` and
      `evidence/2026-08-28_access_regranted_check.txt` (the before/after DB query + the run). The
      earlier two FAILED attempts (`evidence/backfill_2026-08-28_live_attempt{1,2}/`) are kept as
      historical record of the original blocker, not deleted or overwritten.
- [x] **13. DB ground-truth** — historical, PR #479: `Code Should Be Present/Absent In View
      OV_DEFERMENT_GROUP` (insert/find/delete) + `Field Should Equal In View OV_DEFERMENT_GROUP <code>
      NAME` (update), plus this session's own `SELECT ... FROM TV_T_BASIS_ACCESS WHERE OBJECT_ID = 1087`
      query that root-caused today's failure.
- [x] **14. FULL I-U-D scope** — historical, PR #479: Insert + Update + Delete + Find all present
      (TC02-05), confirmed by reading the suite/T3 2026-08-28 — the scope itself hasn't regressed,
      only live reachability has.
- [x] **15. Self-clean confirmed** — RE-VERIFIED 2026-08-28 after today's live 5/5 run: fresh
      `oracledb` connection, `SELECT COUNT(*) FROM OV_DEFERMENT_GROUP WHERE CODE =
      'AUTOTEST_DEFERMENT_GROUP'` → **0 residual rows**. See `evidence/2026-08-28_access_regranted_check.txt`.
- [x] **16. Hygiene PASS** — re-run 2026-08-28: `py scripts/check_bundle_hygiene.py` → repo-wide
      RESULT: PASS (no hardcoded creds, pure ASCII, no CHECKLIST/VERIFY-REPORT contradictions).

## D. Delivery
- [x] **17. Registry row** — already present, `docs/ec_screen_registry.md` line ~288 (PR #479, not
      re-touched by this backfill — no new automation-shape facts to add; the access-regression
      finding is a live-environment fact recorded in JOURNAL/SOW/this CHECKLIST instead).
- [x] **18. Scorecard row** — already present, `docs/automation-scorecard.md` (PR #479, not re-touched
      for the same reason as item 17).
- [x] **19. PR** — this backfill's own PR, standard 6-field body, base branch master, never self-merged.

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/deferment_group.md` — refreshed 2026-08-28
      to add the pattern name, grid-filter keywords, credential note, and the access-regression quirk
      (transcribed from the T3's own Variables section — not re-discovered).
- **21.** Reuse clause — N/A in the original 21-item numbering (this document uses the workorder's
      Section H item set, which does not carry item 21 forward as a separate gate for backfill tasks).

_Items 12/15 were left honestly unticked in this bundle's original PR (#642) — no command that day
proved a live PASS. Update 2026-08-28: the owner granted the `SYST.ADM` role access on
`OBJECT_ID=1087`; both items are now ticked on a real re-run, not a fabricated one — see the DB query
and live-run evidence cited above._
