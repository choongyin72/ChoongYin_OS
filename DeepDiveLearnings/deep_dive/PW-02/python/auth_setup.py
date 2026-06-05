"""
auth_setup.py — EC Auth State Setup (Python version)
Run once before test suite to save Keycloak session state.

Usage:
    python deep_dive/PW-02/python/auth_setup.py

Then in conftest.py:
    storage_state='auth-state.json'
"""

import os
from playwright.sync_api import sync_playwright

EC_URL = os.getenv('EC_URL', 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
EC_USERNAME = os.getenv('EC_USERNAME', 'sysadmin')
EC_PASSWORD = os.getenv('EC_PASSWORD', 'Sysadmin')


def setup_auth_state(output_path: str = 'auth-state.json') -> None:
    """Log in to EC and save session state for test reuse."""
    print(f'[auth_setup] Logging in to: {EC_URL}')

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            ignore_https_errors=True,
            viewport={'width': 1920, 'height': 1080},
        )
        page = context.new_page()

        page.goto(EC_URL, wait_until='domcontentloaded', timeout=30_000)

        # Fill Keycloak form
        page.locator('#username').wait_for(state='visible', timeout=15_000)
        page.locator('#username').fill(EC_USERNAME)
        page.locator('#password').fill(EC_PASSWORD)
        page.locator('#kc-login').click()
        page.wait_for_load_state('networkidle', timeout=60_000)

        if '/auth/realms' in page.url:
            raise RuntimeError(
                f'Login failed — still on Keycloak.\n'
                f'URL: {page.url}\n'
                f'Check: EC_USERNAME={EC_USERNAME}'
            )

        print(f'[auth_setup] Login successful. URL: {page.url}')
        context.storage_state(path=output_path)
        print(f'[auth_setup] Auth state saved to {output_path}')
        browser.close()


if __name__ == '__main__':
    setup_auth_state()
