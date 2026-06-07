# EC Automation — Robot Framework Suite (team-ready)

Layered, Page-Object-Model Robot Framework codebase for EC screen IUD testing.
Built to scale to many screens and many contributors, with the folder tree
mirroring the EC menu path so every suite has an obvious home.

## Layers (where code lives, and why)

| Tier | Location | Holds | Reused by |
|---|---|---|---|
| **T1 — Universal** | `resources/common.resource` (+ area files) and `resources/environment.py` | EC mechanics: login, navigate, fill, save, table/row helpers, screenshot, teardown; URL/creds/DB | every screen |
| **T2 — Pattern** | `resources/manage_object.resource` | Manage-Object (OV) mechanics: new-object form, select row, Go, End=Start delete | Manage-Object screens (Bank, Equipment) |
| **T3 — Screen** | `pageobjects/<menu path>/<screen>_page.resource` | that screen's locators + thin IUD wrapper keywords | one screen only |
| **Tests** | `tests/<menu path>/<screen>_iud.robot` | test cases only (TC01–04), declarative | — |

`<menu path>` mirrors EC, e.g. Bank → `Configuration/Assets/Financial_Objects/`.
Shared resources stay flat in `resources/`; screen-specific resources (if ever
needed) nest under their menu path like page objects/tests do.

## Structure

```
ec-automation/
├── resources/
│   ├── environment.py                # T1: env/connection (URL, creds, DB) — env-var driven, variable file
│   ├── browser.resource              # T1: open / login / close
│   ├── screen.resource               # T1: navigate
│   ├── toolbar.resource              # T1: save (toolbar actions)
│   ├── table.resource                # T1: field/date entry, rows, row assertions
│   ├── utils.resource                # T1: unique code, screenshot
│   ├── common.resource               # T1: aggregator (imports the area files + environment.py)
│   └── manage_object.resource        # T2: Manage-Object (OV) keywords
├── libraries/
│   └── DbVerify.py                   # DB ground-truth keywords (oracledb) — present/absent in a view
├── pageobjects/Configuration/Assets/Financial_Objects/bank_page.resource   # T3
└── tests/Configuration/Assets/Financial_Objects/bank_iud.robot
```

### Database verification (`libraries/DbVerify.py`)

The UI can lie (optimistic state, silent rejects, pagination), so suites assert
against the **database** as ground truth. `DbVerify.py` exposes generic keywords —
`Code Should Be Present In View`, `Code Should Be Absent In View`, `View Row Count` —
that match a code against any VARCHAR column of a given EC view. The Bank suite uses
them inside the tests: TC02 asserts the new bank really persisted in `ov_bank`, TC04
asserts it was truly deleted. DB connection resolves from env vars
(`EC_DB_USER`/`EC_DB_PASS`/`EC_DB_DSN`) with sandbox fallbacks; oracledb thin mode.

### Environment / connection data (`environment.py`)

URL, credentials and DB DSN are **not fixed** — they resolve from OS environment
variables with local-sandbox fallbacks (precedence: `--variable` > env var > default):

| Variable | Env var | Sandbox default |
|---|---|---|
| `${EC_URL}`  | `EC_URL`      | local app URL |
| `${EC_USER}` | `EC_USER`     | `sysadmin` |
| `${EC_PASS}` | `EC_PASS`     | `sysadmin` (CI: inject as secret) |
| `${DB_DSN}`  | `EC_DB_DSN`   | `localhost:1521/ORCL` |
| `${HEADLESS}`| `EC_HEADLESS` | `true` |
| `${HOLD}`    | `EC_HOLD`     | `0s` |

```bash
# other environment / headed demo, no file edits:
EC_URL=https://test... EC_USER=qa EC_PASS=*** EC_HEADLESS=false robot tests/...
```

## Setup

```bash
py -m pip install -r requirements.txt
playwright install chromium          # via Browser lib: py -m Browser.entry init
```

## Run

```bash
# from ec-automation/ — headless (CI)
robot --outputdir results tests/Configuration/Assets/Financial_Objects/bank_iud.robot

# headed (watchable) — the default when running interactively
EC_HEADLESS=false robot --outputdir results tests/Configuration/Assets/Financial_Objects/bank_iud.robot
```

## Lint & format (Robocop 6+, unified)

```bash
robocop format .     # auto-format to the Style Guide
robocop check .      # lint
```

### Pre-commit hooks

`.pre-commit-config.yaml` runs `robocop` (lint) + `robocop-format` on robot files.
Verified working. Because this project currently lives **inside a larger monorepo**,
run the hooks **on-demand** against these files rather than installing a repo-wide hook:

```bash
py -m pre_commit run -c workstreams/master-plan/ec-automation/.pre-commit-config.yaml --files <changed .robot/.resource>
```

When `ec-automation` is split into its **own repository**, activate them for every
commit with `pre-commit install`.

## Conventions

- Multi-word folders use underscores (`Financial_Objects`).
- Files: `<screen>_page.resource`, `<screen>_iud.robot`.
- Keywords are high-level and domain-readable (`Insert Bank Record`).
- Tests contain no raw selectors — those live in page objects / shared resources.
- Credentials default in `environment.py` are for the **local sandbox only**;
  for real CI inject `EC_USER`/`EC_PASS` as secret **environment variables**.

## `screens/` — per-screen reference bundles (non-RF)

Alongside the runnable RF suite, each screen has a reference bundle under `screens/`,
mirroring the same EC menu path. These are **not** part of the RF run — they're the
preserved Playwright implementation + the discovery trail + a spec, per screen:

```
screens/<menu path>/
├── README.md          # Playwright run guide for this screen
├── <screen>_sow.md    # statement of work / spec
├── playwright/        # standalone Playwright (Python) implementation
├── investigation/     # recon scripts (DOM scans + DB queries) used to learn the screen
└── evidence/          # screenshots from a full IUD run
```

Playwright/recon tooling installs from `requirements-dev.txt` (`playwright`); the RF suite
itself only needs `requirements.txt`.

## Roadmap / deferred

| Item | Status |
|---|---|
| **CI pipeline** (Robocop + suite, e.g. Pabot parallel) | On hold until **Jenkins** is installed |
| **Negative / validation testing** (assert EC *rejects* bad input; read the VALIDATION/error panel; make `Save` fail on a silent reject) | Deferred — needs a DOM scan of the error/validation panel + design; tackle as its own pass tied to the "VALIDATION" screen area |
| **Per-test-suite user-id strategy** (data-driven template / per-role suites / context-per-test) + credentials subfolder variable file | Parked until we build a multi-test-case / multi-role suite |
| **Retire original `drafts/` suites** | Kept **frozen as backup**; not retired |
| **Equipment + MIME conversion** into this structure | Pending go-ahead (Bank is the proven template) |
