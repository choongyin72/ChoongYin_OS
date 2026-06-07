*** Settings ***
Documentation       T1 (universal) — EC mechanics reused by every screen suite:
...                 browser bootstrap, login, navigate-by-search, field/date fill,
...                 save, results-table reads, row assertions, screenshots, teardown.

Library             Collections
Library             DateTime
Library             Browser
Resource            environment.resource


*** Keywords ***
Generate Unique Code
    [Documentation]    Return ${prefix} + a YYYYMMDDHHMMSS timestamp (unique per second)
    ...    so re-runs never collide with codes that linger in the DB after a delete.
    [Arguments]    ${prefix}
    ${ts}=    Get Current Date    result_format=%Y%m%d%H%M%S
    RETURN    ${prefix}${ts}

Open EC Browser
    [Documentation]    Launch Chromium + context (headless/slowMo from environment).
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

Navigate To Screen
    [Documentation]    Open a screen via the sidebar search and confirm it loaded.
    [Arguments]    ${screen_name}
    Type Text    css=[id="menu:searchForm:searchTxt"]    ${screen_name}    delay=60ms    clear=Yes
    Wait For Load State    networkidle    timeout=8s
    Sleep    0.5s
    Click
    ...    xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='${screen_name}']
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.5s
    ${label}=    Get Text    css=[id="screenToolbar:form:screenLabel"]
    Should Contain    ${label}    ${screen_name}    msg=Failed to navigate to ${screen_name}

Fill EC Field
    [Documentation]    Fill a text input by EC id and dispatch change/blur for EC validation.
    [Arguments]    ${field_id}    ${value}
    Fill Text    css=[id="${field_id}"]    ${value}
    Evaluate JavaScript
    ...    ${None}
    ...    () => { const e=document.getElementById('${field_id}'); if(e){e.dispatchEvent(new Event('change',{bubbles:true}));e.dispatchEvent(new Event('blur',{bubbles:true}));} }
    Sleep    0.4s

Fill EC Date
    [Documentation]    Fill a da_input calendar field; Tab out triggers PrimeFaces validation.
    [Arguments]    ${field_id}    ${value}
    Fill Text    css=[id="${field_id}"]    ${value}
    Keyboard Key    press    Tab
    Sleep    0.6s
    Evaluate JavaScript
    ...    ${None}
    ...    () => { const e=document.getElementById('${field_id}'); if(e){e.dispatchEvent(new Event('change',{bubbles:true}));e.dispatchEvent(new Event('blur',{bubbles:true}));} }
    Sleep    0.4s

Save
    [Documentation]    Click the Save toolbar button (only when enabled).
    Click    xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.2s

Get Table Rows
    [Documentation]    Return a list of non-empty cell-lists from a results table by id.
    [Arguments]    ${table_id}
    ${rows}=    Evaluate JavaScript
    ...    ${None}
    ...    () => { const t=document.getElementById('${table_id}'); if(!t) return []; const o=[]; t.querySelectorAll('tr').forEach(tr=>{const c=[];tr.querySelectorAll('td').forEach(td=>c.push((td.textContent||'').trim()));if(c.some(x=>x))o.push(c);}); return o; }
    RETURN    ${rows}

Row Exists
    [Documentation]    True if a row whose first cell equals ${code} exists in the table.
    [Arguments]    ${table_id}    ${code}
    ${rows}=    Get Table Rows    ${table_id}
    FOR    ${row}    IN    @{rows}
        ${first}=    Get From List    ${row}    0
        IF    '${first}' == '${code}'    RETURN    ${TRUE}
    END
    RETURN    ${FALSE}

Row Should Exist
    [Documentation]    Assert a row with ${code} is present.
    [Arguments]    ${table_id}    ${code}
    ${exists}=    Row Exists    ${table_id}    ${code}
    Should Be True    ${exists}    msg=Expected row ${code} to exist in ${table_id}

Row Should Not Exist
    [Documentation]    Assert a row with ${code} is absent.
    [Arguments]    ${table_id}    ${code}
    ${exists}=    Row Exists    ${table_id}    ${code}
    Should Be Equal    ${exists}    ${FALSE}    msg=Row ${code} should NOT exist in ${table_id}

Capture Step
    [Documentation]    Take a screenshot into the output dir with a step label.
    [Arguments]    ${label}
    Take Screenshot    filename=${OUTPUT_DIR}/${label}

Close EC
    [Documentation]    Optional hold then close the browser (Suite Teardown).
    Sleep    ${HOLD}
    Close Browser
