# JOURNAL - Well (CO.0049) OV-GM IUD (specific-values nav)

_Screen: Configuration > Assets > Well_and_Reservoir_Objects > Well. View `OV_WELL` (versioned)._
_This JOURNAL covers two events: the 2026-07-30 base build, and the 2026-08-26 Area-pattern
STRUCTURE conversion (PR #540). Backfilled 2026-08-27 (Batch 2 of
`docs/lean-deliverable-backfill-workorder.md` - the bundle had a base-build JOURNAL but was
missing the conversion's own entry, evidence refresh, and CHECKLIST)._

## Built

### 2026-07-30 - base build (branch `feature/well-iud-v2`)
- Previously PARKED: original scan found 5 mandatory nav dds with the 5th empty under the
  first-available AS1 path (fill timeout, grid never loaded).
- UNPARKED by owner screenshot: with only the standard 3-level cascade filled with SPECIFIC P1
  values (P1 Production Unit -> P1 Area -> P1 Facility 1) + GO, the grid lists wells while the
  2nd-row dds (Well & Well Hookup / Well) stay EMPTY - they are optional filters, and the park was
  a data-scope artifact of the AS1 path, not a structural blocker.
- DB pre-checks (real facts): BF CO.0049 (DefaultScreenTreeview); resolver matched
  ['WELL','FORECAST_WELL'] -> OV_WELL confirmed the live view by REAL lookup ('P1 W001 OP'
  present, 506 rows); P1 wells effective 2010-01-01 -> Start Date 2020-01-01.
- Built HAND-WRITTEN (no generator - specific nav values unsupported at the time): thin driver
  `py/well_iud.py` with screen-local `apply_well_navigator`; T3 with screen-local
  `Apply Well Navigator` on T1 `Select EC Dropdown Option` + `Apply Navigator`. Insert: Well Type
  first-available; NO Op Production Unit field on this form (rows list under the nav scope
  regardless, like Facility Class 1).
- `verify_screen.py` -> OVERALL PASS: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4 pass,
  Playwright 8/8. DB residual 0.

### 2026-08-26 - Area-pattern STRUCTURE conversion (PR #540, branch `feature/well-area-pattern`)
- Converted Well's RF IUD automation from its OLD pattern (4 TCs, suite-level login, timestamped
  test code, inline DB-verify calls) to the full Area-pattern structure (5 TCs, per-TC login,
  fixed test code, properties-file-driven, shared navigator keyword), while keeping Well's genuine
  3-level P1 navigator cascade unchanged.
- Files touched: `pageobjects/.../well_page.resource` (rewrite), `tests/.../well_iud.robot`
  (rewrite), `testdata/well_{navigator,insert,update,form_verify,grid_verify}.properties` (new),
  `resources/credentials.py` (additive: `WELL_EC_USER`/`WELL_EC_PASS`),
  `docs/automation-scorecard.md` (Well row updated in place).
- Navigator fill delegated to the existing shared T2 `Apply Navigator From Properties`
  (`resources/manage_object.resource`) - already documented there as a proven 3-level-cascade case
  for Well specifically; **no shared-file changes made by this PR**.
- Well Type's mandatory first-available dropdown preserved via the existing `__FIRST__` sentinel.
- Zero inline DB-verify calls remain in the `.robot` file - DB verification now lives only inside
  the shared T2 `Verify Object Removed`.
- Scope guard respected: only Well (CO.0049) files touched - Well Mode, Well Hole, Well Bore, Well
  Bore Interval, Well Hookup untouched.

## Done well
- Full I-U-D DB-verified vs `OV_WELL` for both the base build and the conversion; self-clean 0
  residual confirmed both times via a fresh oracledb connection.
- The Area-pattern conversion produced a real, cited N/N: live 5/5, full-tree dryrun 850/850 (zero
  new failures vs. baseline at the time), robocop parity with Area's own baseline (7 issues both,
  same VAR02/DOC02 categories), grid-filter keyword confirmed firing 14x via output.xml grep.
- This backfill's own fresh re-run (2026-08-27, no automation changes) reproduces the same result:
  live 5/5 PASS, full-tree dryrun 883/883 PASS (grown since PR #540 from later unrelated batches,
  zero failures = no regression), fresh-connection DB self-clean `AUTOTEST_WELL` = 0 rows, hygiene
  PASS, robocop 7 issues (same categories, unchanged).

## Done wrong / lessons
- **Regression-canary role, disclosed separately from PR #540's own body:** BEFORE PR #540
  converted Well's own navigator-fill logic, Well was used - UNCHANGED, still on its OLD bespoke
  `Apply Well Navigator` keyword and 4-TC structure - as one of TWO regression canaries when the
  shared T2 `Apply Navigator From Properties` keyword was first added to
  `resources/manage_object.resource` for the Area conversion. Per `docs/automation-scorecard.md`'s
  Area (CO.0003) row: "2 existing OV-GM canary screens with their OWN bespoke navigator-fill logic
  re-run live UNCHANGED to prove zero regression from the shared-file addition: Well 4/4, Test
  Separator 4/4." This is a real fact worth flagging here rather than smoothing over: PR #540's own
  body does NOT mention this canary role (it only describes Well's OWN conversion) - the canary
  event happened earlier, in the separate Area PR, and is only visible by cross-referencing the
  scorecard. A reader relying on PR #540 alone would miss that Well had already been load-bearing
  for a DIFFERENT screen's shared-file safety check before its own conversion landed.
- **Base-build lesson (#265) applied:** registry/scorecard rows were column-diffed vs the Channel
  sibling; nav column states SPECIFIC P1 values (not the template first-available text).
- Second confirmation (after Lifting Account) that "deep cascade with an empty level" parks are
  DATA-SCOPE gaps: one owner-provided working scope resolves them in a single pass.
- A scan's "mandatory" flag on extra nav dds can be scope-dependent: under the P1 path the 2nd-row
  Well dds were ignorable filters.

## Blockers -> resolution
- Base build: none once unparked by the owner screenshot (see above) - no live blocker during the
  actual build.
- Conversion (PR #540): none disclosed in the PR body; robocop/hygiene/dryrun/live all passed
  first-cited.
- This backfill (2026-08-27): none - dryrun, live run, DB self-clean, hygiene, and robocop all
  reproduced clean on the first attempt; no stray `chrome.exe` processes found before the live run
  (checked via `tasklist`, only `chrome-headless-shell.exe`/`chrome-native-host.exe` present).

## Decisions
- Do NOT rebuild or re-verify from scratch for this backfill - the RF suite, registry row, and
  scorecard row already exist and are already merged (owner instruction, `docs/lean-deliverable-
  backfill-workorder.md`). This task adds documentation/evidence artifacts only.
- Playwright driver (`py/well_iud.py`) stays waived from a new build per Section H of
  `docs/IUD-DELIVERABLE-CHECKLIST.md` (items 4/5 - Universal Screen Engine supersedes it).
- Kept the original 2026-07-30 `VERIFY-REPORT.md` as a historical record rather than deleting or
  overwriting it with a fabricated re-run against the 4-TC shape it no longer matches; fresh
  evidence for the CURRENT 5-TC suite lives in `evidence/` instead.

## Evidence
- Base build (2026-07-30): `VERIFY-REPORT.md` in this folder (robocop 0, hygiene 0, dryrun 4/4,
  live RF 4/4, Playwright 8/8).
- Area-pattern conversion (PR #540, 2026-08-26): cited inline in the PR body - live 5/5, full-tree
  dryrun 850/850, fresh-connection DB self-clean 0 residual, filter-keyword grep = 14, robocop
  parity (7 issues) vs Area's baseline.
- This backfill (2026-08-27): `evidence/` folder - `output.xml`/`log.html`/`report.html` from a
  fresh live headless run (5/5 PASS), plus this JOURNAL's own citations above for the fresh dryrun
  (5/5 single-suite, 883/883 full-tree), DB self-clean, hygiene, and robocop re-runs.
