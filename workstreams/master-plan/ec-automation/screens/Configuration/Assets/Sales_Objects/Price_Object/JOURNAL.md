# JOURNAL - Price Object (CO.3016) OV-GM IUD

## 2026-08-03
- **Branch:** `feature/build-price-object-iud`. Previously parked as "pager-walk click timeout
  (5-page grid)" (original), then re-investigated for issue #321 (2026-08-02): that characterization
  did NOT hold up under careful re-testing - the pager itself walked all 5 pages cleanly, twice. The
  REAL root cause found that round: inserting with Business Unit deliberately left unset leaves the
  row with no `BUSINESS_UNIT_CODE`, so it is genuinely not visible under any page of a BU-scoped grid
  - the same missing/wrong-scope defect class as Message Group and Planned Well, not a pagination bug.
- **This round: built the fix.** Used `gen_ovgm.py` with `parent_dd: "Business Unit"` so the
  navigator's captured top-parent (first-available Business Unit, e.g. "EC LNG Norway") is bound into
  the insert form's own Business Unit dropdown - the exact mechanism that was missing before.
- **New generator gap found and fixed locally (same class as Service/CO.2103):** the navigator has
  only ONE mandatory dropdown (Business Unit), but 2 more OPTIONAL FILTER dropdown columns exist on
  the same nav row (unrelated to Business Unit, not cascade children). `gen_ovgm.py`'s default
  Python-driver call already supports a `nav_levels` config key to cap the cascade at 1 (confirmed via
  its own comment referencing this exact Service precedent) - added `"nav_levels": 1` to the config
  and the Playwright driver worked immediately (8/8). **However the generator does NOT thread
  `nav_levels` into the generated RF T3** - it always emits `Apply OV-GM Navigator First Available`
  with no cap, which tries columns 1-6 and times out on column 2/3's empty options. Fixed by hand,
  following the exact precedent already set on Service's own T3: replaced the shared cascade keyword
  call with a direct `Select First EC Dropdown Option` on the screen's own single `${NAV_DD}` variable
  (no shared-file change - purely local to this T3, matching the established pattern for screens with
  false-cascade nav columns).
- Confirmed live + DB-verified via `verify_screen.py` (OVERALL PASS: robocop 0, hygiene 0, dryrun 4/4,
  live RF 4/4, Playwright driver 8/8). Full I-U-D (unlike Stream Item/Production Day Table, this
  screen has no scope-of-work restrictions - Update and Delete both work normally). 0 residual.

## Lessons
- **`gen_ovgm.py`'s `nav_levels` config key only caps the PYTHON driver's cascade - it does not
  affect the generated RF T3 at all.** Any screen with a single mandatory nav dropdown plus extra
  OPTIONAL filter columns on the same row (Service, now also Price Object) needs its RF T3 hand-fixed
  to bypass `Apply OV-GM Navigator First Available` in favor of a direct single-dropdown fill, even
  after setting `nav_levels` in the config - the config key alone is NOT sufficient for the RF side.
  Worth fixing in the generator itself if a 3rd screen hits this same gap.
- **A screen's earlier "pager timeout" park reason can mask a completely different, real defect** -
  the original 2026-07-27 diagnosis (pager mechanism) and the 2026-08-02 re-diagnosis (missing scope)
  were both wrong turns before the true cause; only building the actual fix (parent_dd binding)
  proved it. Confirms the standing lesson: verify the SPECIFIC conclusion, not just re-run the same
  test with more patience.
