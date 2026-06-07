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
    [Documentation]    Open the app and authenticate; wait for the sidebar search box.
    New Page    ${EC_URL}
    Fill Text    css=[id="username"]    ${EC_USER}
    Fill Text    css=[id="password"]    ${EC_PASS}
    Click    css=[id="kc-login"]
    Wait For Elements State    css=[id="menu:searchForm:searchTxt"]    visible    timeout=60s
    Wait For Load State    networkidle    timeout=30s

Close EC
    [Documentation]    Optional hold then close the browser (Suite Teardown).
    Sleep    ${HOLD}
    Close Browser
