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
  (object×day) row, **edit-in-place** (T2 `daily_status_grid.resource`). No New/Delete toolbar →
  **IUD is done on the cell VALUE**: INSERT = fill empty cell+Save; UPDATE = change+Save; DELETE =
  clear cell+Save (→DB null). Oracle = `*_DAY_STATUS` (OBJECT_ID, DAYTIME). Self-clean = restore original.
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
