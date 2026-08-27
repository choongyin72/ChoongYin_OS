# JOURNAL — Contract Capacity (CO.2044) OV-GM IUD

_Screen: Configuration > Assets > Contract Objects > Contract Capacity (OV-GM, groupmodel
manage-object, navigator-GATED, date-effective). View `OV_CONTRACT_CAPACITY`._

## Built

### 2026-08-01 — original build
- Branch `feature/contract-capacity-iud`. Check-existing gate: 0b grep ec-automation → only this
  build (0 other files referenced `contract_capacity`); reused shared engine
  (`py/ec_object_iud.py`) + T2 + `DbVerify.py`.
- Recon (`investigation/recon.py`, read-only): OV-GM (grid `manageObject:form:T_data`). Nav:
  Business Unit dropdown + GO. Mandatory Contract Capacity Code / Contract Capacity Name / Start
  Date + dropdowns Contract Name = `TS5 Shipper B Firm`, Location Name =
  `TS5 Domestic Gas Storage`.
- Built label-driven T3 (no hardcoded ids) + Playwright driver + a 4-TC RF suite (single
  suite-level login, hardcoded field-id inline DB-verify wrappers
  `Insert/Update Contract Capacity Record`, `Contract Capacity Should/Should Not Exist In DB`,
  timestamped test code `AUTOTEST_CC<timestamp>`).
- `verify_screen.py` → OVERALL PASS: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4 pass,
  Playwright 8/8. DB residual 0.

### 2026-08-26 — Area-pattern conversion (PR #535)
Under the owner's 2026-08-26 standing rule that any navigator-section screen matching Area's
layout follows Area's full pattern, Contract Capacity's RF automation was converted from the OLD
4-TC/single-login/hardcoded shape to Area's full pattern:
- 5 TCs (added TC04 Find), per-TC login/logout.
- Navigator fill delegated to the shared T2 `Apply Navigator From Properties`, driven by a new
  `contract_capacity_navigator.properties` (Business Unit = `TS5 BU`, the SAME value the
  pre-existing driver already proved live — a real cross-check, not a re-derived value).
- Fixed test code `AUTOTEST_CONTRACT_CAPACITY` (replacing the timestamped `AUTOTEST_CC<ts>`).
- Properties-file-driven insert/update via the shared T2
  `Insert/Update Object From Properties` (`testdata/contract_capacity_{insert,update,form_verify,grid_verify}.properties`).
- Explicit `Find/Clear Contract Capacity Row By Filter` grid-filter wiring into
  Update/Find/Verify-Found/Delete — 15 `Find Object Row By Filter` hits confirmed in output.xml.
- PURE SCREEN verification only — zero inline DB-verify calls remain in
  `contract_capacity_iud.robot` (confirmed via grep).
- Evidence cited in PR #535: robocop 7 issues (exact parity with Area's own reference-pattern
  baseline), full-tree dryrun 850/850, live 5/5, fresh-connection DB self-clean 0, filter-fired
  grep 15 hits, inline-DB-verify grep 0 hits. No shared T1/T2 file changes that round. Playwright
  driver `py/contract_capacity_iud.py` left UNTOUCHED (RF structural conversion only).

### 2026-08-28 — documentation/evidence backfill (this task, Batch 4)
Owner decision 2026-08-27 retired Section G's lean waiver: SOW/README/JOURNAL/evidence/
CHECKLIST/KB map must be backfilled for every Bank-/Area-pattern screen converted since
2026-08-23. This task adds those artifacts around Contract Capacity's already-converted,
already-working automation — **no automation file touched**. Re-ran the existing suite once for
fresh evidence (see "Blockers → resolution" below for a flake hit during that run).

## Done well
- The Business Unit navigator value (`TS5 BU`) required NO re-derivation — it was already proven
  live by the original 2026-08-01 driver, and PR #535 carried it forward unchanged. A genuine
  cross-check between two independently-built automation layers (Playwright driver vs RF T3)
  landing on the same real value.
- Zero inline DB-verify calls in the converted suite — pure screen verification, consistent with
  every other Area-pattern-converted screen.
- This backfill's dryrun (5/5) and DB self-clean (0 residual, fresh connection) both reproduced
  cleanly, confirming PR #535's original evidence still holds two days later.

## Done wrong / lessons
- **Backfill evidence-capture flake (2026-08-28):** the first live run of this backfill task hit
  a TC05 failure — `Row AUTOTEST_CONTRACT_CAPACITY should NOT exist in manageObject:form:T_data:
  1 != 0` — immediately after the delete+GO refresh. Per the T3's own documented quirk ("OV-GM
  grids redraw lazily after Save+GO"), this reads as a screen-render lag, not a DB residual: TC01
  Verify Clean State on the very next run (retry) passed, meaning no leftover row was actually
  present in the DB. One retry (per the process rule for this task) passed 5/5 clean. Disclosed
  here rather than silently re-run-until-green; no automation file was touched to "fix" it.
- The 2026-08-01 build's original CHECKLIST/README/VERIFY-REPORT still described the
  pre-conversion 4-TC/8-Playwright-only gate shape and were not updated at the time of the
  2026-08-26 Area-pattern conversion (PR #535 only touched RF + testdata + registry/scorecard
  rows, not this bundle) — this backfill is what closes that gap.

## Blockers → resolution
- No hard blockers. The one flake (TC05, attempt 1) self-resolved on the single permitted retry;
  no data damage, no automation edit.

## Decisions
- Playwright driver (`py/contract_capacity_iud.py`) and `investigation/recon.py` stay UNCHANGED —
  historical reference only; the Universal Screen Engine is the owner-decided replacement for new
  Playwright work, so no new driver/investigation artifact is produced by this backfill.
- `VERIFY-REPORT.md` (auto-generated 2026-08-01, 4-TC shape) is left as a historical record rather
  than regenerated — `scripts/verify_screen.py` was built for the original build's shape; this
  JOURNAL + the `evidence/backfill_2026-08-28/` folder carry the current 5-TC evidence instead.

## Evidence
- Original build (2026-08-01): `evidence/CC_0[1-5]_*.png` + `evidence/results.json`.
- Area-pattern conversion (PR #535, 2026-08-26): cited in this JOURNAL's "Built" section above
  (robocop 7, dryrun 850/850, live 5/5, self-clean 0, filter-fired grep 15, inline-DB-verify grep
  0) — see PR #535 body for the full citation.
- This backfill (2026-08-28): `evidence/backfill_2026-08-28/` — dryrun 5/5, live attempt 1
  (`output_attempt1_TC05fail.xml`, 4/4+1 flake), live retry (`output.xml`/`log.html`/`report.html`,
  5/5), DB self-clean 0 (fresh oracledb connection), `results_summary.md`.
