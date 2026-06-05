# Playwright — 20 Pitfalls & Troubleshooting Reference

### P01 — Timeout exceeded on locator (Strict mode violation)
**Symptom:** `Error: strict mode violation: locator('.ui-button') resolved to 5 elements`
**Cause:** Locator matches multiple elements — Playwright strict mode requires exactly 1
**Resolution:** Use `.first()`, `.nth(n)`, or more specific selector
**Prevention:** Always qualify selectors to be unique on the page

---

### P02 — Element is not visible (covered by overlay)
**Symptom:** `Error: element is not visible` despite element being in DOM
**Cause:** Modal, loading spinner, or overlay element is covering the target
**Resolution:** Wait for overlay to disappear: `await page.locator('.ui-blockui').waitFor({ state: 'hidden' })`
**Prevention:** After every AJAX-triggering action, wait for networkidle + overlay hidden

---

### P03 — Element is detached from DOM (stale reference)
**Symptom:** `Error: element is detached from DOM`
**Cause:** EC re-renders the component (PrimeFaces partial update) after you got a reference
**Resolution:** Re-query the locator after the page update — don't store locators across AJAX calls
**Prevention:** Never store locator references across `waitForLoadState('networkidle')`

---

### P04 — Auth state not loaded
**Symptom:** Tests redirect to Keycloak login despite `storageState: 'auth-state.json'`
**Cause:** Wrong path to auth-state.json, or file doesn't exist yet
**Resolution:** Run `globalSetup` first. Check path is relative to `playwright.config.ts` location
**Prevention:** Run `npx playwright test` from project root — config resolves paths from there

---

### P05 — ignoreHTTPSErrors not working
**Symptom:** `net::ERR_CERT_AUTHORITY_INVALID` even with `ignoreHTTPSErrors: true`
**Cause:** Set at page level instead of context level
**Resolution:** Set in `browser.newContext({ ignoreHTTPSErrors: true })` or in config `use:`
**Prevention:** Always set `ignoreHTTPSErrors` in playwright.config.ts `use:` block globally

---

### P06 — Flaky parallel tests (shared state)
**Symptom:** Tests pass individually but fail when run in parallel
**Cause:** Tests share browser state, or modify the same database records
**Resolution:** Use test data with `AUTOTEST_<workerIndex>` prefix; ensure teardown after each test
**Prevention:** Test isolation checklist — each test manages its own data lifecycle

---

### P07 — Screenshot baseline mismatch (OS rendering differences)
**Symptom:** Visual regression test fails in CI but passes locally
**Cause:** Font rendering differs between OS versions (Windows vs Linux CI)
**Resolution:** Generate baselines in CI: `npx playwright test --update-snapshots` in CI
**Prevention:** Use `maxDiffPixelRatio: 0.02` for tolerance; mask dynamic content (dates, session IDs)

---

### P08 — Route handler not called
**Symptom:** Mock never fires; real API is called instead
**Cause:** Route pattern doesn't match actual request URL (case, query params, etc.)
**Resolution:** Log all requests: `page.on('request', r => console.log(r.url()))` to see actual URL
**Prevention:** Use broad patterns: `**/api/**` not `https://server/api/endpoint`

---

### P09 — page.waitForTimeout causing flakiness
**Symptom:** Test fails inconsistently — sometimes the fixed sleep is too short
**Cause:** `await page.waitForTimeout(3000)` is timing-based — network speed varies
**Resolution:** Replace with assertion-based wait: `await expect(locator).toBeVisible()`
**Prevention:** Ban all `waitForTimeout` — use `waitForLoadState`, `waitForResponse`, or `expect()`

---

### P10 — Download not triggered
**Symptom:** `await page.waitForEvent('download')` hangs forever
**Cause:** `waitForEvent` called AFTER the click — event already fired
**Resolution:** Call `waitForEvent` BEFORE the click:
```typescript
const [download] = await Promise.all([
    page.waitForEvent('download'),
    page.locator('#downloadBtn').click(),
]);
```
**Prevention:** Always use `Promise.all` pattern for downloads

---

### P11 — PrimeFaces fill() doesn't trigger search
**Symptom:** Search results don't appear after filling search input
**Cause:** `fill()` sets value without triggering DOM events; PrimeFaces listens on keyup
**Resolution:** Use `locator.type(text, { delay: 50 })` to simulate keystrokes
**Prevention:** For ALL EC PrimeFaces search/autocomplete fields — always use `type()` not `fill()`

---

### P12 — networkidle never resolves
**Symptom:** `page.waitForLoadState('networkidle')` times out
**Cause:** EC has a background polling request (WebSocket or periodic AJAX)
**Resolution:** Use `timeout: 60_000`; if still fails, use `domcontentloaded` instead
**Prevention:** Know which EC screens have background polling — document and adjust timeout

---

### P13 — EC colon IDs break CSS selectors
**Symptom:** `page.locator('#check_rules:form:T')` throws CSS parse error
**Cause:** `:` is a pseudo-class character in CSS — EC IDs contain colons
**Resolution:** Escape colons: `#check_rules\\:form\\:T` or use `[id="check_rules:form:T"]` or XPath
**Prevention:** For all EC screenlet IDs — use escaped CSS or `xpath=//element[@id="..."]`

---

### P14 — Selector works in MCP but fails in test
**Symptom:** Locator found via Playwright MCP inspection but `toBeVisible()` fails in test
**Cause:** Timing difference — MCP runs in headed mode interactively; test is headless and faster
**Resolution:** Add `waitFor({ state: 'visible' })` before assertions; use `networkidle` wait
**Prevention:** MCP discovery locators should always include an explicit wait in the page object

---

### P15 — `expect.soft()` failures not reported until end
**Symptom:** Soft assertion failures appear in report but test continues and passes
**Cause:** By design — soft assertions collect failures but don't stop execution
**Resolution:** Add `expect(page).toBeTruthy()` at the end of test to force failure if any soft assertions failed
**Prevention:** Use `expect.soft()` only for optional/informational checks — not for required conditions

---

### P16 — EC session expires mid-test
**Symptom:** Test redirects to Keycloak login page during execution
**Cause:** EC session timeout (typically 30-60 min)
**Resolution:** Implement session recovery pattern (see ec_patterns_guide.md Pattern 7)
**Prevention:** For long test suites, refresh auth-state.json in globalSetup at the start of each run

---

### P17 — `locator.count()` returns 0 for data not yet loaded
**Symptom:** `expect(rows).toHaveCount(8)` fails because grid hasn't loaded yet
**Cause:** Checked count before EC AJAX grid load completed
**Resolution:** `await page.waitForLoadState('networkidle')` before `count()` check
**Prevention:** Always wait for networkidle before asserting grid row counts

---

### P18 — TypeScript type errors with custom fixtures
**Symptom:** TypeScript errors when using `loginPage` fixture — type not recognized
**Cause:** Test file imports from `@playwright/test` instead of custom `fixtures/base.ts`
**Resolution:** Change `import { test, expect } from '@playwright/test'` to `import { test, expect } from '../fixtures/base'`
**Prevention:** Lint rule — enforce import from fixtures/base in test files

---

### P19 — Selector ambiguity in EC autocomplete dropdowns
**Symptom:** `selectOption()` throws — option not found
**Cause:** PrimeFaces autocomplete widgets are not native `<select>` — they render as custom divs
**Resolution:** Use click + filter pattern for PrimeFaces autocomplete:
```typescript
await dropdown.click();
await page.locator('.ui-autocomplete-item').filter({ hasText: optionText }).click();
```
**Prevention:** Identify whether EC dropdown is native `<select>` or PrimeFaces widget — different handling needed

---

### P20 — Test passes locally, fails in CI (headless difference)
**Symptom:** Test reliable locally (`headless: false`) but flaky in CI (`headless: true`)
**Cause:** Headless mode has no GPU rendering — some animations/transitions behave differently
**Resolution:** Add small explicit wait after animations; use `waitForLoadState` instead of timing
**Prevention:** Always run final validation in `headless: true` mode locally before pushing to CI
