# SUMMARY — RF-01: Robot Framework Fundamentals

**Date completed:** 2026-06-05
**Task ID:** RF-01

---

## Topics Covered

- [x] Robot Framework architecture — keyword-driven, 4-layer model
- [x] RF vs pytest — when to use each for EC project
- [x] Why RF for EC Web UI — business readability, existing project structure
- [x] Installation: robotframework, Browser Library, Pabot, Robotidy, Robocop
- [x] VS Code RobotCode extension
- [x] Four .robot file sections: Settings, Variables, Test Cases, Keywords
- [x] Settings section: Library, Resource, Suite/Test Setup/Teardown, Test Tags
- [x] Variable types: ${SCALAR}, @{LIST}, &{DICT}, nested access
- [x] Variable scope: local, suite, global
- [x] Test case anatomy: [Documentation], [Tags], [Setup], [Teardown], [Timeout]
- [x] Keyword anatomy: [Documentation], [Arguments], [Teardown], RETURN
- [x] Browser Library core: New Browser/Context/Page lifecycle
- [x] EC-specific: ignoreHTTPSErrors, viewport, networkidle, type() vs fill()
- [x] EC variable conventions: ${EC_URL}, ${EC_USERNAME}, etc.
- [x] Environment switching via --variablefile
- [x] Two var files: local.py (localhost EC) and cops_dev.py (Woodside Pluto)
- [x] Running RF: basic, tagged, parallel, dry-run

---

## Key Takeaways

1. **Screenshot-on-failure is the mandatory teardown pattern** — `Run Keyword If Test Failed    Take Screenshot    ${OUTPUT_DIR}${/}${SUITE_NAME}_${TEST_NAME}_failure` — every test file must have this in Test Teardown.

2. **Type Text with delay=50ms for ALL EC search fields** — PrimeFaces triggers AJAX on keyup. Fill Text bypasses this. This is the most common cause of EC test failures.

3. **Two environment variable files** — `local.py` (localhost) for local testing, `cops_dev.py` (Woodside Pluto) for integration testing. Switch with `--variablefile` flag.

4. **Wait For Load State networkidle after every EC AJAX action** — EC uses PrimeFaces AJAX extensively. Without networkidle wait, tests click elements still loading from previous action.

5. **ignoreHTTPSErrors=True is mandatory** — EC local and dev environments use self-signed certificates. Without this, Browser Library refuses to connect.

---

## Gotchas

1. `RETURN` statement requires RF 5+ — use `RETURN` (not `[Return]`) in modern RF
2. `New Context` with `viewport=${None}` allows the browser window to control size — don't set fixed viewport when `--start-maximized` is used
3. Test Teardown screenshot path: `${OUTPUT_DIR}${/}` uses RF built-in variable and path separator — always use this pattern for cross-platform compatibility

---

## Files Produced

| File | Description |
|---|---|
| `concepts.md` | Architecture, installation, .robot anatomy, Browser Library, EC conventions |
| `starter_test.robot` | 3 test cases — login, navigate, screenshot — all EC patterns demonstrated |
| `ec_variables.py` | Local environment variable file (localhost EC + Oracle) |
| `browser_library_reference.md` | Top-20 keywords, wait strategies, EC locator patterns |
| `SUMMARY_RF-01.md` | This file |

---

## Confidence Rating: 5/5

Robot Framework fundamentals are fully mastered — the existing EC project (`C:\DEV\ROBOT\APPS\EC\14.2.4\AutomationTest`) is already using the Browser Library with these exact patterns. RF-01 concepts are confirmed by real working code in production. All patterns verified against the existing EC RF project structure.
