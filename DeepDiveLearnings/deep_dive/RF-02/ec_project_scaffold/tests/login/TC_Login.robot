*** Settings ***
Documentation    Login test suite — EC Web App Keycloak authentication
...              Tests: successful login, invalid credentials, session persistence
...              Environment: configured via --variablefile vars/{env}.py
Library          Browser
Resource         ../../resources/keywords/LoginKeywords.resource
Resource         ../../resources/variables/common_variables.robot
Variables        ../../vars/local.py

Suite Setup      Open EC Browser Session
Suite Teardown   Close Browser
Test Teardown    Run Keyword If Test Failed
...              Take Screenshot    ${OUTPUT_DIR}${/}${SUITE_NAME}_${TEST_NAME}_failure

*** Test Cases ***

TC_Login_01 Login Successfully With Valid Credentials
    [Documentation]    Verify sysadmin can login to EC Web App via Keycloak
    [Tags]    smoke    login    critical
    Log In To EC    ${EC_USERNAME}    ${EC_PASSWORD}
    Verify Dashboard Is Loaded

TC_Login_02 Login Fails With Invalid Password
    [Documentation]    Verify invalid credentials show error — not crash
    [Tags]    login    negative
    Log In To EC With Invalid Credentials
    ...    sysadmin    WRONG_PASSWORD    Invalid username or password

TC_Login_03 Session Persists After Navigation
    [Documentation]    After login, navigate to a screen — should not re-redirect to Keycloak
    [Tags]    login    smoke
    Log In To EC    ${EC_USERNAME}    ${EC_PASSWORD}
    Wait For Elements State
    ...    xpath=//input[@id='menu:searchForm:searchTxt']    visible    timeout=30s
    ${url}=    Get Url
    Should Not Contain    ${url}    auth/realms

*** Keywords ***

Open EC Browser Session
    [Documentation]    Launch browser with EC-specific settings.
    IF    '${HEADLESS}' == 'True'
        New Browser    chromium    headless=True
        New Context    ignoreHTTPSErrors=True    viewport={"width": 1920, "height": 1080}
    ELSE
        ${args}=    Create List    --start-maximized
        New Browser    chromium    headless=False    args=${args}
        New Context    ignoreHTTPSErrors=True    viewport=${None}
    END
