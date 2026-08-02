# JOURNAL - Constant Standard (CO.0102) TV-style IUD

## 2026-08-02
- **Branch:** `feature/build-constant-standard-iud`. Previously parked twice: original 2026-07-27
  reason ("standard New-Object menu gesture times out - custom toolbar"), then re-attempted and
  re-parked the same day with a partial finding ("real Copy-based insert mechanism identified, not
  yet proven working" - PR #342) that turned out to be a wrong turn.
- **Real root cause, finally isolated:** the screen's Insert toolbar icon's hover menu shows an item
  whose VISIBLE text is "CONSTANT STANDARD" (all caps), but the REAL underlying DOM text is
  **"Constant Standard"** (title case) - the all-caps rendering is pure CSS `text-transform`, not
  actual page content. Every earlier attempt (this session and the original 2026-07-27 one) searched
  for the all-caps string and silently failed to match, mis-diagnosing this as "the tooltip isn't a
  real menu item" or "must be a Copy mechanism instead." Confirmed by reading the real `onclick`
  handler on the menu `<a>` directly - it's a genuine PrimeFaces AJAX insert call
  (`eventType:"insert"`), not decorative.
- **Second finding: this is genuinely a TV-style inline-editable grid** (`cstandard:form:T_data`),
  not the standard OV New-Object-form pattern - despite `resolve_ec_screen.py` reporting
  `CLASS_TYPE=OBJECT`. Insert = click the (correctly-cased) menu item -> a blank row appears -> fill
  cells directly (real keystrokes, not `.fill()`, matching this project's own T2 `table.resource`
  convention for inline grids).
- **Third finding: "Daytime" is a genuinely separate mandatory field**, not derived from Start Date -
  Save rejects the insert without it even though only Start Date is visually similar/adjacent.
- **Fourth finding: this class IS date-effective (`VERSIONED`) despite looking like a plain TV
  screen** - Delete = set End Date (C3) = Start Date directly in the inline cell + Save, exactly like
  an OV close gesture. The toolbar's Delete icon (also disabled after a normal cell click, requiring
  the same case-sensitive-menu investigation as Insert) was NOT the right path - never fully wired up
  once the End=Start path was confirmed working and simpler.
- **Built** a bespoke driver (no `gen_ovgm.py` - this pattern doesn't fit the OV-GM generator) +
  T3 reusing shared T1 keywords (`Type Cell By Id`, `Get Cell Value By Id`, `Save`, `Refresh Screen`
  from `table.resource`/`toolbar.resource`) + a suite.
- **One shared-pattern gap found while building the T3:** every operation (Insert/Update/Delete) MUST
  call `Refresh Screen` after `Save`, matching the proven `Language` T3 exemplar exactly - my first
  draft omitted it and TC03/TC04 both failed with Save-button timeouts (the toolbar's Save state
  needs the explicit reload to settle before the next operation's cell-click can re-enable it).
- **One flaky residual found and resolved:** an early debug run of the RF suite (before the
  `Refresh Screen` fix was fully applied to all 3 keywords) left one `AUTOTEST_CS_<timestamp>` row
  live; a second debug run (with the fix) also showed a residual row once, which did NOT reproduce on
  a clean third run - treated as a timing artifact from an interrupted debug session, not a
  systemic issue, since the current code has now self-cleaned correctly on repeated live runs.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4 pass,
  Playwright driver 7/7. DB residual 0 (confirmed via direct query after the final run).

## Lessons
- **Never assume a visually-uppercase menu label matches an uppercase DOM string search** - CSS
  `text-transform` is extremely common in this app's toolbar styling and makes visual screenshots
  misleading for building selectors. Always read the actual `onclick`/text content via
  `page.evaluate` or `outerHTML`, not just what a screenshot shows.
- **When an Insert AND a Delete icon both show an identically-worded submenu item, scope the search
  to the specific icon's own `<li>` ancestor** - a global text search will silently match the wrong
  one's (usually invisible/disabled) copy. This project's own `table_class.resource` already encodes
  this exact lesson in its keyword documentation ("the Delete submenu often has an identically named
  item") - should have consulted it before spending significant effort re-discovering the same gap.
- This single root-cause fix (case-sensitivity + correct scoping) is expected to directly unblock
  Stream Item and Production Day Table too, which share the identical toolbar shape and symptom.
