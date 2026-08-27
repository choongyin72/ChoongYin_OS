# JOURNAL - Calculation Context (CO.1059) OV IUD

_Screen: Configuration > Assets > Calculation_Objects > Calculation Context, OV (manage-object,
date-effective, plain Bank-family). View `OV_CALC_CONTEXT`. Distinct sibling screen from
Calculation Group Context (CO.0245) - do not confuse the two; each has its own bundle/registry row._

_This JOURNAL's 2026-08-28 section was backfilled under `docs/lean-deliverable-backfill-workorder.md`
(Batch 9, owner decision 2026-08-27 retiring the 2026-08-23/26 lean waiver - Section H of
`docs/IUD-DELIVERABLE-CHECKLIST.md`). The RF automation described below (PR #456/#514) was already
built and merged before this backfill session; this JOURNAL narrates what those PRs' bodies actually
recorded - it is not a new build and no automation file was touched to produce it._

## 2026-07-26 (PR #214, original build)
- **Branch:** `feature/calculation_context-iud` (own branch, stacked so the shared-engine helpers are
  present). Check-existing gate: only this build; reused shared engine + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only): DB `CLASS_TYPE=OBJECT` -> OV; treeview
  Configuration > Assets > Calculation_Objects > Calculation Context. Mandatory Code/Name/Start Date;
  optional dropdowns skipped. Plain Bank-layout OV (single Date+GO nav, no mandatory dropdowns).
- **Label-driven** T3 (no hardcoded ids). Playwright driver -> 7/7; RF T3+suite -> live 4/4 (TC01-04,
  no Find TC yet).
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4, Playwright
  7/7.

## 2026-08-23 (PR #456, Batch 7 of the Bank-pattern conversion project)
- **Built:** rebuilt `calculation_context_page.resource` + `calculation_context_iud.robot` on top of
  the existing partial label-driven build to full Bank-pattern parity: properties-file-driven
  Insert/Update (`testdata/calculation_context_{insert,update,form_verify,grid_verify}.properties`,
  new), explicit `Find/Clear Calculation Context Row By Filter` grid-filter wiring wired into
  Update/Find/Verify-Found/Delete, a dedicated `CALC_CONTEXT_EC_USER`/`CALC_CONTEXT_EC_PASS`
  credential pair (additive to `resources/credentials.py`), per-TC login/logout on one browser opened
  once in Suite Setup, and a new TC04 Find (5-TC total: clean-state/insert/update/find/delete).
- **Done well:** live 5/5 pass; DB self-clean confirmed via a FRESH oracledb connection
  (`OV_CALC_CONTEXT` WHERE CODE='AUTOTEST_CALCCTX' -> 0); TC02/TC03 DB-verified via
  `Field Should Equal In View OV_CALC_CONTEXT` on NAME/DESCRIPTION/COMMENTS at the time; robocop
  clean (exit 0); full `tests/` tree dryrun 753/753 pass; grid-filter keyword confirmed fired via
  output.xml grep (12x `Find Calculation Context Row By Filter`, 8x
  `Filter Grid Text Column By Value`). No shared T1/T2 file changes needed - screen genuinely
  Bank-shaped (no mandatory nav dropdown beyond the universal GO bar, confirmed via live recon).
- **Rules applied** (per PR #456's own body, `tmp/batch7_shared_findings.md`): isolated
  sparse-checkout clone under `Workplaces/calculation_context/`; live recon before any new config
  (field labels, mandatory set, grid columns, DB view all confirmed live before writing config); no
  shared T1/T2 changes; reused T2's consolidated keywords as-is; fixed test code `AUTOTEST_CALCCTX`
  (confirmed free live).

## 2026-08-25 (PR #514, "remove inline DB-verify from 3 remaining Bank-pattern suites")
- **Done wrong / lesson (disclosed, not smoothed over):** a Reviewer sweep (Issue #504) found
  Calculation Context was one of 3 suites still carrying a screen-local DB-verify deviation from
  Bank's owner-requested pure-screen-only verification convention (2026-08-18) - the SAME deviation
  class already fixed on County (PR #489), DOA Credit Limit (PR #503), and Document Template
  (PR #505). Specifically: a leftover `Calculation Context Should Exist In DB` keyword + its TC02
  call, plus 5 direct `Field Should Equal In View` calls across TC02/TC03, survived the PR #456
  conversion even though that PR's own stated goal was Bank-pattern PARITY.
- **Resolution:** removed the keyword, its TC02 call, and the 5 direct DB-verify calls; added a
  pure-screen-verify Documentation note; de-staled 2 Variables-section "DB-verifies" comments. T3/page
  object untouched. Coverage NOT reduced - T2's `Verify Calculation Context Record Exists/Updated`
  (already delegated to by this screen's own wrapper keywords) performs the equivalent pure-screen
  field comparison, and TC05's DB ground-truth on delete already lived in the shared T2
  `Verify Object Removed`.
- **Done well:** re-verified live 5/5 (individual suite run), full-tree dryrun 841/841, DB self-clean
  via a fresh connection (`OV_CALC_CONTEXT` WHERE CODE='AUTOTEST_CALCCTX' -> 0). Robocop showed only
  new `VAR02` (unused-variable) findings, an expected side effect of removing the code that consumed
  those variables - accepted, same outcome as the precedent Document Template fix (PR #505).

## Lessons (cumulative)
- Plain OV; generic engine handled appear/absent/pagination with zero screen-specific tuning
  (2026-07-26).
- A "Bank-pattern conversion" PR brings the STRUCTURE (5-TC, filter wiring, properties files) but does
  not automatically strip an older suite's own bespoke DB-verify calls if they predate the
  conversion - a converted suite still needs an explicit pure-screen-verify audit against Bank's own
  convention, which is what PR #514 supplied here after a Reviewer sweep caught the gap (2026-08-25).

## Blockers -> resolution
- No hard blockers across any of the 3 PRs (#214, #456, #514) - each merged same-session with clean
  evidence; the only "blocker" was the PR #514 deviation itself, resolved by that PR.

## Decisions
- Calculation Context stays classified plain OV (Bank family) throughout - PR #456 changed the
  suite's STRUCTURE to Bank-pattern parity, not the screen's classification (it was already Bank-
  shaped, unlike Area/Well which are OV-GM).
- The Playwright driver (`py/calculation_context_iud.py`) and `investigation/` were left untouched by
  PR #456/#514 and by this backfill - per Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`
  (2026-08-27), the Playwright bundle stays permanently waived for Bank-/Area-pattern work (the
  Universal Screen Engine replaces that role going forward); the pre-existing bundle here is kept as
  historical reference, not rebuilt.

## Evidence
- PR #214 (2026-07-26): Playwright `calculation_context_0[1-5]_*.png` (7/7) + `rf_report.html`
  (RF 4/4) - see `evidence/`.
- PR #456/#514: cited live 5/5 (x2) results, full-tree dryrun 753/753 then 841/841, DB self-clean
  0/0, robocop exit 0 then VAR02-only delta - see PR bodies (`gh pr view 456`, `gh pr view 514`) for
  the exact commands/output cited.
- **This backfill session (2026-08-28):**
  - `py -m robot --dryrun tests/Configuration/Assets/Calculation_Objects/calculation_context_iud.robot`
    -> **5/5 PASS**.
  - `py -m robot --dryrun tests/` (full tree) -> **883/883 PASS**.
  - `py -m robocop check calculation_context_page.resource calculation_context_iud.robot` -> **13
    issues**, all DOC02 (missing `[Documentation]` on TC03/TC04/TC05 and several keywords) - baseline
    style noise, no functional finding, no regression introduced by this backfill (no automation file
    touched).
  - `EC_HEADLESS=true py -m robot --outputdir .../evidence tests/.../calculation_context_iud.robot`
    -> **5/5 PASS**, clean first run, no flake.
  - DB self-clean: `DbVerify.view_count_where("OV_CALC_CONTEXT", "CODE", "AUTOTEST_CALCCTX")` ->
    **0** (fresh connection, confirmed absent).
  - `py scripts/check_bundle_hygiene.py` (repo-wide) -> **PASS** (167 bundles + 272 recon scripts
    scanned; the one pre-existing WARN is on Contract Area's `investigation/`, unrelated to this
    screen).
  - Evidence artifacts added to `evidence/`: `log.html`, `output.xml`, `report.html`,
    `playwright-log.txt`, per-TC screenshots (`TC0N ..._{login,open_screen,action,verify,logout}.png`)
    from this run, alongside the pre-existing 2026-07-26 Playwright evidence (unchanged).
