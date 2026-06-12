"""EC environment / connection config — Robot Framework variable file.

These values are NOT fixed: the URL, credentials and DB DSN differ per
environment (dev/test/prod), and credentials are secrets. Each resolves from an
OS environment variable, falling back to the local-sandbox default so a plain
`robot` run works with zero setup.

Override precedence (highest first):
  1. robot --variable EC_URL:...        (per run)
  2. OS environment variable            (CI/CD, secrets)
  3. default below                      (local sandbox)

CI: inject EC_PASS (and others) as secret environment variables; do NOT commit
real secrets here — the fallback is only the throwaway sandbox value.
"""
import os

EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
EC_USER = os.environ.get("EC_USER", "sysadmin")
EC_PASS = os.environ.get("EC_PASS", "sysadmin")
DB_DSN = os.environ.get("EC_DB_DSN", "localhost:1521/ORCL")
HEADLESS = os.environ.get("EC_HEADLESS", "true").lower() in ("1", "true", "yes")
HOLD = os.environ.get("EC_HOLD", "0s")

# Test-data date conventions (centralized so a sandbox/data change is one edit, not 40):
# - TEST_START_DATE: default Start/End date for IUD test objects on plain screens.
# - TEST_START_DATE_REFDD: for screens whose form has REFERENCE DROPDOWNS — the date
#   must be on/after the seed objects' effective dates or the dropdowns come up empty
#   (see registry: "EC Object Start Date = Version Filter"). Keep >= 2003-01-01.
TEST_START_DATE = os.environ.get("EC_TEST_START_DATE", "2000-01-01")
TEST_START_DATE_REFDD = os.environ.get("EC_TEST_START_DATE_REFDD", "2003-01-01")
