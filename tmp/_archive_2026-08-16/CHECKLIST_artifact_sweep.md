# CHECKLIST - close the #299 gap: sweep the generated driver/T3/suite files, not just docs

Owner: "any mistake u had done?" -> the #299 reviewer feedback, acted on directly. Ticks are executed
command output.

## The gap, verified against the reviewer's claim rather than trusted
- [x] confirmed on master: `tmp/gen_ovgm.py`'s driver docstring / T3 Settings / T3 open-keyword / suite
      Settings / suite setup-keyword / TC02 doc are ALREADY fixed by the reviewer (6 sites, all branch on
      `nav_mode`/`nav_values or nav_value`) - `git diff master -- tmp/gen_ovgm.py` is empty this session,
      confirming I did not need to re-fix the template, only add the CHECK that keeps it honest.
- [x] `package_ovgm.py` had NO equivalent check - it only ever validated CHECKLIST/JOURNAL/KB/registry/
      scorecard, never the generated `.py`/`.resource`/`.robot` files themselves. Added.

## The check itself failed its own first TWO runs - both caught and fixed, not shipped
- [x] run 1 (Contract Capacity): flagged the REVIEWER'S OWN CORRECT text ("PROVEN explicit values, not
      first-available") as if it were the bare false claim - same negation-blindness class already fixed
      twice today in `check_row_vocab.py`. Root cause: forbade `navigator-GATED` even for `nav_value`/
      `nav_values` screens, which genuinely ARE still gated (only `go_only` isn't); and matched
      "first-available" without checking for a negation cue.
- [x] run 2 (after adding an exact-phrase negation list, Collection Point): STILL flagged correct text -
      a NEW phrasing of the same contrast ("not X's first-available - first-available broke a later
      level") beat the exact-phrase list. Generalised: any line containing "not" ANYWHERE alongside the
      forbidden term is treated as a legitimate contrast, rather than enumerating more exact phrases.
- [x] run 3 (Collection Point again): STILL flagged - the sentence WRAPS ACROSS SOURCE LINES ("not
      apply_ovgm_navigator's" is line 4, "first-available" recurs on line 5), so a per-line check cannot
      see the negation on the previous line. Rewritten as a WINDOWED check over the whole file text
      (80 chars before each match, not per physical line) rather than per-line.

## Verified clean on all 3 real screens using explicit-nav capabilities
- [x] Contract Capacity (`nav_value`) -> `driver/T3/suite artifact sweep: clean`
- [x] Collection Point (`nav_values`) -> `driver/T3/suite artifact sweep: clean`
- [x] External Location (`nav_mode=go_only`) -> `driver/T3/suite artifact sweep: clean`

## The guard PROVEN to still catch a real defect (not just tuned into silence)
- [x] injected a genuine stale claim into Contract Capacity's generated driver ("Built on the
      gated-navigator capability (apply_ovgm_navigator), first-available.") -> **ABORT fired**, both
      injected phrases named with file:line. File restored immediately after (`tmp/negtest_artifact_sweep.py`).

## A genuine, PRE-EXISTING finding surfaced, deliberately NOT fixed here (scope discipline)
- [x] Service's (#292, predates `nav_is_explicit`) CHECKLIST.md on master STILL says "navigator cascade
      Business Unit first-available + GO; Op Production Unit first-available" - false: Service uses
      `nav_value: "TS3 BU1"` (explicit) and `has_op_pu: false`. Confirmed by reading master directly, not
      inferred.
- [ ] Whether Service's DEEPER driver/T3/suite layer is also stale is **UNVERIFIED** - running the new
      sweep on it hit the pre-existing JOURNAL branch-name guard (unrelated to this fix) before the sweep
      itself could execute, and I did not force past it because mutating an already-merged screen's bundle
      is outside this task's scope. Reported as a separate finding, not silently fixed or silently dropped.

## Side effects of testing caught and reverted before commit
- [x] repeated re-packaging of the 3 real screens during testing wrote test-branch JOURNAL/evidence noise
      into their ALREADY-MERGED bundles (branch name changed to `feature/artifact-sweep-driver-t3`,
      evidence PNGs re-copied). None of that belongs in this PR - `git restore`d every file except
      `tmp/package_ovgm.py` before committing. Confirmed via `git status` (only the one file changed).

## Gates
- [x] `py -c "import ast; ast.parse(...)"` on `package_ovgm.py` -> valid syntax, checked after every edit.
- [x] no shared engine / governance file touched.
