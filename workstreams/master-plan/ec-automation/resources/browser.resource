*** Settings ***
Documentation       T1 area — Browser session lifecycle: open, login, close.

Library             Browser
Variables           environment.py


*** Keywords ***
Open EC Browser
    [Documentation]    Launch Chromium + context (headless from environment).
    ...    Headed: OS-maximised window (--start-maximized, no fixed viewport) so the
    ...    page fills the screen. Headless: 1920x1080 virtual viewport as before.
    IF    ${HEADLESS}
        New Browser    chromium    headless=${TRUE}
        New Context    ignoreHTTPSErrors=${TRUE}    viewport={'width': 1920, 'height': 1080}
    ELSE
        VAR    @{args}    --start-maximized
        New Browser    chromium    headless=${FALSE}    args=${args}    slowMo=${SLOWMO}
        New Context    ignoreHTTPSErrors=${TRUE}    viewport=${None}
    END
    Set Browser Timeout    30s
    Set Strict Mode    False

Fill EC Login Form
    [Documentation]    The ACTUAL login mechanics (fill username, fill password, click login,
    ...    wait for the app to load) on the CURRENT page - the ONE place to update if EC's login
    ...    flow ever changes (a new SSO step, MFA, a renamed field id). Login To EC and Bank's own
    ...    Login To EC Application (bank_page.resource) both call this instead of duplicating the
    ...    steps, so a future flow change is a one-place edit (owner-requested 2026-08-18, after
    ...    Bank's wrapper was found to have copy-pasted this sequence instead of reusing it).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Fill Text    css=[id="username"]    ${user}
    Fill Text    css=[id="password"]    ${pass}
    Click    css=[id="kc-login"]
    Wait For Elements State    css=[id="menu:searchForm:searchTxt"]    visible    timeout=60s
    Wait For Load State    networkidle    timeout=30s

Login To EC
    [Documentation]    Open the app and authenticate as ${user} (defaults to the
    ...    env-configured user); wait for the sidebar search box.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    New Page    ${EC_URL}
    Fill EC Login Form    ${user}    ${pass}

Close EC
    [Documentation]    Optional hold then close the browser (Suite Teardown).
    Sleep    ${HOLD}
    Close Browser

# --- Per-test-case Login/Logout narrative (owner-requested 2026-08-18) --------------------------
# For a suite that wants EVERY test case to show its own real Login/Logout (not one shared
# Suite Setup/Teardown login): Open EC Application (browser + login PAGE only, done ONCE in Suite
# Setup - not a business action, so excluded from the friendly report the same way Capture Step
# is) sets up ONE already-open browser; each screen's own T3 page-resource file then defines its
# OWN "Login To EC Application" wrapper (its screen-specific credentials baked in as defaults, so
# the test case calls it with zero arguments - see bank_page.resource) around the generic
# Fill-username/password/click login steps. Logout From EC Application below IS generic/shared
# (a real logout has no screen-specific credentials to default) so it lives here in T1.

Open EC Application
    [Documentation]    Launch the browser and load the EC login page - no credentials entered yet.
    ...    Pure one-time environment setup (Suite Setup), NOT a business action. Each test case
    ...    then does its own Login To EC Application (screen-specific, see that screen's T3 page
    ...    resource) / Logout From EC Application cycle on this one already-open browser.
    Open EC Browser
    New Page    ${EC_URL}

Logout From EC Application
    [Documentation]    Click EC's real logout icon (top toolbar, next to the username) and confirm
    ...    it genuinely returns to the login page - not just closing the browser tab. Live-verified
    ...    2026-08-18 both from the landing page and from inside a loaded screen (e.g. Bank, after
    ...    Expand Screen To Full Page hides the treeview): clicking it triggers a PrimeFaces AJAX
    ...    logout and redirects to the Keycloak login page (#username field re-appears).
    Click    xpath=//span[contains(@class,'ui-icon-top-logout')]/ancestor::a[1]
    Wait For Elements State    css=[id="username"]    visible    timeout=15s
    Capture Step    ${TEST NAME}_logout

Ensure Logged Out From EC Application
    [Documentation]    Test Teardown safety net (owner discovered this gap live, 2026-08-18): if a
    ...    test case FAILS before reaching its own Logout From EC Application line, the browser is
    ...    left logged in - the NEXT test's Login To EC Application then times out trying to fill
    ...    #username on a page that isn't the login form, cascading ONE failure into failing every
    ...    remaining test. This always runs as [Teardown]/Test Teardown regardless of pass/fail:
    ...    no-ops if already at the login page (nothing to log out of), otherwise clicks the real
    ...    logout icon - guaranteeing every test case starts clean.
    ${already_at_login}=    Get Element Count    css=[id="username"]:visible
    IF    ${already_at_login} == 0
        ${logout_icon_present}=    Get Element Count    css=.ui-icon-top-logout
        IF    ${logout_icon_present} > 0
            Logout From EC Application
        END
    END
