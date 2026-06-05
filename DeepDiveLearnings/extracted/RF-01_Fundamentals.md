# CLAUDE CODE EXECUTION PROMPT — RF-01: Robot Framework Fundamentals

## CONTEXT
This is a **self-directed deep-dive learning task**. The user is NOT present to monitor progress.
You must work autonomously from start to finish, then produce a written summary and backup all outputs.
Do NOT pause to ask questions. If you encounter ambiguity, make the best professional decision and document it in the summary.

---

## TASK IDENTITY
- **Task ID**: RF-01
- **Tool**: Robot Framework + Browser Library (Playwright)
- **Phase**: Fundamentals
- **Backup folder**: `deep_dive/RF-01/`
- **Environment**: Windows 11, VS Code, Python

---

## LEARNING OBJECTIVES

### 1. Architecture Overview
- What Robot Framework is: keyword-driven, acceptance-test oriented framework
- `.robot` file format: plain-text, space-separated (2+ spaces or pipe-separated)
- The four sections of a `.robot` file: `*** Settings ***`, `*** Variables ***`, `*** Test Cases ***`, `*** Keywords ***`
- Resource files (`.resource`): shared keywords, no `*** Test Cases ***` section
- Test suite hierarchy: directories → `.robot` files → test cases
- Execution flow: suite setup → test setup → keywords → test teardown → suite teardown
- Output files: `output.xml`, `log.html`, `report.html`
- Robot Framework vs pytest: when to choose each
- Why Robot Framework is preferred for EC Web UI automation: business-readable keywords, non-developer maintainability

### 2. Installation & Setup (Windows 11)
- Python 3.x requirement
- `pip install robotframework`
- `pip install robotframework-browser` (Browser Library — Playwright-based)
- `rfbrowser init` — installs Playwright browsers
- VS Code: RobotCode extension — features (syntax highlighting, run/debug, code completion)
- Verifying install: `robot --version`, `rfbrowser version`
- Project structure recommendation (initial, will be expanded in RF-02)
- `pip install robotframework-pabot` — parallel executor (install now, use in RF-03)
- `pip install robotframework-tidy` — code formatter (install now, use in RF-03)

### 3. `.robot` File Anatomy — Deep Dive
**`*** Settings ***` section:**
- `Library` — import a library (e.g., `Browser`, `OperatingSystem`, `Collections`)
- `Resource` — import a resource file
- `Variables` — import a variable file
- `Suite Setup` / `Suite Teardown`
- `Test Setup` / `Test Teardown`
- `Test Tags` — apply tags to all tests in file
- `Documentation` — suite-level documentation

**`*** Variables ***` section:**
- Scalar: `${VAR}`
- List: `@{LIST}`
- Dictionary: `&{DICT}`
- Variable naming conventions: UPPER_CASE for constants, lower_case or Mixed for locals
- EC project standard variables:
  - `${EC_URL}` — base URL
  - `${EC_USERNAME}` — login username
  - `${EC_PASSWORD}` — login password
  - `${WAIT_TIMEOUT}` — `30s` standard value

**`*** Test Cases ***` section:**
- Test case naming: business-readable, sentence case
- `[Documentation]` — test-level documentation
- `[Tags]` — categorisation
- `[Setup]` / `[Teardown]` — test-level hooks
- `[Timeout]` — test-level timeout
- Calling keywords: indented keyword names with arguments

**`*** Keywords ***` section:**
- Keyword naming: Capitalised Words (Title Case), verb-first
- `[Documentation]`
- `[Arguments]` — positional and named arguments with defaults: `${arg}=default`
- `[Return]` — returning values (deprecated in RF5+, use `RETURN` statement)
- `RETURN` statement (RF5+)
- `[Teardown]` on keywords
- Embedded arguments: `Select ${option} From Dropdown`

### 4. Browser Library (Playwright) — Core Usage
- `New Browser` / `New Context` / `New Page` — browser lifecycle
- EC automation pattern: use `New Browser` in suite setup, `New Page` per test
- `Go To` — navigation
- `Get Title` / `Get Url`
- `Click` / `Type Text` / `Fill Text` — actions
- `Select Options By` — dropdowns
- `Get Text` / `Get Element` / `Get Elements`
- `Wait For Elements State` — `visible`, `enabled`, `hidden`, `detached`
- `Page Should Contain` / `Element Should Be Visible`
- `Take Screenshot` — with filename argument
- Selector syntax: CSS, XPath, text, id, `>>` chaining
- `Browser.Set Browser Timeout` — global timeout setting
- `ignoreHTTPSErrors` in `New Context`: `New Context    ignoreHTTPSErrors=True`

### 5. EC Project Variable Conventions
These are MANDATORY standards for all EC project `.robot` files:

- `${EC_URL}` — NEVER hardcode URLs; always use this variable
- `${EC_USERNAME}` — NEVER hardcode usernames
- `${EC_PASSWORD}` — NEVER hardcode passwords
- `${WAIT_TIMEOUT}=30s` — default timeout; always pass to `Wait For Elements State`
- Variable files: separate `.py` or `.yaml` file per environment (dev, test, prod)
- Environment switching: `robot --variablefile vars/dev.py tests/`
- Screenshot naming convention: `${TEST_NAME}_${SUITE_NAME}_failure.png`
- Exact-text matching: prefer `text="exact text"` selectors over partial text
- `Run Keyword And Continue On Failure` — use sparingly; document why

---

## DELIVERABLES

Produce ALL of the following inside `deep_dive/RF-01/`:

### 1. `concepts.md`
Comprehensive explanation of all 5 topic areas with annotated `.robot` snippets.
Map each concept to an EC Web UI automation use case.

### 2. `starter_test.robot`
A fully working `.robot` test file demonstrating:
- All four sections
- `Library    Browser` import
- `${EC_URL}`, `${EC_USERNAME}`, `${EC_PASSWORD}`, `${WAIT_TIMEOUT}` variables
- At least 3 test cases in a logical flow
- `Suite Setup` that opens browser with `ignoreHTTPSErrors=True`
- `Suite Teardown` that closes browser
- `Test Teardown` with screenshot on failure:
  ```robot
  Test Teardown    Run Keyword If Test Failed    Take Screenshot    ${TEST_NAME}_failure
  ```
- At least 5 different Browser Library keywords
- At least 3 custom keywords in `*** Keywords ***`
- All keywords properly documented with `[Documentation]`
- All arguments with defaults where appropriate
- Inline comments (`#`) explaining non-obvious steps

### 3. `ec_variables.py`
A Python variable file for EC environment:
```python
EC_URL = "http://localhost:8080/ec"
EC_USERNAME = "admin"
EC_PASSWORD = "changeme"
WAIT_TIMEOUT = "30s"
BROWSER = "chromium"
HEADLESS = True
```

### 4. `browser_library_reference.md`
Quick-reference table of the most important Browser Library keywords:
- Keyword name
- Arguments
- Return value
- EC use case example

### 5. `SUMMARY_RF-01.md`
Task completion summary containing:
- Date/time completed
- Topics covered (checklist)
- Key takeaways (minimum 5)
- Gotchas discovered
- Files produced (with one-line description each)
- Recommended prerequisites for RF-02
- Confidence rating (1–5 with justification)

---

## EXECUTION INSTRUCTIONS

1. Create the folder `deep_dive/RF-01/`
2. Produce files in order: `concepts.md` → `ec_variables.py` → `starter_test.robot` → `browser_library_reference.md` → `SUMMARY_RF-01.md`
3. All `.robot` files must pass `robot --dryrun` logic checks (simulate this mentally and ensure no syntax errors)
4. Append to `deep_dive/PROGRESS_LOG.md`:
   `[RF-01] COMPLETED — <date> — Robot Framework Fundamentals — Files: 5`
5. Do NOT ask the user any questions. Complete the task fully and autonomously.
