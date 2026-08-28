# JOURNAL — Cost Object Mapping IUD

_Screen: Configuration > Assets > Financial Objects > Cost Object Mapping (OV, manage-object, no
navigator). View `OV_FIN_COST_OBJECT`. This JOURNAL was backfilled 2026-08-28 under the
retired-lean-waiver work order (`docs/lean-deliverable-backfill-workorder.md`, Batch 7; Section H
of `docs/IUD-DELIVERABLE-CHECKLIST.md`) — Cost Object Mapping was converted to the Bank pattern
via PR #442 (2026-08-23, Batch 4 of the Bank-pattern conversion project), which never produced
the SOW/README/JOURNAL/evidence/CHECKLIST/KB-map bundle under the then-active lean waiver. This
JOURNAL is built from PR #442's real body and this bundle's own pre-existing (2026-06-11) legacy
Playwright-era files, not invented._

## Built

### Original legacy build (2026-06-11, Playwright, superseded)
- A Playwright-based IUD driver (`playwright/ec_iud_cost_object_mapping.py`) with a full
  SOW/README/evidence/investigation bundle, using a per-run timestamped test code
  (`AUTOTEST_COM_<timestamp>`) and banner-discovered "first available option" dropdown values.
  This build predates the RF Bank-pattern conversion and is kept here as historical reference
  only — not re-run, not maintained.

### Bank-pattern conversion (PR #442, merged 2026-08-23, Batch 4)
- Converted the **Cost Object Mapping** screen from the older hardcoded-field-id/generated-code
  IUD suite to the label-driven, properties-file-driven, T2-consolidated "Bank pattern".
- Live recon confirmed this is NOT a scope mismatch despite the "Mapping" name — it is a genuine
  manage-object OV with generic Code/Name fields, not a linking-only grid.
- Files touched: `pageobjects/.../cost_object_mapping_page.resource` (rebuilt), `tests/.../
  cost_object_mapping_iud.robot` (rebuilt, 5-TC zero-argument business narrative),
  `testdata/cost_object_mapping_{insert,update,form_verify,grid_verify}.properties` (all new),
  `resources/credentials.py` (additive `COST_OBJECT_MAPPING_EC_USER`/`_EC_PASS`),
  `docs/ec_screen_registry.md`, `docs/automation-scorecard.md`,
  `docs/bank-pattern-conversion-checklist.md`, `docs/grid-filter-standardization-checklist.md`
  (updated).
- Switched the fixed test code from the legacy `AUTOTEST_COM_<timestamp>` to the current fixed
  `AUTOTEST_CMAP`, and from banner-discovered "first available option" dropdown values to real
  literal option text for all 4 mandatory dropdowns (Object Type/Cost Object/Company/Distribution
  Object Type).

### This backfill (2026-08-28)
- Added this `JOURNAL.md`, `CHECKLIST.md`, the KB selector map
  `ec-ui-knowledge/screens/cost_object_mapping.md`, refreshed `cost_object_mapping_sow.md` and
  `README.md` to describe the current RF-only implementation (the pre-existing versions of both
  described the superseded 2026-06-11 Playwright build), and added
  `evidence/backfill_2026-08-28/` (fresh dryrun + live re-run of the already-proven RF suite — no
  automation code touched). The legacy `playwright/`/`investigation/`/`evidence/*.png` folder
  contents from the 2026-06-11 build were left completely untouched.

## Done well
- Full I-U-D DB-verified vs `OV_FIN_COST_OBJECT` (insert Code/Name/Description/4 dropdowns,
  update Name/Description, delete End=Start absent); self-clean re-confirmed this backfill via a
  FRESH `oracledb` connection: 0 residual `AUTOTEST_CMAP` / `AUTOTEST%` rows, 90 total rows
  unchanged — identical to PR #442's original cited evidence.
- Live re-run 2026-08-28: **5/5 PASS on the first attempt**, no retry needed.
- `--dryrun` re-run 2026-08-28 (screen-scoped): **5/5 PASS**.
- Filter wiring re-confirmed: `grep -c 'name="Find Cost Object Mapping Row By Filter"'` on this
  backfill's own live `output.xml` = **5** (same count PR #442 cited).
- robocop re-run 2026-08-28: **9 issues total** (matches PR #442's cited "9 issues"), though the
  breakdown by rule differs slightly from the PR body's "4 VAR02 + 5 DOC02" — this session's run
  shows **2 VAR02 + 2 LEN32 + 5 DOC02 = 9**. Disclosed plainly, not smoothed over: the total count
  matches, the per-rule split does not, most likely a robocop version/ruleset drift between
  2026-08-23 and 2026-08-28 rather than a code change (no automation file was touched between the
  two runs). Not treated as a regression since the total and the DOC02 component both match
  exactly.

## Done wrong / lessons
- No regressions or wrong turns disclosed in PR #442's body for the original conversion.
- **Backfill-specific observation, disclosed here, not smoothed over:** the pre-existing bundle at
  this path (`cost_object_mapping_sow.md`, `README.md`) described the SUPERSEDED 2026-06-11
  Playwright build (different test-code convention, different dropdown-value strategy, Playwright
  positioned as primary) and had never been updated to reflect the 2026-08-23 RF conversion. This
  backfill refreshed both files to describe the current RF-only implementation while explicitly
  preserving the legacy content's provenance (dated, not deleted) rather than silently erasing the
  screen's real history.
- One transient environment glitch during this backfill session (an msys/bash stack-trace error on
  the first `robot --dryrun` invocation, unrelated to the RF suite itself) resolved cleanly on a
  single retry per the standing process rule — no chrome/node process was killed, no grinding past
  the one retry.

## Blockers -> resolution
- No hard blockers. The one transient bash/msys crash (see above) resolved on retry #1; the DB
  self-clean check and live run both passed cleanly without any workaround.

## Decisions
- Playwright bundle (`playwright/`, `investigation/`) stays as historical reference only —
  permanently waived from active maintenance per owner decision 2026-08-27
  (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H, items 4/5); the Universal Screen Engine is the
  owner-decided replacement for hand-written Playwright drivers going forward. Not deleted (real
  build history), but not re-run or extended either.
- The RF suite (`cost_object_mapping_page.resource` + `cost_object_mapping_iud.robot`) is the ONLY
  automation actively maintained for this screen going forward.
- Code lives in `ec-automation`; `ec-ui-knowledge/` stays MD-only.

## Evidence
- Original conversion (PR #442, 2026-08-23): live run 5/5 PASS, fresh `oracledb` post-run check
  0 residual `AUTOTEST_CMAP` rows (90 total unchanged), full-tree dryrun 740/740, robocop 9 issues
  (4 VAR02 + 5 DOC02 per the PR body), filter-fired grep = 5 — all cited in the PR body.
- This backfill (2026-08-28): `evidence/backfill_2026-08-28/` — `dryrun/` (5/5 PASS,
  `log.html`/`report.html`/`output.xml`) and `live/` (5/5 PASS headless, `log.html`/`report.html`/
  `output.xml` + per-TC screenshots), plus a DB self-clean result (`OV_FIN_COST_OBJECT`: 0
  `AUTOTEST_CMAP` rows, 0 residual `AUTOTEST%` rows, 90 total rows, fresh connection), a
  re-confirmed 5-hit filter-fired grep, a re-confirmed robocop total of 9 issues, and
  `py scripts/check_bundle_hygiene.py` -> `RESULT: PASS` (one unrelated pre-existing WARN about
  `Contract_Area/investigation/live_recon_contract_area.py`, not related to Cost Object Mapping).
- Legacy 2026-06-11 build: `evidence/cost_object_mapping_0[1-8]_*.png` +
  `evidence/cost_object_mapping_results.json` (historical, superseded, unmodified by this
  backfill).
