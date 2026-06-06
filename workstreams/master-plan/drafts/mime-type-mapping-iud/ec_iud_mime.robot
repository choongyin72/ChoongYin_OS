*** Settings ***
Documentation    EC IUD Test — MIME Type Mapping (Configuration > System)
...
...    Screen type: TABLE class (TV view) — inline-editable paginated grid, NO navigator.
...    Backing: TV_CTRL_MIME_TYPE_MAPPING over base table CTRL_MIME_TYPE_MAPPING.
...    Contrast to Bank/Equipment (OV object class): DELETE here is a PHYSICAL row removal
...    (table classes are not date-effective — no End=Start).
...
...    Cell commit gotcha: each cell input fires onchange -> PrimeFaces.ab partial submit.
...    Must Type Text + press Tab (real blur) so the value stages server-side before Save,
...    then RELOAD (Refresh) before verifying so the grid reflects the DB (not stale client state).
...    Grid is paginated (~20/page) -> find rows by paging.
...
...    NEVER touch existing rows. Test row only. Author: Choong-Yin Lee / Claude Opus 4.8 | 2026-06-07
...    Requires: robotframework-browser (rfbrowser init)

Library           Browser
Library           Collections
Suite Setup       Open EC And Open MIME
Suite Teardown    Run Keywords    Sleep    ${HOLD}    AND    Close Browser

*** Variables ***
${EC_URL}        https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/
${EC_USER}       sysadmin
${EC_PASS}       sysadmin
${TEST_MIME}     application/x-ec-autotest-rf
${EXT_INS}       .ectest
${EXT_UPD}       .ectest,.ectest2
${HEADLESS}      ${TRUE}
${SLOWMO}        ${0}
${HOLD}          0s

*** Test Cases ***

TC01 Verify Clean State
    [Documentation]    Confirm the test MIME row is not already present (search across pages)
    [Tags]    iud    mime    clean
    ${row}=    EC Find Row    ${TEST_MIME}
    Should Be Equal As Integers    ${row}    -1    msg=${TEST_MIME} already exists
    Take Screenshot    filename=${OUTPUT_DIR}/rfmime_tc01_clean

TC02 Insert MIME Mapping
    [Documentation]    Insert toolbar -> new blank row -> type cells (Tab-commit) -> Save -> reload -> verify
    [Tags]    iud    mime    insert
    EC Insert New Row
    ${blank}=    EC Find Blank Row
    Should Be True    ${blank} >= 0    msg=No blank row after Insert
    EC Type Cell    ${blank}    0    ${TEST_MIME}
    EC Type Cell    ${blank}    1    ${EXT_INS}
    Take Screenshot    filename=${OUTPUT_DIR}/rfmime_tc02a_filled
    EC Save
    EC Reload
    ${row}=    EC Find Row    ${TEST_MIME}
    Should Be True    ${row} >= 0    msg=INSERT FAILED: ${TEST_MIME} not persisted
    Take Screenshot    filename=${OUTPUT_DIR}/rfmime_tc02b_verified
    Log    INSERT PASS: ${TEST_MIME}

TC03 Update File Extensions
    [Documentation]    Find row -> edit File Extensions cell -> Save -> reload -> verify
    [Tags]    iud    mime    update
    ${row}=    EC Find Row    ${TEST_MIME}
    Should Be True    ${row} >= 0
    EC Type Cell    ${row}    1    ${EXT_UPD}
    EC Save
    EC Reload
    ${row2}=    EC Find Row    ${TEST_MIME}
    Should Be True    ${row2} >= 0
    ${ext}=    EC Cell Value    ${row2}    1
    Should Be Equal    ${ext}    ${EXT_UPD}    msg=UPDATE FAILED: ext=${ext}
    Take Screenshot    filename=${OUTPUT_DIR}/rfmime_tc03_verified
    Log    UPDATE PASS

TC04 Delete MIME Mapping (physical)
    [Documentation]    Select row -> Delete -> Save -> reload -> verify physically gone
    [Tags]    iud    mime    delete    cleanup
    ${row}=    EC Find Row    ${TEST_MIME}
    Should Be True    ${row} >= 0
    Click    css=[id="mime_type_table:form:T:${row}:C0_in"]
    Sleep    0.4s
    ${active}=    EC Cell Value    ${row}    0
    Should Be Equal    ${active}    ${TEST_MIME}    msg=SAFETY: active row is not the test row
    EC Delete Selected
    EC Save
    EC Reload
    ${gone}=    EC Find Row    ${TEST_MIME}
    Should Be Equal As Integers    ${gone}    -1    msg=DELETE FAILED: still present
    Take Screenshot    filename=${OUTPUT_DIR}/rfmime_tc04_verified
    Log    DELETE PASS (physical removal)

*** Keywords ***

Open EC And Open MIME
    New Browser    chromium    headless=${HEADLESS}    slowMo=${SLOWMO}
    New Context    ignoreHTTPSErrors=${TRUE}    viewport={'width': 1680, 'height': 1050}
    Set Browser Timeout    30s
    Set Strict Mode    False
    New Page    ${EC_URL}
    Fill Text    css=[id="username"]    ${EC_USER}
    Fill Text    css=[id="password"]    ${EC_PASS}
    Click    css=[id="kc-login"]
    Wait For Elements State    css=[id="menu:searchForm:searchTxt"]    visible    timeout=60s
    Wait For Load State    networkidle    timeout=30s
    Type Text    css=[id="menu:searchForm:searchTxt"]    MIME Type Mapping    delay=50ms    clear=Yes
    Wait For Load State    networkidle    timeout=8s
    Sleep    0.5s
    Click    xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='MIME Type Mapping']
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.5s
    ${label}=    Get Text    css=[id="screenToolbar:form:screenLabel"]
    Should Contain    ${label}    MIME

EC Get Row Index On Page
    [Documentation]    Returns the T:N index of ${mime} on the CURRENT page, or -1
    [Arguments]    ${mime}
    ${idx}=    Evaluate JavaScript    ${None}    () => { let r=-1; document.querySelectorAll('input[id^="mime_type_table:form:T:"][id$=":C0_in"]').forEach(i=>{ if((i.value||'').trim()==='${mime}'){const m=i.id.match(/:T:(\\d+):C0_in/); if(m) r=parseInt(m[1]);}}); return r; }
    RETURN    ${idx}

EC Find Row
    [Documentation]    Search across paginator pages; return T:N index or -1
    [Arguments]    ${mime}
    # go to first page if possible
    ${nfirst}=    Get Element Count    css=.ui-paginator-first:not(.ui-state-disabled)
    IF    ${nfirst} > 0
        Click    css=.ui-paginator-first
        Wait For Load State    networkidle    timeout=10s
        Sleep    0.5s
    END
    FOR    ${p}    IN RANGE    12
        ${idx}=    EC Get Row Index On Page    ${mime}
        IF    ${idx} >= 0    RETURN    ${idx}
        ${nnext}=    Get Element Count    css=.ui-paginator-next:not(.ui-state-disabled)
        IF    ${nnext} == 0    RETURN    -1
        Click    css=.ui-paginator-next
        Wait For Load State    networkidle    timeout=10s
        Sleep    0.5s
    END
    RETURN    -1

EC Find Blank Row
    ${idx}=    EC Get Row Index On Page    ${EMPTY}
    RETURN    ${idx}

EC Cell Value
    [Arguments]    ${row}    ${col}
    ${v}=    Get Property    css=[id="mime_type_table:form:T:${row}:C${col}_in"]    value
    RETURN    ${v}

EC Type Cell
    [Documentation]    Real keystrokes + Tab so onchange PrimeFaces.ab stages the value
    [Arguments]    ${row}    ${col}    ${value}
    ${sel}=    Set Variable    css=[id="mime_type_table:form:T:${row}:C${col}_in"]
    Click    ${sel}
    Type Text    ${sel}    ${value}    clear=Yes
    Keyboard Key    press    Tab
    Wait For Load State    networkidle    timeout=12s
    Sleep    0.6s

EC Save
    Click    xpath=//a[@title='Save [Ctrl+s]']
    Wait For Load State    networkidle    timeout=15s
    Sleep    1s

EC Reload
    Click    xpath=//a[@title='Refresh [Ctrl+r]']
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.2s

EC Insert New Row
    Hover    xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]
    Sleep    1s
    Click    xpath=(//ul[contains(@class,'ui-menu-child')]//li//a)[1]
    Wait For Load State    networkidle    timeout=12s
    Sleep    1s

EC Delete Selected
    Hover    xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-delete')]]
    Sleep    1s
    # scope the submenu click to the DELETE menu-parent (the insert submenu has an identically named item)
    Click    xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-delete')]]//ul[contains(@class,'ui-menu-child')]//a[normalize-space(.)='MIME Type Mapping']
    Wait For Load State    networkidle    timeout=12s
    Sleep    1s
