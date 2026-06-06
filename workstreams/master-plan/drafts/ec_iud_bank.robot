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
...    Proven working with: AUTOTEST_BNK_003 (2026-06-06)
...
...    Author:       Choong-Yin Lee / Claude Sonnet 4.6
...    Date:         2026-06-06
...    Environment:  Local EC (ap-f0a7g341jn6d.corp.quorumsoftware.com:8443)

Library           Browser
Library           String
Library           Collections

*** Variables ***
${EC_URL}              https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/
${EC_USER}             sysadmin
${EC_PASS}             sysadmin
${TEST_CODE}           AUTOTEST_BNK_003
${TEST_NAME}           AUTOTEST Bank 003
${TEST_NAME_UPD}       AUTOTEST Bank 003 UPDATED
${START_DATE}          2000-01-01
${END_DATE}            2000-01-02
${HEADLESS}            ${TRUE}
${NAV_TABLE}           manage_object_nav_nav:form:T_data
${SS_DIR}              ${CURDIR}${/}..${/}..${/}docs${/}EC${/}screenshots${/}iud_bank${/}rf

*** Test Cases ***

TC01 Navigate To Bank Screen
    [Documentation]    Open EC, login, navigate to Bank screen via sidebar search
    [Tags]    iud    bank    navigation
    New Browser    chromium    headless=${HEADLESS}    args=["--ignore-certificate-errors"]
    New Context    ignoreHTTPSErrors=${TRUE}    viewport={'width': 1920, 'height': 1080}
    New Page    ${EC_URL}
    Fill Text    id=username    ${EC_USER}
    Fill Text    id=password    ${EC_PASS}
    Click    id=kc-login
    Wait For URL    **/dashboard**    timeout=60s
    Wait For Load State    networkidle    timeout=30s
    # Navigate to Bank via sidebar search
    Fill Text    id=menu:searchForm:searchTxt    Bank
    Wait For Load State    networkidle    timeout=8s
    Sleep    0.4s
    Click    xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='Bank']
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.5s
    ${label}=    Get Text    id=screenToolbar:form:screenLabel
    Should Contain    ${label}    Bank
    Take Screenshot    ${SS_DIR}${/}rf_tc01_bank_screen.png

TC02 Verify Clean State
    [Documentation]    Confirm AUTOTEST_BNK_003 does not exist before inserting
    [Tags]    iud    bank    clean-state
    ${rows}=    EC Get Table Rows
    Log    Current banks: ${rows}
    ${exists}=    EC Row Exists    ${TEST_CODE}
    Should Be Equal    ${exists}    ${FALSE}
    ...    msg=AUTOTEST_BNK_003 already exists — cannot run INSERT test
    Take Screenshot    ${SS_DIR}${/}rf_tc02_clean_state.png

TC03 Insert New Bank Record
    [Documentation]    Insert AUTOTEST_BNK_003 via Insert → New Object → fill 3 mandatory fields
    ...
    ...    Mandatory fields: Bank Code, Bank Name, Start Date
    ...    objectForm field IDs:
    ...      Code:       tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
    ...      Name:       tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
    ...      Start Date: tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
    [Tags]    iud    bank    insert
    # Hover Insert toolbar button → submenu appears
    Hover    xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]
    Sleep    1s
    # Click New Object submenu item
    ${sub_links}=    Get Element Count    xpath=//ul[contains(@class,'ui-menu-child')]//li//a
    Should Be True    ${sub_links} > 0    msg=Insert submenu not visible after hover
    Click    xpath=//ul[contains(@class,'ui-menu-child')]//li//a    # clicks first item = New Object
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.2s
    Take Screenshot    ${SS_DIR}${/}rf_tc03a_new_object_form.png
    # Fill Bank Code
    Fill Text    id=tab:tabPanel:objectForm:form:G:0:R:0:C:1:in    ${TEST_CODE}
    Evaluate JavaScript    None    () => {
    ...    const e = document.getElementById('tab:tabPanel:objectForm:form:G:0:R:0:C:1:in');
    ...    if (e) { e.dispatchEvent(new Event('change', {bubbles:true})); e.dispatchEvent(new Event('blur', {bubbles:true})); }
    ... }
    Sleep    0.4s
    # Fill Bank Name
    Fill Text    id=tab:tabPanel:objectForm:form:G:0:R:1:C:1:in    ${TEST_NAME}
    Evaluate JavaScript    None    () => {
    ...    const e = document.getElementById('tab:tabPanel:objectForm:form:G:0:R:1:C:1:in');
    ...    if (e) { e.dispatchEvent(new Event('change', {bubbles:true})); e.dispatchEvent(new Event('blur', {bubbles:true})); }
    ... }
    Sleep    0.4s
    # Fill Start Date (da_input calendar widget — fill + Tab to trigger calendar validation)
    Fill Text    id=tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input    ${START_DATE}
    Keyboard Key    Tab
    Sleep    0.6s
    Evaluate JavaScript    None    () => {
    ...    const e = document.getElementById('tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input');
    ...    if (e) { e.dispatchEvent(new Event('change', {bubbles:true})); e.dispatchEvent(new Event('blur', {bubbles:true})); }
    ... }
    Sleep    0.4s
    Take Screenshot    ${SS_DIR}${/}rf_tc03b_insert_fields_filled.png
    # Save
    Click    xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.2s
    Take Screenshot    ${SS_DIR}${/}rf_tc03c_after_save.png
    # Refresh table via Go button
    Click    id=button:form:B
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.2s
    # Verify
    ${exists}=    EC Row Exists    ${TEST_CODE}
    Should Be True    ${exists}    msg=INSERT FAILED: ${TEST_CODE} not found in table after save
    Take Screenshot    ${SS_DIR}${/}rf_tc03d_insert_verified.png
    Log    INSERT PASS: ${TEST_CODE} found in Bank table

TC04 Update Bank Name
    [Documentation]    Select AUTOTEST_BNK_003 → update Bank Name in updateAttributes form
    ...
    ...    After row selection, bank data loads in tabs:
    ...      updateAttributes form Name field: tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
    [Tags]    iud    bank    update
    # Click the bank row (click on the Bank Code span in the table)
    Click    css=#manage_object_nav_nav\:form\:T_data span >> text="${TEST_CODE}"
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.2s
    Take Screenshot    ${SS_DIR}${/}rf_tc04a_row_selected.png
    # Verify updateAttributes loaded
    ${code_val}=    Get Property    id=tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in    value
    Should Be Equal    ${code_val}    ${TEST_CODE}    msg=Row selection failed — code field not loaded
    # Update Bank Name
    Fill Text    id=tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in    ${TEST_NAME_UPD}
    Evaluate JavaScript    None    () => {
    ...    const e = document.getElementById('tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in');
    ...    if (e) { e.dispatchEvent(new Event('change', {bubbles:true})); e.dispatchEvent(new Event('blur', {bubbles:true})); }
    ... }
    Sleep    0.4s
    Take Screenshot    ${SS_DIR}${/}rf_tc04b_name_updated.png
    # Save
    Click    xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.2s
    # Refresh and verify
    Click    id=button:form:B
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.2s
    Take Screenshot    ${SS_DIR}${/}rf_tc04c_after_update_save.png
    # Check the row shows the updated name
    ${row_text}=    Get Text    xpath=//tbody[@id='manage_object_nav_nav:form:T_data']//tr[.//span[normalize-space(text())='${TEST_CODE}']]
    Should Contain    ${row_text}    ${TEST_NAME_UPD}
    ...    msg=UPDATE FAILED: updated name not found in row
    Take Screenshot    ${SS_DIR}${/}rf_tc04d_update_verified.png
    Log    UPDATE PASS: Bank Name updated to ${TEST_NAME_UPD}

TC05 Soft-Delete Bank (Set End Date)
    [Documentation]    Soft-delete AUTOTEST_BNK_003 by setting End Date = day after Start Date
    ...
    ...    EC Bank hard-delete is DISABLED by design. Soft-delete pattern:
    ...    Select row → objectdates form End Date field → set expiry date → Save
    ...    After save, bank disappears from table (expired at current nav date) = delete confirmed.
    ...
    ...    objectdates End Date field: tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
    [Tags]    iud    bank    delete    cleanup
    # Click the bank row
    Click    css=#manage_object_nav_nav\:form\:T_data span >> text="${TEST_CODE}"
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.2s
    Take Screenshot    ${SS_DIR}${/}rf_tc05a_row_for_delete.png
    # Verify objectdates loaded
    ${start_val}=    Get Property    id=tab:tabPanel:objectdates:form:G:0:R:0:C:1:da_input    value
    Log    Bank Start Date: ${start_val}
    # Set End Date
    Fill Text    id=tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input    ${END_DATE}
    Keyboard Key    Tab
    Sleep    0.6s
    Evaluate JavaScript    None    () => {
    ...    const e = document.getElementById('tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input');
    ...    if (e) { e.dispatchEvent(new Event('change', {bubbles:true})); e.dispatchEvent(new Event('blur', {bubbles:true})); }
    ... }
    Sleep    0.4s
    Take Screenshot    ${SS_DIR}${/}rf_tc05b_end_date_set.png
    # Save
    Click    xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.2s
    # Refresh table
    Click    id=button:form:B
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.2s
    Take Screenshot    ${SS_DIR}${/}rf_tc05c_after_delete_save.png
    # Verify bank no longer visible (expired at current nav date)
    ${still_exists}=    EC Row Exists    ${TEST_CODE}
    Should Be Equal    ${still_exists}    ${FALSE}
    ...    msg=DELETE FAILED: ${TEST_CODE} still visible after End Date set
    Take Screenshot    ${SS_DIR}${/}rf_tc05d_delete_verified.png
    Log    DELETE PASS: ${TEST_CODE} expired (EndDate=${END_DATE}), no longer visible

*** Keywords ***

EC Get Table Rows
    [Documentation]    Return list of [Bank Code, Bank Name, Date, ...] rows from the Bank table
    ${rows}=    Evaluate JavaScript    None    () => {
    ...    const tbody = document.getElementById('manage_object_nav_nav:form:T_data');
    ...    if (!tbody) return [];
    ...    const out = [];
    ...    tbody.querySelectorAll('tr').forEach(tr => {
    ...        const cells = [];
    ...        tr.querySelectorAll('td').forEach(td => cells.push(td.textContent.trim()));
    ...        if (cells.some(c => c)) out.push(cells);
    ...    });
    ...    return out;
    ... }
    RETURN    ${rows}

EC Row Exists
    [Documentation]    Return True if a row with the given Bank Code exists in the table
    [Arguments]    ${code}
    ${rows}=    EC Get Table Rows
    FOR    ${row}    IN    @{rows}
        ${first_cell}=    Get From List    ${row}    0
        IF    '${first_cell}' == '${code}'
            RETURN    ${TRUE}
        END
    END
    RETURN    ${FALSE}
