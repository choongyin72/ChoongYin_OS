# SOW — Lifting Account IUD (Configuration > Assets > Transport_Objects)

**Backfill note (2026-08-28):** this SOW REFRESHES the pre-existing bundle written for the original
2026-07-30 hand-built build (see history below), to reflect the 2026-08-27 Area-pattern conversion
(PR #562) under `docs/lean-deliverable-backfill-workorder.md` Batch 5. The RF automation itself was
NOT rebuilt or re-verified from scratch for this backfill task — it already exists, is already
merged to master, and already passed its live-canary gate. This document is sourced from PR #562's
own body/review-comment history, the real page-object/suite files, and
`docs/ec_screen_registry.md`, not invented.

## Current classification (post PR #562)
- **Screen:** Lifting Account — **BF:** CO.2004 — **View:** `OV_LIFTING_ACCOUNT` (versioned/
  date-effective; key `CODE`)
- **Type:** OV-GM (groupmodel manage-object), navigator-gated — grid stays empty until the mandatory
  navigator cascade is filled and GO is clicked.
- **Pattern:** Area-pattern (5-TC, per-TC login/logout, properties-file-driven insert/update,
  explicit grid-filter wiring, pure-screen verification) — grid `manageObject:form:T_data`.

## Navigator shape — the real, verified story
An earlier UNVERIFIED chat-level classification had flagged this screen's navigator as "two separate
rows/groups" — a shape that would disqualify it from the shared Area-pattern navigator keyword (that
disqualifying shape is Tract's precedent: genuinely separate `G:1`/`G:2` fieldsets). Live per-field DOM
recon during the PR #562 build corrected this: Lifting Account's navigator is **ONE fieldset**
(`nav:form:G:0`), not two groups. Its mandatory 4-value cascade is simply *rendered* across TWO grid
rows within that single group:
- **R:1** — `C:1` Production Unit, `C:2` Area, `C:3` Facility Class 1
- **R:3** — `C:0` Storage

All four dropdown spans were confirmed live to carry `{mandatory:true} MandatoryCellStyle` (genuinely
empty on load). This is a genuinely novel shape versus every other screen surveyed for the Area
pattern up to that point — distinct from Tract's separate-groups shape and from the plain
single-row-per-field-groups shape used elsewhere.

## Shared-keyword extension (and the regression it caused — read this)
Because the pre-existing shared T2 keyword `Apply Navigator From Properties`
(`resources/manage_object.resource`) only supported a single row (`${row}`/`${group}`/`${start_col}`),
the PR #562 build extended it with three new **optional** arguments — `${row2_from}`, `${row2}`,
`${row2_start_col}` — to span the row break in one call, filling all four values then clicking GO
exactly once (matching the pre-existing hand-built driver's fill-both-rows-then-GO-once sequence,
below).

**This shared-file change shipped with a real bug on the first attempt.** The reviewer's mandatory
live-canary requirement (2+ existing callers of a changed shared keyword, live, every time — no
exceptions) caught it before merge: Robot Framework substitutes `${row2_from}` **textually** before
the boolean IF condition is evaluated, so its empty default (`${EMPTY}`, used by every caller except
this one) collapsed the condition `"${idx} > ${row2_from}"` to `"1 > "` — invalid Python syntax,
**unconditionally**, for every existing caller. Area and Meter both failed the live canary 0/5 with an
`Invalid IF condition ... SyntaxError`. The fix switched to RF's native-variable syntax (`$var`, no
braces) inside a dedicated `Evaluate` call with an explicit `int()` conversion, avoiding the textual
pre-substitution trap. Re-canaried after the fix: Area 5/5, Meter 5/5, Lifting Account's own suite
5/5 (one unrelated transient locator-click timeout on the first TC01 attempt, clean on immediate
re-run). Full-tree dryrun re-confirmed 883/883, zero collisions. This is one of the most important
incidents in this backfill project's history — a real regression that reached a PR and was caught by
the review gate before merge, not after. See `JOURNAL.md` for the full timeline.

## Grid / cell shape
- **Grid:** `manageObject:form:T_data`
- **Insert form (`objectForm`, label-driven):** Lifting Account Code*, Lifting Account Name*,
  Start Date* (date), Company Name* (first-available), Storage Name* (must equal the navigator's own
  Storage value — parent-matching rule, or the new row is invisible under this OV-GM scope).
- **Update (`updateAttributes`):** Lifting Account Code (read-only), Lifting Account Name.
- **Delete (`objectdates`):** End Date = Start Date (true delete in `OV_LIFTING_ACCOUNT`), field id
  `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` — hardcoded deliberately (same rationale as
  Area/Bank's own del-enddate id), confirmed live via the pre-existing Playwright driver.

## Test data used (unchanged from the original 2026-07-30 build — field-reuse rule)
- Fixed test code `AUTOTEST_LA_001`, confirmed absent from `OV_LIFTING_ACCOUNT` via a fresh oracledb
  query before it was wired into the Area-pattern suite.
- Navigator: P1 Production Unit → P1 Area → P1 Facility 1 → Storage `P1_CRUDE_STOR` — the SPECIFIC
  scope originally owner-provided (2026-07-30, unparked via owner walk-through + screenshot) and
  proven live by the original hand-built driver (`py/lifting_account_iud.py`, commit `6e88e371`),
  reused verbatim, not re-derived. Storage has no options under the first-available AS1 path, which
  is why this screen was originally parked, then hand-built, rather than automated with a generic
  first-available cascade.
- Insert: `Lifting Account Name=AUTOTEST Lifting Account 001`, `Start Date=2020-01-01`,
  `Company Name=__FIRST__` (146 companies effective at Start Date 2020-01-01, DB-checked in the
  original build), `Storage Name=P1_CRUDE_STOR` (must match the nav Storage value).
- Update: `Lifting Account Name=AUTOTEST Lifting Account 001 UPDATED`.
- All five properties files now live at `testdata/lifting_account_{navigator,insert,update,
  form_verify,grid_verify}.properties` (properties-file-driven since PR #562; the original build's
  test data lived inline in the hand-built driver/T3).

## Dev story
**2026-07-30 (original build, PARKED then UNPARKED):** an early scan found a 4th mandatory nav
dropdown (Storage) that timed out empty under the generic first-available `AS1` path — the grid
never loaded, so the screen was parked. It was unparked after the owner walked through the working
scope with a screenshot: P1 Production Unit → P1 Area → P1 Facility 1 → Storage `P1_CRUDE_STOR`,
with Storage sitting on a second navigator row below Date. Because the generator supported neither a
second nav row nor specific (non-first-available) nav values, the screen was hand-built: a thin
Playwright driver with a screen-local `apply_lifting_account_navigator`, and an RF T3 with a
screen-local `Apply Lifting Account Navigator` keyword. `verify_screen.py` returned OVERALL PASS
(dryrun 4/4, live RF 4/4, Playwright 8/8, DB residual 0).

**2026-08-27 (PR #562, Area-pattern conversion):** upgraded the hand-built RF automation to the full
Area-pattern shape (5-TC, per-TC login/logout, properties-file-driven, explicit grid-filter wiring).
Required correcting a prior unverified chat-level classification of the navigator as "two separate
groups" via live DOM recon, which found instead a single group whose cascade spans two rendered
rows — leading to the new `${row2_from}`/`${row2}`/`${row2_start_col}` extension of the shared
navigator-fill keyword described above. That extension broke every other screen using the keyword on
its first attempt, was caught by the reviewer's mandatory live-canary gate before merge, fixed with
RF's native-variable `Evaluate` syntax, and re-verified live (Area 5/5, Meter 5/5, Lifting Account
5/5) before the PR was merged to master at `6a8c328`. The Playwright driver (`py/
lifting_account_iud.py`) was left untouched — this was an RF-only structural conversion.

## Lessons
- Live per-field DOM recon overrides any unverified chat-level classification — the "two rows within
  one group" vs. "two groups" distinction was only knowable by looking at the real DOM.
- A "deep cascade with an empty level" park can be a DATA-SCOPE gap, not a structural blocker: the
  Storage level was empty only under the first-available path, not under every path.
- A shared-keyword change that *restructures* existing logic (not just appends an optional arg) is
  exactly the case the live-regression-canary rule exists for; a full-tree dryrun proves syntax, not
  behavior, and passed the dryrun while still breaking every existing caller live.
- RF substitutes `${var}`-style variables textually before an IF condition is parsed; an empty-string
  default can collapse a numeric comparison to invalid syntax. Use native `$var` syntax inside
  `Evaluate` for anything that needs to stay valid Python when the argument is unset.

## Known risks (carried from the original build)
- The nav scope is DATA-dependent (P1 objects): if the sandbox's `P1_CRUDE_STOR` storage or the P1
  cascade is removed/renamed, the suite fails at navigator-apply — re-derive a working scope the same
  way (owner walk-through or DB query of storages under a facility).
