# CLAUDE CODE EXECUTION PROMPT — PW-01: Playwright Fundamentals

## CONTEXT
This is a **self-directed deep-dive learning task**. The user is NOT present to monitor progress.
You must work autonomously from start to finish, then produce a written summary and backup all outputs.
Do NOT pause to ask questions. If you encounter ambiguity, make the best professional decision and document it in the summary.

---

## TASK IDENTITY
- **Task ID**: PW-01
- **Tool**: Playwright (latest stable)
- **Phase**: Fundamentals
- **Backup folder**: `deep_dive/PW-01/`
- **Environment**: Windows 11, VS Code, Node.js

---

## LEARNING OBJECTIVES

### 1. Architecture Overview
- What Playwright is: browser automation library vs test framework
- Playwright vs Selenium vs Cypress — key architectural differences
- Supported browsers: Chromium, Firefox, WebKit
- How Playwright communicates with browsers: CDP vs WebSocket protocol
- Playwright Test (`@playwright/test`) vs Playwright library (`playwright`) — distinction
- The execution model: async/await, context isolation, parallelism by default

### 2. Installation & Setup (Windows 11 / VS Code)
- `npm init playwright@latest` — what it scaffolds
- Installing browsers: `npx playwright install`
- VS Code extension: Playwright Test for VS Code — features and how to use
- `playwright.config.ts` anatomy:
  - `testDir`, `timeout`, `retries`, `workers`
  - `use`: `baseURL`, `headless`, `screenshot`, `video`, `trace`
  - `projects`: multi-browser matrix
- Running tests: `npx playwright test`, `--headed`, `--debug`, `--ui`
- Viewing reports: `npx playwright show-report`

### 3. Core Concepts
**Browser, BrowserContext, Page hierarchy:**
- `Browser` — the browser process
- `BrowserContext` — isolated session (cookies, localStorage, permissions)
- `Page` — a single tab; all actions happen here
- Why you should almost always work at `Page` level

**Navigation:**
- `page.goto(url)` — options: `waitUntil` (`load`, `domcontentloaded`, `networkidle`)
- `page.reload()`, `page.goBack()`, `page.goForward()`
- `page.waitForURL()`

**Waiting strategy:**
- Auto-waiting: Playwright's built-in actionability checks (visible, enabled, stable, attached)
- `page.waitForSelector()` — legacy, prefer locators
- `page.waitForLoadState()`
- `page.waitForTimeout()` — discouraged, document when acceptable
- `expect(locator).toBeVisible()` — assertion-based waiting

### 4. Locator Strategies
- `page.locator()` — the primary API
- Recommended locators (priority order):
  1. `getByRole()` — ARIA roles
  2. `getByLabel()` — form labels
  3. `getByPlaceholder()`
  4. `getByText()`
  5. `getByTestId()` — `data-testid` attribute
  6. CSS selectors — last resort
  7. XPath — avoid unless no alternative
- Chaining locators: `locator.locator()`
- `locator.filter()` — narrow by text or another locator
- `locator.nth(n)` — index into list
- `locator.first()`, `locator.last()`
- Strict mode: what happens when a locator matches multiple elements
- `locator.all()` — iterate over multiple matches

### 5. Core Actions
- `locator.click()` — options: `button`, `clickCount`, `force`, `modifiers`, `position`
- `locator.fill()` — clear + type
- `locator.type()` — character by character (for special inputs)
- `locator.press()` — keyboard keys
- `locator.selectOption()` — dropdowns
- `locator.check()` / `locator.uncheck()` — checkboxes
- `locator.hover()`
- `locator.dragTo()`
- `page.keyboard.press()` / `page.keyboard.type()`
- Handling file uploads: `locator.setInputFiles()`

### 6. Core Assertions (`expect`)
- `expect(locator).toBeVisible()`
- `expect(locator).toBeEnabled()` / `.toBeDisabled()`
- `expect(locator).toHaveText()` / `.toContainText()`
- `expect(locator).toHaveValue()`
- `expect(locator).toHaveCount()`
- `expect(locator).toBeChecked()`
- `expect(page).toHaveURL()`
- `expect(page).toHaveTitle()`
- Soft assertions: `expect.soft()`
- Custom error messages: `expect(locator, 'message').toBeVisible()`

---

## DELIVERABLES

Produce ALL of the following inside `deep_dive/PW-01/`:

### 1. `concepts.md`
Comprehensive explanation of all 6 topic areas with annotated code snippets.
Map each concept to an EC Web UI automation use case.

### 2. `starter_test.spec.ts`
A working Playwright test file demonstrating:
- At least 3 test cases in a `test.describe` block
- Navigation using `page.goto()`
- At least 5 different locator strategies
- At least 5 different action types
- At least 6 different assertions
- Auto-waiting in practice (no `page.waitForTimeout` unless commented with reason)
- `beforeEach` hook for setup
- `afterEach` hook with screenshot on failure pattern:
  ```ts
  test.afterEach(async ({ page }, testInfo) => {
    if (testInfo.status !== testInfo.expectedStatus) {
      await page.screenshot({ path: `screenshots/${testInfo.title}.png` });
    }
  });
  ```
- Inline comments explaining every non-obvious line

### 3. `playwright.config.ts`
A production-quality config file for the EC Web UI project:
- `baseURL` using environment variable: `process.env.EC_URL ?? 'http://localhost'`
- `headless: true` default with `headed` override via env var
- Screenshot on failure enabled
- Video on failure enabled
- Trace on retry enabled
- 30s timeout
- 2 retries in CI
- Chromium project (primary) + Firefox project (secondary)
- HTML reporter configured

### 4. `locator_reference.md`
Quick-reference table of all locator strategies:
- Strategy name
- Syntax
- When to use
- When to avoid
- EC-specific example

### 5. `SUMMARY_PW-01.md`
Task completion summary containing:
- Date/time completed
- Topics covered (checklist)
- Key takeaways (minimum 5)
- Gotchas discovered
- Files produced (with one-line description each)
- Recommended prerequisites for PW-02
- Confidence rating (1–5 with justification)

---

## EXECUTION INSTRUCTIONS

1. Create the folder `deep_dive/PW-01/`
2. Produce files in order: `concepts.md` → `playwright.config.ts` → `starter_test.spec.ts` → `locator_reference.md` → `SUMMARY_PW-01.md`
3. Ensure `starter_test.spec.ts` uses TypeScript and imports from `@playwright/test`
4. Append to `deep_dive/PROGRESS_LOG.md`:
   `[PW-01] COMPLETED — <date> — Playwright Fundamentals — Files: 5`
5. Do NOT ask the user any questions. Complete the task fully and autonomously.
