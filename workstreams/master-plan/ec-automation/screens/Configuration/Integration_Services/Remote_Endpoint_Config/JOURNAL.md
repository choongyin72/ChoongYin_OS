# JOURNAL - Remote Endpoint Configuration (CO.1082) IUD

## 2026-08-03
- **Branch:** `feature/build-remote-endpoint-config-iud`. New screen, discovered via a DB-first
  coverage audit (`SELECT class_name FROM CLASS_CNFG WHERE CLASS_TYPE='OBJECT'`, 295 total,
  cross-referenced against every tracking doc to find genuinely unautomated classes with a real
  live screen).
- **Real screen title differs from the class's own LABEL property** - `class_property_cnfg` stores
  "Endpoint configuration", but the live menu title is "Remote Endpoint Configuration" (same class
  of naming gap already seen on Contact Group Set this session). Confirmed the real title via a
  live menu search, then verified via `scan_ec_screen.py` before committing to build.
- **Genuine, screen-specific Code format constraint found on first insert attempt:** the usual
  `AUTOTEST_XX_<timestamp>` uppercase-underscore code was rejected live with *"Invalid Code, must
  consist of lower case alphanumeric characters or '-', and must start and end with an alphanumeric
  character (e.g. 'my-name', or '123-abc')"* - a DNS-slug format. Switched to
  `autotest-rec-<timestamp>`, confirmed clean insert immediately after.
- Simple TV-style grid (Code/Name/Remote Type dropdown/Description), no navigator, matches the
  proven Language exemplar shape exactly - built a bespoke driver (no generator fits TV screens)
  reusing shared T1 keywords.
- **First live RF run hit the established "missing `Refresh Screen` after Save" gap** (TC03 Update
  failed with a 30s Save-button timeout) - same root cause as Constant Standard's own build: the
  toolbar Save button needs the explicit reload after each Save to re-enable for the next
  operation's cell-click. Fixed by adding `Refresh Screen` after all 3 Save calls; also split the
  Delete keyword's menu-opening logic into its own keyword to fix a robocop LEN03 (too-many-keywords)
  violation the fix introduced. Re-ran live: 4/4 pass.
- Confirmed live + DB-verified via `verify_screen.py` (OVERALL PASS: robocop 0, hygiene 0, dryrun
  4/4, live RF 4/4, Playwright driver 7/7). Full I-U-D (physical delete), 0 residual.

## Lessons
- **A screen can enforce its own Code format distinct from this project's usual `AUTOTEST_XX_`
  convention** - always attempt one throwaway insert with the standard convention FIRST during
  recon (before building the full bundle) to catch a format-rejection error early, rather than
  discovering it mid-build. Confirmed a real, live EC validation message this time, not a guess.
- **`Refresh Screen` after every Save is now a confirmed-recurring requirement for TV-style inline
  grids**, not a one-off found only on Constant Standard - the exact same symptom (30s Save-button
  timeout on the SECOND operation) recurred here on a completely unrelated screen/table. Any future
  TV-style bespoke driver/T3 should include this from the first draft, not discover it via a live
  failure.
