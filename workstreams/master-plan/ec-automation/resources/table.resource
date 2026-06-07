*** Settings ***
Documentation       T1 area — Grid/table data: field & date entry, row reads, row assertions.

Library             Collections
Library             Browser


*** Keywords ***
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
