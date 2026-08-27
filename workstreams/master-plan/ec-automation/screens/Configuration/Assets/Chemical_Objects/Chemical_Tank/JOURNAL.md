# JOURNAL - Chemical Tank (CO.0070) OV-GM IUD

## 2026-07-30
- **Branch:** `feature/ov-gm-chemical-tank` (stacked on the gated-navigator capability, PR #244).
  Check-existing gate: grep ec-automation -> only this build; reused shared engine (ec_object_iud.py) + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only + tmp/chemical_tank/config.json scan): OV-GM (grid
  `manageObject:form:T_data`), navigator cascade Production Unit -> Area -> Facility Class 1. Mandatory Chemical Tank Code / Chemical Tank Name / Start Date + dropdowns Measure unit.
- **Built** (generator `tmp/gen_ovgm.py` -> proven Node/Chemical-Tank template): label-driven T3 (no hardcoded
  ids); Playwright driver + RF T3/suite. Op Production Unit set first-available for grid visibility.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4 pass, Playwright 8/8. DB residual 0.

## Lessons (from the original 2026-07-30 build)
- OV-GM: first-available nav scope + Op PU first-available lists the row after GO (parent-dd need not equal
  the nav PU - probe per screen). Generic engine handled cascade/appear/absent/pagination with zero tuning.

## 2026-08-26 — Area-pattern conversion (PR #549)

### Built
Converted the screen's RF suite from its original suite-level-login/4-TC shape to Area's full
5-TC pattern (adds TC04 Find), per-TC login/logout, fixed test code `AUTOTEST_CT`, explicit
grid-filter wiring (`Find/Clear Chemical Tank Row By Filter`), and the shared T2
`Apply Navigator From Properties` keyword driving the screen's genuine 3-level
Production Unit -> Area -> Facility Class 1 navigator cascade via a new
`testdata/chemical_tank_navigator.properties` (values: `Op Production Unit=AS1 EC Exploration
Norway`, `Op Area=AS1_Area`, `Op Facility Class 1=AS1_Facility_01` — the same values the prior
first-available cascade already resolved to, captured live).

### Done well
- Reproduced the real TC02 timeout live (`tmp/recon_ct_insert_exact_properties_order.py`) before
  writing any fix, instead of guessing a cause.
- Full-tree dryrun 850/850 both before and after the fix — no regression to the other 849 tests.
- Robocop parity confirmed side-by-side against Area's/Facility Class 1's own baseline (13 issues,
  identical count) rather than assumed clean.

### Done wrong / lessons — the `__FIRST__` gotcha
Area's own rule is that a converted OV-GM/navigator screen's insert-form "Op Production Unit" (or
equivalent parent-scope dropdown) must be forced to equal the navigator's own PU value, or the
newly-inserted row is invisible under the navigator's scope. Applying that rule unedited to
Chemical Tank produced a reproducible live TC02 timeout: this screen's insert-form "Op Production
Unit" dropdown becomes FILTERED once Start Date/Measure unit are set, and its filtered option list
does **not** include the navigator's own PU value at all — so there is no way to force it to match.
Root-caused before touching code (per CLAUDE.md's "verify, don't guess" rule) via a live recon
script, not a hypothesis. Resolution: kept `Op Production Unit=__FIRST__` in
`chemical_tank_insert.properties`, matching the already-proven pre-existing Playwright driver's
real behavior (`py/chemical_tank_iud.py`, unchanged) — the same class of issue previously seen on
Chemical Injection Point and Production Separator, where a screen's dropdown scope does not
mechanically match Area's own field. Documented the finding in three places rather than silently
working around it: the properties file, the page object's Documentation block, and the registry row.

### Blockers -> resolution
- **Blocker:** TC02 (Insert) timed out live when Op Production Unit was forced to the nav's PU value.
  **Resolution:** live recon proved the dropdown's option list is filtered and excludes that value;
  reverted that one field to `__FIRST__`; TC02 passed on retest, full suite went live 5/5.

### Decisions
- Screen classification stays OV-GM (genuine 3-level cascade), not reclassified as plain
  Bank-shaped, per the owner's Area-is-role-model standing rule for navigator screens.
- Playwright driver (`py/chemical_tank_iud.py`) left unchanged — still the proven flow; this
  conversion only touched the RF layer.

### Evidence (PR #549)
- Live 5/5: `EC_HEADLESS=true robot tests/Configuration/Assets/Chemical_Objects/chemical_tank_iud.robot`
  → TC01-TC05 all PASS.
- Full-tree dryrun: `robot --dryrun tests/` → 850/850 passed, 0 failed (before and after the fix).
- DB self-clean: fresh `oracledb` connection, `SELECT CODE, NAME FROM OV_CHEM_TANK WHERE CODE LIKE
  'AUTOTEST%'` → `[]` (0 residual rows), both before and after the live run.
- Grid-filter keyword fired: `grep -c "Find Object Row By Filter" output.xml` → 15 (non-zero).

## 2026-08-28 — Documentation/evidence backfill (Batch 4, owner decision 2026-08-27)
Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md` retired the 2026-08-23/26 lean waiver; this entry
and the refreshed SOW/README/CHECKLIST/KB-map backfill the artifacts that waiver skipped for the
PR #549 conversion above. No RF automation file was touched by this backfill — the existing suite,
page object, and Playwright driver are unchanged. A one-time live re-run was executed to capture
fresh evidence (see `evidence/` and `CHECKLIST.md` for the exact result and citation).
