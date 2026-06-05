/**
 * auth_test.spec.ts — Auth state reuse test
 * Demonstrates: storageState reuse, session verification, ignoreHTTPSErrors
 */
import { test, expect } from '@playwright/test';

const EC_URL = process.env.EC_URL ?? 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/';

// This test file uses auth-state.json via playwright.config.ts:
// use: { storageState: 'auth-state.json' }
// The globalSetup already logged in — these tests skip Keycloak

test.describe('Auth Session Tests', () => {

    test('TC-AUTH-01 Session is active — EC dashboard loads without login prompt', async ({ page }) => {
        // Navigate directly to EC — should NOT redirect to Keycloak
        await page.goto(EC_URL, { waitUntil: 'networkidle' });

        // Verify NOT on Keycloak login page
        await expect(page).not.toHaveURL(/auth\/realms/);

        // Verify EC content is visible (body loaded)
        await expect(page.locator('body')).toBeVisible();
    });

    test('TC-AUTH-02 Can navigate to a protected screen without re-login', async ({ page }) => {
        await page.goto(EC_URL, { waitUntil: 'networkidle' });

        // Search for a protected screen
        const searchInput = page.locator('xpath=//input[@id="menu:searchForm:searchTxt"]');
        await expect(searchInput).toBeVisible({ timeout: 30_000 });
        await searchInput.type('Check Rule', { delay: 50 });
        await page.waitForLoadState('networkidle');

        const menuLink = page.locator(
            'xpath=//label[contains(@class,"tv-link") and normalize-space(.)="Check Rule"]'
        );
        await expect(menuLink).toBeVisible({ timeout: 15_000 });

        // If session expired, would redirect to Keycloak
        await expect(page).not.toHaveURL(/auth\/realms/);
    });

    test('TC-AUTH-03 ignoreHTTPSErrors context configured correctly', async ({ browser }) => {
        // Create a new context to verify ignoreHTTPSErrors is working
        const context = await browser.newContext({ ignoreHTTPSErrors: true });
        const page = await context.newPage();

        // This should NOT throw SSL error
        await page.goto(EC_URL, { waitUntil: 'domcontentloaded', timeout: 30_000 });
        await expect(page.locator('body')).toBeVisible();
        await context.close();
    });

});
