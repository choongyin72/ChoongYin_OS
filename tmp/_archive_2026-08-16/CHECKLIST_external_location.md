# CHECKLIST - External Location (CO.0227): first `nav_mode="go_only"` OV-GM screen

Ticks are executed-command output. Gate ticks come from `verify_screen.py` -> `VERIFY-REPORT.md`
(**OVERALL: PASS**, exit 0).

## Recon (read-only, before any code)
- [x] step-0 check: only the target row + my own prior UNVERIFIED flag, no fresh diagnosis skipped.
- [x] live scan: per-field nav (Date/Ext Loc Code/Ext Loc Name/Type), **all 4 optional**, no mandatory
      dropdown -> scanner correctly refused to record grid=None as this screen's shape (its new loud note).
- [x] follow-up probe: GO with no filters -> grid loads with **15 rows**. Confirmed a search-filter screen,
      not a scope cascade.
- [x] `ov-non-bank-targets.md:127` again wrong: labelled OV-GM "needs capability" from the 2026-07-27 batch
      guess. This is the THIRD screen that doc has been wrong about (Report Group; Truck/Trailer/Driver;
      now this one) - its Flavour column should not be trusted without a live scan, ever.
- [x] insert-form probe AFTER GO (the scan never reached it - no mandatory dd to trigger the gated path):
      3 mandatory fields, and their real labels are **External Location Code / External Location Name**,
      not the abbreviated `Ext Loc Code/Name` guessed from the navigator filters. Caught BEFORE the live run.

## New generator capability: `nav_mode: "go_only"`
- [x] `apply_ovgm_navigator` looks for `C:1..N` dropdowns; none exist here, so it returned `None` and the
      driver's unconditional `assert pu` killed an otherwise-correct run. Root cause read from source, not
      guessed.
- [x] Added `nav_mode` (Playwright + RF): GO-only click, `pu = None` treated as legitimate, assert removed
      ONLY for this mode (not weakened for every OV-GM screen).
- [x] REGRESSION PROVEN, not assumed: old-style config (`levels=4` cascade) still emits the identical driver
      body except an already-planned docstring cleanup (see below) - diffed byte-for-byte before/after.

## Live gate - FIRST RUN, all 5 PASS
- [x] robocop exit 0 - [x] hygiene exit 0 - [x] dryrun 4/4 - [x] **LIVE RF suite 4/4 pass 0 fail** -
      [x] **Playwright driver 8/8**

## Wrong-family text found and fixed - SIX sites, not one
The first packaging pass used a FAKE `nav: ["(filters only, no scope)"]` entry just to satisfy the
non-empty-nav assert, and it printed verbatim into the docs. Found by reading every artifact back, not by
trusting a single grep:
- [x] registry row - "(filters only, no scope) cascade + GO" -> "GO only (navigator fields are optional
      filters, no mandatory scope)"
- [x] scorecard row - "OV-GM gated-navigator" -> "OV-GM, GO only (no mandatory nav scope)"
- [x] JOURNAL - same false cascade line -> corrected
- [x] KB map - Navigator line AND the Quirks paragraph both claimed a cascade at
      `nav:form:G:0:R:1:C:1..N:dd` that does not exist on this screen -> both corrected
- [x] CHECKLIST footer - "OV-GM specifics: navigator cascade first-available + GO; Op Production Unit
      first-available" -> corrected, AND made `has_op_pu`-conditional (this screen has none)
- [x] SOW + README (gen_ovgm.py templates, not just package_ovgm.py) - "navigator-GATED" / "Navigator cascade
      first-available" -> corrected; ALSO removed the leftover false "Built on the item-1 gated-navigator
      capability (PR #244)" claim from the OV-GM README template (already removed from the plain-OV one
      earlier this session; now consistent across both generators).
- [x] fixed at the ROOT (the config no longer needs a fake nav entry) plus a REAL `nav_mode` key in the
      packager, not a one-off string replace on this screen's files.

## Re-verification after the fix
- [x] re-packaged: `check_row_vocab.py` OK; `grep -rn "cascade|navigator-GATED|Op Production Unit
      first-available|PR #244"` across all 6 artifacts + the KB map -> **0 residual hits**.
- [x] idempotency: second package run -> `registry+=False scorecard+=False` (no duplicate rows).
- [x] `verify_screen.py` re-run after the template fix -> still **OVERALL PASS** (driver/T3 regenerated
      identically apart from docstrings, so the live gate result is unaffected).
- [x] `check_bundle_hygiene.py` -> RESULT PASS (32 manifest screens).
- [x] R23: registry/scorecard/manifest edits are pure appends.

## Known follow-up, NOT done in this task (scope discipline)
- [ ] `check_row_vocab.py`'s `EXPECTED_ANY`/`FORBIDDEN` tables are keyed by family only; they cannot yet
      detect "cascade" claimed on a `nav_mode=go_only` screen, because `screen_families.json` only stores
      the family string, not the nav mode. Would need a schema extension. Flagged, not built here, to avoid
      scope creep at the tail of this task - the packager fix at the SOURCE plus hand-verification across
      all 6 files is what actually protects this screen; the gate extension is a separate, smaller PR.

## Sandbox
- [x] Suite self-cleans in-suite (gate 15 passed within `verify_screen`'s live RF run).
