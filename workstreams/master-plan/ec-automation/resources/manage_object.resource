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

Click Go
    [Documentation]    Click the navigator Go button to (re)load the object list.
    Click    css=[id="button:form:B"]
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.2s

Delete Object By Zero-Length Window
    [Documentation]    Set End Date = Start Date -> zero-length window -> EC true delete.
    [Arguments]    ${enddate_id}    ${date}
    Fill EC Date    ${enddate_id}    ${date}
