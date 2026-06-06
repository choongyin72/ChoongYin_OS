*** Settings ***
Documentation    EC IUD Test — Equipment (Configuration > Assets > Equipment Objects > Equipment)
...
...    Screen Type: Manage Object (EC14+) — screen 2 of 2 (confirms the Bank pattern).
...    KEY DIFFERENCE vs Bank: a 5-field CASCADING navigator must be set before the list loads.
...    Navigator (EXACT values): Production Unit | Offshore area | Offshore facility | Compressor -> Go
...    Each filter is a ui-autocomplete-dd dropdown: click the dd_button chevron, then click the
...    exact option in the dd_panel (typing fires re-render AJAX and is unreliable).
...
...    INSERT objectForm:       Code R:1, Name R:2, Start Date R:4 (Equipment Type R:0 auto=Compressor, read-only)
...    UPDATE updateAttributes: Name R:2
...    DELETE objectdates:      End Date R:0:C:3 = Start Date (zero-length window = true delete; DB-verified in OV_EQPM)
...    Result table: manageObject:form:T_data
...
...    NEVER touch existing data (OFF_* equipment). Test data: AUTOTEST_EQP_* (self-cleaning via true delete).
...    Author: Choong-Yin Lee / Claude Opus 4.8 | Date: 2026-06-06 | Requires: robotframework-browser (rfbrowser init)

Library           Browser
Library           Collections
Suite Setup       Open EC And Open Equipment
Suite Teardown    Run Keywords    Sleep    ${HOLD}    AND    Close Browser

*** Variables ***
${EC_URL}              https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/
${EC_USER}             sysadmin
${EC_PASS}             sysadmin
${TEST_CODE}           AUTOTEST_EQP_003
${TEST_NAME}           AUTOTEST Equipment 003
${TEST_NAME_UPD}       AUTOTEST Equipment 003 UPDATED
${START_DATE}          2000-01-01
${END_DATE}            2000-01-01    # = Start Date -> true delete
${HEADLESS}            ${TRUE}
${SLOWMO}              ${0}
${HOLD}                0s
${TABLE}               manageObject:form:T_data
# objectForm (insert)
${INS_CODE}            tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${INS_NAME}            tab:tabPanel:objectForm:form:G:0:R:2:C:1:in
${INS_DATE}            tab:tabPanel:objectForm:form:G:0:R:4:C:1:da_input
# updateAttributes (update)
${UPD_NAME}            tab:tabPanel:updateAttributes:form:G:0:R:2:C:1:in
# objectdates (delete)
${DEL_END}             tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input

*** Test Cases ***

TC01 Verify Clean State
    [Documentation]    Apply navigator filters, confirm 3 existing rows load and AUTOTEST not present
    [Tags]    iud    equipment    clean-state
    ${rows}=    EC Get Table Rows
    Log    Equipment rows: ${rows}
    Should Not Be Empty    ${rows}    msg=Navigator returned no rows — filter combo wrong
    ${exists}=    EC Row Exists    ${TEST_CODE}
    Should Be Equal    ${exists}    ${FALSE}    msg=${TEST_CODE} already exists — use a fresh code
    Take Screenshot    filename=${OUTPUT_DIR}/rfeq_tc01_clean

TC02 Insert New Equipment
    [Documentation]    Insert toolbar -> New Object -> fill Code/Name/Start Date -> Save
    [Tags]    iud    equipment    insert
    Hover    xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]
    Sleep    1s
    Click    xpath=//ul[contains(@class,'ui-menu-child')]//li//a[normalize-space(.)='New Object']
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.2s
    Take Screenshot    filename=${OUTPUT_DIR}/rfeq_tc02a_new_object
    EC Fill Field    ${INS_CODE}    ${TEST_CODE}
    EC Fill Field    ${INS_NAME}    ${TEST_NAME}
    EC Fill Date     ${INS_DATE}    ${START_DATE}
    ${etype}=    Get Property    css=[id="tab:tabPanel:objectForm:form:G:0:R:0:C:1:in"]    value
    Log    Equipment Type auto-set: ${etype}
    Take Screenshot    filename=${OUTPUT_DIR}/rfeq_tc02b_filled
    EC Save
    EC Go
    ${exists}=    EC Row Exists    ${TEST_CODE}
    Should Be True    ${exists}    msg=INSERT FAILED: ${TEST_CODE} not in table
    Take Screenshot    filename=${OUTPUT_DIR}/rfeq_tc02c_verified
    Log    INSERT PASS: ${TEST_CODE}

TC03 Update Equipment Name
    [Documentation]    Select row -> updateAttributes -> edit Name -> Save
    [Tags]    iud    equipment    update
    EC Select Row    ${TEST_CODE}
    EC Fill Field    ${UPD_NAME}    ${TEST_NAME_UPD}
    Take Screenshot    filename=${OUTPUT_DIR}/rfeq_tc03a_filled
    EC Save
    EC Go
    ${row}=    Get Text    xpath=//tbody[@id='manageObject:form:T_data']//tr[.//span[normalize-space(text())='${TEST_CODE}']]
    Should Contain    ${row}    ${TEST_NAME_UPD}    msg=UPDATE FAILED
    Take Screenshot    filename=${OUTPUT_DIR}/rfeq_tc03b_verified
    Log    UPDATE PASS: ${TEST_NAME_UPD}

TC04 Delete Equipment (End Date = Start Date)
    [Documentation]    Select row -> objectdates End Date = Start Date -> Save (true delete; - button disabled)
    [Tags]    iud    equipment    delete    cleanup
    EC Select Row    ${TEST_CODE}
    EC Fill Date    ${DEL_END}    ${END_DATE}
    Take Screenshot    filename=${OUTPUT_DIR}/rfeq_tc04a_enddate
    EC Save
    EC Go
    ${still}=    EC Row Exists    ${TEST_CODE}
    Should Be Equal    ${still}    ${FALSE}    msg=DELETE FAILED: ${TEST_CODE} still present
    Take Screenshot    filename=${OUTPUT_DIR}/rfeq_tc04b_verified
    Log    DELETE PASS: ${TEST_CODE} removed (EndDate=StartDate=${END_DATE})

*** Keywords ***

Open EC And Open Equipment
    New Browser    chromium    headless=${HEADLESS}    slowMo=${SLOWMO}
    New Context    ignoreHTTPSErrors=${TRUE}    viewport={'width': 1920, 'height': 1080}
    Set Browser Timeout    30s
    Set Strict Mode    False
    New Page    ${EC_URL}
    Fill Text    css=[id="username"]    ${EC_USER}
    Fill Text    css=[id="password"]    ${EC_PASS}
    Click    css=[id="kc-login"]
    Wait For Elements State    css=[id="menu:searchForm:searchTxt"]    visible    timeout=60s
    Wait For Load State    networkidle    timeout=30s
    Type Text    css=[id="menu:searchForm:searchTxt"]    Equipment    delay=60ms    clear=Yes
    Wait For Load State    networkidle    timeout=8s
    Sleep    0.5s
    Click    xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='Equipment']
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.5s
    ${label}=    Get Text    css=[id="screenToolbar:form:screenLabel"]
    Should Contain    ${label}    Equipment
    # apply cascading navigator (EXACT values)
    EC Set Nav    G:1    Production Unit
    EC Set Nav    G:2    Offshore area
    EC Set Nav    G:3    Offshore facility
    EC Set Nav    G:4    Compressor
    EC Go
    Take Screenshot    filename=${OUTPUT_DIR}/rfeq_tc00_filtered

EC Set Nav
    [Documentation]    Set a navigator autocomplete-dd: click chevron trigger, click exact option in panel
    [Arguments]    ${group}    ${value}
    Click    css=[id="nav:form:${group}:R:1:C:0:dd_button"]
    Sleep    1s
    Click    css=[id="nav:form:${group}:R:1:C:0:dd_panel"] >> text="${value}"
    Wait For Load State    networkidle    timeout=12s
    Sleep    0.9s

EC Fill Field
    [Arguments]    ${field_id}    ${value}
    Fill Text    css=[id="${field_id}"]    ${value}
    Evaluate JavaScript    ${None}    () => { const e=document.getElementById('${field_id}'); if(e){e.dispatchEvent(new Event('change',{bubbles:true}));e.dispatchEvent(new Event('blur',{bubbles:true}));} }
    Sleep    0.4s

EC Fill Date
    [Arguments]    ${field_id}    ${value}
    Fill Text    css=[id="${field_id}"]    ${value}
    Keyboard Key    press    Tab
    Sleep    0.6s
    Evaluate JavaScript    ${None}    () => { const e=document.getElementById('${field_id}'); if(e){e.dispatchEvent(new Event('change',{bubbles:true}));e.dispatchEvent(new Event('blur',{bubbles:true}));} }
    Sleep    0.4s

EC Save
    Click    xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.2s

EC Go
    Click    css=[id="button:form:B"]
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.2s

EC Select Row
    [Arguments]    ${code}
    Click    xpath=//tbody[@id='manageObject:form:T_data']//span[normalize-space(text())='${code}']
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.2s

EC Get Table Rows
    ${rows}=    Evaluate JavaScript    ${None}    () => { const t=document.getElementById('manageObject:form:T_data'); if(!t) return []; const o=[]; t.querySelectorAll('tr').forEach(tr=>{const c=[];tr.querySelectorAll('td').forEach(td=>c.push((td.textContent||'').trim()));if(c.some(x=>x))o.push(c);}); return o; }
    RETURN    ${rows}

EC Row Exists
    [Arguments]    ${code}
    ${rows}=    EC Get Table Rows
    FOR    ${row}    IN    @{rows}
        ${first}=    Get From List    ${row}    0
        IF    '${first}' == '${code}'    RETURN    ${TRUE}
    END
    RETURN    ${FALSE}
