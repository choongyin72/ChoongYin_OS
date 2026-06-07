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
├── pageobjects/Configuration/Assets/Financial_Objects/bank_page.resource   # T3
└── tests/Configuration/Assets/Financial_Objects/bank_iud.robot
```

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
# from ec-automation/
robot --outputdir results tests/Configuration/Assets/Financial_Objects/bank_iud.robot
```

## Lint & format (Robocop 6+, unified)

```bash
robocop format .     # auto-format to the Style Guide
robocop check .      # lint
```

Pre-commit: `pre-commit install` then both hooks run on every commit.

## Conventions

- Multi-word folders use underscores (`Financial_Objects`).
- Files: `<screen>_page.resource`, `<screen>_iud.robot`.
- Keywords are high-level and domain-readable (`Insert Bank Record`).
- Tests contain no raw selectors — those live in page objects / shared resources.
- Credentials default in `environment.py` are for the **local sandbox only**;
  for real CI inject `EC_USER`/`EC_PASS` as secret **environment variables**.
