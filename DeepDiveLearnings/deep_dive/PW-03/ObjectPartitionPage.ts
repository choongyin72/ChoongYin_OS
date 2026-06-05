/**
 * ObjectPartitionPage.ts — EC Object Partition Screen Page Object (TypeScript)
 * Screen: CO.0??? — Object Partition (role assignment per object)
 * Idempotent patterns included for safe test repetition
 */

import { Page, Locator, expect } from '@playwright/test';

export class ObjectPartitionPage {
    readonly page: Page;

    // Navigator locators
    readonly searchInput: Locator;

    // Screen locators (adjust selectors after live DOM inspection)
    readonly operatorDropdown: Locator;
    readonly roleDropdown: Locator;
    readonly insertButton: Locator;
    readonly dataGrid: Locator;
    readonly gridRows: Locator;

    constructor(page: Page) {
        this.page = page;

        // Sidebar search (PrimeFaces)
        this.searchInput = page.locator('xpath=//input[@id="menu:searchForm:searchTxt"]');

        // Object Partition screen selectors
        // NOTE: Exact IDs to be verified against live EC DOM in runtime test
        this.operatorDropdown = page.locator('[id*="operatorDropdown"], [id*="operator_select"]').first();
        this.roleDropdown     = page.locator('[id*="roleDropdown"], [id*="role_select"]').first();
        this.insertButton     = page.locator('xpath=//button[contains(@id,"insertBtn") or contains(@id,"addBtn")]').first();
        this.dataGrid         = page.locator('.ui-datatable').first();
        this.gridRows         = page.locator('.ui-datatable tr[data-rk]');
    }

    /** Navigate to Object Partition screen via sidebar. */
    async navigate(): Promise<void> {
        await this.searchInput.waitFor({ state: 'visible', timeout: 30_000 });
        await this.searchInput.click();
        await this.searchInput.clear();
        await this.searchInput.type('Object Partition', { delay: 50 });
        await this.page.waitForLoadState('networkidle', { timeout: 15_000 });

        const menuLink = this.page.locator(
            'xpath=//label[contains(@class,"tv-link") and contains(normalize-space(.),"Object Partition")]'
        );
        await menuLink.waitFor({ state: 'visible', timeout: 15_000 });
        await menuLink.click();
        await this.page.waitForLoadState('networkidle', { timeout: 30_000 });
    }

    /** Select an operator from the operator dropdown. */
    async selectOperator(operatorName: string): Promise<void> {
        await this.operatorDropdown.waitFor({ state: 'visible', timeout: 10_000 });
        await this.operatorDropdown.selectOption({ label: operatorName });
        await this.page.waitForLoadState('networkidle', { timeout: 15_000 });
    }

    /** Insert a role for the currently selected operator. */
    async insertRole(roleName: string): Promise<void> {
        await this.roleDropdown.waitFor({ state: 'visible', timeout: 10_000 });
        await this.roleDropdown.selectOption({ label: roleName });
        await this.insertButton.click();
        await this.page.waitForLoadState('networkidle', { timeout: 15_000 });
    }

    /** Assert a specific role row exists in the data grid. */
    async expectRowExists(roleName: string): Promise<void> {
        const row = this.gridRows.filter({ hasText: roleName });
        await expect(row).toHaveCount(1, { timeout: 10_000 });
    }

    /** Assert role does NOT exist in the grid. */
    async expectRowNotExists(roleName: string): Promise<void> {
        const row = this.gridRows.filter({ hasText: roleName });
        await expect(row).toHaveCount(0, { timeout: 10_000 });
    }

    /**
     * Idempotency helper: insert role only if it doesn't already exist.
     * Prevents duplicate data errors on re-runs.
     */
    async ensureRowExists(roleName: string): Promise<void> {
        const count = await this.gridRows.filter({ hasText: roleName }).count();
        if (count === 0) {
            await this.insertRole(roleName);
        }
    }

    /**
     * Idempotency helper: delete role only if it exists.
     * Safe to call in teardown even if test failed before insert.
     */
    async ensureRowNotExists(roleName: string): Promise<void> {
        const row = this.gridRows.filter({ hasText: roleName });
        const count = await row.count();
        if (count > 0) {
            // Click delete button on that row
            const deleteBtn = row.locator('button[id*="delete"], span.ui-icon-trash').first();
            if (await deleteBtn.isVisible()) {
                await deleteBtn.click();
                await this.page.waitForLoadState('networkidle', { timeout: 15_000 });
            }
        }
    }

    /** Count rows currently in grid. */
    async getRowCount(): Promise<number> {
        return await this.gridRows.count();
    }
}
