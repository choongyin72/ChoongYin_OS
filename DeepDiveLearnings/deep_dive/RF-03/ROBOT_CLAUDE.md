# ROBOT_CLAUDE.md — EC Robot Framework code-generation governance
**Claude Code MUST read this before generating/modifying ANY `.robot`, `.resource`, or `.py` file
in the EC RF automation project.** (Corrected 2026-06-15 to match the project as it actually is.)

---

## 0. WHICH project this governs (read first — avoids a known confusion)

- ✅ **THE project** = `workstreams/master-plan/ec-automation/` (inside the `ChoongYin_OS` repo). This is
  the real, active EC RF automation suite for eventual project/automation-testing usage. Everything below
  describes IT.
- ⚠️ **NOT** `C:\DEV\ROBOT\APPS\EC\14.2.4\AutomationTest`. That is a **pre-existing, external repo that
  predates our system** — we treat it as **reference only** (to borrow ideas for common RF keyword
  implementations). We never build/deliver there. Do not conflate the two or copy its layout.

Standing conventions also live in: this project's `README.md`, the screen registry
(`workstreams/master-plan/ec-automation/docs/ec_screen_registry.md`), and the memory files
`feedback_rf_best_practice_shared_keywords`, `reference_ec_screen_registry`, `feedback_ec_test_working_rhythm`.

---

## 1. Architecture layers (the REAL tree)

| Tier | Location | Holds |
|---|---|---|
| **T1 — Universal** | `resources/common.resource` (aggregator → `browser/screen/toolbar/table/utils.resource`) + `resources/environment.py` | EC mechanics: login, navigate, fill, save, table/row helpers, screenshot, teardown; URL/creds/DB |
| **T2 — Pattern** | `resources/<pattern>.resource` — e.g. `manage_object` (OV), `daily_status_grid` (N1), `status_process_run` (N3), `allocation_run` (N2), `message_send` (N-notify), `navigator` | mechanics shared by 2+ screens of one pattern |
| **T3 — Screen** | `pageobjects/<menu path>/<screen>_page.resource` | that screen's **locators (in its own `*** Variables ***`)** + thin IUD/run wrapper keywords that delegate to T2/T1 |
| **Tests** | `tests/<menu path>/<screen>_<suffix>.robot` (`_iud`, `_edit`, `_run`, …) | test cases only — declarative, no selectors |
| **DB oracle** | `libraries/DbVerify.py` | DB ground-truth keywords (oracledb thin) |
| **Reference bundle (non-RF)** | `screens/<menu path>/` — `<screen>_sow.md`, `playwright/`, `investigation/`, `evidence/` | recon trail + Playwright prototype + spec; NOT part of the RF run |

`<menu path>` mirrors the EC sidebar, e.g. Bank → `Configuration/Assets/Financial_Objects/`.
**Rule of thumb:** logic used by 2+ screens → T1/T2 shared keyword; T3 stays thin (locators + one-line
delegations). Reference T3: `pageobjects/Configuration/Assets/Financial_Objects/bank_page.resource`.

---

## 2. Environment / connection (NO hardcoding, NO `vars/` files)

Resolved by `resources/environment.py` from OS env vars with **local-sandbox** fallbacks
(precedence: `--variable` > env var > default). There is **no `vars/${ENV}.py`** and **no
`common_variables.robot`** — that was an early plan, not the real structure.

| Variable | Env var | Sandbox default |
|---|---|---|
| `${EC_URL}` | `EC_URL` | local sandbox app URL |
| `${EC_USER}` / `${EC_PASS}` | `EC_USER` / `EC_PASS` | `sysadmin` (CI: inject `EC_PASS` as a secret) |
| `${DB_DSN}` | `EC_DB_DSN` | `localhost:1521/ORCL` |
| `${HEADLESS}` | `EC_HEADLESS` | `true` (interactive: `false`) |

```bash
# headed run (interactive default):
EC_HEADLESS=false robot --outputdir results tests/Configuration/Assets/Financial_Objects/bank_iud.robot
```

---

## 3. DB ground-truth is mandatory (the independent-proof rule)

The UI can lie (optimistic state, silent rejects, pagination, derived/non-persisting cells). A test
**passes only when the database agrees**, not just the screen. Use `libraries/DbVerify.py`:
- generic: `Code Should Be Present In View` / `Code Should Be Absent In View` / `View Row Count`
- pattern oracles: `Day Status Value Should Be` / `Record Status Family Count` / `Status Process Run Count`
  / `Latest Status Process Rows Updated` / `Message Journal *`, plus `Reset/Restore` self-clean helpers.

Examples (from `bank_page.resource`): `Code Should Be Present In View    ov_bank    ${code}` after insert;
`Code Should Be Absent In View    ov_bank    ${code}` after delete. Convert UI↔DB units where stored in
SI/base (e.g. pressure psi↔bar ×14.5038) — derive the factor (UI/DB), don't hardcode.

---

## 4. Pre-flight checklist (complete ALL before writing code)

- [ ] 1. Read this file + the project `README.md`.
- [ ] 2. Read the relevant existing `.robot`/`.resource` for the screen/pattern, and the screen registry row.
- [ ] 3. Check `resources/` (T1/T2) — does a shared keyword already exist? Reuse/extend, don't duplicate.
- [ ] 4. Check `libraries/DbVerify.py` — does the needed DB oracle exist? (extend **append-only**.)
- [ ] 5. New screen: **recon the LIVE UI first** (Playwright/MCP scan) — never guess locators or the nav
      model. Confirm the visible/intended element (a guessed nav/screen model has bitten us twice).
- [ ] 6. Map discovered locators → `${VARIABLE}` names in the T3 page object BEFORE writing keywords.

---

## 5. Hard-stop conditions (STOP, report, don't churn)

1. A locator/screen-model can't be confirmed via a live scan (don't guess).
2. The live screen differs significantly from the spec/description.
3. A change would touch **real seeded/production data destructively** (read the FULL row first; never
   destructive-write on an assumption — Oracle Flashback is the net, not a plan).
4. The change needs a DB migration / client extension config, or touches a **client repo** (`C:\DEV\GIT\*`
   — READ-ONLY).
5. Stuck after ~8 attempts → stop and ask, don't loop.

---

## 6. Forbidden / required code patterns

**Forbidden**
1. ❌ Inline locator strings in tests or T1/T2 keywords (locators live in the **T3 page object's Variables**).
2. ❌ Duplicating an existing keyword — reuse/extend (defaulted optional args; never change a live signature).
3. ❌ Hardcoded URL/user/pass/DSN (use `environment.py`).
4. ❌ `Fill Text` for PrimeFaces autocomplete/search — use `Type Text … delay=…` (re-render drops chars).
5. ❌ Test cases in `.resource`; locators in `.robot`; tests that depend on execution order.
6. ❌ `[Return]` — use `RETURN`. Keyword > ~15 steps — split.
7. ❌ Reassigning built-ins (`Sleep`/etc.) in Python; Unicode arrows in console prints (cp1252 → use `->`).

**Required**
1. ✅ `[Documentation]` on every test + keyword; docstrings must match the code/Variables (R7).
2. ✅ `Wait For Load State    networkidle` after every PrimeFaces AJAX action; `Wait For Elements State …
   visible` before interacting. `Sleep` only as a short settle AFTER networkidle where EC re-renders —
   not as the primary wait.
3. ✅ `ignoreHTTPSErrors=True` on `New Context`.
4. ✅ `AUTOTEST_` prefix on all test-created data; **self-clean** so the suite leaves the sandbox exactly
   as found (End Date = Start Date true-delete for OV objects; DB-restore for status edits/processes;
   assert 0 residual).
5. ✅ Idempotent setup+teardown (clean state both ends).
6. ✅ Screenshot the key steps (`Capture Step`) / on failure.

---

## 7. Working rhythm + change protocol

**Per-screen rhythm:** recon-first → propose scope → confirm → slice thin → `--dryrun` (structure) →
**live headed run** (the proof) → **DB-verify** → robocop → commit. Clean-day-0 ≠ rule fires (use a
seeded date/2nd date for status/validation screens).

**Shared-file change protocol** (T1/T2 `resources/*.resource`, `libraries/*.py` — load-bearing for every
suite): BACKUP first → classify (additive / conditional / behavioral; no live-signature changes) → grep
all callers → verify by class: dryrun all + **canary pack** (`py tmp/scripts/run_canary.py`, one live
suite per pattern) + **random spot-check** (`py tmp/scripts/run_random_suite.py`) → cite both in the
commit. Edits to conflict-magnet shared files are **append-only** (new keywords/rows/sections; never
rewrite existing lines) so parallel PRs don't collide.

**Lint:** `robocop check .` (and `robocop format .`) — clean before done.

**Git:** feature-branch + PR into `master`; never commit to master or self-merge; stage only this
session's files by explicit path. (Per the trial workflow + memory.)

---

## 8. Self-validation before delivering
- [ ] No locators in tests/ or T1/T2; every T3 keyword uses a `${VARIABLE}`.
- [ ] Every test/keyword has `[Documentation]`; docstrings match the code.
- [ ] networkidle wait after each AJAX action; `Type Text` for autocomplete.
- [ ] DB ground-truth assertion present (not UI-only); `AUTOTEST_` prefix; self-clean asserts 0 residual.
- [ ] `robot --dryrun` passes; `robocop check` clean.
