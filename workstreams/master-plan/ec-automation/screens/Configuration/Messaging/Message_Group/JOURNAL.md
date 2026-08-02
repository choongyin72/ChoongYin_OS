# JOURNAL - Message Group (CO.0236) OV-GM IUD

## 2026-08-02
- **Branch:** `feature/retry-message-group-iud`. Previously parked (recovered on an unmerged branch,
  `feature/message-group-iud`) as "insert PERSISTS but lands in WRONG SCOPE" - the navigator's
  first-available Functional Area came back "Administration", but the form's Functional Area
  (`parent_dd`) silently persisted "Allocation" instead - suspected as a shared `select_dropdown`/
  `Fill OV Dropdown By Label` engine defect (same symptom class as Property/Price Index/Royalty
  Contract). Marked "NOT confirmed systemic" at the time since Area's own `parent_dd` mechanism had
  separately validated 7/7.
- **Real root cause (4th confirmation of the same class - see
  [[feedback_child_object_date_must_follow_parent]]):** the generator config had no `start_date`
  set at all, defaulting to `2000-01-01`. "Administration" (`ADM`) is only effective from
  `2001-01-01` onward (`OV_FUNCTIONAL_AREA.OBJECT_START_DATE`). At `2000-01-01`, "Administration"
  wasn't in the form's filtered Functional Area option list, so the fallback landed on a different
  available option ("Allocation", effective since 1900).
- **Fix:** added `start_date: "2003-01-01"` to `tmp/cfg_message_group.json`, regenerated. No
  shared-engine change needed. Also explicitly re-verified the DB persisted the CORRECT Functional
  Area code (`FUNCTIONAL_AREA_CODE = 'ADM'`), not just the record Name, since this is the `parent_dd`
  binding mechanism (distinct from the `extra_dropdowns` mechanism used on the other 3 screens).
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4 pass,
  Playwright driver 8/8. DB residual 0.

## Lessons
- 4th confirmed instance of the same root cause class (Property, Price Index, Royalty Contract,
  now Message Group) - and the first one using the `parent_dd` binding mechanism instead of
  `extra_dropdowns`, confirming the date trap applies to BOTH mechanisms equally.
- This also RESOLVES the "NOT confirmed systemic" uncertainty left open in the original park note -
  Area's `parent_dd` validation (7/7) never hit this because Area's own nav/form values happened to
  already be date-compatible; it wasn't that Message Group's mechanism was broken while Area's
  worked, both mechanisms work fine once the date is correct.
