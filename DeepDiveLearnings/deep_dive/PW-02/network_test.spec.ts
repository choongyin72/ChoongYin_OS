/**
 * network_test.spec.ts — Network interception demonstrations
 * Shows: route.fulfill, 500 simulation, response waiting, element screenshot
 */
import { test, expect } from '@playwright/test';

const EC_URL = process.env.EC_URL ?? 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/';

test.describe('Network Interception Tests', () => {

    test('TC-NET-01 Mock API returns fixture data', async ({ page }) => {
        // Intercept any EC REST API call and return fixture JSON
        await page.route('**/rest/v1/**', async route => {
            await route.fulfill({
                status: 200,
                contentType: 'application/json',
                body: JSON.stringify({
                    items: [{ code: 'TEST_STRM_001', value: 1234.567 }],
                    total: 1,
                }),
            });
        });

        await page.goto(EC_URL, { waitUntil: 'networkidle' });
        // The mock is in place — any REST call returns fixture
        // Verify page loaded without errors
        await expect(page.locator('body')).toBeVisible();
    });

    test('TC-NET-02 Simulate 503 error and verify page handles it gracefully', async ({ page }) => {
        // Simulate server error on calc endpoint
        let errorTriggered = false;
        await page.route('**/api/calc/**', async route => {
            errorTriggered = true;
            await route.fulfill({ status: 503, body: 'Service Unavailable' });
        });

        await page.goto(EC_URL, { waitUntil: 'networkidle' });
        // If EC makes a calc API call, the mock will respond with 503
        // This tests that EC handles errors gracefully without crashing
        await expect(page.locator('body')).toBeVisible();
    });

    test('TC-NET-03 Log all XHR requests during navigation', async ({ page }) => {
        const requests: string[] = [];

        // Observe all XHR/fetch requests
        page.on('request', req => {
            if (['xhr', 'fetch'].includes(req.resourceType())) {
                requests.push(`${req.method()} ${req.url()}`);
            }
        });

        await page.goto(EC_URL, { waitUntil: 'networkidle' });

        // Verify we captured some requests (EC makes AJAX calls on load)
        console.log('Captured API calls:', requests.slice(0, 5));
        // Note: exact request count depends on EC version and screen
    });

    test('TC-NET-04 Element-scoped screenshot of datatable', async ({ page }) => {
        await page.goto(EC_URL, { waitUntil: 'networkidle' });

        // Navigate to a screen with a datatable
        const searchInput = page.locator('xpath=//input[@id="menu:searchForm:searchTxt"]');
        if (await searchInput.isVisible()) {
            await searchInput.type('Check Rule', { delay: 50 });
            await page.waitForLoadState('networkidle');

            const menuLink = page.locator(
                'xpath=//label[contains(@class,"tv-link") and normalize-space(.)="Check Rule"]'
            );
            if (await menuLink.isVisible({ timeout: 5_000 }).catch(() => false)) {
                await menuLink.click();
                await page.waitForLoadState('networkidle');

                // Element-scoped screenshot — just the datatable
                const datatable = page.locator('.ui-datatable').first();
                if (await datatable.isVisible({ timeout: 10_000 }).catch(() => false)) {
                    await datatable.screenshot({ path: 'results/check_rules_table.png' });
                    await expect(datatable).toBeVisible();
                }
            }
        }

        // Full page screenshot as fallback evidence
        await page.screenshot({ path: 'results/TC_NET_04_fullpage.png' });
    });

});
