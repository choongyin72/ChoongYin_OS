*** Settings ***
Documentation       T1 (universal) aggregator — imports every shared EC keyword area
...                 so a suite can import this one file for everything, or cherry-pick
...                 an individual area file (browser / screen / toolbar / table / utils).
...                 Also home of cross-area helpers (e.g. Launch EC And Open Screen,
...                 which spans browser + screen areas).

Resource            browser.resource
Resource            screen.resource
Resource            navigator.resource
Resource            toolbar.resource
Resource            table.resource
Resource            utils.resource
Variables           environment.py


*** Keywords ***
Login To EC Screen
    [Documentation]    Authenticate on the CURRENT page with ${user}/${pass}, then capture the
    ...    login evidence screenshot. Shared body for every screen's own zero-arg "Login To EC
    ...    Application" wrapper (bank_page.resource, object_list_page.resource, etc.) - each of
    ...    those only supplies its own screen-specific credential defaults and delegates the
    ...    actual mechanics here, since Bank's and Object List's wrappers were found to have
    ...    identical bodies (owner query 2026-08-21) differing only in which credential constants
    ...    were passed. Lives in common.resource (not browser.resource alone), which aggregates
    ...    utils.resource - browser.resource deliberately has no Capture Step dependency.
    [Arguments]    ${user}    ${pass}
    Fill EC Login Form    ${user}    ${pass}
    Capture Step    ${TEST NAME}_login

Open EC Screen
    [Documentation]    Navigate to ${screen_name} and capture the open-screen evidence
    ...    screenshot. Shared body for every screen's own zero-arg "Open <Screen> Screen"
    ...    wrapper (bank_page.resource's Open Bank Screen, object_list_page.resource's Open
    ...    Object List Screen, etc.) - each of those only supplies its own screen-name
    ...    constant and delegates the actual navigation here, since Bank's and Object List's
    ...    wrappers were found to have identical bodies (owner query 2026-08-21) differing
    ...    only in which screen-name constant was passed. Assumes the caller already logged
    ...    in this test case - this keyword ONLY navigates.
    [Arguments]    ${screen_name}
    Navigate To Screen    ${screen_name}
    Capture Step    ${TEST NAME}_open_screen

Launch EC And Open Screen
    [Documentation]    The standard Suite Setup gesture: launch the browser, login as
    ...    ${user} (defaults to the env-configured user), navigate to ${screen_name}.
    ...    Page objects delegate their Open <X> Screen keyword here in one line.
    [Arguments]    ${screen_name}    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Open EC Browser
    Login To EC    ${user}    ${pass}
    Navigate To Screen    ${screen_name}
