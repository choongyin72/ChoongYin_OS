# RF-01: Robot Framework Fundamentals — Concepts

## 1. Architecture Overview

### What Robot Framework Is
Robot Framework is a Python-based, keyword-driven test automation framework. Tests are written in plain English (or any human language) keywords. Non-developers can read and understand tests without knowing Python.

**Four-layer model:**
```
Test Data (.robot files)
    ↓ parsed by
Robot Framework Core Engine
    ↓ calls
Test Libraries (Browser, OperatingSystem, Collections, etc.)
    ↓ drives
System Under Test (EC Web App, DB, APIs)
```

### Robot Framework vs pytest
| Aspect | Robot Framework | pytest |
|---|---|---|
| Syntax | Keyword-driven (.robot) | Python code |
| Readability | Business-readable for non-devs | Developer-oriented |
| EC project | ✅ Current choice for Phase 2 | Used for DB unit tests |
| Browser library | Browser (Playwright) | playwright-pytest |
| Reporting | HTML log + report built-in | pytest-html plugin |

### Why Robot Framework for EC Web UI
- Test cases read like business requirements: `Verify Check Rule PHD_STRM_COMP_MOL_PCT_VAL1 Exists In DB`
- Non-technical team members can review tests
- Strong integration with EC's existing automation project structure
- Browser Library already in use in `C:\DEV\ROBOT\APPS\EC\14.2.4\AutomationTest`

---

## 2. Installation & Setup (Windows 11)

```bash
# Install Robot Framework
pip install robotframework

# Install Browser Library (Playwright-based)
pip install robotframework-browser
rfbrowser init    # downloads Playwright browsers

# Install parallel executor
pip install robotframework-pabot

# Install code formatter
pip install robotframework-tidy

# Install linter
pip install robotframework-robocop

# Verify
robot --version
rfbrowser version
```

### VS Code — RobotCode Extension
Install: `ms-robotframework.robotcode`
Features: syntax highlighting, test discovery, run/debug from VS Code, Robocop inline linting, auto-complete keywords

---

## 3. .robot File Anatomy

### Four Sections
```robot
*** Settings ***
Documentation    Suite description — what these tests cover
Library          Browser                          # import library
Library          OperatingSystem
Library          Collections
Resource         ../../resources/ec_keywords.robot  # import shared keywords
Suite Setup      Open EC Application    ${EC_URL}    ${HEADLESS}
Suite Teardown   Close Browser
Test Tags        smoke                            # applied to ALL tests in file

*** Variables ***
${EC_URL}         https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/
${EC_USERNAME}    sysadmin
${EC_PASSWORD}    Sysadmin
${WAIT_TIMEOUT}   30s
${HEADLESS}       False
@{CHECK_RULES}    PHD_STRM_COMP_MOL_PCT_VAL1    PHD_STRM_COMP_WT_PCT_VAL1

*** Test Cases ***
TC01 Verify Check Rule Exists In Database
    [Documentation]    Rule 1142 must exist in CTRL_CHECK_RULES
    [Tags]    unit    check_rule    critical
    [Setup]    Log    Starting TC01
    ${result}=    Run Python Check    PHD_STRM_COMP_MOL_PCT_VAL1
    Should Be Equal    ${result}    PASS

*** Keywords ***
Run Python Check
    [Documentation]    Execute DB check via Python and return PASS/FAIL
    [Arguments]    ${check_name}
    ${result}=    Run Process
    ...    py    -c
    ...    import oracledb; conn=oracledb.connect(user='ECKERNEL_EC',password='energy',dsn='localhost:1521/ORCL'); cur=conn.cursor(); cur.execute("SELECT COUNT(*) FROM TV_CTRL_CHECK_RULES WHERE CHECK_NAME=:n",n='${check_name}'); cnt=cur.fetchone()[0]; cur.close(); conn.close(); print('PASS' if cnt>0 else 'FAIL')
    ...    stdout=PIPE    stderr=PIPE
    RETURN    ${result.stdout.strip()}
```

### Variable Types
```robot
${SCALAR}     single value — string, number, object
@{LIST}       list: @{BROWSERS}    chromium    firefox
&{DICT}       dict: &{USER}    name=admin    pass=secret

# Access
${LIST}[0]    first element
${DICT}[name]  dictionary value by key

# Set during execution
${VAR}=    Set Variable    hello world
Set Suite Variable    ${SHARED_VAR}    value    # share with all tests in suite
```

---

## 4. Browser Library Core Usage for EC

### EC-Specific Patterns
```robot
# Open EC with self-signed cert support
New Browser    chromium    headless=False
New Context    ignoreHTTPSErrors=True    viewport={"width": 1920, "height": 1080}
New Page    ${EC_URL}

# Login (Keycloak)
Wait For Load State    domcontentloaded    timeout=30s
Fill Text    id=username    ${EC_USERNAME}
Fill Text    id=password    ${EC_PASSWORD}
Click        id=kc-login
Wait For Load State    networkidle    timeout=60s

# Navigate via sidebar (MUST use Type Text for PrimeFaces)
Wait For Elements State    xpath=//input[@id='menu:searchForm:searchTxt']    visible    timeout=30s
Click                      xpath=//input[@id='menu:searchForm:searchTxt']
Clear Text                 xpath=//input[@id='menu:searchForm:searchTxt']
Type Text                  xpath=//input[@id='menu:searchForm:searchTxt']    Check Rule    delay=50ms
Wait For Load State        networkidle    timeout=15s

# Click treeview link
Click    xpath=//label[contains(@class,'tv-link') and normalize-space(.)='Check Rule']
Wait For Load State    networkidle    timeout=30s

# Screenshot evidence
Take Screenshot    filename=TC01_check_rule_exists.png
```

### Key Browser Library Keywords
```robot
New Browser      chromium    headless=${HEADLESS}
New Context      ignoreHTTPSErrors=True
New Page         ${URL}
Go To            ${URL}
Click            ${LOCATOR}
Fill Text        ${LOCATOR}    ${VALUE}
Type Text        ${LOCATOR}    ${VALUE}    delay=50ms
Clear Text       ${LOCATOR}
Get Text         ${LOCATOR}
Get Element      ${LOCATOR}
Get Elements     ${LOCATOR}
Wait For Elements State    ${LOCATOR}    visible    ${WAIT_TIMEOUT}
Wait For Load State        networkidle    timeout=30s
Take Screenshot  filename=${TEST_NAME}.png
Close Browser
```

---

## 5. EC Project Variable Conventions (MANDATORY)

```robot
# ALWAYS use these variable names — NEVER hardcode
${EC_URL}          base URL — loaded from vars file
${EC_USERNAME}     login username
${EC_PASSWORD}     login password
${WAIT_TIMEOUT}    30s     default timeout for all waits
${HEADLESS}        False   override to True for CI
${DB_URL}          localhost:1521/ORCL
${DB_USER}         ECKERNEL_EC
${DB_PASS}         energy

# Variable files per environment
robot --variablefile vars/local.py tests/
robot --variablefile vars/cops_dev.py tests/
```

### vars/local.py
```python
EC_URL = 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/'
EC_USERNAME = 'sysadmin'
EC_PASSWORD = 'Sysadmin'
WAIT_TIMEOUT = '30s'
HEADLESS = False
DB_URL = 'localhost:1521/ORCL'
DB_USER = 'ECKERNEL_EC'
DB_PASS = 'energy'
BROWSER = 'chromium'
```

### vars/cops_dev.py
```python
EC_URL = 'https://app-plutodev.woodside-pluto.tieto-og.cloud/'
EC_USERNAME = 'sysadmin'
EC_PASSWORD = 'Sysadmin@01'
WAIT_TIMEOUT = '30s'
HEADLESS = True
DB_URL = 'db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev'
DB_USER = 'ECKERNEL_EC'
DB_PASS = 'energy'
BROWSER = 'chromium'
```

---

## Running Robot Framework

```bash
# Basic run
robot tests/

# With variable file (environment switching)
robot --variablefile vars/local.py tests/

# Run only tagged tests
robot --include smoke tests/
robot --include unit AND critical tests/
robot --exclude slow tests/

# Output directory
robot --outputdir results/ tests/

# Dry run (syntax check without execution)
robot --dryrun tests/

# Parallel (pabot)
pabot --processes 4 --variablefile vars/local.py tests/
```
