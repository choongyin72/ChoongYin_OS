*** Settings ***
Documentation       T2 (pattern) — Manage-Object (OV) screen mechanics, shared by
...                 date-effective object screens (e.g. Bank, Equipment).
...                 DELETE here = End Date set equal to Start Date (zero-length
...                 effective window) which EC treats as a TRUE delete (object
...                 removed from its OV view). The toolbar "-" button is disabled
...                 for these screens by design.

Library             Browser
Resource            common.resource


*** Keywords ***
Open New Object Form
    [Documentation]    Hover the Insert toolbar menu and choose "New Object".
    ...    Wait for the submenu item to be visible before clicking (robust vs a fixed sleep).
    Hover    xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]
    Wait For Elements State
    ...    xpath=//ul[contains(@class,'ui-menu-child')]//li//a[normalize-space(.)='New Object']
    ...    visible    timeout=10s
    Click    xpath=//ul[contains(@class,'ui-menu-child')]//li//a[normalize-space(.)='New Object']
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.2s

Select Object Row
    [Documentation]    Select an object row by its code (text lives in a span child).
    [Arguments]    ${table_id}    ${code}
    Click    xpath=//tbody[@id='${table_id}']//span[normalize-space(text())='${code}']
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.2s

Delete Object By Zero-Length Window
    [Documentation]    Set End Date = Start Date -> zero-length window -> EC true delete.
    [Arguments]    ${enddate_id}    ${date}
    Fill EC Date    ${enddate_id}    ${date}

Fill New Object Form
    [Documentation]    Open the New Object form and fill the universal trio
    ...    (Code / Name / Start Date). Screen-specific mandatory extras (e.g. a
    ...    dropdown) are filled by the caller BEFORE it calls Save And Refresh List.
    # 3 locator ids + their 3 values belong together - splitting hurts readability
    [Arguments]    ${code_id}    ${name_id}    ${date_id}    ${code}    ${name}    ${start_date}    # robocop: off=LEN07
    Open New Object Form
    Fill EC Field    ${code_id}    ${code}
    Fill EC Field    ${name_id}    ${name}
    Fill EC Date    ${date_id}    ${start_date}

Save And Refresh List
    [Documentation]    Save the form, then Apply Navigator so the list reloads from
    ...    the DB (the grid does not refresh on its own — see registry: GO is mandatory).
    Save
    Apply Navigator

Update Object Name
    [Documentation]    Select the object row by code, prove the row actually loaded
    ...    (guards against silent mis-select), edit the Name attribute, save + reload.
    [Arguments]    ${table_id}    ${upd_code_id}    ${upd_name_id}    ${code}    ${new_name}
    Select Object Row    ${table_id}    ${code}
    ${loaded}=    Get Property    css=[id="${upd_code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill EC Field    ${upd_name_id}    ${new_name}
    Save And Refresh List

Delete Object Via End Date
    [Documentation]    Select the object row, set End Date = Start Date (EC true
    ...    delete for date-effective objects), save + reload.
    [Arguments]    ${table_id}    ${enddate_id}    ${code}    ${date}
    Select Object Row    ${table_id}    ${code}
    Delete Object By Zero-Length Window    ${enddate_id}    ${date}
    Save And Refresh List

Object Row Should Show Name
    [Documentation]    Assert the grid row holding ${code} displays ${name}.
    [Arguments]    ${table_id}    ${code}    ${name}
    ${row}=    Get Text    xpath=//tbody[@id='${table_id}']//tr[.//span[normalize-space(text())='${code}']]
    Should Contain    ${row}    ${name}    msg=Row ${code} does not show name ${name}
