"""
EC Web App — Playwright Starter Test (Python / pytest-playwright)
Target: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/
Auth: sysadmin / Sysadmin (Keycloak)

Install:
    pip install pytest pytest-playwright
    playwright install chromium

Run:
    pytest deep_dive/PW-01/python/starter_test.py -v

Differences from TypeScript version:
- Synchronous API (no async/await)
- pytest fixtures instead of test.describe
- expect() from playwright.sync_api
- conftest.py handles browser context setup
"""

import os
import pytest
from playwright.sync_api import Page, expect

EC_URL = os.getenv('EC_URL', 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
EC_USER = os.getenv('EC_USERNAME', 'sysadmin')
EC_PASS = os.getenv('EC_PASSWORD', 'Sysadmin')


# ── Shared login helper ───────────────────────────────────────────────────────

def login_to_ec(page: Page) -> None:
    """Navigate to EC and log in via Keycloak form."""
    page.goto(EC_URL, wait_until='domcontentloaded')
    page.locator('#username').fill(EC_USER)
    page.locator('#password').fill(EC_PASS)
    page.locator('#kc-login').click()
    page.wait_for_load_state('networkidle', timeout=60_000)


# ── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture(scope='session')
def browser_context_args(browser_context_args):
    """Override browser context — add ignoreHTTPSErrors for self-signed EC cert."""
    return {
        **browser_context_args,
        'ignore_https_errors': True,
        'viewport': {'width': 1920, 'height': 1080},
    }


# ── Tests ─────────────────────────────────────────────────────────────────────

class TestECSmoke:

    def test_login_successfully(self, page: Page) -> None:
        """TC01 - Login to EC Web App via Keycloak."""
        page.goto(EC_URL, wait_until='domcontentloaded')

        # Assertion 1: Login form visible
        expect(page.locator('#username')).to_be_visible()
        expect(page.locator('#password')).to_be_visible()

        page.locator('#username').fill(EC_USER)
        page.locator('#password').fill(EC_PASS)
        page.locator('#kc-login').click()
        page.wait_for_load_state('networkidle', timeout=60_000)

        # Assertion 2: No longer on Keycloak login page
        assert '/auth/realms' not in page.url, f"Still on login page: {page.url}"

    def test_navigate_to_check_rule_screen(self, page: Page) -> None:
        """TC02 - Navigate to Check Rule screen via sidebar search."""
        login_to_ec(page)

        # XPath selector for PrimeFaces sidebar search
        search_input = page.locator('xpath=//input[@id="menu:searchForm:searchTxt"]')
        expect(search_input).to_be_visible(timeout=30_000)

        search_input.click()
        search_input.clear()
        # type() with delay — triggers PrimeFaces AJAX keyup
        search_input.type('Check Rule', delay=50)
        page.wait_for_load_state('networkidle', timeout=15_000)

        # XPath with text for treeview link
        menu_link = page.locator(
            'xpath=//label[contains(@class,"tv-link") and normalize-space(.)="Check Rule"]'
        )
        expect(menu_link).to_be_visible(timeout=15_000)
        expect(menu_link).to_contain_text('Check Rule')

        menu_link.click()
        page.wait_for_load_state('networkidle', timeout=30_000)

    def test_validation_overview_loads(self, page: Page) -> None:
        """TC03 - Navigate to Validation Overview and take screenshot."""
        login_to_ec(page)

        search_input = page.locator('xpath=//input[@id="menu:searchForm:searchTxt"]')
        expect(search_input).to_be_visible(timeout=30_000)
        search_input.click()
        search_input.clear()
        search_input.type('Validation Overview', delay=50)
        page.wait_for_load_state('networkidle', timeout=15_000)

        menu_link = page.locator(
            'xpath=//label[contains(@class,"tv-link") and normalize-space(.)="Validation Overview"]'
        )
        expect(menu_link).to_be_visible(timeout=15_000)
        menu_link.click()
        page.wait_for_load_state('networkidle', timeout=30_000)

        # Screenshot evidence
        page.screenshot(path='results/TC03_validation_overview_python.png')
