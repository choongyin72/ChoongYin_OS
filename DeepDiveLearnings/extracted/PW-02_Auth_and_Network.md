# CLAUDE CODE EXECUTION PROMPT — PW-02: Auth Sessions & Network

## CONTEXT
This is a **self-directed deep-dive learning task**. The user is NOT present to monitor progress.
You must work autonomously from start to finish, then produce a written summary and backup all outputs.
Do NOT pause to ask questions. If you encounter ambiguity, make the best professional decision and document it in the summary.

**Prerequisite**: PW-01 must be completed. Read `deep_dive/PW-01/concepts.md` before starting.

---

## TASK IDENTITY
- **Task ID**: PW-02
- **Tool**: Playwright
- **Phase**: Auth Sessions & Network
- **Backup folder**: `deep_dive/PW-02/`

---

## LEARNING OBJECTIVES

### 1. Authentication Patterns
**Session storage state:**
- `browserContext.storageState()` — save cookies + localStorage to JSON file
- Loading saved state: `storageState` option in `playwright.config.ts` or `browser.newContext()`
- `globalSetup` pattern: log in once, save state, reuse across all tests
- `auth.json` / `auth-state.json` — file convention and `.gitignore` rules
- Token expiry handling: detect 401, re-authenticate, retry

**Login helper patterns:**
- `loginPage.ts` as a reusable Page Object
- Form-based login: fill username/password, click submit, wait for redirect
- Handling MFA / OTP in test environments (bypass strategies)
- Basic Auth: `page.goto(url, { auth: { username, password } })`
- Bearer token injection: `page.setExtraHTTPHeaders()`

**EC-specific authentication:**
- EC Web uses form-based login with session cookies
- Pattern: `${EC_URL}/login` → fill `${EC_USERNAME}` / `${EC_PASSWORD}` → wait for dashboard
- Environment variable injection: `process.env.EC_USERNAME`, `process.env.EC_PASSWORD`
- `.env` file setup with `dotenv` package
- Why NOT to hardcode credentials — `.gitignore` and secret management

### 2. Self-Signed Certificate Handling
- Why EC Docker Swarm environments use self-signed certs
- `ignoreHTTPSErrors: true` — where to set it (config level vs context level)
- Custom CA: `PLAYWRIGHT_CHROMIUM_CA_CERT_PATH` environment variable
- Certificate pinning bypass: differences between browsers
- Testing both HTTP and HTTPS versions of the same app
- Common error: `net::ERR_CERT_AUTHORITY_INVALID` — full resolution steps
- Security implications: only use `ignoreHTTPSErrors` in test environments, never production

### 3. Network Interception & Mocking
**Route interception:**
- `page.route(pattern, handler)` — intercept requests matching pattern
- `route.fulfill()` — return mock response
- `route.continue()` — pass through (optionally modified)
- `route.abort()` — simulate network failure
- `route.fetch()` + modify response — real request + tampered response

**Request/Response inspection:**
- `page.on('request', handler)` — observe outgoing requests
- `page.on('response', handler)` — observe incoming responses
- `page.waitForRequest()` / `page.waitForResponse()` — wait for specific network event
- Asserting API calls were made: `expect(requestPromise).resolves.toBeTruthy()`

**Use cases in EC testing:**
- Mock JasperServices REST endpoints to return fixture data
- Simulate slow API responses: `route.fulfill({ delay: 2000, ... })`
- Simulate 500/503 errors for error-handling tests
- Intercept and log all XHR/fetch requests for debugging

### 4. Screenshot Capture Patterns
- `page.screenshot()` — full page vs viewport
- `locator.screenshot()` — element-scoped screenshot
- Screenshot options: `fullPage`, `clip`, `type` (png/jpeg), `quality`
- Screenshot on failure: `afterEach` hook pattern (recap from PW-01, now with network context)
- `expect(page).toHaveScreenshot()` — visual regression baseline
- Managing baseline images: committing to version control
- Visual diff threshold: `maxDiffPixels`, `maxDiffPixelRatio`, `threshold`
- Masking dynamic content: `mask` option
- Updating baselines: `npx playwright test --update-snapshots`

### 5. Handling Complex UI Patterns
- Iframes: `frameLocator()`, actions inside frames
- Shadow DOM: Playwright's automatic piercing
- Popups and new tabs: `page.waitForEvent('popup')`
- File downloads: `page.waitForEvent('download')`
- Dialogs: `page.on('dialog', handler)` — alert, confirm, prompt
- Tooltips and hover states
- Drag and drop: `locator.dragTo(target)`

---

## DELIVERABLES

Produce ALL of the following inside `deep_dive/PW-02/`:

### 1. `auth_guide.md`
Complete guide to all authentication patterns with:
- Code examples for each pattern
- EC-specific login flow example
- Environment variable setup instructions
- `.env.example` template (never real credentials)

### 2. `globalSetup.ts`
A production-quality global setup file that:
- Launches a browser context
- Navigates to `${process.env.EC_URL}/login`
- Fills `${process.env.EC_USERNAME}` and `${process.env.EC_PASSWORD}`
- Waits for successful login (wait for a known post-login element)
- Saves storage state to `auth-state.json`
- Handles login failure gracefully (throws with descriptive message)

### 3. `network_guide.md`
Complete guide to route interception and network observation with:
- Code examples for each pattern
- EC testing use cases: mocking JasperServices endpoints
- Request/response logging utility snippet

### 4. `auth_test.spec.ts`
Test file demonstrating:
- Using saved auth state (`storageState`)
- Verifying the session is active (check a protected page element)
- Handling session expiry (mock a 401, trigger re-login)
- `ignoreHTTPSErrors: true` in the context options (with comment explaining why)

### 5. `network_test.spec.ts`
Test file demonstrating:
- Mocking an API endpoint with `route.fulfill()`
- Simulating a 500 error and asserting the UI handles it
- Waiting for a specific API response before asserting UI state
- Element-scoped screenshot assertion

### 6. `SUMMARY_PW-02.md`
Task completion summary containing:
- Date/time completed
- Topics covered (checklist)
- Key takeaways (minimum 5)
- Gotchas discovered
- Files produced (with one-line description each)
- Recommended prerequisites for PW-03
- Confidence rating (1–5 with justification)

---

## EXECUTION INSTRUCTIONS

1. Create the folder `deep_dive/PW-02/`
2. Read `deep_dive/PW-01/concepts.md` first
3. Produce files in order: `auth_guide.md` → `network_guide.md` → `globalSetup.ts` → `auth_test.spec.ts` → `network_test.spec.ts` → `SUMMARY_PW-02.md`
4. Append to `deep_dive/PROGRESS_LOG.md`:
   `[PW-02] COMPLETED — <date> — Auth Sessions & Network — Files: 6`
5. Do NOT ask the user any questions. Complete the task fully and autonomously.
