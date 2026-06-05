*** Settings ***
Documentation    Layer 2 (Keywords) — Business-level login operations.
...              Calls page layer only — no direct locators here.
Resource         ../pages/LoginPage.resource
Resource         ../variables/common_variables.robot

*** Keywords ***

Log In To EC
    [Documentation]    Open EC, fill credentials, submit, verify success.
    ...                Pre-condition: browser context open.
    ...                Post-condition: EC dashboard loaded, session active.
    [Arguments]    ${username}=${EC_USERNAME}    ${password}=${EC_PASSWORD}
    Navigate To Login Page
    Fill Login Credentials    ${username}    ${password}
    Submit Login Form
    Verify Login Successful

Log In To EC With Invalid Credentials
    [Documentation]    Attempt login with wrong credentials — expect error.
    [Arguments]    ${username}    ${password}    ${expected_error}=Invalid username or password
    Navigate To Login Page
    Fill Login Credentials    ${username}    ${password}
    Submit Login Form
    Verify Login Error Message    ${expected_error}

Verify Dashboard Is Loaded
    [Documentation]    Assert EC dashboard is fully loaded after login.
    Verify Login Successful

Log Out From EC
    [Documentation]    Log out from EC (if logout URL or menu exists).
    ...                Note: EC may handle logout via Keycloak session expiry.
    Go To    ${EC_URL}/logout
    Wait For Load State    networkidle    timeout=30s
