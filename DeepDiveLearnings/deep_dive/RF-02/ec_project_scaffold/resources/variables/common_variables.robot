*** Settings ***
Documentation    Common variables shared across all EC test suites.
...              Environment-specific values loaded via --variablefile vars/{env}.py

*** Variables ***
# ── EC Application ──────────────────────────────────────────────────────────
# Loaded from vars/*.py via --variablefile — these are DEFAULTS only
${EC_URL}           https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/
${EC_USERNAME}      sysadmin
${EC_PASSWORD}      Sysadmin
${BROWSER}          chromium
${HEADLESS}         False
${WAIT_TIMEOUT}     30s

# ── Database ─────────────────────────────────────────────────────────────────
${DB_URL}           localhost:1521/ORCL
${DB_USER}          ECKERNEL_EC
${DB_PASS}          energy

# ── Selectors shared across all screens ──────────────────────────────────────
${SEARCH_INPUT}     xpath=//input[@id='menu:searchForm:searchTxt']
${SCREEN_TOGGLE}    id=screenToolbar:form:minmaxMenu

# ── Timeouts ──────────────────────────────────────────────────────────────────
${LOGIN_TIMEOUT}    60s
${AJAX_TIMEOUT}     30s
${PAGE_TIMEOUT}     60s
