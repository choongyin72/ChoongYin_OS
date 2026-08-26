---
name: ec-area-pattern-new-screen
description: Use when building a BRAND-NEW RF suite (no existing automation at all) for an EC screen that has a NAVIGATOR section (OV-GM) with the SAME LAYOUT as Area — e.g. "build the Area-pattern RF suite for <screen>", "automate <screen> like Area, RF only". Produces the lean, RF-only deliverable matching `area_page.resource`/`area_iud.robot`'s current shape, using the shared `Apply Navigator From Properties` keyword. For a navigator screen that already has SOME automation to upgrade, use `ec-area-pattern-converter` instead. For a screen with NO navigator section at all, use `ec-bank-pattern-new-screen` instead.
---

# EC Area-Pattern New Screen — lean RF-only build from scratch, for navigator screens

> **INPUT CONTRACT: the user gives an EC screen name (or a batch of names).** You classify,
> recon, build, verify, and raise a PR — hands-off. Only come back to the user for: a genuine
> blocker, a navigator shape that doesn't fit Area's pattern (log it, don't force it), or a
> merge-authorization decision.

The navigator-screen counterpart to `ec-bank-pattern-new-screen`. Area is the OV-GM role-model
(the owner's standing rule, 2026-08-26: any navigator screen matching Area's layout follows
Area's full pattern, same status Bank holds for non-navigator screens). Read
`docs/SUBAGENT-DELEGATION-GUIDE.md` before dispatching any part of this as a subagent batch.

## Step 0 — check it's genuinely new, and genuinely Area-shaped

- `grep -ril "<screen-slug>" workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}`
  — if ANYTHING turns up, this is not a from-scratch case; switch to `ec-area-pattern-converter`
  instead.
- Confirm the screen genuinely has a navigator section (OV-GM) — if it has none at all (plain
  Date+GO or no navigator), use `ec-bank-pattern-new-screen` instead, not this skill.
- Confirm the navigator is addressed as **one row, increasing column**:
  `nav:form:G:0:R:${row}:C:1`, then `C:2`, then `C:3`... — proven live on 4 shapes so far: zero
  mandatory values (GO-only), single dropdown, and 2-level same-row cascades. Confirm via a live
  DOM scan, not from a sibling screen's shape or an old survey note.
- **Does NOT fit — do not force it.** Per-field navigator groups (a distinct `G:` id per cascade
  level), a POPUP-based child-object picker, or any other structurally different mechanism: STOP,
  do not build with this skill. Append a row to
  `workstreams/master-plan/ec-automation/docs/navigator-screens-not-matching-area.md` with the
  real shape and evidence, and report plainly — this is a legitimate, useful result.

## Step 1 — recon (DB-first, then one live scan)

- **DB metadata**: resolve `CLASS_TYPE` (`OBJECT`⇒OV) and `TIME_SCOPE_CODE` (`VERSIONED`⇒
  date-effective, End=Start delete), plus the base table / version table / `OV_<class>` view name
  — via `tmp/scripts/resolve_ec_screen.py` if present in the repo, else a direct
  `class_cnfg`/`class_property_cnfg` query.
- **Live scan** (read-only, never Saves): open the screen, confirm the navigator's real shape
  (which fields, mandatory or optional, single dropdown vs cascade vs zero-mandatory), the grid
  id (`manageObject:form:T_data` for OV-GM), and the New-Object (`objectForm`)/Update
  (`updateAttributes`) field ids with mandatory flags and real labels (screen-prefixed vs
  generic Code/Name — never assume either way).
- Confirm the fixed `AUTOTEST_<SCREEN>` test code is free in the DB (fresh oracledb connection:
  dsn `localhost:1521/ORCL`, user `ECKERNEL_EC`, password `energy`) before using it.
- Confirm the navigator's real value(s) live (e.g. which Production Unit/Area/etc. option to
  use) — don't invent a plausible-looking code; pick one that genuinely exists and is selectable.

## Step 2 — build (RF only, label-driven, T2-consolidated, navigator via the shared keyword)

Mirror `area_page.resource`/`area_iud.robot`'s CURRENT shape exactly:
- `pageobjects/<menu path>/<screen>_page.resource` — thin T3, locators from Variables. A single
  `Open <Screen> Screen With Navigator Values Populated` keyword that opens the screen and calls
  the shared T2 `Apply Navigator From Properties    ${<SCREEN>_NAVIGATOR_PROPERTIES}`
  (`resources/manage_object.resource`) — do NOT inline a bespoke `Select EC Dropdown Option`+
  `Apply Navigator` call; the shared keyword already covers zero-value, single-dropdown, and
  same-row-cascade shapes.
- **Confirm `libraries/PropertiesReader.py` is imported** in the new page object — the shared
  navigator keyword's `Read Properties` call needs it; a missing import fails at suite-setup
  time with "No keyword with name 'Read Properties' found," caught by the mandatory dryrun if
  missed.
- `tests/<menu path>/<screen>_iud.robot` — 5-TC business narrative (TC01 Verify Clean State /
  TC02 Insert / TC03 Update / TC04 Find / TC05 Delete), per-TC `Login To EC Application`/
  `Logout From EC Application`, fixed test code, dedicated `<SCREEN>_EC_USER`/`<SCREEN>_EC_PASS`
  pair appended (additive only) to `resources/credentials.py`.
- All field fills via T2's `Fill OV Field By Label`/`Insert Object From Properties`/`Update
  Object From Properties` — never a hardcoded `…R:<n>:C:<n>:in` id.
- Explicit `Find/Clear <Screen> Row By Filter` T3 wrapper delegating to shared T2's `Find/Clear
  Object Row By Filter`, wired into Update/Find/Verify-Found/Delete only.
- 5 properties files under `testdata/`: `<screen>_{insert,update,form_verify,grid_verify,navigator}.properties`.
- PURE SCREEN verification only — zero inline DB-verify calls in the `.robot` file.
- Delete = **End Date = Start Date** (date-effective OV) via the `objectdates` form, same as
  every other OV/OV-GM screen.

## Hard rule: never touch shared files unless a genuine gap is found

**Do NOT edit `resources/manage_object.resource` or `resources/common.resource`** unless the
navigator shape genuinely needs something the existing `Apply Navigator From Properties`
keyword doesn't cover (see Step 0's fit check — if it doesn't fit, that's a scope-mismatch to log,
not a reason to extend the shared keyword solo). If a shared-file change is ever genuinely
warranted, follow the full safety protocol: backup first, additive-only, full-tree dryrun, AND a
live regression canary on 2+ existing screens using the keyword (e.g. re-run Area's own suite).

## Step 3 — verify (every step must actually run, cite real output)

1. `py -m robocop check <changed files>` — compare against Area's own current baseline; parity =
   not a regression.
2. `robot --dryrun` on the FULL `tests/` tree — must stay 100% pass.
3. Live run, `EC_HEADLESS=true`, of the new suite — must be 5/5.
4. Independent DB self-clean: a FRESH oracledb connection, 0 residual `AUTOTEST%` rows, checked
   AFTER the live run.
5. Confirm the filter keyword fired: `grep -c "Find Object Row By Filter" output.xml` (or the
   screen-specific wrapper name) — non-zero.
6. Confirm zero inline DB-verify calls remain: grep for `Should Exist In DB`/`Field Should Equal
   In View`/`Code Should Be Present/Absent In View` in the `.robot` file — no matches.

Never report "done" without having actually run all five and citing the real numbers.

## Blocker protocol

Same as `ec-bank-pattern-new-screen`: retry once with a genuine evidence-based fix, then STOP and
log BLOCKED with exact evidence. A field that looks optional in a static scan but a Save
silently fails without it may be a conditional-mandatory business rule — re-test with it included
before concluding it's a defect. A navigator shape that doesn't fit Area's pattern is a SCOPE
MISMATCH for `docs/navigator-screens-not-matching-area.md`, not a failure.

## Git / PR

Same isolated-clone, explicit-path-commit, sync-before-push, 6-field-PR-body, never-self-merge
discipline as `ec-bank-pattern-new-screen`. Append a NEW row to
`docs/ec_screen_registry.md`/`docs/automation-scorecard.md` (this is a genuinely new screen).
**Before writing any PR's merge status into a dispatch prompt, verify it via a PR-read tool** —
don't state "already merged" from memory.

## Running as a batch of N new screens

Same orchestration as `ec-bank-pattern-new-screen`'s batch playbook. If any screen in the batch
turns out not to fit Area's supported navigator shape, log it to the not-matching-Area checklist
and continue with the rest — don't let one mismatch block the batch.

## What "done" looks like

5 TCs, per-TC login/logout, navigator filled via the shared `Apply Navigator From Properties`
keyword, fixed test code, properties-file-driven insert/update/verify, explicit grid-filter
wiring, zero inline DB-verify calls — matching `area_page.resource`/`area_iud.robot` exactly.
Live 5/5, dryrun 100% on the full tree, DB self-clean confirmed via a fresh connection, filter
keyword confirmed fired, no unauthorized shared T1/T2 file changes, new registry/scorecard rows
added, PR raised (not self-merged). No Playwright bundle, SOW, JOURNAL, evidence, or KB-map entry
required — if those are wanted, use `ec-object-iud-builder` instead.
