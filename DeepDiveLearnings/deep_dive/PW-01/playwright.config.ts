import { defineConfig, devices } from '@playwright/test';

/**
 * EC Web App — Playwright Configuration
 * Local EC: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/
 * Self-signed cert: ignoreHTTPSErrors handled at context level
 */
export default defineConfig({
    testDir: './tests',
    timeout: 60_000,           // 60s per test (EC AJAX can be slow)
    retries: process.env.CI ? 2 : 0,
    workers: process.env.CI ? 2 : 1,
    reporter: [
        ['html', { outputFolder: 'playwright-report', open: 'never' }],
        ['list'],
    ],

    use: {
        baseURL: process.env.EC_URL ?? 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/',
        headless: process.env.HEADLESS === 'true',
        ignoreHTTPSErrors: true,      // EC uses self-signed cert
        screenshot: 'only-on-failure',
        video: 'on-first-retry',
        trace: 'on-first-retry',
        actionTimeout: 30_000,
        navigationTimeout: 60_000,
    },

    outputDir: 'results/',

    projects: [
        // Primary: Chromium
        {
            name: 'chromium',
            use: {
                ...devices['Desktop Chrome'],
                ignoreHTTPSErrors: true,
                viewport: { width: 1920, height: 1080 },
            },
        },
        // Secondary: Firefox
        {
            name: 'firefox',
            use: {
                ...devices['Desktop Firefox'],
                ignoreHTTPSErrors: true,
                viewport: { width: 1920, height: 1080 },
            },
        },
    ],
});
