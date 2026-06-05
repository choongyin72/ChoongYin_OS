# ROBOT_CLAUDE.md — Robot Framework Code Generation Governance
**Place this file at the root of the EC Robot Framework project.**
**Claude Code MUST read this file before generating ANY .robot, .resource, or .py file.**

---

## Purpose & Scope
This document governs how Claude Code generates, modifies, and reviews Robot Framework files for the EC Web App automation project. All rules apply to:
- `.robot` test files
- `.resource` keyword/page files
- Python variable files (`vars/*.py`)
- Python library files (`resources/libraries/*.py`)

---

## Pre-Flight Checklist (MANDATORY — complete ALL before writing any code)

- [ ] 1. Read this file (ROBOT_CLAUDE.md) — no exceptions
- [ ] 2. Read ALL existing `.robot` and `.resource` files relevant to the screen being automated
- [ ] 3. Read `resources/variables/common_variables.robot` and relevant screen variables file
- [ ] 4. Check `resources/keywords/` — does a similar keyword already exist?
- [ ] 5. If automating a new screen: use Playwright MCP to scan live UI BEFORE writing locators
- [ ] 6. Map all discovered locators to variable names BEFORE writing page keywords
- [ ] 7. Check `resources/libraries/ECHelpers.py` — does the needed DB function exist?

---

## Hard-Stop Conditions (STOP and report to user)

1. A locator cannot be found via live MCP scan of the target screen
2. The screen layout differs significantly from the description provided
3. An existing keyword almost covers the need — confirm with user before extending vs creating new
4. The task requires inserting/modifying real production or user data
5. The task requires creating a new database migration or extension config

---

## Architecture Layer Rules

```
Layer 1: tests/           ONLY test cases — import from keywords/
Layer 2: resources/keywords/  Business operations — call pages/, no locators
Layer 3: resources/pages/     Screen interactions — use ${VARIABLES} from variables/
Layer 4: resources/variables/ ALL selectors — naming: ${SCREEN_ELEMENT_TYPE}
Layer 5: resources/libraries/ Python utilities — ROBOT_LIBRARY_SCOPE = 'SUITE'
```

---

## Code Generation Rules

### Forbidden Patterns (NEVER generate these)
1. ❌ Locator strings inline in pages or keywords: `Click    id=submitBtn`
2. ❌ Duplicate existing keywords — reuse or extend
3. ❌ `Sleep    Ns` — use `Wait For Load State    networkidle` or `Wait For Elements State`
4. ❌ Hardcoded URLs, usernames, passwords, environment values
5. ❌ `Fill Text` for PrimeFaces search/autocomplete fields — use `Type Text    delay=50ms`
6. ❌ Test cases in resource files (`.resource` has no `*** Test Cases ***` section)
7. ❌ Locators in test files or keyword files (belong in variables/ only)
8. ❌ `[Return]` statement — use `RETURN` (RF5+)
9. ❌ More than 15 steps in a single keyword (split into sub-keywords)
10. ❌ Test cases that depend on execution order

### Required Patterns (ALWAYS generate these)
1. ✅ `[Documentation]` on every keyword and test case
2. ✅ Test Teardown: `Run Keyword If Test Failed    Take Screenshot    ${OUTPUT_DIR}${/}${SUITE_NAME}_${TEST_NAME}_failure`
3. ✅ `Wait For Load State    networkidle    timeout=${WAIT_TIMEOUT}` after EVERY PrimeFaces AJAX action
4. ✅ `Wait For Elements State    ${SEL}    visible    ${WAIT_TIMEOUT}` BEFORE every element interaction
5. ✅ `ignoreHTTPSErrors=True` in every `New Context` call
6. ✅ Variable file import: `Variables    ../../vars/${ENV}.py` (not hardcoded values)
7. ✅ AUTOTEST_ prefix on all test data created by tests
8. ✅ Idempotency: `Ensure Role Does Not Exist` in BOTH Test Setup AND Test Teardown

---

## Variable Naming Conventions

| Pattern | Example | Use for |
|---|---|---|
| `${SCREEN_ELEMENT_TYPE}` | `${OP_INSERT_BTN}` | Screen-specific selectors |
| `${EC_URL}` / `${EC_USERNAME}` | as-is | Environment variables |
| `${WAIT_TIMEOUT}` | as-is | All wait timeouts |
| `${AUTOTEST_PREFIX}` | `AUTOTEST_` | Test data prefix |

Selector value examples:
```robot
${LOGIN_USERNAME_INPUT}    id=username
${OP_INSERT_BTN}          xpath=//button[contains(@id,'insertBtn')]
${GRID_ROW}               tr[data-rk]
${LAST_PAGE_BTN}          css=span.ui-icon-seek-end
```

---

## Keyword Naming Conventions

| Layer | Style | Examples |
|---|---|---|
| Tests | Business sentence | `Insert Role For Operator` |
| Keywords | Verb-first Title Case | `Insert Role For Operator`, `Verify Role Exists` |
| Pages | Action + Screen element | `Click Insert Button`, `Select Operator From Dropdown` |
| Variables | SCREAMING_SNAKE for constants | `${OP_INSERT_BTN}` |

---

## EC-Specific Patterns (Must Follow)

```robot
# 1. Browser setup (always ignoreHTTPSErrors)
New Context    ignoreHTTPSErrors=True    viewport={"width": 1920, "height": 1080}

# 2. After EVERY EC AJAX action
Wait For Load State    networkidle    timeout=${WAIT_TIMEOUT}

# 3. Sidebar search (Type Text not Fill Text)
Type Text    ${SEARCH_INPUT}    ${screen_name}    delay=50ms

# 4. EC screenlet ID with colon — use xpath not id selector
xpath=//element[@id='screenlet:form:element']    # NOT: id=screenlet:form:element

# 5. Screenshot on failure (mandatory teardown)
Test Teardown    Run Keyword If Test Failed
...    Take Screenshot    ${OUTPUT_DIR}${/}${SUITE_NAME}_${TEST_NAME}_failure

# 6. Environment switching
robot --variablefile vars/local.py tests/     # local EC
robot --variablefile vars/test.py tests/      # COPS DEV
```

---

## How to Handle Ambiguous Requirements

1. When screen name is unclear → ask user for exact screen name as shown in EC sidebar
2. When selector is ambiguous → use Playwright MCP to scan live UI, do not guess
3. When keyword scope is unclear → err on the side of creating in pages/ not keywords/
4. When idempotency requirements are unclear → always implement clean setup + teardown
5. When test data values are unclear → use AUTOTEST_ prefix with timestamp

---

## Self-Validation Before Delivering

Run mentally against this checklist:
- [ ] No locators in tests/ or keywords/ layers
- [ ] Every pages/ keyword uses a ${VARIABLE} not an inline string
- [ ] Every test has [Documentation] and [Tags]
- [ ] Every keyword has [Documentation] and [Arguments] where applicable
- [ ] Test Teardown includes screenshot-on-failure
- [ ] Suite Setup opens browser with ignoreHTTPSErrors
- [ ] networkidle wait after every AJAX action
- [ ] Type Text (not Fill Text) for all PrimeFaces search/autocomplete fields
- [ ] AUTOTEST_ prefix on all created test data
- [ ] `robot --dryrun` would pass (syntax check)
