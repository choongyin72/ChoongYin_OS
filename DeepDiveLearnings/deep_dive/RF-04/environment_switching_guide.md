# Environment Switching Guide — Robot Framework

## Variable File Hierarchy
Command-line `--variable` > `--variablefile` file > suite `Variables` section default

## Three EC Environments

### Local (default for development)
```bash
robot --variablefile vars/local.py tests/
```
```python
# vars/local.py
EC_URL = 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/'
EC_USERNAME = 'sysadmin'
EC_PASSWORD = 'Sysadmin'
DB_URL = 'localhost:1521/ORCL'
DB_USER = 'ECKERNEL_EC'
DB_PASS = 'energy'
HEADLESS = False
WAIT_TIMEOUT = '30s'
```

### Test / COPS DEV (Woodside Pluto)
```bash
robot --variablefile vars/test.py tests/
```
```python
# vars/test.py
EC_URL = 'https://app-plutodev.woodside-pluto.tieto-og.cloud/'
EC_USERNAME = 'sysadmin'
EC_PASSWORD = 'Sysadmin@01'
DB_URL = 'db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev'
DB_USER = 'ECKERNEL_EC'
DB_PASS = 'energy'
HEADLESS = True
WAIT_TIMEOUT = '45s'
```

### Production (read-only tests only)
```bash
robot --variablefile vars/prod.py --include readonly tests/
```
```python
# vars/prod.py — NEVER store prod passwords here
EC_URL = 'https://app-pluto.woodside-pluto.tieto-og.cloud/'
EC_PASSWORD = os.environ.get('EC_PROD_PASSWORD')  # from vault/env
HEADLESS = True
WAIT_TIMEOUT = '60s'
```

## CI Override via --variable Flag
```bash
# Override individual variables at runtime (highest priority)
robot --variablefile vars/test.py \
      --variable EC_USERNAME:ci_user \
      --variable EC_PASSWORD:%CI_PASSWORD% \
      tests/
```

## Switching Browsers
```bash
robot --variablefile vars/local.py --variable BROWSER:firefox tests/
```
