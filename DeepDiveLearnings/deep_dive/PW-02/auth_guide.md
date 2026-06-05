# PW-02: Authentication & Session Management

## 1. Session Storage State — Save & Reuse

### Why Use Saved Sessions
- EC login via Keycloak takes 2-5 seconds per test
- With 50 tests, that's 100-250 seconds wasted on login alone
- Save auth state once → reuse across all tests → cuts setup time dramatically

### TypeScript — globalSetup Pattern
```typescript
// globalSetup.ts
import { chromium, FullConfig } from '@playwright/test';

async function globalSetup(config: FullConfig) {
    const browser = await chromium.launch();
    const context = await browser.newContext({
        ignoreHTTPSErrors: true,
        viewport: { width: 1920, height: 1080 },
    });
    const page = await context.newPage();

    await page.goto(
        process.env.EC_URL ?? 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/',
        { waitUntil: 'domcontentloaded' }
    );
    await page.locator('#username').fill(process.env.EC_USERNAME ?? 'sysadmin');
    await page.locator('#password').fill(process.env.EC_PASSWORD ?? 'Sysadmin');
    await page.locator('#kc-login').click();
    await page.waitForLoadState('networkidle', { timeout: 60_000 });

    // Verify login succeeded
    if (page.url().includes('/auth/realms')) {
        throw new Error('Login failed — still on Keycloak page. Check credentials.');
    }

    // Save cookies + localStorage to file
    await context.storageState({ path: 'auth-state.json' });
    await browser.close();
}

export default globalSetup;
```

### playwright.config.ts — Wire Up globalSetup
```typescript
export default defineConfig({
    globalSetup: require.resolve('./globalSetup'),
    use: {
        storageState: 'auth-state.json',  // reuse session in all tests
        ignoreHTTPSErrors: true,
    },
});
```

### Python — Auth State
```python
# setup_auth.py — run once before test suite
from playwright.sync_api import sync_playwright
import os, json

EC_URL = os.getenv('EC_URL', 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()

    page.goto(EC_URL, wait_until='domcontentloaded')
    page.locator('#username').fill(os.getenv('EC_USERNAME', 'sysadmin'))
    page.locator('#password').fill(os.getenv('EC_PASSWORD', 'Sysadmin'))
    page.locator('#kc-login').click()
    page.wait_for_load_state('networkidle', timeout=60_000)

    if '/auth/realms' in page.url:
        raise RuntimeError('Login failed — still on Keycloak page')

    context.storage_state(path='auth-state.json')
    browser.close()
    print('Auth state saved to auth-state.json')
```

### conftest.py — Use Saved Auth State
```python
# conftest.py
import pytest

@pytest.fixture(scope='session')
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        'ignore_https_errors': True,
        'storage_state': 'auth-state.json',  # reuse session
    }
```

### .gitignore
```
auth-state.json    # contains session cookies — never commit
.env               # contains credentials — never commit
```

---

## 2. Self-Signed Certificate Handling for EC

### Why EC Has Self-Signed Certs
EC Docker Swarm environments use self-signed certificates for HTTPS — not signed by a public CA. Playwright refuses connections to self-signed cert servers by default.

### Solutions (in priority order)

**Solution 1: ignoreHTTPSErrors (simplest — use this)**
```typescript
// In playwright.config.ts
use: { ignoreHTTPSErrors: true }

// Or per-context
const context = await browser.newContext({ ignoreHTTPSErrors: true });
```
```python
# Python
context = browser.new_context(ignore_https_errors=True)
```

**Solution 2: Custom CA Certificate**
```bash
# Set env var to your CA cert file
export PLAYWRIGHT_CHROMIUM_CA_CERT_PATH=/path/to/ca.crt
```

### Security Rule
`ignoreHTTPSErrors: true` MUST only be used in test environments. Never in production automation.

---

## 3. Network Interception & Mocking

### TypeScript — Route Interception
```typescript
// Mock an API endpoint
await page.route('**/api/production/**', async route => {
    await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ data: [{ code: 'TEST', value: 100.5 }] }),
    });
});

// Simulate server error
await page.route('**/api/calc/**', route => {
    route.fulfill({ status: 503, body: 'Service Unavailable' });
});

// Pass through (no mock)
await page.route('**/*', route => route.continue());

// Abort request
await page.route('**/analytics/**', route => route.abort());

// Intercept and modify response
await page.route('**/api/data', async route => {
    const response = await route.fetch();
    const json = await response.json();
    json.extraField = 'injected';
    await route.fulfill({ response, body: JSON.stringify(json) });
});
```

### Python — Route Interception
```python
def mock_handler(route):
    route.fulfill(
        status=200,
        content_type='application/json',
        body='{"data": [{"code": "TEST", "value": 100.5}]}'
    )

page.route('**/api/production/**', mock_handler)

# Simulate error
page.route('**/api/calc/**', lambda route: route.fulfill(status=503))
```

### Request/Response Observation
```typescript
// Log all API requests
page.on('request', req => {
    if (req.url().includes('/api/')) {
        console.log(`→ ${req.method()} ${req.url()}`);
    }
});

// Wait for specific API response
const responsePromise = page.waitForResponse('**/api/production/daily');
await page.locator('#goButton').click();
const response = await responsePromise;
const data = await response.json();
```

```python
# Python
page.on('request', lambda req: print(f"→ {req.method} {req.url}") if '/api/' in req.url else None)

with page.expect_response('**/api/production/daily') as response_info:
    page.locator('#goButton').click()
response = response_info.value
```

---

## 4. Screenshot Patterns

### TypeScript
```typescript
// Full page screenshot
await page.screenshot({ path: 'full-page.png', fullPage: true });

// Viewport only
await page.screenshot({ path: 'viewport.png' });

// Element screenshot
await page.locator('.ui-datatable').screenshot({ path: 'table.png' });

// JPEG with quality
await page.screenshot({ path: 'compressed.jpg', type: 'jpeg', quality: 80 });

// Embed in test report
await testInfo.attach('evidence', {
    body: await page.screenshot(),
    contentType: 'image/png',
});
```

### Python
```python
page.screenshot(path='full-page.png', full_page=True)
page.locator('.ui-datatable').screenshot(path='table.png')
```

---

## 5. Complex UI Patterns in EC

### Iframes (EC may have some)
```typescript
const frame = page.frameLocator('#reportFrame');
await frame.locator('.report-content').waitFor();
await expect(frame.locator('.report-title')).toHaveText('Production Report');
```

### PrimeFaces Dialog / Modal
```typescript
// Wait for dialog to appear
await page.locator('.ui-dialog').waitFor({ state: 'visible' });
// Interact inside dialog
await page.locator('.ui-dialog').locator('button').first().click();
```

### File Downloads
```typescript
const downloadPromise = page.waitForEvent('download');
await page.locator('#downloadButton').click();
const download = await downloadPromise;
await download.saveAs(`results/${download.suggestedFilename()}`);
```
