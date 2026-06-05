*** Settings ***
Documentation    Layer 3 (Pages) — Login screen interactions.
...              All selectors come from variables/login_variables.robot.
...              Calls Browser Library directly.
Library          Browser
Resource         ../variables/common_variables.robot
Resource         ../variables/login_variables.robot

*** Keywords ***

Navigate To Login Page
    [Documentation]    Open EC URL — redirects to Keycloak login.
    New Page    ${EC_URL}
    Wait For Load State    domcontentloaded    timeout=30s

Fill Login Credentials
    [Documentation]    Type username and password into Keycloak form.
    [Arguments]    ${username}    ${password}
    Wait For Elements State    ${LOGIN_USERNAME_INPUT}    visible    timeout=15s
    Fill Text    ${LOGIN_USERNAME_INPUT}    ${username}
    Fill Text    ${LOGIN_PASSWORD_INPUT}    ${password}

Submit Login Form
    [Documentation]    Click Keycloak submit button and wait for EC dashboard.
    Click    ${LOGIN_SUBMIT_BTN}
    Wait For Load State    networkidle    timeout=${LOGIN_TIMEOUT}

Verify Login Successful
    [Documentation]    Assert URL is not Keycloak — EC dashboard loaded.
    ${url}=    Get Url
    Should Not Contain    ${url}    auth/realms
    ...    msg=Login failed — still on Keycloak page: ${url}

Verify Login Error Message
    [Documentation]    Assert error message is visible with expected text.
    [Arguments]    ${expected_text}
    Wait For Elements State    ${LOGIN_ERROR_MSG}    visible    timeout=10s
    ${msg}=    Get Text    ${LOGIN_ERROR_MSG}
    Should Contain    ${msg}    ${expected_text}
