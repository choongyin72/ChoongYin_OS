# Playwright Cheatsheet — TypeScript + Python

## Setup
```bash
# TypeScript
npm init playwright@latest
npx playwright install chromium

# Python
pip install pytest pytest-playwright
playwright install chromium
```

## Locator API Quick Reference
| Method | TS | Python |
|---|---|---|
| By Role | `getByRole('button', {name:'X'})` | `get_by_role('button', name='X')` |
| By Label | `getByLabel('Username')` | `get_by_label('Username')` |
| By Text | `getByText('Submit')` | `get_by_text('Submit')` |
| By Placeholder | `getByPlaceholder('Search')` | `get_by_placeholder('Search')` |
| By ID/CSS | `locator('#id')` | `locator('#id')` |
| By XPath | `locator('xpath=//tag')` | `locator('xpath=//tag')` |
| First | `locator.first()` | `locator.first()` |
| Nth | `locator.nth(2)` | `locator.nth(2)` |
| Filter | `locator.filter({hasText:'x'})` | `locator.filter(has_text='x')` |
| Child | `locator.locator('span')` | `locator.locator('span')` |

## Action Methods Quick Reference
| Action | TS | Python |
|---|---|---|
| Click | `await l.click()` | `l.click()` |
| Fill | `await l.fill('text')` | `l.fill('text')` |
| Type (keyup) | `await l.type('text', {delay:50})` | `l.type('text', delay=50)` |
| Press key | `await l.press('Enter')` | `l.press('Enter')` |
| Select | `await l.selectOption('val')` | `l.select_option('val')` |
| Check | `await l.check()` | `l.check()` |
| Screenshot | `await page.screenshot({path:'f.png'})` | `page.screenshot(path='f.png')` |
| Navigate | `await page.goto(url)` | `page.goto(url)` |
| Wait | `await page.waitForLoadState('networkidle')` | `page.wait_for_load_state('networkidle')` |

## Assertion Quick Reference
| Assertion | TS | Python |
|---|---|---|
| Visible | `toBeVisible()` | `to_be_visible()` |
| Hidden | `toBeHidden()` | `to_be_hidden()` |
| Text | `toHaveText('x')` | `to_have_text('x')` |
| Contains text | `toContainText('x')` | `to_contain_text('x')` |
| Value | `toHaveValue('x')` | `to_have_value('x')` |
| Count | `toHaveCount(5)` | `to_have_count(5)` |
| URL | `toHaveURL('url')` | `to_have_url('url')` |
| Enabled | `toBeEnabled()` | `to_be_enabled()` |
| Soft | `expect.soft(l).toBeVisible()` | N/A (use try/except) |

## Config Options Quick Reference
```typescript
use: {
    baseURL: 'https://...',
    headless: true,
    ignoreHTTPSErrors: true,   // EC self-signed cert
    screenshot: 'only-on-failure',
    trace: 'on-first-retry',
    actionTimeout: 30_000,
    navigationTimeout: 60_000,
    storageState: 'auth-state.json',
}
```

## CLI Flags
```bash
npx playwright test                    # run all
npx playwright test --headed           # visible browser
npx playwright test --debug            # inspector
npx playwright test --ui               # UI mode
npx playwright test --project=chromium # one browser
npx playwright test --shard=1/4        # CI sharding
npx playwright test --update-snapshots # update visual baselines
npx playwright show-report             # view HTML report
npx playwright show-trace trace.zip    # view trace
```

## Auth State Pattern (3 lines)
```typescript
// globalSetup: save
await context.storageState({ path: 'auth-state.json' });
// config: reuse
use: { storageState: 'auth-state.json' }
// .gitignore
auth-state.json
```

## Route Intercept Pattern (3 lines)
```typescript
await page.route('**/api/**', route =>
    route.fulfill({ status: 200, body: '{"ok": true}' })
);
```

## POM Class Skeleton (10 lines)
```typescript
export class MyPage {
    readonly myButton = this.page.locator('#btn');
    constructor(readonly page: Page) {}
    async goto() { await this.page.goto('/path'); }
    async clickButton() {
        await this.myButton.click();
        await this.page.waitForLoadState('networkidle');
    }
    async expectResult() { await expect(this.myButton).toBeVisible(); }
}
```

## EC-Specific Patterns
```typescript
// Login
await page.locator('#username').fill(user); await page.locator('#kc-login').click();
// After EVERY EC action
await page.waitForLoadState('networkidle', { timeout: 30_000 });
// Search sidebar (type not fill!)
await sidebar.type('Check Rule', { delay: 50 });
// Escape colon in EC IDs
page.locator('#check_rules\\:form\\:T')
```
