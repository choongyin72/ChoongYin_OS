/**
 * LoginPage.ts — EC Web App Login Page Object (TypeScript)
 * Handles Keycloak-based login for Energy Components
 */

import { Page, Locator, expect } from '@playwright/test';

export class LoginPage {
    readonly page: Page;

    // Keycloak form locators
    readonly usernameInput: Locator;
    readonly passwordInput: Locator;
    readonly loginButton: Locator;
    readonly errorMessage: Locator;

    constructor(page: Page) {
        this.page = page;
        this.usernameInput  = page.locator('#username');
        this.passwordInput  = page.locator('#password');
        this.loginButton    = page.locator('#kc-login');
        this.errorMessage   = page.locator('.kc-feedback-text, .alert-error');
    }

    /**
     * Navigate to EC Web App (redirects to Keycloak login).
     * Uses EC_URL env var or falls back to local EC instance.
     */
    async goto(): Promise<void> {
        const url = process.env.EC_URL ?? 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/';
        await this.page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30_000 });
    }

    /**
     * Fill Keycloak credentials and submit.
     * Waits for networkidle to confirm EC dashboard has loaded.
     */
    async login(username: string, password: string): Promise<void> {
        await this.usernameInput.waitFor({ state: 'visible', timeout: 15_000 });
        await this.usernameInput.fill(username);
        await this.passwordInput.fill(password);
        await this.loginButton.click();
        await this.page.waitForLoadState('networkidle', { timeout: 60_000 });
    }

    /**
     * Login with default EC credentials from environment variables.
     */
    async loginWithDefaults(): Promise<void> {
        const user = process.env.EC_USERNAME ?? 'sysadmin';
        const pass = process.env.EC_PASSWORD ?? 'Sysadmin';
        await this.login(user, pass);
    }

    /**
     * Assert login error message is visible with expected text.
     * Use for testing invalid credentials scenarios.
     */
    async expectLoginError(message: string): Promise<void> {
        await expect(this.errorMessage).toBeVisible({ timeout: 10_000 });
        await expect(this.errorMessage).toContainText(message);
    }

    /**
     * Assert login was successful — URL no longer contains Keycloak path.
     */
    async expectLoginSuccessful(): Promise<void> {
        await expect(this.page).not.toHaveURL(/auth\/realms/, { timeout: 10_000 });
    }

    /**
     * Assert currently on login page (Keycloak).
     */
    async expectOnLoginPage(): Promise<void> {
        await expect(this.usernameInput).toBeVisible({ timeout: 10_000 });
        await expect(this.loginButton).toBeVisible();
    }
}
