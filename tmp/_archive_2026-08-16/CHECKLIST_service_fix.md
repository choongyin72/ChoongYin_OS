# CHECKLIST - items 1 & 2: fix Service's stale claim + the negtest hardcoded path

Owner: "u complete 1 and 2 items first". Ticks are executed-command output.

## Item 1 - Service's stale CHECKLIST claim (real, now verified end-to-end)
- [x] confirmed on master (before fixing): CHECKLIST.md said "navigator cascade Business Unit
      first-available + GO; Op Production Unit first-available" - both false (Service uses explicit
      `nav_value: "TS3 BU1"`, `has_op_pu: false`).
- [x] ran `find_populated_scope.py`-era config (`tmp/cfg_service.json`) through the CURRENT (post-#300)
      templates via `tmp/run_gen.py` + `tmp/run_pkg_service.py`, rather than hand-editing the CHECKLIST text.
- [x] the driver/T3/suite sweep from #300 CAUGHT A REAL, PREVIOUSLY-UNVERIFIED DEFECT at the deeper layer:
      `service_iud.py` said "Built on the gated-navigator capability (apply_ovgm_navigator)" and
      `service_page.resource` said "Apply OV-GM Navigator First Available" / "Op Production Unit
      first-available" - both flatly false, no negation, confirmed by reading full context.
- [x] regenerated driver/T3/suite from the current (already-fixed) `gen_ovgm.py` templates - fixed at the
      source, not patched per-file.
- [x] **re-ran the LIVE gate after regenerating code files** (not just docs) - `verify_screen.py` ->
      OVERALL PASS, exit 0: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4, Playwright 8/8. Confirms the
      corrected docstrings did not change runtime behaviour.
- [x] repackaged -> sweep prints `driver/T3/suite/recon artifact sweep: clean`.
- [x] read the WHOLE bundle back: `grep -rn "first-available|apply_ovgm_navigator|gated-navigator
      capability"` across every file + the KB map -> **0 residual false claims** (the one remaining
      "navigator-GATED" mention in README/SOW is TRUE - Service genuinely is gated, just not
      first-available; only `go_only` screens lose that word).
- [x] idempotent: re-run -> `registry+=False scorecard+=False`.
- [x] hygiene -> RESULT PASS.
- [x] no other screen's bundle touched - `git status` shows only Service's own files + `tmp/package_ovgm.py`.

## A 4TH generated-file layer found DURING this fix, not part of #300's original scope
- [x] `investigation/recon.py`'s OWN docstring claims "Reruns the scan used to build this bundle", but the
      code always called `apply_ovgm_navigator()` unconditionally - confirmed the SAME bug exists on
      Contract Capacity's already-shipped recon.py too, so it is a generic template gap, not Service-only.
      For any explicit-value screen, running this script would silently apply an UNPROVEN first-available
      scope instead of the one the screen was actually built with - contradicting the file's own stated
      purpose.
- [x] fixed at the template root (`recon_nav_block` in `package_ovgm.py`, mirroring `gen_ovgm.py`'s 4-way
      nav_mode/nav_values/nav_value/default branch) and added `recon.py` to the sweep's checked-file list.
- [x] unit-tested all 4 branches in isolation (`tmp/test_recon_block_logic.py`) - go_only, nav_values,
      nav_value, and the unchanged default (`apply_ovgm_navigator`) all produce correct code.
- [x] MY FIRST negative-test attempt was structurally invalid and I caught it before trusting the result:
      editing the already-written `recon.py` and re-running the packager doesn't prove anything, because
      the packager REWRITES `recon.py` from the template every run, silently overwriting my injection
      before the sweep could see it. Fixed by reverting the TEMPLATE (`package_ovgm.py`) to the original
      unconditional call, confirming the sweep catches ITS OWN regenerated (bad) output at `recon.py:19`,
      then restoring the real fix and confirming byte-identical (`diff` clean).

## Item 2 - the trivial path fix, done alongside for consistency
- [x] `tmp/negtest_artifact_sweep.py` (the reviewer's NICE-TO-HAVE on #300), plus the 2 new negtest
      scripts written during this fix, all switched from a hardcoded absolute path to
      `Path(__file__).resolve().parents[1]`. Verified it resolves to the repo root.

## Gates
- [x] `py -c "import ast; ast.parse(...)"` on `package_ovgm.py` after every edit -> valid syntax.
- [x] `check_bundle_hygiene.py` -> RESULT PASS.
- [x] no governance file, no shared engine touched.
