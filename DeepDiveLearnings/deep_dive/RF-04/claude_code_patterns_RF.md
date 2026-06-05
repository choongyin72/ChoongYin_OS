# Robot Framework — Claude Code Prompt Patterns

**IMPORTANT:** Always prefix every prompt with:
"Read ROBOT_CLAUDE.md before starting. Apply all rules."

---

## Pattern 1: Automate New EC Screen

**Trigger:** New screen needs to be automated
**Template:**
```
Read ROBOT_CLAUDE.md before starting. Apply all rules.

Automate the EC {ScreenName} screen for Robot Framework.

Screen details:
- Screen name in EC sidebar: "{exact sidebar name}"
- EC local URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/
- Test scenarios needed:
  1. {scenario 1}
  2. {scenario 2}

Use Playwright MCP to discover locators, then:
1. Create resources/variables/{screen_name}_variables.robot
2. Create resources/pages/{ScreenName}Page.resource
3. Create resources/keywords/{ScreenName}Keywords.resource
4. Create tests/{category}/TC_{ScreenName}.robot

Follow 5-layer architecture from RF-02/architecture_guide.md.
```

---

## Pattern 2: Convert Manual Test Steps to RF

**Trigger:** Have manual test steps, want automated version
**Template:**
```
Read ROBOT_CLAUDE.md before starting. Apply all rules.

Convert these manual EC test steps to Robot Framework:

Manual steps:
1. {step 1}
2. {step 2}
Expected: {expected result}

Context:
- Use existing keywords from resources/keywords/ if they exist
- Target: tests/{category}/TC_{name}.robot
- Environment: vars/local.py
- Apply idempotent setup/teardown if data is created/modified
```

---

## Pattern 3: Add Keyword for Action on Screen

**Trigger:** Need a new operation on an already-automated screen
**Template:**
```
Read ROBOT_CLAUDE.md before starting. Apply all rules.

Add a keyword for: {action description} on {ScreenName} screen.

Existing files to read first:
- resources/pages/{ScreenName}Page.resource
- resources/keywords/{ScreenName}Keywords.resource
- resources/variables/{screen_name}_variables.robot

New keyword should:
- Go in: resources/keywords/{ScreenName}Keywords.resource
- Call page layer: NOT Browser Library directly
- Include [Documentation] and [Arguments]
- Add any new selectors to variables/ file
```

---

## Pattern 4: Fix Failing Test

**Trigger:** Test fails — need root cause and fix
**Template:**
```
Read ROBOT_CLAUDE.md before starting. Apply all rules.

Fix this failing Robot Framework test:

Test name: {test name}
Error: {paste error message}
Log excerpt: {paste relevant log lines}

Test file: {paste test file or path}

Use Playwright MCP to verify current EC UI state.
Apply minimum change principle — only fix what's broken.
Do not refactor unless necessary.
```

---

## Pattern 5: Add Idempotency to Existing Test

**Trigger:** Test fails on second run because data from first run wasn't cleaned up
**Template:**
```
Read ROBOT_CLAUDE.md before starting. Apply all rules.

Add idempotency to this test:
{paste test file content}

Requirements:
1. Test Setup: clean before test (ensure data does NOT exist)
2. Test Teardown: clean after test (Run Keyword And Continue On Failure)
3. Add 'Ensure {thing} Does Not Exist' keyword if not present
4. Use AUTOTEST_ prefix on all created test data
5. Verify cleanup works by running test twice consecutively
```

---

## Pattern 6: Refactor .robot File to Comply with ROBOT_CLAUDE.md

**Trigger:** Old test file has inline selectors, Sleep keywords, hardcoded values
**Template:**
```
Refactor this .robot file to comply with ROBOT_CLAUDE.md:
{paste file content}

Required fixes:
1. Move all inline selectors to resources/variables/{screen}_variables.robot
2. Replace Sleep with Wait For Load State networkidle
3. Replace Fill Text with Type Text delay=50ms for search fields
4. Add [Documentation] to all keywords and test cases
5. Add screenshot-on-failure to Test Teardown
6. Replace hardcoded URLs with ${EC_URL}
```

---

## Pattern 7: Add Pabot Parallel Support

**Trigger:** Need to run test suite in parallel
**Template:**
```
Add Pabot parallel execution support to this test suite:
{paste suite or describe test suite}

Requirements:
1. Identify tests that share mutable data
2. Add AUTOTEST_{workerIndex} prefix to test data where needed
3. Add Acquire Lock / Release Lock around shared resource operations
4. Create run script: pabot --processes 4 --pabotlib --variablefile vars/local.py tests/
5. Document which tests can/cannot run in parallel (and why)
```

---

## Pattern 8: Generate Variable File Entries for Screen

**Trigger:** New selectors discovered via MCP — need to add to variables file
**Template:**
```
Read ROBOT_CLAUDE.md before starting. Apply all rules.

Generate variable file entries for these discovered selectors on {ScreenName}:
{list of element: selector pairs from MCP inspection}

Format: ${SCREEN_ELEMENT_TYPE} = {selector value}
Naming convention: ${OP_INSERT_BTN}, ${CR_NAME_FILTER}, ${NAV_DATE_INPUT}
Add to: resources/variables/{screen_name}_variables.robot
Group under comment: # --- {ScreenName} Screen ---
```

---

## Pattern 9: Review .robot File for Robocop Violations

**Trigger:** Before PR — need clean linting pass
**Template:**
```
Review this .robot file for Robocop violations and fix them:
{paste file content}

Priority rules to enforce:
- missing-doc-keyword
- missing-doc-test-case
- no-sleep-keyword
- wrong-case-in-keyword-name
- duplicated-library-import

Do NOT flag: too-long-test-case (EC end-to-end tests can be 15+ steps)
Return: corrected file
```

---

## Pattern 10: Generate Complete Test Suite from Test Specification

**Trigger:** Have a test specification document — need full suite
**Template:**
```
Read ROBOT_CLAUDE.md before starting. Apply all rules.

Generate a complete Robot Framework test suite from this specification:
{paste specification}

Environment: vars/local.py (local EC)
Structure required:
- tests/{category}/TC_{ScreenName}.robot
- resources/keywords/{ScreenName}Keywords.resource
- resources/pages/{ScreenName}Page.resource
- resources/variables/{screen_name}_variables.robot

Apply all ROBOT_CLAUDE.md rules: idempotency, screenshot-on-failure, 
networkidle waits, Type Text for search fields, AUTOTEST_ prefix.
```
