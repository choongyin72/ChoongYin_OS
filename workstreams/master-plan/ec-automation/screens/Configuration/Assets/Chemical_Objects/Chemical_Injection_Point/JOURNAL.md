# JOURNAL - Chemical Injection Point (CO.0212) OV-GM IUD

_This JOURNAL was extended 2026-08-27 under `docs/lean-deliverable-backfill-workorder.md`
(Batch 2, owner decision retiring the 2026-08-23/26 lean waiver - Section H of
`docs/IUD-DELIVERABLE-CHECKLIST.md`). The 2026-08-26 section below narrates PR #550's own real
body/commit content; the backfill session content is its own dated section. No automation file was
touched to produce either addition - the RF suite already existed and was already merged._

## 2026-07-30
- **Branch:** `feature/ov-gm-chem-injection-point` (stacked on the gated-navigator capability, PR #244).
  Check-existing gate: grep ec-automation -> only this build; reused shared engine (ec_object_iud.py) + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only + tmp/chem_injection_point/config.json scan): OV-GM (grid
  `manageObject:form:T_data`), navigator cascade Production Unit -> Area -> Facility Class 1. Mandatory Chem Inj Point Code / Chem Inj Point Name / Start Date.
- **Built** (generator `tmp/gen_ovgm.py` -> proven Node/Chemical-Tank template): label-driven T3 (no hardcoded
  ids); Playwright driver + RF T3/suite. Op Production Unit set first-available for grid visibility.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4 pass, Playwright 8/8. DB residual 0.

## Lessons (original build)
- OV-GM: first-available nav scope + Op PU first-available lists the row after GO (parent-dd need not equal
  the nav PU - probe per screen). Generic engine handled cascade/appear/absent/pagination with zero tuning.

## 2026-08-26 (PR #550) - converted to Area's full pattern

### Built
- Converted Chemical Injection Point from the OLD 4-TC/suite-level-login shape (2026-07-30 build
  above) to **Area's full pattern**: 5 TCs, per-TC login/logout, fixed test code (`AUTOTEST_CIP`,
  replacing the per-run generated code), properties-file-driven insert/update/verify
  (`testdata/chem_injection_point_{navigator,insert,update,form_verify,grid_verify}.properties`),
  explicit grid-filter wiring (`Find/Clear Chemical Injection Point Row By Filter`), and the shared
  T2 `Apply Navigator From Properties` keyword driving the screen's genuine 3-level Production
  Unit -> Area -> Facility Class 1 navigator cascade + GO. The screen stayed classified **OV-GM**
  throughout - a structural RF conversion, not a reclassification as plain Bank-shaped.
  `resources/manage_object.resource` (shared T2/T1 file) was left untouched.

### Done well
- Live RF suite, `EC_HEADLESS=true`: **5/5 PASS** (TC01 Verify Clean State, TC02 Insert, TC03
  Update, TC04 Find, TC05 Delete) - cited in PR #550's own body.
- Full-tree dryrun: **850/850 PASS, 0 failed** at merge time (no regression on any other suite).
- robocop: 5 DOC02 (missing per-TC `[Documentation]`) - exact same count/shape as the Area/Facility
  Class 1 baselines at the time, confirmed by side-by-side robocop run; no new issue classes
  introduced.
- Fresh `oracledb` connection to `OV_CHEM_INJ_POINT` after the live run: **0 residual `AUTOTEST%`
  rows** (self-clean confirmed).
- Filter keyword fired: `grep -c "Find Object Row By Filter" output.xml` = **15** (non-zero),
  cited in the PR body.
- Live navigator recon (`tmp/recon_cip_navigator_cascade.py`) confirmed the 3-level cascade values
  used in `chem_injection_point_navigator.properties`: `Op Production Unit=AS1 EC Exploration
  Norway`, `Op Area=AS1_Area`, `Op Facility Class 1=AS1_Facility_01` - matching the previously-
  proven driver's own first-available picks.

### Done wrong / lessons - Op Production Unit / `__FIRST__` gotcha
The one genuine live blocker on this conversion: the Insert form's own "Op Production Unit"
`objectForm` field (separate from the mandatory navigator cascade) is a long (~25-row) autocomplete
that renders only a small (~5-row) MRU/default subset before its full reference list finishes
loading. A hardcoded exact-label wait for the navigator's own picked value (`AS1 EC Exploration
Norway`) was flaky against that subset - the requested label could be absent from whichever partial
subset happened to render within the click-wait window. Diagnosed live via
`tmp/recon_cip_pu_scroll_diagnosis.py`, which confirmed the DOM held only 5 `<tr>` rows at that
moment - not a guess. Fixed by reverting that ONE field to `__FIRST__` in
`chem_injection_point_insert.properties`, matching the exact tolerant mechanism the already-proven,
currently-passing legacy driver (`py/chem_injection_point_iud.py`, `verify_screen` PASS 2026-07-30)
already used for this field - not a new invention. Re-ran live after the fix: 5/5 PASS. Recorded
here as a real, disclosed issue, not smoothed over.

### Blockers -> resolution
- Op Production Unit `__FIRST__` gotcha (above) - resolved same-session by reverting to the proven
  mechanism, no escalation needed.

### Decisions
- Chemical Injection Point stays classified **OV-GM**, not reclassified as plain Bank-shaped,
  despite adopting Bank/Area's 5-TC RF STRUCTURE.
- No shared-file changes: `resources/manage_object.resource` reused as-is.
- Never self-merge: PR #550 raised for reviewer merge.

### Evidence
- Cited in PR #550's own body: live 5/5, full-tree dryrun 850/850, robocop parity (5 DOC02), DB
  self-clean 0 residual, filter-fire count 15 - see `gh pr view 550`.

## 2026-08-27 - documentation/evidence backfill (Batch 2, this session)

_Per `docs/lean-deliverable-backfill-workorder.md`: this session adds SOW/README/JOURNAL/evidence/
CHECKLIST/KB-map around PR #550's already-merged, already-working automation. No RF file
(`chem_injection_point_page.resource`, `chem_injection_point_iud.robot`,
`testdata/chem_injection_point_*.properties`) was modified._

### Found
- The screen's pre-existing `screens/.../Chemical_Injection_Point/` bundle (SOW/README/CHECKLIST/
  VERIFY-REPORT) still described the OLD pre-conversion 4-TC shape from the 2026-07-30 build,
  unrefreshed after PR #550 merged 2026-08-26 - it needed **updating**, not fresh creation,
  matching the same pattern Batch 1 flagged for several of its own screens.
- The KB map `ec-ui-knowledge/screens/chem_injection_point.md` likewise predated PR #550 and needed
  the same refresh (5-TC structure, `__FIRST__` quirk, current last-verified date).

### Done well (this session's re-run, reproducing PR #550's cited evidence)
- `robot --dryrun tests/Configuration/Assets/Chemical_Objects/chem_injection_point_iud.robot` ->
  **5/5 PASS**.
- `EC_HEADLESS=true robot --outputdir .../Chemical_Injection_Point/evidence tests/.../
  chem_injection_point_iud.robot` -> **5/5 PASS** clean, single run, no flake.
- Full-tree dryrun (`robot --dryrun tests/`) -> **883/883 PASS** (repo-wide suite count grew since
  PR #550's own 850/850 citation as other screens were added in the interim; zero regression on
  this screen's own suite either way).
- DB self-clean: `libraries.DbVerify.fetch_object("OV_CHEM_INJ_POINT", "AUTOTEST_CIP")` -> `None`
  (confirmed absent) via a fresh connection after the live run.
- `py -m robocop check` on `chem_injection_point_page.resource` +
  `chem_injection_point_iud.robot` -> **7 issues** (DOC02 missing TC/keyword docs) - same category
  as PR #550's cited baseline, no drift.
- `py scripts/check_bundle_hygiene.py` (repo-wide) -> **PASS** - "no hardcoded creds (R16), pure
  ASCII (R20), no CHECKLIST/VERIFY-REPORT contradictions, doc rows match declared families"
  (167 bundles + 271 recon scripts scanned; the one WARN emitted is a pre-existing, unrelated
  Contract Area recon script, not this screen).

### Decisions (this session)
- The pre-existing legacy Playwright driver (`py/chem_injection_point_iud.py`) and its
  `investigation/recon.py` were left untouched - per Section H of
  `docs/IUD-DELIVERABLE-CHECKLIST.md`, the Playwright driver + `investigation/` stay permanently
  waived for Bank-/Area-pattern work (the Universal Screen Engine replaces that role going
  forward); kept as historical reference, not rebuilt.
- The pre-existing `VERIFY-REPORT.md` (2026-07-30, describing the pre-conversion 4-TC suite) is
  kept as historical record, not deleted or overwritten - superseded in practice by PR #550's own
  live 5/5 evidence and this backfill's `CHECKLIST.md`/this JOURNAL section.

### Evidence (this session)
- Evidence artifacts added: `evidence/log.html`, `evidence/output.xml`, `evidence/report.html`
  from this session's clean 5/5 run, alongside the pre-existing 2026-07-30 Playwright evidence
  (`cip_01_loaded.png` ... `cip_05_final.png`, `results.json`) which is kept unchanged.
