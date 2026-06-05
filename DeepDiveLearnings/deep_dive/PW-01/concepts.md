# PW-01: Playwright Fundamentals — Concepts

## 1. Architecture Overview

### What Playwright Is
Playwright is a browser automation library by Microsoft. It controls Chromium, Firefox, and WebKit through **native browser protocols** (Chrome DevTools Protocol for Chromium; WebSocket for Firefox/WebKit) — not the slower HTTP-based WebDriver standard.

**Key differentiators from Selenium:**
| Aspect | Playwright | Selenium |
|---|---|---|
| Protocol | CDP / WebSocket (direct) | HTTP WebDriver |
| Auto-waiting | Built-in (actionability checks) | Manual waits needed |
| Browser spawn | < 10ms new context | Seconds per session |
| Network interception | Built-in | External proxy needed |
| Multi-tab/popup | Native support | Complex workarounds |
| Shadow DOM | Auto-piercing | Manual frame handling |

### Playwright vs @playwright/test
- `playwright` — the browser automation **library** (API calls)
- `@playwright/test` — the **test runner** built on top (test/expect/fixtures/config)
- Always use `@playwright/test` for test suites — it provides HTML reports, trace viewer, retries, parallel execution

### Execution Model
- **Async/await** in TypeScript/JavaScript — all browser operations return Promises
- **Sync** in Python — Playwright Python uses synchronous API by default
- Parallel by default — each test worker gets its own Browser/Context/Page

---

## 2. Browser / BrowserContext / Page Hierarchy

```
Browser (one process — chromium, firefox, webkit)
    └── BrowserContext (isolated session — own cookies, localStorage, permissions)
        └── Page (single tab — all test interactions happen here)
```

**Why BrowserContext matters:**
- New context = fresh session in < 10ms (no full browser restart)
- Tests share a Browser but each gets its own BrowserContext → no state leakage
- Auth state stored in context (cookies, localStorage) → can be saved and reused

**Practical rule:** Work at the `Page` level in tests. The Browser and BrowserContext are managed by the framework (fixtures or config).

---

## 3. Core Concepts — Navigation and Waiting

### Navigation
```typescript
// TypeScript
await page.goto('https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/');
await page.goto(url, { waitUntil: 'networkidle' }); // wait for AJAX to settle
```
```python
# Python
page.goto('https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
page.goto(url, wait_until='networkidle')
```

### `waitUntil` Options
| Value | Fires when |
|---|---|
| `load` | `load` event (DOM + resources) |
| `domcontentloaded` | DOM parsed (fastest) |
| `networkidle` | No network requests for 500ms (**EC: use this after AJAX actions**) |

### Auto-Waiting — How It Works
Before executing an action, Playwright automatically checks:
1. **Visible** — element is in viewport and not hidden
2. **Enabled** — not disabled
3. **Stable** — not animating
4. **Attached** — in the DOM

This means NO manual `waitForSelector` before clicking — just call `click()` and Playwright waits.

**EC-specific:** After clicking Go/Save buttons that trigger PrimeFaces AJAX:
```typescript
await page.locator('#goButton').click();
await page.waitForLoadState('networkidle'); // wait for AJAX to fully settle
```

---

## 4. Locator Strategies — Priority Order

### TypeScript
```typescript
// Priority 1: ARIA role (accessible, stable)
page.getByRole('button', { name: 'Login' })
page.getByRole('textbox', { name: 'Username' })

// Priority 2: Label (form elements)
page.getByLabel('Production Date')

// Priority 3: Placeholder
page.getByPlaceholder('Search...')

// Priority 4: Text
page.getByText('Validation Overview')

// Priority 5: Test ID (data-testid)
page.getByTestId('go-button')

// Priority 6: CSS (stable, specific)
page.locator('id=username')
page.locator('css=span.ui-icon-seek-end')
page.locator('.ui-dialog .ui-button-text')

// Priority 7: XPath (last resort)
page.locator('xpath=//label[contains(@class,"tv-link") and normalize-space(.)="Check Rule"]')

// Chaining
page.locator('.ui-datatable').locator('tr').nth(0)

// Filter
page.locator('tr').filter({ hasText: 'PHD_STRM_COMP' })
```

### Python
```python
# Same priorities, different syntax
page.get_by_role('button', name='Login')
page.get_by_label('Production Date')
page.get_by_placeholder('Search...')
page.get_by_text('Validation Overview')
page.locator('#username')
page.locator('css=span.ui-icon-seek-end')
page.locator('xpath=//label[@class="tv-link"]')
```

### EC-Specific Locator Patterns
```typescript
// EC sidebar search (PrimeFaces — must use Type, not Fill)
page.locator('xpath=//input[@id="menu:searchForm:searchTxt"]')

// EC screenlet table rows
page.locator('tr[data-rk]')

// EC specific screenlet ID pattern: {screenletId}:form:{elementId}
page.locator('#check_rules\\:form\\:T\\:sfilter0_ft_filter')

// EC Keycloak login
page.locator('#username')
page.locator('#password')
page.locator('#kc-login')

// EC pagination last page
page.locator('css=span.ui-icon-seek-end')
```

---

## 5. Core Actions

### TypeScript
```typescript
// Click
await locator.click();
await locator.click({ button: 'right' });
await locator.dblclick();

// Type
await locator.fill('text');              // clear + type (use for most inputs)
await locator.type('text', { delay: 50 }); // char by char (use for AJAX-triggered search)
await locator.clear();

// Keyboard
await locator.press('Enter');
await locator.press('Tab');
await page.keyboard.press('Escape');

// Select dropdown
await locator.selectOption('value');
await locator.selectOption({ label: 'Verified' });

// Checkbox
await locator.check();
await locator.uncheck();

// Hover
await locator.hover();

// File upload
await locator.setInputFiles('path/to/file.csv');
```

### Python
```python
locator.click()
locator.dblclick()
locator.fill('text')
locator.type('text', delay=50)
locator.clear()
locator.press('Enter')
locator.select_option('value')
locator.check()
locator.uncheck()
locator.hover()
locator.set_input_files('path/to/file.csv')
```

---

## 6. Core Assertions

### TypeScript — `expect()` with auto-retry
```typescript
// Visibility
await expect(locator).toBeVisible();
await expect(locator).toBeHidden();

// Enabled state
await expect(locator).toBeEnabled();
await expect(locator).toBeDisabled();

// Text content
await expect(locator).toHaveText('exact text');
await expect(locator).toContainText('partial');
await expect(locator).toHaveText(/regex/);

// Value
await expect(locator).toHaveValue('input value');

// Count
await expect(locator).toHaveCount(5);

// Checked state
await expect(locator).toBeChecked();

// Page-level
await expect(page).toHaveURL('https://...');
await expect(page).toHaveTitle('EC - Dashboard');

// Soft assertion (continues even on failure)
await expect.soft(locator).toBeVisible();
await expect.soft(locator).toHaveText('value');
// ... all soft assertions collected, test completes, then fails at end

// Custom error message
await expect(locator, 'Login button should be visible').toBeVisible();
```

### Python
```python
from playwright.sync_api import expect

expect(locator).to_be_visible()
expect(locator).to_be_hidden()
expect(locator).to_have_text('exact text')
expect(locator).to_contain_text('partial')
expect(locator).to_have_value('value')
expect(locator).to_have_count(5)
expect(locator).to_be_enabled()
expect(page).to_have_url('https://...')
expect(page).to_have_title('EC')
```

---

## EC Web App Automation Key Facts

- **Local EC URL:** `https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/`
- **Login:** sysadmin / Sysadmin (Keycloak form — ids: `#username`, `#password`, `#kc-login`)
- **Self-signed cert:** use `ignoreHTTPSErrors: true` in context options
- **PrimeFaces AJAX:** after EVERY action → `page.waitForLoadState('networkidle')`
- **Search fields:** use `type()` with delay (not `fill()`) — PrimeFaces triggers on keyup
- **EC IDs:** `{screenlet}:form:{element}` — escape colons in CSS: `\\:`
