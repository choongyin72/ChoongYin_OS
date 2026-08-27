# SOW - Shift IUD (Configuration > Assets > Facility_Objects)

- **Screen:** Shift   **BF:** CO.0224   **View:** `OV_SHIFT`   **Base:** `SHIFT`
- **Type:** OV-GM (grid `manageObject:form:T_data`) - a genuine 3-level, same-row navigator
  cascade (Production Unit -> Area -> Facility Class 1, `nav:form:G:0:R:1:C:1/2/3:dd`) + GO,
  gating the grid until filled. Shift ALSO carries a **mandatory FREE-TEXT extra on the insert
  form: Start Time (HH:MI)** - the field class the OV-GM generator cannot fill (the original
  park reason from the 2026-07-31 build). Value `07:00`, format read from the existing P1 S001
  row (owner technique: scan an existing row's populated values to learn every element).
- **Navigator = SPECIFIC P1 values** (P1 Production Unit -> P1 Area -> P1 Facility 1; lists the
  4 existing P1 shifts - owner screenshot 2026-07-31), NOT first-available. **Op Production
  Unit = nav PU** (parent-matching, from the existing row's values).
- **Start Date = 2020-01-01** (existing P1 shifts effective 2011-01-01/15).
- DELETE = End Date = Start Date. Fixed test code `AUTOTEST_SHIFT` (confirmed free in `OV_SHIFT`
  via a fresh oracledb connection before being wired in, per PR #547); self-cleaning every run.
- View confirmed by REAL lookup: `OV_SHIFT` contains 'P1 S001' (4 rows total).

## Pattern history / dev story
- **2026-07-31** - original hand-built 4-TC suite (`py/shift_iud.py` Playwright driver + bespoke
  RF `shift_page.resource`/`shift_iud.robot`), suite-level login, inline DB-verify calls,
  bespoke inline navigator fill. `verify_screen.py` OVERALL PASS: robocop 0, hygiene 0,
  dryrun 4/4, LIVE RF 4/4, Playwright 8/8.
- **2026-08-26, PR #547** - converted to the Area-pattern **structure**: 5 TCs (Verify Clean
  State / Insert / Update / Find / Delete), per-TC login/logout on one Suite-Setup browser,
  navigator fill delegated to the shared T2 `Apply Navigator From Properties` keyword driven by
  a new `testdata/shift_navigator.properties` (EXPLICIT SPECIFIC P1 values, confirmed via the
  prior driver's own literal locators, not re-derived from a sibling screen), properties-file-
  driven insert/update/verify (`shift_insert.properties`/`shift_update.properties`/
  `shift_form_verify.properties`/`shift_grid_verify.properties`), explicit grid-filter wiring
  (`Find/Clear Shift Row By Filter`), zero inline DB-verify calls (pure-screen verification;
  the one remaining DB check lives inside the shared T2 `Verify Object Removed` for TC05 only).
  This is a **structural** conversion, not a reclassification of the screen as plain
  Bank-shaped - Shift keeps its genuine 3-level P1 navigator cascade + GO exactly as the prior
  driver proved it. The mandatory free-text Start Time (HH:MI) requirement/handling was kept
  exactly as the prior driver proved it (`07:00`), just moved into `shift_insert.properties` -
  auto-detected as a plain text field by the existing shared `Fill OV Field By Label Any Kind`
  mechanism, no special-casing needed. PR #547 evidence cited: full-tree dryrun 850/850, live
  RF 5/5, robocop parity (10 issues, no new), DB self-clean via fresh oracledb connection,
  grid-filter fired 15x/cleared 15x.
- **Real operational incident during that same 2026-08-26 session (see JOURNAL.md, Blockers ->
  resolution):** the isolated git worktree used for the PR #547 conversion work hit a Windows
  long-path failure while checking out the worktree; resolved via an owner-approved
  `git config --local core.longpaths true` change. This was a Windows/git-worktree environment
  limitation, not a Shift-screen defect - recorded here honestly rather than smoothed over.
- **2026-08-28 - this backfill (Batch 4, `docs/lean-deliverable-backfill-workorder.md`)** -
  adds the SOW/README/JOURNAL/evidence/CHECKLIST/KB-map artifacts that Section G's now-retired
  lean waiver had skipped around PR #547's already-merged conversion. Re-ran the suite once
  live (5/5 PASS, first attempt, no retry needed) purely to capture fresh evidence - no RF/
  Playwright file was touched.

## Known risks
- Nav scope is DATA-dependent (P1 objects); re-derive if renamed/removed.
- Start Time is free text - EC may accept malformed values silently; '07:00' matches the
  existing-data format exactly.
- `${SHIFT_DEL_ENDDATE}` is a hardcoded field id (not label-driven) - the `objectdates` row
  packs Start Date (C:1) and End Date (C:3) together with the End Date label at C:2, a shape
  the one-field-per-row label scan cannot safely resolve; documented rationale matches Area's/
  Facility Class 1's own del-enddate constant.
