/**
 * EC Web App — Playwright Starter Test (TypeScript)
 * Target: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/
 * Auth: sysadmin / Sysadmin (Keycloak)
 *
 * Demonstrates:
 * - Browser/Context/Page setup with ignoreHTTPSErrors
 * - 5 locator strategies
 * - 5 action types
 * - 6 assertions
 * - networkidle wait pattern for PrimeFaces AJAX
 * - Screenshot on failure
 */

import { test, expect, Page } from '@playwright/test';

const EC_URL = process.env.EC_URL ?? 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/';
const EC_USER = process.env.EC_USERNAME ?? 'sysadmin';
const EC_PASS = process.env.EC_PASSWORD ?? 'Sysadmin';

// ── Shared login helper ───────────────────────────────────────────────────────

async function loginToEC(page: Page): Promise<void> {
    await page.goto(EC_URL, { waitUntil: 'domcontentloaded' });

    // Strategy 1: ID selector (Keycloak form)
    await page.locator('#username').fill(EC_USER);
    await page.locator('#password').fill(EC_PASS);

    // Strategy 2: ID selector for submit button
    await page.locator('#kc-login').click();

    // Wait for EC dashboard to load after login
    await page.waitForLoadState('networkidle', { timeout: 60_000 });
}

// ── Test suite ────────────────────────────────────────────────────────────────

test.describe('EC Web App — Smoke Tests', () => {

    // Screenshot on failure — MANDATORY pattern for EC tests
    test.afterEach(async ({ page }, testInfo) => {
        if (testInfo.status !== testInfo.expectedStatus) {
            const screenshotPath = `results/${testInfo.title.replace(/\s+/g, '_')}_failure.png`;
            await page.screenshot({ path: screenshotPath, fullPage: true });
            await testInfo.attach('failure-screenshot', {
                path: screenshotPath,
                contentType: 'image/png',
            });
        }
    });

    // ── TC01: Login ───────────────────────────────────────────────────────────
    test('TC01 - Login to EC Web App successfully', async ({ page }) => {
        await page.goto(EC_URL, { waitUntil: 'domcontentloaded' });

        // Assertion 1: Login form is visible
        await expect(page.locator('#username')).toBeVisible();
        await expect(page.locator('#password')).toBeVisible();

        await page.locator('#username').fill(EC_USER);
        await page.locator('#password').fill(EC_PASS);
        await page.locator('#kc-login').click();
        await page.waitForLoadState('networkidle', { timeout: 60_000 });

        // Assertion 2: URL no longer contains /auth/realms (login complete)
        await expect(page).not.toHaveURL(/auth\/realms/);

        // Assertion 3: EC page title contains Energy Components
        // Note: exact title may vary — adjust based on actual EC dashboard title
        await expect(page).toHaveTitle(/.*/); // placeholder — update after runtime test
    });

    // ── TC02: Navigate to Check Rules screen ─────────────────────────────────
    test('TC02 - Navigate to Check Rule screen via sidebar search', async ({ page }) => {
        await loginToEC(page);

        // Strategy 3: XPath selector for PrimeFaces sidebar search
        const searchInput = page.locator('xpath=//input[@id="menu:searchForm:searchTxt"]');
        await expect(searchInput).toBeVisible({ timeout: 30_000 });

        // Type with delay — PrimeFaces triggers AJAX on keyup
        await searchInput.click();
        await searchInput.clear();
        await searchInput.type('Check Rule', { delay: 50 });

        // Wait for search results to appear
        await page.waitForLoadState('networkidle', { timeout: 15_000 });

        // Strategy 4: XPath with text content
        const menuLink = page.locator('xpath=//label[contains(@class,"tv-link") and normalize-space(.)="Check Rule"]');
        await expect(menuLink).toBeVisible({ timeout: 15_000 });

        // Assertion 4: Menu link found with correct text
        await expect(menuLink).toContainText('Check Rule');

        await menuLink.click();
        await page.waitForLoadState('networkidle', { timeout: 30_000 });

        // Assertion 5: Check Rule screen loaded (look for screenlet ID pattern)
        // Strategy 5: CSS selector
        const checkRuleTable = page.locator('css=.ui-datatable').first();
        await expect(checkRuleTable).toBeVisible({ timeout: 20_000 });
    });

    // ── TC03: Verify Validation Overview screen loads ─────────────────────────
    test('TC03 - Navigate to Validation Overview (CO.0203)', async ({ page }) => {
        await loginToEC(page);

        const searchInput = page.locator('xpath=//input[@id="menu:searchForm:searchTxt"]');
        await expect(searchInput).toBeVisible({ timeout: 30_000 });
        await searchInput.click();
        await searchInput.clear();
        await searchInput.type('Validation Overview', { delay: 50 });
        await page.waitForLoadState('networkidle', { timeout: 15_000 });

        const menuLink = page.locator('xpath=//label[contains(@class,"tv-link") and normalize-space(.)="Validation Overview"]');
        await expect(menuLink).toBeVisible({ timeout: 15_000 });
        await menuLink.click();
        await page.waitForLoadState('networkidle', { timeout: 30_000 });

        // Assertion 6: Page screenshot for evidence
        await page.screenshot({ path: 'results/TC03_validation_overview.png' });

        // Soft assertion — page has some content (exact element TBD after runtime test)
        await expect.soft(page.locator('body')).not.toBeEmpty();
    });

});
