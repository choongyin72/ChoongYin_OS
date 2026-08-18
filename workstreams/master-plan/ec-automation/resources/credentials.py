"""EC login credentials - Robot Framework variable file, kept separate from environment.py
(owner request, 2026-08-17): a screen can retrieve its login credentials from here instead of the
general environment config. Same env-var-with-safe-fallback pattern as environment.py - only the
throwaway local-sandbox value is ever committed, real secrets are always injected via OS
environment variables (CI/CD).

Override precedence (highest first):
  1. BANK_EC_USER / BANK_EC_PASS OS environment variable (screen-specific override)
  2. EC_USER / EC_PASS OS environment variable (shared fallback, same as environment.py)
  3. default below (local sandbox)

Future direction (owner-stated, 2026-08-17): migrate this file to a real secrets store
(vault/keyring/CI secret manager) once the RF EC suite is otherwise complete. This file is the
interim step - only its internals change when that happens, no consuming .resource file does.
"""
import os

BANK_EC_USER = os.environ.get("BANK_EC_USER", os.environ.get("EC_USER", "sysadmin"))
BANK_EC_PASS = os.environ.get("BANK_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
