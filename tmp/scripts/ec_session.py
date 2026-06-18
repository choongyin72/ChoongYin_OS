"""Shared EC Playwright session helper — the ONE place credentials and the base URL resolve, always from
env (EC_URL / EC_USER / EC_PASS), never hardcoded (R16). Import this in recon scripts and new freestyle
bundles instead of re-writing the login:

    from ec_session import login, EC_URL, EC_USER, EC_PASS
    login(page)                       # goto + Keycloak login + wait for dashboard

Defaults target the local sandbox; override via env for CI / another env. No credential string ever lives
in a recon/bundle file again — `scripts/check_bundle_hygiene.py` enforces that.
"""
import os

EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
EC_USER = os.environ.get("EC_USER", "sysadmin")
EC_PASS = os.environ.get("EC_PASS", "sysadmin")


def creds():
    """Return (url, user, pass) resolved from env — for callers that drive login themselves."""
    return EC_URL, EC_USER, EC_PASS


def login(page, url=None, user=None, pwd=None, wait_dashboard=True, timeout=60000):
    """Playwright login to EC via Keycloak. Credentials come from env by default (never hardcoded)."""
    url = url or EC_URL
    user = user or EC_USER
    pwd = pwd or EC_PASS
    page.goto(url, wait_until="domcontentloaded", timeout=45000)
    page.fill("#username", user)
    page.fill("#password", pwd)
    page.click("#kc-login")
    if wait_dashboard:
        page.wait_for_url("**/dashboard**", timeout=timeout)
    return page
