# JOURNAL - Stream Item (CD.0008) Insert+Delete IUD

## 2026-08-02 / 2026-08-03
- **Branch:** `feature/build-stream-item-iud`. Previously parked twice (2026-07-27, re-attempted
  2026-08-02) on a wrong assumption that this screen used a "Copy STREAM ITEM"-based insert mechanism
  (same wrong turn later disproven on Constant Standard). Fresh recon this session disproved it: this
  screen's Insert menu already shows correctly-cased text ("New Object"/"New Version", not an
  all-caps CSS illusion like Constant Standard) - `ec._open_new_object()` (existing shared engine
  function) already works correctly here, no fix needed.
- **First real blocker: 12 mandatory reference fields.** Save initially rejected with "Required fields
  are empty" listing 12 fields with `[..._POPUP]`-style bracket names (Stream Item Category, Product,
  Field, Company, Stream, Measurement Node, Calc. Method, Conversion Method, Master UOM Group, Daily/
  Monthly Accrual Method, Reporting Category). Live DOM inspection showed these all resolve as ordinary
  autocomplete **dropdowns** (`dd_input`), not "Pick from EC Object" popups (`pin`) - the bracket
  naming in the error message is misleading. `__FIRST__` on each satisfies Save.
- **Second finding: Name is server-derived.** Confirmed 3x (including typing it LAST, immediately
  before Save, verified in-DOM right before the click) that any manually-typed Name value is discarded
  server-side and replaced with an auto-generated string
  (`<Category>/<Product>/<Field>/[<Well>/]<Company>`). Later confirmed as DOCUMENTED EC behavior via
  the screen's own online help page - not a bug, not a timing issue.
- **Third finding, genuine blocker: Update.** Any Save on `updateAttributes` (tested via Description,
  an otherwise-unrelated field) fails with EC's own error "Cannot run schedule job UpdateStreamItem
  because it has not been configured." Reproduced live 3x, twice headed with the owner watching
  directly, once more with a corrected reproduction script (the first headed attempt had a script bug -
  Name was accidentally omitted from the insert fields, which the owner caught by screenshot review;
  fixed and re-confirmed the real blocker cleanly on the corrected reruns). Cross-checked against the
  screen's own EC online help page: changing a Stream Item's core attributes can kick off a background
  scheduler job (BF VO.0031 - Daily SI Pending Calculation) - genuinely documented EC behavior, and this
  sandbox's job is not configured/enabled. **Owner instruction: skip Update, ship Insert + Delete only.**
- **Fourth finding: navigator GO button id.** This screen's GO has id `buttongo:form:B`, not the
  generic `button:form:B` the shared engine's `click_go()`/`Apply Navigator` expect. The Python driver
  and T3 both define their own local navigator-GO wrapper instead of using the shared one - using the
  shared one's Refresh-icon fallback silently succeeded at the Save/error-check level but failed to
  re-list the just-inserted row in the grid (a real "insert succeeded, verification false-failed" gap,
  caught and fixed before shipping).
- **Fifth finding, RF-only flake that wasn't a flake:** the live RF suite failed twice in a row on the
  SAME dropdown (Stream Item Category) with an apparent 10s timeout waiting for the option panel to
  render. A headed re-run + screenshot review (per the owner's insistence on reading the actual failure
  screenshot rather than assuming a selector/timing bug) showed the panel WAS open and correctly
  displayed **"No records found"** - the suite's `${START_DATE}` was wired to the plain
  `${TEST_START_DATE}` (2000-01-01) instead of `${TEST_START_DATE_REFDD}` (2003-01-01), the exact
  existing framework convention for reference-dropdown screens, which this screen qualifies for.
  Fixed the variable reference; suite went 3/3 on the very next run. See
  [[feedback_child_object_date_must_follow_parent]] (4th confirmed instance of this exact class of bug).
- Built a thin Python driver (`py/stream_item_iud.py`, Insert+Delete only, Update explicitly marked
  SKIPPED with the reason inline) + T3 (`stream_item_page.resource`, reuses T2 label-driven keywords
  `Fill OV Field/Date/Dropdown By Label`) + a 3-test-case suite (clean-state/insert/delete, no update
  test case). `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 3/3, live RF 3/3,
  Playwright driver 6/6. DB residual 0 (confirmed via direct query after every run, including the two
  failed RF attempts before the date fix - neither left any residual since the insert never completed).

## Lessons
- **Read the failure screenshot before assuming timing/selector issues** - "No records found" in an
  autocomplete panel is unmistakable proof of a date-scope problem, not something more retries or a
  longer timeout will ever fix. This cost 2 live suite runs before the owner's insistence on reviewing
  the actual screenshot surfaced the real cause in seconds.
- **When a screen's GO button has a non-standard id, define a local wrapper rather than relying on the
  shared engine's fallback** - the fallback can silently "succeed" (no error thrown) while failing to
  actually refresh the view being asserted against, producing a false verification failure that looks
  like the insert itself failed.
- **Bracket-style field names in an EC validation error (`[..._POPUP]`) are not proof of field kind** -
  always confirm live via DOM inspection (`dd_input` vs `pin`) rather than trusting the error message's
  naming convention.
- Owner-simplified standing default going forward: use Start Date `2020-01-01` for any new
  reference-dropdown-bearing screen's test data, rather than hunting the exact effective date of each
  referenced parent object.
