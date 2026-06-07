*** Settings ***
Documentation       T2 (pattern) — Table-class (TV) screen mechanics, shared by
...                 inline-grid screens (e.g. MIME Type Mapping, Language).
...                 Add a blank editable row via the Insert toolbar; physically delete
...                 the selected row via the Delete toolbar submenu (the row is removed
...                 from the base table — contrast manage_object's End=Start true delete).

Library             Browser


*** Keywords ***
Insert New Grid Row
    [Documentation]    Insert toolbar -> first submenu item -> a blank editable row appears.
    Hover    xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]
    Wait For Elements State    xpath=(//ul[contains(@class,'ui-menu-child')]//li//a)[1]    visible    timeout=10s
    Click    xpath=(//ul[contains(@class,'ui-menu-child')]//li//a)[1]
    Wait For Load State    networkidle    timeout=12s
    Sleep    1s

Delete Selected Grid Row
    [Documentation]    Delete toolbar -> the ${submenu_label} item, scoped to the DELETE
    ...    menu-parent (the Insert submenu has an identically named item).
    [Arguments]    ${submenu_label}
    Hover    xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-delete')]]
    Wait For Elements State
    ...    xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-delete')]]//ul[contains(@class,'ui-menu-child')]//a[normalize-space(.)='${submenu_label}']
    ...    visible
    ...    timeout=10s
    Click
    ...    xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-delete')]]//ul[contains(@class,'ui-menu-child')]//a[normalize-space(.)='${submenu_label}']
    Wait For Load State    networkidle    timeout=12s
    Sleep    1s
