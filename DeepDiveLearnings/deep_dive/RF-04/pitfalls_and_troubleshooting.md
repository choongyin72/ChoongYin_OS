# Robot Framework — 20 Pitfalls & Troubleshooting Reference

### P01 — No keyword with name X
**Symptom:** `No keyword with name 'Search And Open Screen' found`
**Cause:** Resource file not imported, or typo in keyword name
**Resolution:** Check `*** Settings ***` Resource imports. Verify file path is correct relative to test file.
**Prevention:** Use RobotCode VS Code extension — auto-complete shows available keywords

---

### P02 — Variable not found
**Symptom:** `Variable '${EC_URL}' not found`
**Cause:** Variable file not loaded, or `Variables` import path wrong
**Resolution:** Check `--variablefile` is passed, or `Variables` path in Settings is correct
**Prevention:** Use `common_variables.robot` as anchor — always import it

---

### P03 — ElementNotFound after navigation
**Symptom:** `Element '#username' not found`
**Cause:** Clicked navigation before page fully loaded — no networkidle wait
**Resolution:** Add `Wait For Load State    networkidle    timeout=30s` after every navigation
**Prevention:** Pattern: every `Click` on a screen link must be followed by networkidle wait

---

### P04 — Selector works in MCP but fails in test
**Symptom:** Locator found during MCP discovery but `Wait For Elements State` times out
**Cause:** MCP was in different browser state than test (different screen, different timing)
**Resolution:** Add `Wait For Load State    networkidle` before attempting to find element
**Prevention:** MCP locator discovery must be done AFTER the screen is fully loaded

---

### P05 — Sleep causing flakiness
**Symptom:** Tests pass sometimes, fail sometimes with element not found
**Cause:** `Sleep    3s` is arbitrary — sometimes enough, sometimes not
**Resolution:** Replace all Sleep with `Wait For Elements State    ${SEL}    visible    ${WAIT_TIMEOUT}`
**Prevention:** `no-sleep-keyword` Robocop rule enforced in CI

---

### P06 — Parallel test data conflict
**Symptom:** Parallel tests fail intermittently with constraint violations
**Cause:** Two workers insert the same test data simultaneously
**Resolution:** Use unique test data per worker: `AUTOTEST_${workerIndex}_ROLE`; use Pabot lock
**Prevention:** AUTOTEST_ prefix + timestamp or workerIndex in all created test data

---

### P07 — Screenshot path with special chars (Windows)
**Symptom:** Screenshot not saved — path contains `/` vs `\` mismatch
**Cause:** Hardcoded `/` separator doesn't work on Windows
**Resolution:** Use `${OUTPUT_DIR}${/}${SUITE_NAME}_${TEST_NAME}_failure` — ${/} is OS-aware
**Prevention:** Always use `${/}` for path separation in Robot Framework

---

### P08 — Variable file not loaded
**Symptom:** Using defaults from common_variables.robot not from vars/local.py
**Cause:** `--variablefile` flag not passed, or wrong path
**Resolution:** Always run: `robot --variablefile vars/local.py tests/`
**Prevention:** Create `run-local.bat` script that always includes the correct --variablefile

---

### P09 — Embedded ${} in XPath string
**Symptom:** `Variable '${class}' not found` in XPath
**Cause:** XPath `//label[contains(@class,'tv-link')]` — RF interprets `@class` as variable
**Resolution:** Escape: `//label[contains(@class,'tv-link')]` OR use `\${` if needed
**Prevention:** Use single-quoted XPath attributes OR store XPath in variables/ (no escaping needed)

---

### P10 — Test passes locally, fails in CI (headless)
**Symptom:** Test stable with headless=False, fails with headless=True
**Cause:** Headless mode renders elements differently; some EC animations differ
**Resolution:** Add `Wait For Elements State    stable    timeout=5s` before clicks in headless
**Prevention:** Always run a headless validation pass locally before pushing to CI

---

### P11 — Fill Text doesn't trigger EC search
**Symptom:** Search results don't appear after `Fill Text    ${SEARCH_INPUT}    Check Rule`
**Cause:** Fill Text sets value without firing keyup DOM events
**Resolution:** Replace `Fill Text` with `Type Text    ${SEL}    ${value}    delay=50ms`
**Prevention:** Rule in ROBOT_CLAUDE.md: Fill Text for normal fields, Type Text for PrimeFaces search

---

### P12 — PrimeFaces dropdown selectOption fails
**Symptom:** `Select Options By` throws "option not found"
**Cause:** EC dropdown is a custom PrimeFaces widget, not a native `<select>`
**Resolution:** Use click-then-filter: `Click    ${DROPDOWN}` then `Click    xpath=//li[text()='${value}']`
**Prevention:** Identify if element is `<select>` (use Select Options By) or PrimeFaces widget (use click)

---

### P13 — networkidle timeout with EC background polling
**Symptom:** `Wait For Load State    networkidle` times out on some EC screens
**Cause:** EC has background AJAX polling requests that never stop
**Resolution:** Use `timeout=60s` or fall back to `Wait For Elements State` on specific element
**Prevention:** Know which EC screens have background polling; document in variables file

---

### P14 — Resource file import loop
**Symptom:** `Circular import` error when loading resources
**Cause:** Resource A imports Resource B which imports Resource A
**Resolution:** Move shared keywords to common_variables.robot or a base resource
**Prevention:** Layer rule: tests → keywords → pages → variables (always one-way)

---

### P15 — [Return] deprecated warning
**Symptom:** `[Return]    ${value}` causes deprecation warning in RF5+
**Cause:** `[Return]` is deprecated since Robot Framework 5
**Resolution:** Replace with `RETURN    ${value}` (no square brackets)
**Prevention:** Robocop rule catches deprecated syntax; use RETURN in all new code

---

### P16 — Get Element Count returns string, not integer
**Symptom:** `Should Be Equal As Numbers    ${count}    0` fails with type error
**Cause:** `Get Element Count` returns a string "0" not integer 0 in some contexts
**Resolution:** Use `${count}=    Get Element Count` and then `Should Be Equal As Integers`
**Prevention:** Use `Should Be Equal As Integers` not `As Numbers` for element counts

---

### P17 — Suite Setup fails, all tests skipped
**Symptom:** All tests in suite show as "Not Run" — suite was skipped
**Cause:** Suite Setup keyword failed (e.g. browser didn't open, login failed)
**Resolution:** Fix the Suite Setup keyword. Add logging to identify where it fails.
**Prevention:** Suite Setup should be simple: open browser + login only. Complex setup → move to Test Setup

---

### P18 — Keyword arguments mismatch
**Symptom:** `Keyword 'Insert Role For Operator' expected 2 arguments, got 1`
**Cause:** Called keyword with wrong number of arguments
**Resolution:** Check `[Arguments]` definition. Use named arguments: `Insert Role For Operator    operator=OPS    role=ROLE`
**Prevention:** Always define `[Arguments]` explicitly; use default values for optional args

---

### P19 — Test data not cleaned up between runs
**Symptom:** Second run fails because previous run's AUTOTEST data still exists
**Cause:** Test Teardown didn't run (test process killed), or teardown failed silently
**Resolution:** Add `Run Keyword And Continue On Failure` wrapper in teardown; also clean in Test Setup
**Prevention:** ALWAYS clean in BOTH Test Setup AND Test Teardown (idempotency principle)

---

### P20 — Browser Library keyword names changed
**Symptom:** `No keyword with name 'Page Should Contain Text'`
**Cause:** Mixed SeleniumLibrary and Browser Library keyword names
**Resolution:** Browser Library uses different names: `Get Text` not `Get Text`, `Wait For Elements State` not `Wait Until Element Is Visible`
**Prevention:** ROBOT_CLAUDE.md forbidden: import SeleniumLibrary. Only Browser Library allowed.
