"""
EC Variable File — Local Environment
Usage: robot --variablefile vars/local.py tests/

All EC project tests MUST use these variables.
NEVER hardcode URLs, credentials, or environment values in .robot files.
"""

# EC Web App (Local)
EC_URL = 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/'
EC_USERNAME = 'sysadmin'
EC_PASSWORD = 'Sysadmin'

# EC Database (Local)
DB_URL = 'localhost:1521/ORCL'
DB_USER = 'ECKERNEL_EC'
DB_PASS = 'energy'

# Browser settings
BROWSER = 'chromium'
HEADLESS = False

# Timeouts
WAIT_TIMEOUT = '30s'
NAVIGATION_TIMEOUT = '60s'

# Screenshot settings
SCREENSHOT_DIR = 'results/screenshots'
