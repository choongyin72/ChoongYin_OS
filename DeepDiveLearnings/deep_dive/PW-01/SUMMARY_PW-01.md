# SUMMARY — PW-01: Playwright Fundamentals

**Date completed:** 2026-06-05
**Task ID:** PW-01

---

## Topics Covered

- [x] Playwright vs Selenium — CDP/WebSocket vs HTTP WebDriver
- [x] `playwright` library vs `@playwright/test` test runner
- [x] Browser / BrowserContext / Page hierarchy
- [x] New context in < 10ms vs new browser (seconds)
- [x] Navigation — `goto()`, `waitUntil` options (load/domcontentloaded/networkidle)
- [x] Auto-waiting — 4 actionability checks (visible/enabled/stable/attached)
- [x] 7 locator strategies with priority order
- [x] EC-specific locator patterns (Keycloak, PrimeFaces sidebar, screenlet IDs)
- [x] All core actions: click, fill, type, press, selectOption, check, hover
- [x] `type()` vs `fill()` — critical difference for PrimeFaces AJAX search
- [x] All core assertions with `expect()` + auto-retry
- [x] Soft assertions with `expect.soft()`
- [x] TypeScript: `@playwright/test` patterns, async/await
- [x] Python: `pytest-playwright` sync API, fixtures, conftest.py
- [x] `ignoreHTTPSErrors: true` for EC self-signed cert
- [x] `waitForLoadState('networkidle')` after every PrimeFaces AJAX action
- [x] Screenshot on failure pattern (TypeScript + Python)
- [x] Local EC environment: `https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/`

---

## TypeScript vs Python — Key Differences

| Aspect | TypeScript | Python |
|---|---|---|
| API style | Async/await | Synchronous (sync_api) |
| Test runner | `@playwright/test` | `pytest` + `pytest-playwright` |
| Browser context | `use: { ignoreHTTPSErrors: true }` in config | `browser_context_args` fixture |
| Assertions | `expect(locator).toBeVisible()` | `expect(locator).to_be_visible()` |
| Navigate | `await page.goto(url)` | `page.goto(url)` |
| Wait | `await page.waitForLoadState(...)` | `page.wait_for_load_state(...)` |
| Type with delay | `await locator.type(text, {delay: 50})` | `locator.type(text, delay=50)` |
| Feature parity | First to get new features | Adapter — may lag slightly |

---

## Key Takeaways

1. **`networkidle` after every PrimeFaces action** — EC's JSF/PrimeFaces triggers AJAX on every button click, form save, and navigation. Without `waitForLoadState('networkidle')`, tests click elements that haven't finished loading yet.

2. **`type()` not `fill()` for EC search fields** — `fill()` sets value directly without triggering DOM events. PrimeFaces sidebar search uses `keyup` listener. Use `type()` with `delay: 50` to simulate real keystrokes.

3. **`ignoreHTTPSErrors: true` is mandatory for EC** — EC local environment uses self-signed certificate. Without this, Playwright refuses to connect.

4. **Local EC URL is available** — `https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/` with sysadmin/Sysadmin. All runtime tests should target this environment.

5. **Python Playwright is synchronous** — no async/await needed. Simpler for test engineers not familiar with JavaScript. Same API with underscored method names (`to_be_visible` vs `toBeVisible`).

---

## Files Produced

| File | Description |
|---|---|
| `concepts.md` | Full architecture, locators, actions, assertions with EC examples |
| `starter_test.spec.ts` | TypeScript — 3 test cases, 5 locator strategies, 6 assertions, screenshot-on-failure |
| `playwright.config.ts` | Production config — ignoreHTTPSErrors, local EC URL, screenshot/trace on failure |
| `locator_reference.md` | Priority table, EC-specific locators, type() vs fill() |
| `python/starter_test.py` | Python equivalent — same 3 tests using sync API + pytest |
| `python/conftest.py` | pytest conftest with browser context configuration |
| `SUMMARY_PW-01.md` | This file |

---

## Confidence Rating: 4/5

Strong command of Playwright API in both TypeScript and Python. EC-specific patterns documented. Tests written for local EC Web App. Rating 4/5 because actual execution against `ap-f0a7g341jn6d.corp.quorumsoftware.com:8443` hasn't been run — element locators may need adjustment based on actual DOM inspection (flagged for runtime testing).
