*** Settings ***
Documentation    EC IUD Test — Bank (Configuration > Finance Objects > Bank)
...
...    Screen Type: Manage Object (EC14+ pattern)
...    Insert pattern: Insert toolbar → New Object submenu → fill objectForm → Save
...    Update pattern: Select row (span click) → updateAttributes form → edit Name → Save
...    Delete pattern: Select row → objectdates form → set End Date → Save (soft-delete)
...
...    NOTE: EC Bank hard-delete is DISABLED by design (banks are permanent master data).
...    Soft-delete is implemented by setting End Date = day after Start Date, making the bank
...    inactive/expired. The bank is no longer visible at the current navigator date.
...
...    Test Data: AUTOTEST_BNK_XXX prefix. NEVER use existing bank codes.
...    Each run must use a fresh incrementing code (expired banks persist in DB).
...
...    Author:       Choong-Yin Lee / Claude Sonnet 4.6
...    Date:         2026-06-06
...    Environment:  Local EC (ap-f0a7g341jn6d.corp.quorumsoftware.com:8443)
...    Requires:     robotframework-browser (rfbrowser init)

Library           Browser
Library           Collections
Suite Setup       Open EC And Navigate To Bank
Suite Teardown    Close Browser

*** Variables ***
${EC_URL}              https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/
${EC_USER}             sysadmin
${EC_PASS}             sysadmin
${TEST_CODE}           AUTOTEST_BNK_005
${TEST_NAME}           AUTOTEST Bank 005
${TEST_NAME_UPD}       AUTOTEST Bank 005 UPDATED
${START_DATE}          2000-01-01
${END_DATE}            2000-01-02
${HEADLESS}            ${TRUE}

# objectForm field IDs (Insert — new object)
${INS_CODE}            tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${INS_NAME}            tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${INS_DATE}            tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
# updateAttributes field IDs (Update — existing object)
${UPD_CODE}            tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${UPD_NAME}            tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field IDs (Delete — soft-delete via End Date)
${DEL_ENDDATE}         tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input

*** Test Cases ***

TC01 Verify Clean State
    [Documentation]    Confirm AUTOTEST_BNK_005 does not exist before inserting
    [Tags]    iud    bank    clean-state
    ${rows}=    EC Get Table Rows
    Log    Current banks: ${rows}
    ${exists}=    EC Row Exists    ${TEST_CODE}
    Should Be Equal    ${exists}    ${FALSE}
    ...    msg=${TEST_CODE} already exists — cannot run INSERT test (use next code)
    Take Screenshot    filename=${OUTPUT_DIR}/rf_tc01_clean_state

TC02 Insert New Bank Record
    [Documentation]    Insert via Insert toolbar → New Object → fill 3 mandatory fields (Code, Name, Start Date)
    [Tags]    iud    bank    insert
    # Hover Insert toolbar button → submenu appears
    Hover    xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]
    Sleep    1s
    # Click "New Object" (first submenu item under the insert menu)
    Click    xpath=(//ul[contains(@class,'ui-menu-child')]//li//a)[1]
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.2s
    Take Screenshot    filename=${OUTPUT_DIR}/rf_tc02a_new_object_form
    # Fill the 3 mandatory fields
    EC Fill Field      ${INS_CODE}    ${TEST_CODE}
    EC Fill Field      ${INS_NAME}    ${TEST_NAME}
    EC Fill Date       ${INS_DATE}    ${START_DATE}
    Take Screenshot    filename=${OUTPUT_DIR}/rf_tc02b_insert_filled
    # Save + refresh
    EC Save
    EC Go
    # Verify
    ${exists}=    EC Row Exists    ${TEST_CODE}
    Should Be True    ${exists}    msg=INSERT FAILED: ${TEST_CODE} not in table after save
    Take Screenshot    filename=${OUTPUT_DIR}/rf_tc02c_insert_verified
    Log    INSERT PASS: ${TEST_CODE} created

TC03 Update Bank Name
    [Documentation]    Select row → updateAttributes form → edit Bank Name → Save
    [Tags]    iud    bank    update
    EC Select Row    ${TEST_CODE}
    Take Screenshot    filename=${OUTPUT_DIR}/rf_tc03a_row_selected
    # Verify updateAttributes loaded
    ${code_val}=    Get Property    css=[id="${UPD_CODE}"]    value
    Should Be Equal    ${code_val}    ${TEST_CODE}    msg=Row select failed — code not loaded
    # Edit name + save
    EC Fill Field    ${UPD_NAME}    ${TEST_NAME_UPD}
    Take Screenshot    filename=${OUTPUT_DIR}/rf_tc03b_name_updated
    EC Save
    EC Go
    # Verify row shows updated name
    ${row_text}=    Get Text    xpath=//tbody[@id='manage_object_nav_nav:form:T_data']//tr[.//span[normalize-space(text())='${TEST_CODE}']]
    Should Contain    ${row_text}    ${TEST_NAME_UPD}    msg=UPDATE FAILED: name not updated
    Take Screenshot    filename=${OUTPUT_DIR}/rf_tc03c_update_verified
    Log    UPDATE PASS: name → ${TEST_NAME_UPD}

TC04 Soft-Delete Bank (Set End Date)
    [Documentation]    Select row → objectdates form → set End Date → Save → bank expires
    [Tags]    iud    bank    delete    cleanup
    EC Select Row    ${TEST_CODE}
    Take Screenshot    filename=${OUTPUT_DIR}/rf_tc04a_row_for_delete
    # Set End Date (expire the bank)
    EC Fill Date    ${DEL_ENDDATE}    ${END_DATE}
    Take Screenshot    filename=${OUTPUT_DIR}/rf_tc04b_end_date_set
    EC Save
    EC Go
    # Verify bank no longer visible (expired at current nav date)
    ${still}=    EC Row Exists    ${TEST_CODE}
    Should Be Equal    ${still}    ${FALSE}    msg=DELETE FAILED: ${TEST_CODE} still visible
    Take Screenshot    filename=${OUTPUT_DIR}/rf_tc04c_delete_verified
    Log    DELETE PASS: ${TEST_CODE} expired (EndDate=${END_DATE})

*** Keywords ***

Open EC And Navigate To Bank
    [Documentation]    Login to EC and navigate to the Bank screen (Suite Setup)
    New Browser    chromium    headless=${HEADLESS}
    New Context    ignoreHTTPSErrors=${TRUE}    viewport={'width': 1920, 'height': 1080}
    Set Browser Timeout    30s
    # EC renders some links twice (search list + favorites); first-match like Playwright .first
    Set Strict Mode    False
    New Page    ${EC_URL}
    Fill Text    css=[id="username"]    ${EC_USER}
    Fill Text    css=[id="password"]    ${EC_PASS}
    Click    css=[id="kc-login"]
    Wait For Elements State    css=[id="menu:searchForm:searchTxt"]    visible    timeout=60s
    Wait For Load State    networkidle    timeout=30s
    # Navigate to Bank via sidebar search (Type Text triggers PrimeFaces keyup AJAX)
    Type Text    css=[id="menu:searchForm:searchTxt"]    Bank    delay=60ms    clear=Yes
    Wait For Load State    networkidle    timeout=8s
    Sleep    0.5s
    Click    xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='Bank']
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.5s
    ${label}=    Get Text    css=[id="screenToolbar:form:screenLabel"]
    Should Contain    ${label}    Bank    msg=Failed to navigate to Bank screen
    Take Screenshot    filename=${OUTPUT_DIR}/rf_tc00_bank_loaded

EC Fill Field
    [Documentation]    Fill a text input by EC id and dispatch change/blur for EC validation
    [Arguments]    ${field_id}    ${value}
    Fill Text    css=[id="${field_id}"]    ${value}
    Evaluate JavaScript    ${None}    () => { const e=document.getElementById('${field_id}'); if(e){e.dispatchEvent(new Event('change',{bubbles:true}));e.dispatchEvent(new Event('blur',{bubbles:true}));} }
    Sleep    0.4s

EC Fill Date
    [Documentation]    Fill a da_input calendar field (Tab out triggers PrimeFaces calendar validation)
    [Arguments]    ${field_id}    ${value}
    Fill Text    css=[id="${field_id}"]    ${value}
    Keyboard Key    press    Tab
    Sleep    0.6s
    Evaluate JavaScript    ${None}    () => { const e=document.getElementById('${field_id}'); if(e){e.dispatchEvent(new Event('change',{bubbles:true}));e.dispatchEvent(new Event('blur',{bubbles:true}));} }
    Sleep    0.4s

EC Save
    [Documentation]    Click the Save toolbar button (waits for it to be enabled)
    Click    xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.2s

EC Go
    [Documentation]    Click the Go button to refresh the Bank list
    Click    css=[id="button:form:B"]
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.2s

EC Select Row
    [Documentation]    Click the table row for a given Bank Code (text is in a span child)
    [Arguments]    ${code}
    Click    xpath=//tbody[@id='manage_object_nav_nav:form:T_data']//span[normalize-space(text())='${code}']
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.2s

EC Get Table Rows
    [Documentation]    Return list of row-cell-lists from the Bank navigator table
    ${rows}=    Evaluate JavaScript    ${None}    () => { const t=document.getElementById('manage_object_nav_nav:form:T_data'); if(!t) return []; const o=[]; t.querySelectorAll('tr').forEach(tr=>{const c=[];tr.querySelectorAll('td').forEach(td=>c.push(td.textContent.trim()));if(c.some(x=>x))o.push(c);}); return o; }
    RETURN    ${rows}

EC Row Exists
    [Documentation]    Return True if a row with the given Bank Code exists
    [Arguments]    ${code}
    ${rows}=    EC Get Table Rows
    FOR    ${row}    IN    @{rows}
        ${first}=    Get From List    ${row}    0
        IF    '${first}' == '${code}'    RETURN    ${TRUE}
    END
    RETURN    ${FALSE}
