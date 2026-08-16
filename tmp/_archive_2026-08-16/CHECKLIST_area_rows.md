# CHECKLIST - Area (CO.0003): record the built-but-unrecorded screen

## The finding
- [x] Area has a T3, a suite and a Playwright driver in the repo, but **0 registry rows** and **no entry in
      `screen_families.json`** - `grep -c "^| Area " ec_screen_registry.md` -> 0, `grep -c '"Area"'
      screen_families.json` -> 0.
- [x] Two consequences, both verified: the Group A count treated a built screen as unbuilt, and because the
      manifest drives hygiene's doc-row family gate, **Area's rows were never gated at all**.
- [x] Found while re-verifying the Group A count after I doubted my own "25 remaining" figure.

## Rows EARNED, not asserted
- [x] `verify_screen.py --name Area` -> **OVERALL: PASS**, exit 0: robocop 0, hygiene 0, dryrun 4/4,
      **LIVE RF suite 4/4 pass 0 fail**, **Playwright driver 6/6**. Row text taken from that report.
- [x] BF code `CO.0003` resolved from `DefaultScreenTreeview`, not guessed. `OV_AREA` has 28 rows.

## Narrowest possible edit (the #287 lesson)
- [x] Appended the 3 missing rows ONLY. Did NOT run the full packager: Area already has its own
      README/SOW/investigation/evidence and regenerating risks overwriting content I did not write.
- [x] No CHECKLIST/JOURNAL/KB created for Area here - that is a separate decision, deliberately not bundled.
- [x] Row wording is family-correct: Area IS OV-GM and DOES have Op PU, and the row states the real
      constraint - Op PU must EQUAL the navigator PU or the row will not appear in the filtered grid.

## Verification
- [x] `check_row_vocab.py "Area" ovgm` -> exit 0, "2 row(s) + bundle docs use 'ovgm' vocabulary consistently".
- [x] R23 append-only: registry, scorecard and manifest each **1 insertion, 0 deletions**.
- [x] `check_bundle_hygiene.py` -> RESULT PASS with Area now INSIDE the gate (manifest 30 -> 31 screens).
- [x] Sandbox: Area's suite self-cleans in-suite; the live run left no AUTOTEST residue (gate 15 passed).
