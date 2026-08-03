# JOURNAL - Production Day Table (CO.1033) Insert-only IUD

## 2026-08-03
- **Branch:** `feature/build-production-day-table-iud`. Previously parked twice (2026-07-27,
  re-attempted 2026-08-02) on the hypothesis that this screen shared Constant Standard's/Stream
  Item's "toolbar insert dead end" root cause. Deliberately did NOT assume that this time (per the
  explicit lesson recorded in Stream Item's own JOURNAL: "the toolbar-mystery batch had at least 2
  distinct root causes, not one shared cause"). Correct call - this screen's real blocker was a
  THIRD, distinct cause.
- **Recon confirmed:** `TIME_SCOPE_CODE=INVARIANT` (unlike Constant Standard's `VERSIONED`) - delete
  should be a physical row removal, not End=Start, if it existed at all.
- **Insert menu text is already correctly title-cased** ("Production Days") - no CSS-uppercase
  illusion here, confirmed via raw `onclick`/`textContent` inspection. The click itself worked
  immediately and cleanly on the first live attempt.
- **Real blocker found on Insert: cell-fill method.** Filling Object Code (`C0_in`) via
  `ec.fill_field()`'s plain `.fill()` silently broke the Time Zone dropdown's panel from ever
  rendering (confirmed reproducible via isolated tests - with `.fill()` first, the panel times out
  with 0 options; skip the `.fill()` and the SAME panel has 9 real options). Root cause not fully
  isolated at the DOM level, but the fix is exactly this project's own established convention for
  inline grids: real keystrokes + Tab (`Type Cell By Id`), not a form-field-style `.fill()`. Once
  switched, Insert worked cleanly and reproducibly.
- **Delete genuinely does not exist on this screen - confirmed by the owner directly, live.**
  Independently exhausted 6+ distinct row-selection attempts first (cell click, td click, tr click,
  edge click, fresh-reload-then-click, tested against 3 different pre-existing real rows, not just
  test data) - the toolbar Delete icon never enabled regardless of method. Also confirmed via DB
  that End Date = Start Date does NOT remove a row from `OV_PRODUCTION_DAY` (the view has no
  date-range filter). Rather than keep grinding, asked the owner to check live directly - they
  confirmed this is a genuine, permanent business-process decision: "no deletion is allow in
  Production Day Table screen... Production Day Table set object end date its not trigger delete
  record as its implementation are different than other objects implementation."
- **Self-clean impossibility - owner decision.** Since no delete path exists, every Insert
  (including every future live test run) permanently accumulates one row. Presented the tradeoff to
  the owner (accept permanent residual / run-once-ever / skip the screen entirely) - owner chose to
  accept permanent residual, matching the Royalty Contract precedent. 8 `AUTOTEST_PDT_*` rows are
  now permanently live in the sandbox from this session's investigation + build (2 from early
  diagnostic scripts before the owner's confirmation, 6 from the driver/suite proof runs after).
- **Second finding: DB commit visibility is measured ~8s slower than every other screen built so
  far.** A direct timed test (checking `code_present()` at t+0/1/2/3/5/8s after Save) showed the
  commit was NOT visible to a fresh DB session until 8 seconds had passed - every prior screen's
  commit was visible near-instantly. The driver/T3 both use a 10s wait after Save to cover this.
- **Third finding, RF-specific: `Evaluate JavaScript`'s trailing-argument form does not thread
  values into the JS function.** The Python driver's row-finder worked fine using a genuine function
  parameter (`(code) => {...}` + a trailing Python arg, real Playwright semantics). The direct RF
  Browser-library port of that same pattern (`Evaluate JavaScript ${None} (code) => {...} ${code}`)
  silently received `code=undefined` in the browser, causing every comparison to fail regardless of
  the actual row state - a full live RF failure ("No blank row after Insert") even though the blank
  row genuinely existed (confirmed via a standalone debug script that dumped all grid values). Fixed
  by following this project's own established convention (seen in `allocation_run.resource`/
  `popup.resource`): inline the value via RF's own `${VARIABLE}` string substitution directly into
  the JS source, not as a separate function argument.
- Built a bespoke driver (Insert-only, `py/production_day_table_iud.py`) + T3 reusing shared T1
  keywords (`Type Cell By Id`, `Select First EC Dropdown Option`, `Save` from `table.resource`) + a
  1-test-case suite (no clean-state/update/delete cases - none apply to an Insert-only, no-delete
  screen). `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 1/1, live RF 1/1,
  Playwright driver 5/5.

## Lessons
- **Never assume a shared root cause across superficially similar screens in the same batch** - this
  screen shared NONE of Constant Standard's or Stream Item's actual blockers (no case-sensitivity
  bug, no server-derived Name, no unconfigured scheduler job) - its real issues were a cell-fill
  method gotcha, a slow commit-visibility window, and an RF-specific argument-passing gap.
- **When a toolbar action stays disabled regardless of every plausible selection gesture tried, stop
  and ask rather than keep inventing new click strategies** - this was a genuine, permanent
  business-process decision, not a selector puzzle to solve. The owner's direct live check settled
  it in seconds after 6+ automated attempts found nothing.
- **A screen with no delete path makes "self-clean" impossible by definition** - this needs an
  explicit owner decision up front (accept permanent residual / run sparingly / skip the screen),
  not a silent workaround. Disclose the exact residual count in the JOURNAL for auditability.
- **RF's `Evaluate JavaScript` trailing-argument form is unreliable in this project's setup** - always
  inline values via `${VARIABLE}` substitution into the JS source string, matching every other
  working usage in this codebase (`allocation_run.resource`, `popup.resource`, `daily_status_grid.resource`).
