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
Launch EC And Open Screen
    [Documentation]    The standard Suite Setup gesture: launch the browser, login as
    ...    ${user} (defaults to the env-configured user), navigate to ${screen_name}.
    ...    Page objects delegate their Open <X> Screen keyword here in one line.
    [Arguments]    ${screen_name}    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Open EC Browser
    Login To EC    ${user}    ${pass}
    Navigate To Screen    ${screen_name}
