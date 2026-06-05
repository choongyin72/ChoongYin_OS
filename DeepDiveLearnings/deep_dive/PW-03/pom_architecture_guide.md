# PW-03: Page Object Model Architecture Guide

## Why POM
- **Single point of change** — when UI changes, update one page object, not 20 test files
- **Readable tests** — `await loginPage.login(user, pass)` vs 5 raw locator lines
- **Reusable actions** — `objectPartitionPage.insertRole(op, role)` called from many tests

## POM Class Anatomy

```typescript
// pages/LoginPage.ts
import { Page, Locator } from '@playwright/test';

export class LoginPage {
    readonly page: Page;

    // Locators as class properties — defined ONCE, used everywhere
    readonly usernameInput: Locator;
    readonly passwordInput: Locator;
    readonly loginButton: Locator;
    readonly errorMessage: Locator;

    constructor(page: Page) {
        this.page = page;
        this.usernameInput = page.locator('#username');
        this.passwordInput = page.locator('#password');
        this.loginButton = page.locator('#kc-login');
        this.errorMessage = page.locator('.kc-feedback-text');
    }

    /** Navigate to EC login page. */
    async goto(): Promise<void> {
        await this.page.goto(
            process.env.EC_URL ?? 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/'
        );
    }

    /** Fill credentials and submit Keycloak form. */
    async login(username: string, password: string): Promise<void> {
        await this.usernameInput.fill(username);
        await this.passwordInput.fill(password);
        await this.loginButton.click();
        await this.page.waitForLoadState('networkidle', { timeout: 60_000 });
    }

    /** Assertion method — keeps assertions out of action methods. */
    async expectLoginError(message: string): Promise<void> {
        await expect(this.errorMessage).toContainText(message);
    }

    async expectLoginSuccessful(): Promise<void> {
        await expect(this.page).not.toHaveURL(/auth\/realms/);
    }
}
```

## Fixtures Pattern — Replace beforeEach

```typescript
// fixtures/base.ts
import { test as base, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { ObjectPartitionPage } from '../pages/ObjectPartitionPage';

type Fixtures = {
    loginPage: LoginPage;
    objectPartitionPage: ObjectPartitionPage;
};

export const test = base.extend<Fixtures>({
    loginPage: async ({ page }, use) => {
        await use(new LoginPage(page));
    },
    objectPartitionPage: async ({ page }, use) => {
        await use(new ObjectPartitionPage(page));
    },
});

export { expect };
```

```typescript
// In test file — import from fixtures, not @playwright/test
import { test, expect } from '../fixtures/base';

test('Login works', async ({ loginPage }) => {
    await loginPage.goto();
    await loginPage.login('sysadmin', 'Sysadmin');
    await loginPage.expectLoginSuccessful();
});
```

## Directory Structure
```
playwright/
├── pages/
│   ├── LoginPage.ts
│   ├── ObjectPartitionPage.ts
│   └── components/
│       ├── GridComponent.ts      ← reusable grid logic
│       └── NavigatorComponent.ts ← EC navigator
├── fixtures/
│   └── base.ts
├── tests/
│   ├── login.spec.ts
│   └── objectPartition.spec.ts
├── playwright.config.ts
└── globalSetup.ts
```

## Python POM Pattern

```python
# pages/login_page.py
from playwright.sync_api import Page, expect

class LoginPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.username_input = page.locator('#username')
        self.password_input = page.locator('#password')
        self.login_button = page.locator('#kc-login')

    def goto(self) -> None:
        import os
        self.page.goto(
            os.getenv('EC_URL', 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
        )

    def login(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        self.page.wait_for_load_state('networkidle', timeout=60_000)

    def expect_login_successful(self) -> None:
        assert '/auth/realms' not in self.page.url, f'Still on login: {self.page.url}'
```

## When to Split a Page Object
- Page object has > 15 locators → split by feature area
- Locators for a component (grid, modal, navigator) appear in multiple pages → extract to component object
- Rule: one page object per screen or major screen section

## Component Objects — Reusable Grid
```typescript
// pages/components/GridComponent.ts
export class GridComponent {
    constructor(private page: Page, private gridSelector: string) {}

    get rows() { return this.page.locator(`${this.gridSelector} tr[data-rk]`); }

    async waitForLoad(): Promise<void> {
        await this.page.waitForLoadState('networkidle');
    }

    async getRowCount(): Promise<number> {
        return await this.rows.count();
    }

    async findRowByText(text: string): Promise<Locator> {
        return this.rows.filter({ hasText: text }).first();
    }

    async rowExists(text: string): Promise<boolean> {
        return await this.rows.filter({ hasText: text }).count() > 0;
    }
}
```
