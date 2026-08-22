"""EC login credentials - Robot Framework variable file, kept separate from environment.py
(owner request, 2026-08-17): a screen can retrieve its login credentials from here instead of the
general environment config. Same env-var-with-safe-fallback pattern as environment.py - only the
throwaway local-sandbox value is ever committed, real secrets are always injected via OS
environment variables (CI/CD).

STANDING DECISION (owner, 2026-08-22): every EC screen gets its OWN dedicated <SCREEN>_EC_USER/
<SCREEN>_EC_PASS pair here - real EC deployments gate different screens behind different role
access, so a screen-specific login identity is the correct default going forward, not an
exception. This supersedes docs/rf-suite-styles.md point 6 (shared environment.py default,
override only via an explicit Login argument) - that doc is being updated to match. Kept as ONE
shared file (not one file per screen, which would sprawl to 100+ tiny files as more screens are
built) - the per-screen distinction lives in the VARIABLE NAME, not the file.

Override precedence (highest first), same shape for every screen's pair:
  1. <SCREEN>_EC_USER / <SCREEN>_EC_PASS OS environment variable (screen-specific override)
  2. EC_USER / EC_PASS OS environment variable (shared fallback, same as environment.py)
  3. default below (local sandbox)

Future direction (owner-stated, 2026-08-17): migrate this file to a real secrets store
(vault/keyring/CI secret manager) once the RF EC suite is otherwise complete. This file is the
interim step - only its internals change when that happens, no consuming .resource file does.
"""
import os

BANK_EC_USER = os.environ.get("BANK_EC_USER", os.environ.get("EC_USER", "sysadmin"))
BANK_EC_PASS = os.environ.get("BANK_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

OBJECT_LIST_EC_USER = os.environ.get("OBJECT_LIST_EC_USER", os.environ.get("EC_USER", "sysadmin"))
OBJECT_LIST_EC_PASS = os.environ.get("OBJECT_LIST_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

STATE_EC_USER = os.environ.get("STATE_EC_USER", os.environ.get("EC_USER", "sysadmin"))
STATE_EC_PASS = os.environ.get("STATE_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

REGION_EC_USER = os.environ.get("REGION_EC_USER", os.environ.get("EC_USER", "sysadmin"))
REGION_EC_PASS = os.environ.get("REGION_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

FUNCTIONAL_AREA_EC_USER = os.environ.get("FUNCTIONAL_AREA_EC_USER", os.environ.get("EC_USER", "sysadmin"))
FUNCTIONAL_AREA_EC_PASS = os.environ.get("FUNCTIONAL_AREA_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

BUSINESS_UNIT_EC_USER = os.environ.get("BUSINESS_UNIT_EC_USER", os.environ.get("EC_USER", "sysadmin"))
BUSINESS_UNIT_EC_PASS = os.environ.get("BUSINESS_UNIT_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

PRODUCTION_UNIT_EC_USER = os.environ.get("PRODUCTION_UNIT_EC_USER", os.environ.get("EC_USER", "sysadmin"))
PRODUCTION_UNIT_EC_PASS = os.environ.get("PRODUCTION_UNIT_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
