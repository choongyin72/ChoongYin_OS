# RF Suite Styles — convention (owner + Reviewer decision, 2026-08-18)

Resolves Issue #403 (Reviewer's RF best-practice assessment of PR #402's Bank suite style).
Bottom line: the Bank shape (per-TC login/logout, 5-line narrative, `simple_report.py` output) is
a good **client-demo** shape but should not become the default for the regression fleet wholesale.
This doc names two suite styles and states which elements of Bank's build belong in each.

## The two styles

| Style | When to use | Login | Everything else |
|---|---|---|---|
| `client-demo` | Showing a screen's IUD flow to a client/owner, or explicitly demonstrating "real login/logout per action" | Per-TC (`Login To EC Application` / `Logout From EC Application`, own Suite Setup only opens the browser) | Same T2/T3 keywords as `regression` |
| `regression` | The default for the 92-screen fleet, CI runs, anything not specifically a client demo | ONE login in Suite Setup (`Launch EC And Open Screen`, unchanged), ONE logout in Suite Teardown | Same T2/T3 keywords as `client-demo` |

A screen can have both — the T2/T3 layers built for Bank already support either shape, since the
login mechanics and the business keywords are separate concerns.

## Element-by-element (owner + Reviewer decisions on Issue #403's 6 points)

**1. Per-TC Login/Logout — style-specific, not universal.** Owner correction (2026-08-18): *"actual
RF will not act that way — only need re-login if need different role access."* Standard test-
engineering guidance agrees: login is expensive shared state and belongs in Suite Setup; test
independence comes from data/state isolation, not from repeating the slowest step per test. Per-TC
login on a 5-test suite (Bank) costs little and reads well for a client demo. Scaled to the fleet
(hundreds of TCs) it multiplies wall-clock by the login count for zero extra defect-finding power —
the login path itself only needs testing once per run.
**Rule:** `regression` suites default to Suite Setup/Teardown login (the pre-Bank pattern, unchanged
for every other current suite — Equipment etc.). Per-TC login is reserved for `client-demo` suites,
or for a `regression` suite that specifically needs to test with a DIFFERENT USER/ROLE per test case
(a real access-control test) — in that case, pass the differing credentials as arguments to
`Login To EC` (already supports this) inside that one test, not as a suite-wide pattern.

**2. `Ensure Logged Out From EC Application` teardown net — adopt everywhere, unconditionally.**
This fixes a real cascading-failure class (one mid-TC failure leaving the browser logged in, which
then fails every later test's login on a missing `#username` field) and costs nothing when it
no-ops. It belongs in `regression` suites too, as a standard `Test Teardown`, even though those
suites don't otherwise do per-TC login/logout — a `regression` suite can still have a single test
fail mid-way and leave the app in a bad state for the next test, so the safety net is
style-independent.

**3. 5-line business-narrative TCs with zero arguments — keep, both styles, no caveats.** This is
textbook RF keyword-driven design: the test case is pure business intent (WHAT), all technical
mechanics (HOW — locators, field-kind detection, DB queries, credentials) live in T2/T3 keywords
underneath. Unlike point 1, this has no scale tradeoff — a business-readable, zero-argument test
case is strictly better for readability/maintainability whether the suite has 5 tests or 500.
Confirmed already correct in Bank; no code change needed, just documenting the pattern here so
future suites follow it deliberately rather than by copying Bank.

**4. Properties-file test data — keep the concept for Bank; standardize the FORMAT going forward.**
Externalized test data (not hardcoded in the test case or arguments) is good practice and stays.
Format decision for **new** suites: prefer RF's **native Variables files** (`.py` or `.yaml`) over
`.properties` — RF loads these directly (`Variables testdata/bank_insert.yaml`), no custom parser
needed, and YAML gives typed values and nesting for free (a `.properties` file is flat strings only,
requiring the caller to know every value is a string). `.properties` needed `libraries/
PropertiesReader.py` specifically because RF has no native reader for that Java-convention format.
**Decision:** Bank's `.properties` files are NOT converted retroactively — not worth the churn on an
already-merged, working suite. New suites built after this doc should use `.yaml` Variables files
instead, so the fleet converges on one native format rather than accumulating three.

**5. Screen-vs-DB oracle rule — generalize, it's correct.** The Country finding (live recon,
2026-08-18: `COUNTRY_CODE = 'NL'` in the database while the screen and properties file both show
`"The Netherlands"`) yields a general rule, not a Bank-specific one:
> **A field's value is verified against the SCREEN when the database stores a different internal
> representation than what's displayed (dropdowns/reference fields backed by a code, GUID, or
> lookup id). A field is verified against the DATABASE when the stored value equals the displayed
> value (plain text fields), or when the check is existence/absence rather than a value comparison
> (those have no representation-mismatch risk).**
This is a per-FIELD oracle choice, not a per-suite one — a single suite can and should mix both
(Bank's TC02/TC03 do: Name/Description/Swift Code/Address via DB or screen as appropriate, Country
via screen only, existence/absence via DB). This rule is cross-referenced in
`ec-ui-knowledge/EC_KNOWLEDGE_BASE.md` (see that file's "UI ↔ DB value mapping" note) so it's found
during EC screen work generally, not only when reading this RF-specific doc.

**6. Per-screen credential files — cap the pattern now.** `resources/credentials.py`
(`BANK_EC_USER`/`BANK_EC_PASS`) is fine as Bank's own interim file, but 90 screens × per-screen
prefixed variables would sprawl badly, and the owner's stated future secrets-store migration lands
easier on one mechanism than on N per-screen files.
**Decision:** do not create another per-screen `credentials.py` for the next suite. Default every
screen to the shared `environment.py` (`EC_USER`/`EC_PASS`) unless a real, specific reason exists to
override it — and if one does, pass the override as an explicit argument to that suite's Login
keyword (already supported) rather than adding a new per-screen variables file. Bank's existing
`credentials.py` is left as-is (already merged, low cost to keep) — this decision only caps FUTURE
screens from replicating the pattern.

## Summary table for a new suite

| Decision point | Default for a NEW suite |
|---|---|
| Login/Logout | Suite Setup/Teardown (`regression` style) unless the suite is explicitly a client demo |
| Teardown safety net | Always include an `Ensure Logged Out`-style Test Teardown |
| Test case shape | 5-line-or-similar business narrative, zero arguments, mechanics in T2/T3 |
| Test data format | `.yaml` Variables file (not `.properties`) |
| Field verification oracle | Screen for display-mapped fields, DB for plain-value/existence checks |
| Credentials | Shared `environment.py` `EC_USER`/`EC_PASS`; per-screen override only via an explicit Login argument, not a new credentials file |

Issue #403 closed by this doc.
