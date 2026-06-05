# EC Web App — Playwright Patterns Guide

## EC-Specific Environment

```typescript
// All EC tests use these constants
const EC_URL = process.env.EC_URL ?? 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/';
const EC_USERNAME = process.env.EC_USERNAME ?? 'sysadmin';
const EC_PASSWORD = process.env.EC_PASSWORD ?? 'Sysadmin';
// Local DB: localhost:1521/ORCL (ECKERNEL_EC/energy)
```

## Pattern 1: EC Login Flow

```typescript
async function loginToEC(page: Page): Promise<void> {
    await page.goto(EC_URL, { waitUntil: 'domcontentloaded' });
    await page.locator('#username').fill(EC_USERNAME);
    await page.locator('#password').fill(EC_PASSWORD);
    await page.locator('#kc-login').click();
    await page.waitForLoadState('networkidle', { timeout: 60_000 });
    // Verify logged in
    await expect(page).not.toHaveURL(/auth\/realms/);
}
```

## Pattern 2: Navigate EC Screen via Sidebar

```typescript
async function navigateToScreen(page: Page, screenName: string): Promise<void> {
    const search = page.locator('xpath=//input[@id="menu:searchForm:searchTxt"]');
    await search.waitFor({ state: 'visible', timeout: 30_000 });
    await search.click();
    await search.clear();
    // type() not fill() — PrimeFaces AJAX on keyup
    await search.type(screenName, { delay: 50 });
    await page.waitForLoadState('networkidle', { timeout: 15_000 });

    const link = page.locator(
        `xpath=//label[contains(@class,"tv-link") and normalize-space(.)="${screenName}"]`
    );
    await link.waitFor({ state: 'visible', timeout: 15_000 });
    await link.click();
    await page.waitForLoadState('networkidle', { timeout: 30_000 });
}
```

## Pattern 3: EC Oracle Grid — Wait and Verify

```typescript
// EC grids load data via AJAX — always wait for networkidle first
await page.waitForLoadState('networkidle', { timeout: 30_000 });

// EC grid rows have data-rk attribute
const rows = page.locator('tr[data-rk]');
await expect(rows).toHaveCount(8, { timeout: 15_000 }); // 8 check rules expected

// Find specific row by content
const ruleRow = page.locator('tr[data-rk]').filter({ hasText: 'PHD_STRM_COMP_MOL_PCT_VAL1' });
await expect(ruleRow).toBeVisible({ timeout: 10_000 });
```

## Pattern 4: EC Navigator Date Setting

```typescript
// EC navigator form — set date value
const dateInput = page.locator('#nav\\:form\\:G\\:0\\:R\\:1\\:C\\:0\\:da_input');
await dateInput.fill('01-Jan-2025');
await page.keyboard.press('Tab'); // trigger AJAX update

// Click Go button
await page.locator('#button\\:form\\:T').click();
await page.waitForLoadState('networkidle', { timeout: 30_000 });
```

## Pattern 5: EC Pagination — Navigate to Last Page

```typescript
// Go to last page of EC grid
const lastPageBtn = page.locator('css=span.ui-icon-seek-end');
const isVisible = await lastPageBtn.isVisible().catch(() => false);
if (isVisible) {
    await lastPageBtn.click();
    await page.waitForLoadState('networkidle', { timeout: 15_000 });
}
```

## Pattern 6: EC Column Filter

```typescript
// Toggle column filters (hamburger menu)
await page.locator('xpath=//span[contains(@id,"tfo")]').click();
await page.waitForLoadState('networkidle');

// Filter by check name
await page.locator('#check_rules\\:form\\:T\\:sfilter0_ft_filter').fill('PHD_STRM');
await page.waitForLoadState('networkidle', { timeout: 15_000 });
```

## Pattern 7: EC Session Timeout Detection

```typescript
// EC sessions expire — detect and re-authenticate
async function withSessionRecovery(page: Page, action: () => Promise<void>): Promise<void> {
    try {
        await action();
    } catch (e) {
        // If redirected to Keycloak, re-login and retry
        if (page.url().includes('/auth/realms')) {
            console.log('Session expired — re-authenticating');
            await loginToEC(page);
            await action(); // retry once
        } else {
            throw e;
        }
    }
}
```

## Pattern 8: EC Status Area Check

```typescript
// EC shows success/error in status area after save
const statusArea = page.locator('.ui-messages, .ui-growl');
// Success message
await expect(statusArea).toContainText('saved', { timeout: 10_000 });
// Error detection
const hasError = await page.locator('.ui-messages-error').isVisible().catch(() => false);
```

## Pattern 9: EC Idempotent Insert (Before/After)

```typescript
// BEFORE test: ensure clean state
async function cleanupTestRole(page: Page, roleName: string): Promise<void> {
    const row = page.locator('tr[data-rk]').filter({ hasText: roleName });
    const count = await row.count();
    if (count > 0) {
        await row.locator('[id*="delete"]').click();
        await page.waitForLoadState('networkidle');
    }
}

test.beforeEach(async ({ page }) => { await cleanupTestRole(page, 'AUTOTEST_ROLE'); });
test.afterEach(async ({ page }) => { await cleanupTestRole(page, 'AUTOTEST_ROLE'); });
```
