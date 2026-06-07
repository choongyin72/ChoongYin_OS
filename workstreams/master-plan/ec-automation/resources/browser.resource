*** Settings ***
Documentation       T1 area — Browser session lifecycle: open, login, close.

Library             Browser
Variables           environment.py


*** Keywords ***
Open EC Browser
    [Documentation]    Launch Chromium + context (headless from environment).
    New Browser    chromium    headless=${HEADLESS}
    New Context    ignoreHTTPSErrors=${TRUE}    viewport={'width': 1920, 'height': 1080}
    Set Browser Timeout    30s
    Set Strict Mode    False

Login To EC
    [Documentation]    Open the app and authenticate as ${user} (defaults to the
    ...    env-configured user); wait for the sidebar search box.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    New Page    ${EC_URL}
    Fill Text    css=[id="username"]    ${user}
    Fill Text    css=[id="password"]    ${pass}
    Click    css=[id="kc-login"]
    Wait For Elements State    css=[id="menu:searchForm:searchTxt"]    visible    timeout=60s
    Wait For Load State    networkidle    timeout=30s

Close EC
    [Documentation]    Optional hold then close the browser (Suite Teardown).
    Sleep    ${HOLD}
    Close Browser
