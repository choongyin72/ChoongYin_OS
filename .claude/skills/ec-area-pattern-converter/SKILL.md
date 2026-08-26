---
name: ec-area-pattern-converter
description: Use when upgrading an EC (Energy Components) screen's EXISTING RF automation, where the screen has a NAVIGATOR section (OV-GM), to the full "Area pattern" — e.g. "convert <screen> to the Area pattern", "bring <screen>'s navigator screen up to full pattern", "apply the shared navigator keyword to <screen>". The screen already has SOME RF automation and a navigator section matching Area's layout (single dropdown, or a same-row/increasing-column cascade, or a zero-mandatory-value GO-only navigator) and needs upgrading to the properties-file-driven, per-TC-login, T2-consolidated shape used by `area_page.resource`. Distinct from `ec-bank-pattern-converter`, which is for screens with NO navigator section at all.
---

# EC Area-Pattern Converter — upgrade an existing navigator-screen's RF automation

> **INPUT CONTRACT: the user gives one or more EC screen names.** You determine each screen's
> current pattern, confirm its navigator matches Area's supported shape, convert it if
> eligible, and raise a PR — hands-off. Only come back to the user for: a genuine blocker, a
> navigator shape that doesn't fit (log it, don't force it), or a merge-authorization decision.

Distilled from the Area role-model conversion (PR #521/#523, then proven reusable on External
Location/Field/Facility Class 1, PRs #524-530, 2026-08-26). Area is the OV-GM (navigator-bearing)
counterpart to Bank — the owner's standing rule: **any EC screen with a navigator section, whose
layout otherwise matches Area, MUST follow Area's full pattern**, the same status Bank already
holds for non-navigator screens. Read `docs/SUBAGENT-DELEGATION-GUIDE.md` before dispatching any
part of this as a subagent batch.

## Step 0 — confirm the navigator shape fits Area's supported case

Area's pattern only fits screens whose navigator is addressed as **one row, increasing column**:
`nav:form:G:0:R:${row}:C:1`, then `C:2`, then `C:3`... (all cascade levels on the SAME row).
Proven live across 4 shapes so far:
- **Zero mandatory values** (External Location) — navigator fields are optional filters, GO
  alone loads the grid.
- **Single dropdown** (Area's own Production Unit; Field's Area dropdown).
- **2-level same-row cascade** (Facility Class 1: Production Unit → Area, C:1 then C:2).
- (Not yet proven, but should fit by design: 3+ level same-row cascades, e.g. Well's PU→Area→
  Facility Class 1 shape — verify live before assuming.)

**Does NOT fit — do not force it.** If live recon shows the navigator uses PER-FIELD groups
(a distinct `G:` id per cascade level, not one row's increasing column index), a POPUP-based
child-object picker instead of a plain dropdown, or any other structurally different mechanism —
**STOP, do not convert.** Append a row to
`workstreams/master-plan/ec-automation/docs/navigator-screens-not-matching-area.md` with the
real shape found and why it doesn't fit (live evidence, not assumption), and report this plainly.
This is a legitimate, useful result — not a failure.

Confirm live via a DOM scan (grep the screen's own JS click handlers / a Playwright element dump
for `id^="nav:form:G:0:R:"`) — never assume from a sibling screen's shape, and never trust an old
survey/registry note's navigator description at face value (this project has repeatedly found
navigator-shape doc claims wrong, including on Area's own siblings).

## The three starting patterns (classify BEFORE touching anything)

Grep the screen's existing `pageobjects/.../<screen>_page.resource`:

| Pattern | Signal | What's needed |
|---|---|---|
| **FULL Area pattern (already done)** | Has `Apply Navigator From Properties` AND 5 TCs AND per-TC login AND fixed test code AND zero inline DB-verify calls | Nothing — skip it |
| **PARTIAL** | Has `Apply Navigator From Properties` (navigator-fill delegated) but is missing one or more of: TC04 Find, per-TC login, fixed test code, zero inline DB-verify calls | Add the missing piece(s) — this is the exact gap PRs #528/#529/#530 closed |
| **OLD** | Bespoke inline navigator-fill (`Select EC Dropdown Option`+`Apply Navigator`, or `Apply OV-GM Navigator First Available`), 4 TCs, single suite-level login, generated/timestamped test code, possibly inline DB-verify calls | Full rebuild: delegate navigator-fill to the shared keyword AND bring the rest of the structure to Area's shape, in the same pass |

**Do not scope narrower than the full pattern unless explicitly told to.** A prior round of this
project's own work (2026-08-26) deliberately scoped 3 screens to "just test the navigator
keyword," leaving the rest of their structure on the old pattern — the owner corrected this
directly: once a screen is being touched for its navigator, it should reach FULL Area parity in
the same pass, not a follow-up. Only scope narrower if the user's own instruction explicitly says
so for that specific screen (e.g. "just test the keyword on X").

## The shared navigator keyword — use it, don't reinvent it

`Apply Navigator From Properties    ${properties_path}    ${row}=1` lives in
`resources/manage_object.resource` (added 2026-08-26, proven across 4 screens, zero shared-file
changes needed on 3 of them). It reads a `<screen>_navigator.properties` file via
`PropertiesReader.Read Properties` (same mechanism `Insert/Update Object From Properties`
already use), fills each line in file order against the same-row/increasing-column navigator
dropdowns via `Select EC Dropdown Option`, then clicks `Apply Navigator` once. An intentionally
EMPTY (comments-only) properties file degrades gracefully to a bare GO click — already proven on
External Location, no special-casing needed.

**Before using it, confirm the target page object's own `.resource` file imports
`libraries/PropertiesReader.py`** — several existing OV-GM screens never had a properties-file
mechanism before (Field didn't), so the shared keyword's `Read Properties` call fails at
suite-setup time with "No keyword with name 'Read Properties' found" until the import is added.
The mandatory full-tree dryrun (see Verification below) will catch this if missed — but check for
it up front to save a wasted run.

**Do not modify `resources/manage_object.resource` itself** unless you find a genuine gap the
keyword doesn't cover (e.g. a navigator shape it doesn't support — see Step 0). If you do need a
shared-file change, follow the full safety protocol: back up the file first, additive-only
(never change an existing keyword's signature), full-tree dryrun, AND a live regression canary on
2+ EXISTING screens that already use the keyword (e.g. re-run Area's own suite) to prove no
regression — this is mandatory, not optional, every time the shared file changes.

## Recon-first, no guessing

- Read the screen's OWN existing page object and OWN existing driver before writing any new
  config. Never extrapolate field labels, mandatory sets, grid ids, or the navigator's real
  values from a sibling screen.
- Confirm the fixed `AUTOTEST_<SCREEN>` test code is free in the DB (fresh oracledb connection:
  dsn `localhost:1521/ORCL`, user `ECKERNEL_EC`, password `energy`) before using it.
- Confirm the navigator's real value(s) live — don't invent a plausible-looking PU/Area/etc.
  code; reuse whatever the screen's own already-working driver/suite already proved live.
- If the objectForm exposes fields the registry/prior build didn't mention as mandatory (this
  happened on Facility Class 1 — "Op Production Unit"/"Op Area" turned out to exist on the form),
  do NOT add them as new requirements if the already-proven driver passes without filling them —
  trust the proven behavior over a static field-presence scan (don't hunt unstated requirements).

## Build

Mirror `area_page.resource`/`area_iud.robot`'s CURRENT (post PR #521/#523) shape exactly:
- Per-TC `Login To EC Application`/`Logout From EC Application`, 5-TC business narrative (TC01
  Verify Clean State / TC02 Insert / TC03 Update / TC04 Find / TC05 Delete), fixed test code,
  dedicated `<SCREEN>_EC_USER`/`<SCREEN>_EC_PASS` pair appended (additive only) to
  `resources/credentials.py`.
- A single `Open <Screen> Screen With Navigator Values Populated` T3 keyword that opens the
  screen AND calls `Apply Navigator From Properties` with the screen's own
  `<screen>_navigator.properties` file — one line per TC in the test file, not two separate
  calls.
- Reuse shared T2 keywords as-is: `Insert/Update Object From Properties`, `Verify Object Insert
  Exists/Form Record/Found/Removed/Does Not Exist`, `Find/Clear Object Row By Filter`.
- A thin T3 wrapper `Find/Clear <Screen> Row By Filter` delegating to the shared T2 filter
  keywords, wired into **Update/Find/Verify-Found/Delete only**.
- 4 properties files under `testdata/`: `<screen>_{insert,update,form_verify,grid_verify}.properties`,
  plus the new `<screen>_navigator.properties`.
- PURE SCREEN verification only — zero inline DB-verify calls (`Should Exist In DB`, `Field
  Should Equal In View`, `Code Should Be Present/Absent In View`) in the `.robot` file. Confirm
  by grep, not by trusting the suite passes.
- Keep the screen's GENUINE navigator requirement exactly as it is — this conversion is about
  STRUCTURE, never about removing or faking a real mandatory-scope requirement.

## Verification — every step must actually run, cite real output

1. `py -m robocop check <changed files>` — compare against Area's own current baseline; parity =
   not a regression.
2. `robot --dryrun` on the FULL `tests/` tree — must stay 100% pass.
3. Live run, `EC_HEADLESS=true`, of the screen's own suite — must be 5/5.
4. Independent DB self-clean: a FRESH oracledb connection, 0 residual `AUTOTEST%` rows, checked
   AFTER the live run.
5. Confirm the filter keyword fired: `grep -c "Find Object Row By Filter" output.xml` (or the
   screen-specific wrapper name) — non-zero.
6. If the navigator has a dependent (cascading) 2nd-level dropdown: confirm the shared keyword's
   flat sleep is sufficient for THIS screen's redraw timing — if a live failure shows it isn't,
   do not silently patch just this screen; flag whether the shared keyword's default needs
   revisiting (this has NOT been needed yet across 4 screens, but don't assume it never will be).
7. If you touched the shared file: also re-run Area's own suite live as a regression canary.

Never report "done" without having actually run all applicable steps and citing the real numbers.

## Blocker / scope-mismatch protocol

Same as `ec-bank-pattern-converter`: retry once with a genuine evidence-based fix, then STOP and
log BLOCKED with exact evidence — don't grind. A navigator shape that doesn't fit Area's pattern
is a SCOPE MISMATCH, logged to `docs/navigator-screens-not-matching-area.md`, not a failure.

## Git / PR

Same isolated-clone/sparse-checkout, explicit-path-commit, sync-before-push, 6-field-PR-body,
never-self-merge discipline as `ec-bank-pattern-converter`. **Before writing "PR #N is already
merged" into any dispatch prompt or PR body, actually check via a PR-read tool** — this project
hit real wrong-base-branch problems twice (Area's own PR #521/#522, then the External
Location/Field/Facility Class 1 follow-ups) from stating an unverified merge status as fact. If
the screen's own row already exists in `docs/ec_screen_registry.md`/`docs/automation-scorecard.md`,
say explicitly you're MODIFYING it, not adding a new one.

## Running this as a batch of N parallel screens

Same orchestration as `ec-bank-pattern-converter`'s batch playbook (classify first, pre-create
+ wait-for-merge on any shared checklist header, one subagent per screen in an isolated clone,
independently re-verify every PR via a read tool before counting it done, personally spot-check
1-2 screens live after the batch merges). One extra step specific to navigator screens: if ANY
screen in the batch turns out not to fit Area's supported navigator shape, don't let that block
the rest of the batch — log it to the not-matching-Area checklist and continue with the others.

## What "done" looks like for a screen

5 TCs, per-TC login/logout, navigator filled via the shared `Apply Navigator From Properties`
keyword, fixed test code, properties-file-driven insert/update/verify, explicit grid-filter
wiring, zero inline DB-verify calls — matching `area_page.resource`/`area_iud.robot` exactly,
with the screen's own genuine navigator requirement kept intact. Live 5/5, dryrun 100% on the
full tree, DB self-clean confirmed via a fresh connection, filter keyword confirmed fired, no
unauthorized shared T1/T2 file changes, registry/scorecard docs updated, PR raised (not
self-merged).
