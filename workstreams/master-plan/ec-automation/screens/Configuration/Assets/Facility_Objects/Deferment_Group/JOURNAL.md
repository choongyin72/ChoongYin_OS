# JOURNAL — Deferment Group (CO.0149) OV IUD

_Screen: Configuration > Assets > Facility_Objects > Deferment Group (OV, date-effective, plain
Bank-pattern). View `OV_DEFERMENT_GROUP`. This JOURNAL was rewritten 2026-08-28 to model
`screens/Configuration/Assets/Financial_Objects/Bank/JOURNAL.md`'s structure, per
`docs/lean-deliverable-backfill-workorder.md` (Batch 11, last screen) — the previous version
(2026-07-26) predated the Batch 8 Bank-pattern rebuild and is superseded._

## Built
- **2026-07-26 (original build, superseded):** label-driven Playwright driver (`py/deferment_group_iud.py`,
  7/7) + a first-generation RF T3/suite (label-driven but without the shared T2 grid-filter wiring),
  built on the shared OV engine + `DbVerify.py`. Live RF 4/4 at that time.
- **2026-08-23, PR #479 (Batch 8 of the Bank-pattern-conversion project) — the current shape:**
  `pageobjects/.../deferment_group_page.resource` rebuilt to mirror Bank/State/Berth exactly —
  label-driven, properties-file-driven (`deferment_group_{insert,update,form_verify,grid_verify}.properties`),
  T2-consolidated, explicit grid-filter keywords (`Find/Clear Deferment Group Row By Filter` ->
  shared T2 `Find/Clear Object Row By Filter`). Suite rebuilt to TC01-05 (clean-state / insert /
  update / find / delete) with per-TC Login/Logout, matching the Batch 7-11 suite-style convention.
  Added dedicated `DEFERMENT_GROUP_EC_USER`/`DEFERMENT_GROUP_EC_PASS` to `resources/credentials.py`.

## Done well
- Full I-U-D-Find, DB-verified vs `OV_DEFERMENT_GROUP` (insert Code/Name, update Name, delete via
  End Date = Start Date), self-clean 0 residual — confirmed at PR #479 merge time via a fresh,
  independent `oracledb` connection (not the RF library's own state).
- Grid-filter keyword usage confirmed fired for real (not just present in code): `grep -c "Find
  Object Row By Filter" output.xml` -> 15 hits across TC02-05 at merge time.
- Zero hardcoded field ids anywhere in the T3 — everything resolves BY LABEL via the shared T2
  `Fill OV * By Label` / `OV Field Id By Label` helpers.
- One PR, one screen, sync-with-master-before-push done correctly: PR #479's own body notes a
  non-conflicting `credentials.py` merge conflict (Batches 9-11 had landed since this clone's last
  sync) resolved manually, keeping both sides' new constants.

## Done wrong / lessons
- The original 2026-07-26 build was declared "done" (verify_screen.py OVERALL PASS at the time) but
  left the screen on an older RF shape without the T2 grid-filter convention that Bank/State/Berth
  later standardised on (2026-08-22 owner decision) — it needed a full re-conversion (PR #479), not
  a small patch, once that standard was set. Lesson already generalised in this project: a screen's
  "done" status from an earlier convention doesn't survive a later pattern-standardisation decision
  without an explicit re-conversion pass.
- **This backfill session (2026-08-28) found the same "screen unreachable via menu search" symptom
  from the ORIGINAL Batch 8 blocker has RECURRED** — see "Blockers -> resolution" below. This is
  disclosed here rather than smoothed over, per this project's rule that a repeated live-run failure
  is a stop-and-ask signal, not something to script around.

## Blockers -> resolution
- **Original blocker (2026-08-23, PR #479's own body):** `TV_T_BASIS_ACCESS` had `LEVEL_ID=0`
  ("No access") for ALL 5 roles configured against this screen object (`OBJECT_ID=1087`,
  `/com.ec.frmw.co.screens/manage_object_nav/CLASS_NAME/DEFERMENT_GROUP`) — the menu-search link was
  unreachable regardless of role, a live-sandbox role-access gate, not a code defect (root-caused and
  tracked as item 3 in `docs/universal_screen_engine_open_items.md`, "Not a code fix... a live-sandbox
  permissions/security config, out of scope to change without explicit authorization"). The rebuilt
  work sat uncommitted in `Workplaces/deferment_group` rather than being merged untested. The owner
  granted sysadmin-role access in the sandbox; PR #479 re-verified live access first (login + menu
  search actually found and opened the screen), then ran the full live gate (5/5 PASS) before raising
  the PR. Resolved at that time.
- **REGRESSION found 2026-08-28 (this backfill session):** re-running the suite live, purely to
  capture fresh evidence for this backfill task (no automation changes intended or made), reproduced
  the exact same symptom — `TimeoutError: locator.waitFor: Timeout 10000ms exceeded` waiting for the
  `Deferment Group` tv-link, on ALL 5 test cases, on BOTH an initial attempt and one retry (per this
  project's "retry once, then disclose" rule — no further scripts were written to test alternate
  theories, per the "NEVER DO BLIND TEST" standing rule). Root-caused via a single direct DB query
  (not a guess): `SELECT OBJECT_ID, ROLE_ID, LEVEL_ID FROM TV_T_BASIS_ACCESS WHERE OBJECT_ID = 1087`
  returned `LEVEL_ID=0` for all 5 roles (`INST.MAN`, `OP`, `RES`, `SUP`, `SYST.ADM`) — **the same
  access grant that unblocked PR #479 has since regressed in this sandbox.** This is a live-environment
  fact, not an automation defect, and is **NOT resolved by this backfill task** (out of scope — a
  role-access grant is a real, consequential sandbox security-config change requiring its own explicit
  owner authorization, same conclusion as the original blocker). Flagged here, in the SOW, and in
  CHECKLIST.md rather than silently worked around or assumed fixed.

## Decisions
- The RF automation itself (T3, suite, testdata, credentials) was **NOT modified** as part of this
  backfill — this task is documentation/evidence only, per its own scope instruction.
- Registry/scorecard rows (`docs/ec_screen_registry.md`, `docs/automation-scorecard.md`) already
  document PR #479's rebuild in full and are NOT re-touched by this backfill (no new facts to add
  there; the access-regression finding lives in this JOURNAL/SOW/CHECKLIST instead, since it's a
  live-environment state, not a change to the automation's own shape).
- Kept the 2026-08-23 evidence (PR #479's own citations: 5/5 live, 774/774 dryrun, 15 filter hits, 0
  residual) as the historical proof of a working, previously-verified suite; added the 2026-08-28
  re-verification attempt (failed, disclosed) as a SEPARATE, dated entry rather than overwriting or
  hiding the earlier PASS.

## Evidence
- **2026-08-23 (PR #479 merge time, historical):** live RF 5/5, cited in the PR body; full-tree
  dryrun 774/774; robocop page object 0 issues; 15 `Find Object Row By Filter` hits in `output.xml`;
  DB self-clean 0 residual via a fresh `oracledb` connection.
- **2026-08-28 (this backfill session):**
  - `evidence/backfill_2026-08-28_live_attempt1/` and `evidence/backfill_2026-08-28_live_attempt2/` —
    `log.html` + `output.xml` + per-TC login/logout screenshots from the two live attempts, both
    0/5 PASS with the menu-search timeout described above.
  - `evidence/backfill_2026-08-28_dryrun/` — `--dryrun` re-run, 5/5 PASS (static structure only,
    doesn't touch live access).
  - `evidence/backfill_2026-08-28_access_check.txt` — the exact `TV_T_BASIS_ACCESS` query + result
    that root-caused the regression (`LEVEL_ID=0` for all 5 roles on `OBJECT_ID=1087`).
  - Pre-existing `deferment_group_0[1-5]_*.png` + `rf_report.html` (2026-07-26) — kept as historical
    evidence of the PRE-Batch-8 shape; superseded by PR #479's own (uncaptured-as-files, PR-body-cited)
    5/5 evidence for the current shape.
