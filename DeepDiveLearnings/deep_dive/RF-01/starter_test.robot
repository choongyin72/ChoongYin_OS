*** Settings ***
Documentation    EC Web App — Robot Framework Starter Test
...              Demonstrates all four sections, Browser Library,
...              EC conventions, custom keywords, screenshot-on-failure
...              Target: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/
Library          Browser
Library          OperatingSystem
Library          Collections
Library          Process
Library          String
Variables        vars/local.py

Suite Setup      Open EC Application    ${EC_URL}    ${HEADLESS}
Suite Teardown   Close Browser
Test Teardown    Run Keyword If Test Failed
...              Take Screenshot    ${OUTPUT_DIR}${/}${SUITE_NAME}_${TEST_NAME}_failure

*** Variables ***
# Loaded from vars/local.py — shown here for clarity
# ${EC_URL}         https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/
# ${EC_USERNAME}    sysadmin
# ${EC_PASSWORD}    Sysadmin
# ${WAIT_TIMEOUT}   30s
# ${HEADLESS}       False

${SCREEN_CHECK_RULE}         Check Rule
${SCREEN_VALIDATION}         Validation Overview
${SEARCH_INPUT}    xpath=//input[@id='menu:searchForm:searchTxt']

*** Test Cases ***

# ──────────────────────────────────────────────────────────────────────────────
# TC01 — Login
# ──────────────────────────────────────────────────────────────────────────────
TC01 Login To EC Web App
    [Documentation]    Verify Keycloak login succeeds and EC dashboard loads
    [Tags]    smoke    login    critical
    Log In To EC    ${EC_USERNAME}    ${EC_PASSWORD}
    Verify EC Dashboard Loaded

# ──────────────────────────────────────────────────────────────────────────────
# TC02 — Navigate to Check Rule screen
# ──────────────────────────────────────────────────────────────────────────────
TC02 Navigate To Check Rule Screen
    [Documentation]    Search sidebar and open Check Rule screen
    [Tags]    smoke    navigation    check_rule
    Search And Open Screen    ${SCREEN_CHECK_RULE}
    Verify Screen Loaded    ${SCREEN_CHECK_RULE}

# ──────────────────────────────────────────────────────────────────────────────
# TC03 — Navigate to Validation Overview
# ──────────────────────────────────────────────────────────────────────────────
TC03 Navigate To Validation Overview
    [Documentation]    Open CO.0203 Validation Overview screen
    [Tags]    smoke    navigation    validation
    Search And Open Screen    ${SCREEN_VALIDATION}
    Verify Screen Loaded    ${SCREEN_VALIDATION}
    Take Screenshot    filename=TC03_validation_overview.png

*** Keywords ***

Open EC Application
    [Documentation]    Launch Chromium and navigate to EC URL with ignoreHTTPSErrors.
    ...                Headless mode controlled by ${HEADLESS} variable.
    [Arguments]    ${url}    ${headless}=False
    IF    '${headless}' == 'True'
        New Browser      chromium    headless=True
        New Context      ignoreHTTPSErrors=True    viewport={"width": 1920, "height": 1080}
    ELSE
        ${args}=    Create List    --start-maximized
        New Browser      chromium    headless=False    args=${args}
        New Context      ignoreHTTPSErrors=True    viewport=${None}
    END
    New Page    ${url}
    Log    Opened EC Application: ${url}

Log In To EC
    [Documentation]    Fill Keycloak login form and wait for EC dashboard.
    ...                Pre-condition: Browser must be open on EC URL.
    ...                Post-condition: User is logged in, EC dashboard loaded.
    [Arguments]    ${username}    ${password}
    Wait For Load State    domcontentloaded    timeout=30s
    Wait For Elements State    id=username    visible    timeout=15s
    Fill Text    id=username    ${username}
    Fill Text    id=password    ${password}
    Click        id=kc-login
    Wait For Load State    networkidle    timeout=60s
    Log    Logged in as ${username}

Verify EC Dashboard Loaded
    [Documentation]    Assert EC dashboard is loaded — URL not on Keycloak.
    ${url}=    Get Url
    Should Not Contain    ${url}    auth/realms    msg=Still on Keycloak login page
    Log    Dashboard loaded: ${url}

Search And Open Screen
    [Documentation]    Type screen name in sidebar search and click the result link.
    ...                Uses Type Text (not Fill) — PrimeFaces triggers AJAX on keyup.
    ...                Pre-condition: EC is logged in, sidebar visible.
    [Arguments]    ${screen_name}
    Wait For Elements State    ${SEARCH_INPUT}    visible    timeout=${WAIT_TIMEOUT}
    Click        ${SEARCH_INPUT}
    Clear Text   ${SEARCH_INPUT}
    # Type with delay — triggers PrimeFaces AJAX keyup listener
    Type Text    ${SEARCH_INPUT}    ${screen_name}    delay=50ms
    Wait For Load State    networkidle    timeout=15s
    # Click the matching treeview link
    ${link_xpath}=    Set Variable
    ...    xpath=//label[contains(@class,'tv-link') and normalize-space(.)='${screen_name}']
    Wait For Elements State    ${link_xpath}    visible    timeout=15s
    Click    ${link_xpath}
    Wait For Load State    networkidle    timeout=30s
    Log    Opened screen: ${screen_name}

Verify Screen Loaded
    [Documentation]    Verify the target screen name appears somewhere on the page.
    [Arguments]    ${screen_name}
    ${page_text}=    Get Text    xpath=//body
    Should Contain    ${page_text}    ${screen_name}
    ...    msg=Screen '${screen_name}' not found on page
