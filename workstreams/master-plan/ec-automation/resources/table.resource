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

Select EC Dropdown Option
    [Documentation]    Pick an option from an EC autocomplete dropdown (…:dd) by its
    ...    exact item label: click the chevron, wait for the option row
    ...    (tr[data-item-label]) and click it. A pending form re-render (e.g. after a
    ...    date Tab-out) can close the panel between open and click, so one re-open
    ...    retry is built in. Typing into autocomplete-dd fields is unreliable.
    [Arguments]    ${dd_prefix}    ${value}
    # normalize-space tolerates leading/double spaces in stored labels
    # (real case: OV_AREA names like ' Offshore area' / ' Permit  Block 15')
    VAR    ${item}    xpath=//*[@id='${dd_prefix}_panel']//tr[normalize-space(@data-item-label)='${value}']
    Click    css=[id="${dd_prefix}_button"]
    TRY
        Wait For Elements State    ${item}    visible    timeout=6s
    EXCEPT
        # two stale cases: the panel was closed by a concurrent partial re-render,
        # OR it is open but its options have not arrived yet (cascading dropdown).
        # Escape guarantees a closed panel, then re-open fresh after a settle.
        Keyboard Key    press    Escape
        Sleep    1.5s
        Click    css=[id="${dd_prefix}_button"]
        Wait For Elements State    ${item}    visible    timeout=10s
    END
    Click    ${item}
    Wait For Load State    networkidle    timeout=12s
    Sleep    0.6s

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

Type Cell By Id
    [Documentation]    Commit an inline grid cell: real keystrokes + Tab so the cell's
    ...    onchange -> PrimeFaces.ab partial submit fires (fill()/synthetic events do NOT
    ...    stage the value). Use this for inline grids; Fill EC Field is for object forms.
    [Arguments]    ${cell_id}    ${value}
    Click    css=[id="${cell_id}"]
    Type Text    css=[id="${cell_id}"]    ${value}    clear=Yes
    Keyboard Key    press    Tab
    Wait For Load State    networkidle    timeout=12s
    Sleep    0.6s

Get Cell Value By Id
    [Documentation]    Return the current value of an inline grid cell input by id.
    [Arguments]    ${cell_id}
    ${v}=    Get Property    css=[id="${cell_id}"]    value
    RETURN    ${v}

Go To First Page
    [Documentation]    Click the paginator First button if it is enabled (no-op otherwise).
    ${n}=    Get Element Count    css=.ui-paginator-first:not(.ui-state-disabled)
    IF    ${n} > 0
        Click    css=.ui-paginator-first
        Wait For Load State    networkidle    timeout=10s
        Sleep    0.5s
    END

Current Page Has Next
    [Documentation]    True if the paginator Next button is enabled.
    ${n}=    Get Element Count    css=.ui-paginator-next:not(.ui-state-disabled)
    ${has}=    Evaluate    ${n} > 0
    RETURN    ${has}

Go To Next Page
    [Documentation]    Click the paginator Next button.
    Click    css=.ui-paginator-next
    Wait For Load State    networkidle    timeout=10s
    Sleep    0.5s
