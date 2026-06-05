# Robot Framework Cheatsheet — EC Web App

## .robot File Skeleton
```robot
*** Settings ***
Documentation    Suite description
Library          Browser
Library          OperatingSystem
Library          Collections
Library          Process
Resource         ../../resources/ec_keywords.robot
Variables        ../../vars/local.py
Suite Setup      Open EC Application    ${EC_URL}    ${HEADLESS}
Suite Teardown   Close Browser
Test Teardown    Run Keyword If Test Failed
...    Take Screenshot    ${OUTPUT_DIR}${/}${SUITE_NAME}_${TEST_NAME}_failure

*** Variables ***
${MY_VAR}    value
@{MY_LIST}   item1    item2
&{MY_DICT}   key1=val1    key2=val2

*** Test Cases ***
TC Name In Sentence Case
    [Documentation]    What this test verifies
    [Tags]    smoke    critical
    My Business Keyword    arg1    arg2
    Should Be Equal    ${result}    PASS

*** Keywords ***
My Business Keyword
    [Documentation]    What this keyword does
    [Arguments]    ${arg1}    ${arg2}=default
    Log    Processing ${arg1}
    RETURN    ${result}
```

## Built-in Variables
| Variable | Value |
|---|---|
| `${OUTPUT_DIR}` | Test output directory |
| `${SUITE_NAME}` | Current suite name |
| `${TEST_NAME}` | Current test name |
| `${TEST_STATUS}` | PASS / FAIL |
| `${/}` | OS path separator |
| `${SPACE}` | Single space |
| `${EMPTY}` | Empty string |
| `${True}` / `${False}` | Boolean |
| `${None}` | Python None |

## Browser Library Top-20 Keywords
| Keyword | Signature | EC use |
|---|---|---|
| `New Browser` | `chromium headless=F` | Suite Setup |
| `New Context` | `ignoreHTTPSErrors=T` | Suite Setup |
| `New Page` | `url` | Suite Setup |
| `Wait For Load State` | `networkidle timeout=30s` | After every AJAX |
| `Wait For Elements State` | `sel visible 30s` | Before every click |
| `Click` | `selector` | All clicks |
| `Fill Text` | `sel text` | Most inputs |
| `Type Text` | `sel text delay=50ms` | Search/autocomplete |
| `Clear Text` | `selector` | Clear before type |
| `Get Text` | `selector` | Read value |
| `Get Element Count` | `selector` | Count rows |
| `Get Url` | — | Verify URL |
| `Take Screenshot` | `filename=f.png` | Evidence |
| `Select Options By` | `sel label value` | Native `<select>` |
| `Press Keys` | `sel Enter` | Keyboard |
| `Hover` | `selector` | Hover effects |
| `Execute JavaScript` | `script` | DOM manipulation |
| `Close Browser` | — | Suite Teardown |
| `Get Property` | `sel property` | Read attribute |
| `Go To` | `url` | Navigate |

## Variable Types
```robot
${SCALAR}         = single value
@{LIST}           = list: @{L}    a    b    c
&{DICT}           = dict: &{D}    k=v
${L}[0]           = first list element
${D}[key]         = dict value
```

## Argument Patterns
```robot
[Arguments]    ${required}    ${optional}=default    @{varargs}    &{kwargs}
```

## Control Flow (RF5)
```robot
IF    '${x}' == 'PASS'
    Log    passed
ELSE IF    '${x}' == 'SKIP'
    Log    skipped
ELSE
    Fail    unexpected: ${x}
END

FOR    ${item}    IN    @{LIST}
    Log    ${item}
END

WHILE    ${count} < 10
    ${count}=    Evaluate    ${count} + 1
END

TRY
    Click    id=btn
EXCEPT    ElementNotFound*
    Log    Not found, skipping
END
```

## Tag Syntax
```robot
[Tags]    smoke    critical    check_rule    system
robot --include smoke tests/
robot --exclude slow tests/
robot --include smoke AND critical tests/
```

## EC Mandatory Patterns
```robot
# 1. Browser with ignoreHTTPSErrors
New Context    ignoreHTTPSErrors=True    viewport={"width": 1920, "height": 1080}

# 2. After EVERY EC AJAX
Wait For Load State    networkidle    timeout=${WAIT_TIMEOUT}

# 3. Search (Type not Fill)
Type Text    ${SEARCH_INPUT}    ${screen_name}    delay=50ms

# 4. Screenshot teardown
Test Teardown    Run Keyword If Test Failed
...    Take Screenshot    ${OUTPUT_DIR}${/}${SUITE_NAME}_${TEST_NAME}_failure

# 5. Environment switch
robot --variablefile vars/local.py tests/    # local
robot --variablefile vars/test.py tests/     # COPS DEV
```

## Run Commands
```bash
robot tests/                                      # all tests
robot --variablefile vars/local.py tests/         # with env
robot --include smoke tests/                       # tagged
robot --dryrun tests/                              # syntax check
pabot --processes 4 tests/                        # parallel
robotidy tests/                                    # format
robocop tests/ resources/                          # lint
```
