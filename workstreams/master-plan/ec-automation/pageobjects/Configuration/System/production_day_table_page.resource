*** Settings ***
Documentation       T3 (screen) — Production Day Table page object.
...                 Screen: Configuration > System > Production Day Table (BF CO.1033).
...                 TV-style inline-editable grid (`production_day:form:T_data`), no navigator.
...                 INSERT ONLY — Update and Delete are permanently out of scope for this screen
...                 (owner-confirmed live 2026-08-03: "no deletion is allow in Production Day
...                 Table screen. such feature been disabled." End Date is a plain data field
...                 here, NOT a delete trigger, unlike other date-effective object screens).
...
...                 SELF-CLEAN IS IMPOSSIBLE BY DESIGN: every Insert (including every future live
...                 run of this suite) permanently accumulates an AUTOTEST_PDT_* row with no way
...                 to remove it via the UI. Owner decision 2026-08-03: accept this as a permanent,
...                 disclosed exception (same precedent as Royalty Contract's residual). Run this
...                 suite SPARINGLY, not as part of routine regression sweeps.
...
...                 DB commit visibility on this screen is measured ~8s slower than every other
...                 screen built so far - the `Wait For Elements State`/sleep after Save is
...                 deliberately generous (10s) to avoid a false-negative DB assert.

Library             Browser
Library             ../../../libraries/DbVerify.py
Resource            ../../../resources/common.resource
Resource            ../../../resources/table.resource
Resource            ../../../resources/toolbar.resource


*** Variables ***
${PDT_SCREEN}       Production Day Table
${PDT_TABLE}        production_day:form:T_data


*** Keywords ***
Open Production Day Table Screen
    [Documentation]    Suite Setup: launch, login, navigate to the Production Day Table screen.
    ...    No navigator on this screen — the grid loads immediately on open.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${PDT_SCREEN}    ${user}    ${pass}

Open Production Day Table Insert Menu
    [Documentation]    Insert toolbar (icon's OWN <li>) -> the menu item "Production Days"
    ...    (already correctly title-cased on this screen, unlike Constant Standard's CSS
    ...    uppercase illusion) -> a blank row appears.
    Hover    xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]
    Wait For Elements State
    ...    xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]//ul[contains(@class,'ui-menu-child')]//a[normalize-space(.)='Production Days']
    ...    visible    timeout=10s
    Click
    ...    xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]//ul[contains(@class,'ui-menu-child')]//a[normalize-space(.)='Production Days']
    Wait For Load State    networkidle    timeout=12s
    Sleep    1.5s

Find Production Day Table Row By Code
    [Documentation]    Return the 0-based row index whose Object Code cell (C0_in) equals
    ...    ${code}, or -1 if not found. ${code}=${EMPTY} finds the first BLANK row (after Insert).
    [Arguments]    ${code}
    ${row}=    Evaluate JavaScript    ${None}
    ...    () => { const want = '${code}'; const m = document.querySelectorAll('input[id^="production_day:form:T:"][id$=":C0_in"]'); for (const e of m) { if ((e.value||'') === want) { return parseInt(e.id.split(':')[3]); } } return -1; }
    RETURN    ${row}

Insert Production Day Table Record
    [Documentation]    Insert: Code (C0) + Time Zone first-available (C1 dropdown) + Start
    ...    Date (C2) + Name (C4) -> Save. Uses Type Cell By Id (real keystrokes + Tab) for
    ...    every text/date cell — a plain fill()/synthetic set silently breaks the NEXT
    ...    cell's autocomplete dropdown panel from ever rendering (confirmed reproducible).
    [Arguments]    ${code}    ${name}    ${start_date}
    Open Production Day Table Insert Menu
    ${row}=    Find Production Day Table Row By Code    ${EMPTY}
    Should Be True    ${row} >= 0    msg=No blank row after Insert
    Type Cell By Id    production_day:form:T:${row}:C0_in    ${code}
    Select First EC Dropdown Option    production_day:form:T:${row}:C1_dd
    Type Cell By Id    production_day:form:T:${row}:C2_da_input    ${start_date}
    Type Cell By Id    production_day:form:T:${row}:C4_in    ${name}
    Save
    Sleep    10s

Production Day Table Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_PRODUCTION_DAY.
    ...    (Commit visibility on this screen is measured ~8s slower than other screens —
    ...    the 10s Sleep in the Insert keyword above covers this before any assert runs.)
    [Arguments]    ${code}
    Code Should Be Present In View    OV_PRODUCTION_DAY    ${code}
