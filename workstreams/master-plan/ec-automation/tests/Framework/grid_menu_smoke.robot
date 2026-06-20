*** Settings ***
Documentation       Live smoke test for the reusable grid column-menu keywords (resources/grid_menu.resource),
...                 exercised on the Business Function screen. READ-ONLY: filtering + reset personalisation
...                 are per-user VIEW operations - nothing is inserted/updated/deleted and nothing is Saved,
...                 so there is no DB data to verify or clean (the only state touched is this user's own grid
...                 personalisation, which the teardown resets). Proves: Turn Grid Filtering On, Filter Grid
...                 Text Column By Value (exact code + a "contains" name match), Clear Grid Text Column Filter,
...                 and Reset Grid Personalisation - against a live EC grid.

Resource            ../../resources/common.resource
Resource            ../../resources/grid_menu.resource

Suite Setup         Launch EC And Open Screen    Business Function
Suite Teardown      Reset And Close

Test Tags           grid-menu    read-only


*** Variables ***
${BF}               bf:form


*** Test Cases ***
TC01 Turn Filtering On Renders The Filter Row
    [Documentation]    Turning filtering on renders the per-column filter inputs.
    Turn Grid Filtering On    ${BF}
    ${on}=    Grid Filtering Is On    ${BF}
    Should Be True    ${on}    msg=Filter row not rendered after Turn Grid Filtering On

TC02 Filter By BF Code Narrows To One Row
    [Documentation]    BF Code (col 0) = CD.0021 -> exactly the Bank row (an exact full-code match).
    Filter Grid Text Column By Value    ${BF}    0    CD.0021
    ${n}=    Grid Data Row Count    ${BF}
    Should Be Equal As Integers    ${n}    1    msg=Expected 1 row for BF Code CD.0021, got ${n}

TC03 Filter By Name Does A Contains Match
    [Documentation]    Name (col 1) contains "Bank" -> several rows (Bank, Bank Account, Bank Usage, ...).
    Clear Grid Text Column Filter    ${BF}    0
    Filter Grid Text Column By Value    ${BF}    1    Bank
    ${n}=    Grid Data Row Count    ${BF}
    Should Be True    ${n} >= 2    msg=Expected a contains-match (>=2 rows) for Name "Bank", got ${n}

TC04 Reset Personalisation Clears Filtering
    [Documentation]    Reset personalisation returns the grid to defaults - the filter row is gone.
    Reset Grid Personalisation    ${BF}
    ${on}=    Grid Filtering Is On    ${BF}
    Should Be Equal    ${on}    ${FALSE}    msg=Filtering still on after Reset Grid Personalisation


*** Keywords ***
Reset And Close
    [Documentation]    Teardown: reset this grid's personalisation (leave the shared screen clean for the
    ...    next user/session), then close the browser. Best-effort - never fail the teardown.
    Run Keyword And Ignore Error    Reset Grid Personalisation    ${BF}
    Close EC
