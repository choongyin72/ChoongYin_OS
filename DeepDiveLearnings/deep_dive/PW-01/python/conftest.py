"""
pytest conftest.py — Playwright Python configuration for EC Web App
Configures browser context with ignoreHTTPSErrors for EC self-signed cert
"""

import pytest


@pytest.fixture(scope='session')
def browser_context_args(browser_context_args):
    """Session-scoped: add ignoreHTTPSErrors and set viewport for all tests."""
    return {
        **browser_context_args,
        'ignore_https_errors': True,
        'viewport': {'width': 1920, 'height': 1080},
    }


@pytest.fixture(scope='session')
def browser_type_launch_args(browser_type_launch_args):
    """Session-scoped: launch args for browser (headless controlled by env var)."""
    import os
    return {
        **browser_type_launch_args,
        'headless': os.getenv('HEADLESS', 'false').lower() == 'true',
        'args': ['--start-maximized'],
    }
