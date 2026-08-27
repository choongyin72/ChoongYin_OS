---
name: ec-bank-pattern-new-screen
description: Use when building a BRAND-NEW RF suite (no existing automation at all) for an EC screen that has the SAME LAYOUT as Bank — e.g. "build the Bank-pattern RF suite for <screen>", "automate <screen> like Bank, RF only". Produces the RF suite plus SOW/README/JOURNAL/evidence/CHECKLIST/KB-map bundle (owner decision 2026-08-27 — no Playwright bundle, since the Universal Screen Engine replaces it), matching the style of Batches 2-11's `bank_page.resource`/`berth_page.resource`. For a screen that already has SOME automation to upgrade, use `ec-bank-pattern-converter` instead.
---

# EC Bank-Pattern New Screen — RF-only build from scratch (with full bundle deliverables)

> **INPUT CONTRACT: the user gives an EC screen name (or a batch of names).** You classify,
> recon, build, verify, and raise a PR — hands-off. Only come back to the user for: a genuine
> blocker, or a merge-authorization decision.

This is the "from scratch" counterpart to `ec-bank-pattern-converter` — same target shape and
verification bar, but the screen has ZERO existing RF automation to read first, so recon comes
from DB metadata + a live scan instead of an existing driver. **Owner decision 2026-08-27**
retired the earlier lean waiver: this skill now also produces the SOW/README/JOURNAL/evidence/
CHECKLIST/KB-map bundle (see "Bundle deliverables" below) — the only thing still NOT built is a
hand-written Playwright driver, since the Universal Screen Engine is the owner-decided
replacement for that role going forward.

## Step 0 — check it's genuinely new, and genuinely Bank-shaped

- `grep -ril "<screen-slug>" workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}`
  — if ANYTHING turns up, this is not a from-scratch case; switch to `ec-bank-pattern-converter`
  (upgrade existing) instead of duplicating effort.
- Check `docs/ec_screen_registry.md` for the screen's navigator shape. Not listed, or listed as
  ambiguous ("optional" dropdown/date)? Do not assume nav-free — recon live before building.
- Bank-shaped = plain manage-object OV or custom-URL OV, single Date(+GO) navigator (or none at
  all), no mandatory dropdown/cascade gating the grid. If recon shows a real navigator
  requirement or a structurally different shape (multi-object junction, event-log/status-grid,
  PC-style parent-child) — STOP, log it excluded, do not force it into this skill's shape.

## Step 1 — recon (DB-first, then one live scan)

- **DB metadata**: `SCREEN="<name>" py tmp/scripts/resolve_ec_screen.py` — resolves
  `CLASS_TYPE` (`OBJECT`⇒OV) and `TIME_SCOPE_CODE` (`VERSIONED`⇒date-effective, End=Start
  delete), plus the base table / version table / `OV_<class>` view name.
- **Live scan** (read-only, never Saves): `SCREEN="<name>" py tmp/scripts/scan_ec_screen.py` —
  returns the navigator shape + which nav fields are mandatory + the GO id, the grid id, and
  the New-Object (`objectForm`)/Update (`updateAttributes`) field ids with mandatory flags and
  **labels**. Take the grid id and GO presence from THIS scan, verbatim — an OV is EITHER
  manage-object (`manage_object_nav_nav:form:T_data` + GO `button:form:B`) OR custom-URL
  (`nav:form:T_data`, NO GO, toolbar Refresh) — they look identical until checked; never assume
  from a sibling screen.
- Confirm the fixed `AUTOTEST_<SCREEN>` test code is free in the DB (fresh oracledb connection:
  dsn `localhost:1521/ORCL`, user `ECKERNEL_EC`, password `energy`) before using it.

## Step 2 — build (RF only, label-driven, T2-consolidated)

Mirror `bank_page.resource`/`berth_page.resource` exactly:
- `pageobjects/<menu path>/<screen>_page.resource` — thin T3, locators from Variables (grid id,
  screen name), all field fills via T2's `Fill OV Field By Label`/`Insert Object From
  Properties`/`Update Object From Properties` — **never a hardcoded `…R:<n>:C:<n>:in` id**, row
  positions shift per screen.
- `tests/<menu path>/<screen>_iud.robot` — 5-TC business narrative (TC01 Verify Clean State /
  TC02 Insert / TC03 Update / TC04 Find / TC05 Delete), per-TC `Login To EC Application`/
  `Logout From EC Application`, fixed test code, dedicated `<SCREEN>_EC_USER`/`<SCREEN>_EC_PASS`
  pair appended (additive only) to `resources/credentials.py`.
- Explicit `Find/Clear <Screen> Row By Filter` T3 wrapper delegating to shared T2's `Find/Clear
  Object Row By Filter`, wired into Update/Find/Verify-Found/Delete only (not Verify-Removed/
  Does-Not-Exist — those get a filter-based absence check for free from T2's fallback).
- 4 properties files under `testdata/`: `<screen>_{insert,update,form_verify,grid_verify}.properties`.
- Delete = **End Date = Start Date** (date-effective OV) via the `objectdates` form.

## Hard rule: never touch shared files

**Do NOT edit `resources/manage_object.resource` or `resources/common.resource`.** If the
screen genuinely needs a new/modified shared keyword, STOP — log it as a scope mismatch
instead of adding one. (If a shared-file change is ever genuinely warranted, that's a separate,
explicitly-authorized change following `ec-screen-automation`'s shared-file safety protocol —
not something this skill does implicitly.)

## Step 3 — verify (every step must actually run, cite real output)

1. `py -m robocop check <changed files>` — compare issue count/category against an
   already-merged sibling (e.g. `berth_iud.robot`); parity = not a regression.
2. `robot --dryrun` on the FULL `tests/` tree — must stay 100% pass.
3. Live run, `EC_HEADLESS=true`, of the new suite — must be 5/5.
4. Independent DB self-clean: a FRESH oracledb connection querying for `AUTOTEST%` rows — 0
   residual, checked AFTER the live run.
5. Confirm the filter keyword actually fired: `grep -c "Find Object Row By Filter" output.xml`
   (or the screen-specific wrapper name) — non-zero.

Never report "done" without having actually run all five and citing the real numbers.

## Blocker protocol

- A verification step fails: retry ONCE with a genuine evidence-based fix. Fails a second time:
  STOP, log a BLOCKED entry with the exact failure and evidence — don't grind.
- A field looks optional in a static CSS/mandatory-class scan but Save silently fails to
  persist: don't assume the field is truly optional — it may be a conditional-mandatory
  business rule invisible to static scanning (a real, recurring EC pattern — Process Train,
  Storage Flow, Trailer, DOA Credit Limit all hit this). Re-test with the field included before
  concluding it's a defect.
- A genuine environment/access blocker (e.g. a role-permission gate makes the screen
  unreachable — not a code defect): do NOT attempt any sandbox security-config write yourself.
  Confirm it's reproducible (re-run a working sibling suite in the same session to rule out a
  transient issue), log it BLOCKED with the evidence, and leave the already-built work sitting
  uncommitted in its isolated clone — it doesn't need to be rebuilt once the blocker is
  resolved, only re-verified.

## Git / PR

- Isolated clone: `git clone --no-checkout <remote> Workplaces/<screen_slug>/`, then
  `git sparse-checkout init --cone && git sparse-checkout set <relevant subdirs>`, then
  `git checkout -b feature/<screen>-iud origin/master`.
- Commit only the screen's own files by explicit path — never `git add -A`.
- Sync with `origin/master` before pushing.
- Raise a PR with a 6-field body: What was built / Files touched / DB ground-truth evidence /
  Self-clean confirmed / Rules applied / Base branch. **Never merge your own PR.**
- Append a new row to `docs/ec_screen_registry.md` and `docs/automation-scorecard.md`
  (append-only — this is a genuinely new screen, not a modification).

## Running as a batch of N new screens

Same orchestration as `ec-bank-pattern-converter`'s batch playbook:
1. Write `tmp/batchN_shared_findings.md` with the batch's screen list, hard rules, and an
   "Entries" section for agents to append gotchas to.
2. Pre-create the batch's section header in the tracking docs in ONE commit/PR, and **wait for
   it to actually MERGE** (`merged: true`, not just pushed) before dispatching subagents — the
   single biggest process defect in this project's history was skipping this wait.
3. Dispatch one subagent per screen in parallel, each doing recon → build → verify → PR in its
   own isolated clone, no nested subagent delegation.
4. Independently re-verify every subagent's PR via a PR-read tool before counting it done.
5. After merge: sync local master, personally spot-check 1-2 screens live yourself, clean up
   the batch's Workplaces clones.

## Bundle deliverables (owner decision 2026-08-27 — restored from `ec-object-iud-builder`)

Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md` retired the 2026-08-23 lean waiver: every new
Bank-pattern screen build now also produces, under `screens/<menu path>/<Screen>/`:
- **`<screen>_sow.md`** — classification, grid/cell shape, test data, dev story.
- **`README.md`** — bundle overview + exact run commands.
- **`JOURNAL.md`** — per-branch work journal (built / done-wrong / done-well / improve /
  blockers→resolution / decisions / evidence).
- **`evidence/`** — step screenshots + a results record from the real live run.
- **`CHECKLIST.md`** — a copy of `docs/IUD-DELIVERABLE-CHECKLIST.md` (Steps 0, A minus 4/5, B, C, D,
  E), ticked with evidence.
- **KB selector map** `ec-ui-knowledge/screens/<screen>.md`.

**Still NOT required**: a hand-written Playwright driver or its `investigation/` recon scripts —
the Universal Screen Engine covers that role now. A throwaway scratch script in
`Workplaces/<screen>/` (gitignored) is fine for ad-hoc recon.

## What "done" looks like

Label-driven, properties-file-driven RF suite with explicit grid-filter wiring, matching
`bank_page.resource`/`berth_page.resource` exactly. Live 5/5, dryrun 100% on the full tree, DB
self-clean confirmed via a fresh connection, filter keyword confirmed fired, no shared T1/T2
file changes, new registry/scorecard rows added, the bundle deliverables above produced, PR
raised (not self-merged).
