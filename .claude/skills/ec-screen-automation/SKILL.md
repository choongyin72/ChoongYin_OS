---
name: ec-screen-automation
description: Use when automating, reconning, or testing ANY EC (Energy Components) PrimeFaces/JSF web screen — via Playwright recon OR Robot Framework — to apply the proven, DB-verified gestures (login, treeview nav, maximise+expand, navigator cascade, dropdowns, cell edit/clear/save, IUD, status/calc runs, MHM, DB ground-truth) instead of re-discovering them. Covers the real project at workstreams/master-plan/ec-automation.
---

# EC screen automation — proven gesture cookbook

Apply these instead of re-guessing. **Always verify against the DB (ground truth), never the UI alone.**
The active project is `workstreams/master-plan/ec-automation` (NOT `C:\DEV\ROBOT\...\AutomationTest`,
which is a pre-existing reference-only repo). Depth refs: `docs/ec_webapp_internals.md`,
`docs/ec_screen_registry.md` (consult before any screen), `DeepDiveLearnings/deep_dive/RF-03/ROBOT_CLAUDE.md`.

## 0. Recon-first, never guess
Before building a screen: scan it LIVE (Playwright headless) to confirm the nav model, grid id, and the
target cell's column index. Two real misses came from guessing (a non-existent distribution dropdown; a
flat folder). Confirm the *visible/intended* element, and pick a DB scope that actually has data.
**Check CRUD capability BEFORE claiming IUD:** a screen's allowed operations depend on its business
domain — inspect the toolbar (are **New** and **Delete** enabled?). If disabled, it is **UPDATE-ONLY**
(e.g. daily-status grids) — do NOT fabricate insert/delete by re-interpreting value set/clear as record
create/delete (a real mistake on IFLW). Master-data OV screens DO support IUD.

## 1. Environment
- Sandbox: `https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/` · user/pass `sysadmin`/`sysadmin`.
- DB ground truth: oracledb thin, DSN `localhost:1521/ORCL`, user `ECKERNEL_EC`/`energy` (env `EC_DB_*`).
- RF run (headed = the proof): `EC_HEADLESS=false robot --outputdir results <suite>`. Dryrun: `--dryrun`.
- Playwright recon/prototype: `EC_HEADED=1 py -X utf8 <script>`.

## 2. Core gestures (exact selectors)

| Step | Selector / gesture |
|---|---|
| Login | fill `#username`,`#password` → click `#kc-login` |
| Open screen | type into `#menu:searchForm:searchTxt` → click `xpath=//*[contains(@class,'tv-link') and normalize-space(text())='<Screen>']` |
| **Maximise** (headed) | launch `--start-maximized` + no fixed viewport (RF `browser.resource` does this) |
| **Expand to full page** | click `[id="screenToolbar:form:minmaxMenu"]` (hides treeview) AFTER the screen loads |
| Content frame (Playwright) | poll frames for the one with `nav:form:G:0:R:1:C:0:da_input` (URL `dashboard.jsf?top=false`); RF Browser auto-resolves |
| Date field | fill `nav:form:G:<g>:R:1:C:0:da_input` |
| **Dropdown** (autocomplete) | click `<dd>_button` → click `xpath=//*[@id="<dd>_panel"]//tr[normalize-space(@data-item-label)='<Label>']`. Match the **data-item-label**, use `normalize-space` (labels can have leading spaces). Typing into dd is unreliable. |
| Navigator GO | click `[id="button:form:B"]` (mandatory after setting nav values) |
| Cell EDIT (grid) | click cell `…:T:<idx>:C<c>_in` → real keystrokes + Tab (a `fill()` no-op stages nothing; value must differ) |
| Cell CLEAR (= delete value) | click cell → `Control+A` → `Delete` → `Tab`. Save then **nulls the DB column** (proven). |
| Save | click `xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]` (async → then assert DB) |
| Resolve grid row by name | scan `tr` text for the object name → 0-based index (never hardcode row order) |

After every PrimeFaces AJAX action: `Wait For Load State networkidle`. Console prints must be ASCII
(`->` not `→`; Windows cp1252). Never reassign `Sleep`/`time.sleep`.

## 3. Verification = DB ground truth (mandatory)
The UI lies (optimistic state, silent rejects, derived/non-persisting cells). A test PASSES only when the
DB agrees. Use `libraries/DbVerify.py`: `Code Should Be Present/Absent In View`, `View Row Count`,
`Day Status Value Should Be`, `Record Status Family Count`, `Status Process Run Count`,
`Latest Status Process Rows Updated`, `Message Journal *`, + `Reset/Restore` self-clean helpers.
Convert UI↔DB units where stored SI/base (e.g. pressure psi↔bar ×14.5038) — derive factor = UI/DB.

## 4. Screen-type playbook
- **OV / OV-GM / TV / PC (master-data IUD):** INSERT via New-Object form; UPDATE via updateAttributes;
  **DELETE = End Date = Start Date** (zero-length window = true delete; removes from the `ov_*` view).
  OV-GM needs a PU/Area cascade + GO first. (T2 `manage_object.resource`; ref `bank_page.resource`.)
- **N1 daily/sub-daily status grid:** date(+range) nav + object cascade → GO → one pre-instantiated
  (object×day) row, **edit-in-place** (T2 `daily_status_grid.resource`). **UPDATE-ONLY** — New/Delete
  toolbar are DISABLED (the row is batch-instantiated; no record insert/delete on these screens, by the
  business-domain nature). You EDIT the measured value: set / change / clear (clear+Save → DB column
  NULL is update-to-null, **NOT a record delete**). Oracle = `*_DAY_STATUS` (OBJECT_ID, DAYTIME).
  Self-clean = restore original value.
- **N2 allocation/calc RUN:** nav + calc-job dd → GO → Run; SYNCHRONOUS; verify result tables.
- **N3 status process (P→V→A):** nav date(range) + Process dd → GO → Run Process; **ASYNC** (ec-worker
  must be running) → POLL the DB; oracle = `STAT_PROCESS_STATUS.ROWS_UPDATED` + RECORD_STATUS family
  count. (T2 `status_process_run.resource`.) No scheduler node ⇒ rows sit unchanged.
- **N-notify (MHM):** event→producer→store row(+STATUS)→bridge→delivery; oracle = a +1 row delta on the
  store table (`MHM_MSG`/client table). ⚠️ outbound email = gate on a non-deliverable recipient.

## 5. Folder structure = treeview breadcrumb
A screen's files mirror its EC treeview menu path (get the exact path from the **Maintain Treeview**
screen, or hover the tv-link tooltip), spaces→`_`. e.g. Bank → `Configuration/Assets/Financial_Objects/`;
Daily Water Injection Flowline → `EC_Production/Well_and_Reservoir/Daily/Group_Model_-_by_Flowline/`.

## 6. Layering + per-screen deliverables
- **RF (T1/T2/T3):** T1 `resources/common.resource`+`environment.py`; T2 `resources/<pattern>.resource`;
  T3 `pageobjects/<menu path>/<screen>_page.resource` (locators in its own Variables + thin wrappers);
  tests `tests/<menu path>/<screen>_iud.robot`. Logic used by 2+ screens → push to T1/T2; T3 stays thin.
- **Playwright bundle** (`screens/<menu path>/<Screen>/`): `<screen>_sow.md` (SOW), `README.md`,
  `playwright/ec_iud_<slug>.py` (freestyle), `investigation/` (recon scripts), `evidence/` (screenshots).
- A screen is "done" = RF suite (robocop-clean, dryrun, **live + DB-verified, self-cleaning**) + the
  Playwright bundle + SOW + a registry row + scorecard row.

## 7. Shared-file safety protocol (T1/T2 resources, libraries/, DbVerify)
1. **BACK UP FIRST** → `cp <file> <ec-automation>/.keyword_backups/<name>.<tag>.bak` (the referenced
   `backup_keyword_file.py` is missing; do it manually). Revertable even uncommitted.
2. Changes must be **append-only / additive**; never change a live keyword's signature (extend with
   defaulted args). Grep all callers first.
3. After the change: `robot --dryrun` everything, **and pick an EXISTING test that imports the file and
   dryrun (ideally live-run) it** — green = existing flow not broken. For behavioral changes run the
   canary pack (`tmp/scripts/run_canary.py`) + a random suite. Cite results in the commit.

## 8. Git
Feature-branch + PR into master; never commit to master or self-merge; stage only this session's files
by explicit path. Client repos under `C:\DEV\GIT\` are READ-ONLY.

## 9. Recurring problems → proven fix (SME troubleshooting matrix)
The situations that recur on EC screens and their already-solved fix — reach for these instead of
re-discovering. Sourced from the live-proven PRs (#9–#40) + rules R1–R14. **Don't re-derive a fix that
is already here.**

| # | Symptom (what you see) | Cause | Proven fix | Source |
|---|---|---|---|---|
| 1 | Navigator GO loads an **empty grid** though the filters look set | A filter dropdown sits on the first/default option (e.g. composition Analysis Status `*New`) or doesn't match the real record | Query the target record's real attributes from the DB first, then set EVERY filter to MATCH (composition: Analysis Status=**Approved**, Sampling=**\*Spot**) before GO | comp recon 2026-06-17; navigator-GO |
| 2 | GO click does nothing / hits the wrong element | The GO id varies by screen; a hidden default-submit can also match | GO ids seen: `button:form:B` (daily-status), **`go_button:form:B`** (composition), `navButton:form:B` (object/Stream Finders). Confirm the **visible** GO; recon dumps visible `a[id$=':B']` | reference navigator-GO; verify-visible-locator |
| 3 | Cell edit doesn't persist after Save | `fill()`/synthetic events don't fire the change/partial-submit; an unchanged value stages nothing | Real keystrokes + **Tab** (`Type Cell By Id`); the value MUST differ from what the cell shows | T2; #11/#12 |
| 4 | The first editable-looking column won't persist (DB unchanged) | It's a **derived/calculated** cell (e.g. C1 "On Strm[hr]" on sub-daily) | Edit→diff per screen; switch to the proven-editable measured column, confirm by DB **before** building | #12; R7 |
| 5 | Typed value ≠ DB value (off by ~14.5 or a ratio) | UI shows CONFIGURED units; DB stores SI/base (pressure psi↔bar ×14.5038, rates) | Derive factor = UI_before/DB_before; assert DB≈typed/factor. **Multiplicative only** (temp/offset needs the formula). Unitless (ON_STREAM_HRS, GRS_VOL) = direct equality | R1; ui-db-unit-conversion; #11/#12 |
| 6 | A reference dropdown is empty mid-flow (but not standalone) | The form's **Start Date predates the seed objects** (object-start-date = version filter) | Use a data-bearing date (e.g. 2003-01-01+) on screens with reference dropdowns | object-start-date-version |
| 7 | Dropdown pick flaky / typed value rejected | Autocomplete dd; labels can have leading/double spaces; a re-render closes the panel | Click chevron → pick `tr[data-item-label]` by **normalize-space**; one Escape+reopen retry; never type | T1 Select EC Dropdown Option |
| 8 | Targeting the wrong grid row | Grid row order is not predictable | Resolve the row by object **NAME** → 0-based index; never hardcode the row | T2 |
| 9 | Save says success but data didn't persist | UI is optimistic / silently rejects; status processes are **async** | Always assert the **DB** after Save; for N3 poll `STAT_PROCESS_STATUS` | independent-proof; N3 |
| 10 | About to label a screen IUD / build insert+delete | Daily-status & similar grids are **UPDATE-ONLY** (New/Delete disabled; row batch-instantiated) | Check the toolbar New/Delete enabled-state FIRST; build set/change/clear only; clear+Save = NULL (update-to-null, not a record delete) | R10; #24/#27 |
| 11 | Numeric compare fails on a formatted cell | EC formats with thousands separators (`2,949.9`) | Strip commas before compare / before re-typing on revert | T2 |
| 12 | DB verify fails "table not found" | Some objects have **no base table, only a `DV_` view** (e.g. TANK_DAY_DIP_STATUS) | Verify through the `DV_` view (SELECT works) | #39 |
| 13 | `Get Table Rows` returns empty though the grid has data | The grid's cells are all inputs (no text nodes) | Count `<tr>` directly / read input values for presence | #12 |
| 14 | A status process "did nothing" | Down: **silent WAITING** (no error, no `STAT_PROCESS_STATUS` row) = worker down/STANDBY; **ORA-06569** = worker ran, empty scope | Distinguish the two; ORA-06569 ⇒ fix scope/date, not infra | R5 |
| 15 | A status process has **no WHERE filter** | It can lift a large set (whole month) | Gate the live run behind a flag (`LIVE_OK`), observe the first run, DB-restore (reversible) teardown; match oracle grain (month vs day) | #22; R4 |
| 16 | Screen content cramped / treeview blocks the view | — | After the screen loads, click `screenToolbar:form:minmaxMenu` to expand; launch maximised | skill §2 |
| 17 | Playwright can't find the nav fields | They're inside a content iframe | Poll frames for the one containing `nav:form:G:0:R:1:C:0:da_input` (`dashboard.jsf?top=false`) | skill §2 |
| 18 | Object/Stream Finder returns empty scope (PU/Area/Facility) | Finder scrape is flaky | Resolve via the Finder; on empty, fall back to the known scope for that family (e.g. P1 → P1 Production Unit/Area/Facility 1) | comp recon 2026-06-17 |
| 19 | Console crashes / UnicodeEncodeError on Windows | cp1252 can't encode `→` etc. | ASCII only in prints (`->` not `→`); run scripts with `py -X utf8` | skill §2 |
| 20 | Editing a shared T1/T2/`DbVerify.py` file | Risk of breaking other suites + merge conflicts | Back up to `.keyword_backups/`; **append-only** (no signature change); dryrun ALL + canary + 1 random sibling, cite both | R12; #24/#26 |
| 21 | Self-clean for a **null-original** cell | A UI "revert to empty" can pop a save-confirm modal | Use the `DbVerify` reset/restore teardown (the only DB write) to return to the known state; the UI→DB write stays the proof | #11; DbVerify |
| 22 | Two PRs touch the same shared doc (scorecard/registry/lessons) | Merge collision | **APPEND-ONLY** (new rows/sections at the end); stack dependent PRs (`depends on #N`) | R11/R12; #35→#37 |
