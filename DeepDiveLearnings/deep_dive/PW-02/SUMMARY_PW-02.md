# SUMMARY — PW-02: Auth Sessions & Network

**Date completed:** 2026-06-05
**Task ID:** PW-02

---

## Topics Covered

- [x] Session storage state — save cookies/localStorage to auth-state.json
- [x] globalSetup pattern — login once, reuse across all tests
- [x] `storageState` option in playwright.config.ts
- [x] Token expiry detection pattern
- [x] `ignoreHTTPSErrors` for EC self-signed cert
- [x] Custom CA certificate alternative
- [x] `page.route()` — intercept and mock API responses
- [x] `route.fulfill()` — return mock response
- [x] `route.abort()` — simulate network failure
- [x] `route.fetch()` + modify — real request + tampered response
- [x] `page.on('request')` / `page.on('response')` — observe traffic
- [x] `page.waitForResponse()` — wait for specific API call
- [x] Screenshot patterns — fullPage, element-scoped, JPEG quality
- [x] Iframe handling with `frameLocator()`
- [x] PrimeFaces dialog pattern
- [x] File download pattern with `waitForEvent('download')`
- [x] Python equivalents for all patterns

---

## Key Takeaways

1. **globalSetup login once = massive test speed improvement** — for a 50-test suite, saving one Keycloak login (avg 3s) per test saves ~2.5 minutes. With auth-state.json, tests start already authenticated.

2. **Route interception enables testing without breaking EC data** — instead of running allocations or calculations that modify DB data, mock the response to return fixture data. Tests stay idempotent.

3. **`ignoreHTTPSErrors` must be at context level** — not page level. Set it in `browser.newContext()` or in playwright.config.ts `use:` block. Setting it only on `page.goto()` options doesn't fully suppress cert errors.

4. **Python `auth_setup.py` is a standalone script** — run it once before the test suite with `python auth_setup.py`. Then conftest.py picks up auth-state.json for all subsequent tests.

5. **`page.waitForResponse()` is more reliable than timing-based waits** — instead of `Sleep 2s` after clicking Run Calculation, use `page.waitForResponse('**/calc/**')` to wait for the actual API call to complete.

---

## Files Produced

| File | Description |
|---|---|
| `auth_guide.md` | Complete auth patterns — storageState, globalSetup, SSL certs |
| `globalSetup.ts` | Production globalSetup — EC login, session save, error handling |
| `auth_test.spec.ts` | Tests: session reuse, ignoreHTTPSErrors verification |
| `network_guide.md` | Route interception, request observation, EC-specific patterns |
| `network_test.spec.ts` | Tests: mock API, 503 simulation, request logging, element screenshot |
| `python/auth_setup.py` | Python script for saving EC auth state |
| `SUMMARY_PW-02.md` | This file |

---

## Confidence Rating: 4/5
