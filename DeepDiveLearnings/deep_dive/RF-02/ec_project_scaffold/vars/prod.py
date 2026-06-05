"""Production environment — READ ONLY tests only"""
EC_URL = 'https://app-pluto.woodside-pluto.tieto-og.cloud/'
EC_USERNAME = 'sysadmin'
EC_PASSWORD = 'PROD_PASSWORD_FROM_VAULT'    # Never hardcode prod passwords
DB_URL = 'db.pluto.woodside-pluto.tieto-og.cloud:1521/pluto'
DB_USER = 'ECKERNEL_EC'
DB_PASS = 'PROD_DB_PASSWORD_FROM_VAULT'
BROWSER = 'chromium'
HEADLESS = True
WAIT_TIMEOUT = '60s'
