/**
 * globalSetup.ts — EC Web App Auth State Setup
 * Runs ONCE before all tests (configured in playwright.config.ts)
 * Logs in to EC, saves session state to auth-state.json
 * All tests then reuse this session → no repeated Keycloak logins
 */

import { chromium, FullConfig } from '@playwright/test';

async function globalSetup(config: FullConfig): Promise<void> {
    const EC_URL = process.env.EC_URL ?? 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/';
    const EC_USERNAME = process.env.EC_USERNAME ?? 'sysadmin';
    const EC_PASSWORD = process.env.EC_PASSWORD ?? 'Sysadmin';

    console.log(`[globalSetup] Logging in to EC: ${EC_URL}`);

    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
        ignoreHTTPSErrors: true,       // EC self-signed cert
        viewport: { width: 1920, height: 1080 },
    });

    const page = await context.newPage();

    try {
        // Navigate to EC (redirects to Keycloak login)
        await page.goto(EC_URL, { waitUntil: 'domcontentloaded', timeout: 30_000 });

        // Fill Keycloak login form
        await page.locator('#username').waitFor({ state: 'visible', timeout: 15_000 });
        await page.locator('#username').fill(EC_USERNAME);
        await page.locator('#password').fill(EC_PASSWORD);
        await page.locator('#kc-login').click();

        // Wait for EC dashboard
        await page.waitForLoadState('networkidle', { timeout: 60_000 });

        // Verify login succeeded — URL should no longer be Keycloak
        if (page.url().includes('/auth/realms')) {
            throw new Error(
                `Login failed — still on Keycloak page.\n` +
                `URL: ${page.url()}\n` +
                `Check credentials: EC_USERNAME=${EC_USERNAME}`
            );
        }

        console.log(`[globalSetup] Login successful. URL: ${page.url()}`);

        // Save cookies + localStorage to file
        await context.storageState({ path: 'auth-state.json' });
        console.log('[globalSetup] Auth state saved to auth-state.json');

    } finally {
        await browser.close();
    }
}

export default globalSetup;
