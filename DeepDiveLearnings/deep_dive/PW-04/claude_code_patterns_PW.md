# Playwright — Claude Code Prompt Patterns

## Pattern 1: Generate Page Object from Screen Description

**Trigger:** Need a POM class for an EC screen you haven't automated before
**Template:**
```
Generate a TypeScript Playwright Page Object for the EC {ScreenName} screen.

EC URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/
Screen navigation: search sidebar → type "{ScreenName}"

UI elements on this screen:
- {element1}: {description}
- {element2}: {description}

Required methods:
- navigate(): navigate to screen via sidebar
- {action1}({params}): {description}
- {action2}({params}): {description}
- expect{Something}(): assertion method

Rules:
- All locators as class properties (no inline strings)
- Use networkidle after every PrimeFaces AJAX action
- Use type() with delay:50 for search fields, fill() for others
- Escape colons in EC screenlet IDs: \\:
- Include JSDoc on every method
- Follow POM patterns from PW-03/LoginPage.ts
```

---

## Pattern 2: Discover Locators via Playwright MCP

**Trigger:** Need to find actual EC DOM selectors for a new screen
**Template:**
```
Use Playwright MCP to discover locators on the EC {ScreenName} screen.

Steps:
1. Navigate to https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/
2. Login with sysadmin/Sysadmin (Keycloak: #username, #password, #kc-login)
3. Wait for networkidle
4. Search sidebar for "{ScreenName}" and click the link
5. Wait for networkidle
6. Take screenshot
7. For each element I need: {list elements}
   - Inspect the DOM and report: id, class, xpath that uniquely identifies it
8. Generate a variables file entry for each discovered locator

Report: element name, selector type, selector value, confidence (stable/unstable)
```

---

## Pattern 3: Convert Manual Test Steps to Playwright Spec

**Trigger:** Have manual test steps and want automated equivalent
**Template:**
```
Convert these manual test steps to a Playwright TypeScript spec:

Manual Steps:
1. {step 1}
2. {step 2}
3. {step 3}
Expected result: {result}

Context:
- EC local URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/
- Use storageState: 'auth-state.json' (already logged in)
- Import LoginPage and relevant page objects from PW-03/
- Apply networkidle after AJAX actions
- Screenshot on failure
- Use idempotency pattern if test creates data

Output: complete .spec.ts file
```

---

## Pattern 4: Add Auth State to Existing Test Suite

**Trigger:** Test suite does login in beforeEach — needs to be optimised
**Template:**
```
Refactor this Playwright test suite to use saved auth state:
{paste existing test file}

Changes needed:
1. Create globalSetup.ts based on PW-02/globalSetup.ts for EC
2. Add to playwright.config.ts: globalSetup + storageState: 'auth-state.json'
3. Remove login code from beforeEach in tests
4. Verify tests still work without explicit login
5. Add .gitignore entry for auth-state.json

Output: updated playwright.config.ts, globalSetup.ts, and test file
```

---

## Pattern 5: Mock API Endpoint

**Trigger:** Test needs to control API response without touching EC database
**Template:**
```
Add route interception to this Playwright test to mock {endpoint}:
{paste test file}

Mock configuration:
- URL pattern: {pattern}
- Status: {200 | 500 | 503}
- Response body: {JSON or fixture file path}
- Delay: {0 | 2000 for slow response simulation}

Purpose: {why we need this mock — e.g. "test error handling without modifying EC data"}
```

---

## Pattern 6: Debug Failing Test

**Trigger:** Test fails with an error you can't diagnose
**Template:**
```
Debug this failing Playwright test:

Error: {paste full error message and stack trace}

Test file:
{paste test file content}

playwright.config.ts:
{paste relevant config sections}

What I've tried: {any fixes already attempted}

Likely causes to investigate:
1. Timing/wait issues
2. Selector changed in EC update
3. Auth state expired
4. Network/SSL issue

Provide: root cause analysis and fix
```

---

## Pattern 7: Add Visual Regression Baseline

**Trigger:** Need to capture current UI state for regression testing
**Template:**
```
Add visual regression tests for the EC {ScreenName} screen.

Requirements:
- Capture baseline screenshot of: {element or full page}
- Mask dynamic content: {dates, timestamps, session-specific values}
- Tolerance: maxDiffPixelRatio: 0.02
- Update baselines command: npx playwright test --update-snapshots

Generate:
1. Test spec with toHaveScreenshot() assertions
2. Instructions for generating initial baselines
3. CI configuration for consistent rendering
```

---

## Pattern 8: Generate CI Workflow

**Trigger:** Need GitHub Actions pipeline for Playwright tests
**Template:**
```
Generate a GitHub Actions workflow for the EC Playwright test suite.

Requirements:
- Trigger: push + PR to main/master
- Shards: {2 | 4} parallel shards
- Browser: chromium only
- Secrets needed: EC_URL, EC_USERNAME, EC_PASSWORD
- Upload: HTML report + traces on failure
- Retention: 7 days for reports, 3 days for traces

Based on PW-04/ci_workflow.yml — customise for: {any specific requirements}
```
