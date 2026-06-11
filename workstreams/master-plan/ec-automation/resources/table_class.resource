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

Insert New Grid Row By Label
    [Documentation]    Insert toolbar -> the ${submenu_label} item, scoped to the INSERT
    ...    menu-parent (the Delete submenu often has an identically named item).
    [Arguments]    ${submenu_label}
    Hover    xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]
    Wait For Elements State
    ...    xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]//ul[contains(@class,'ui-menu-child')]//a[normalize-space(.)='${submenu_label}']
    ...    visible
    ...    timeout=10s
    Click
    ...    xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]//ul[contains(@class,'ui-menu-child')]//a[normalize-space(.)='${submenu_label}']
    Wait For Load State    networkidle    timeout=12s
    Sleep    1s

Find Grid Row By Cell Input Value
    [Documentation]    Return the row index whose cell input (id ending ${cell_suffix},
    ...    e.g. C2_dd_input) has the given value — or -1. Empty value finds a blank row.
    [Arguments]    ${grid_id}    ${cell_suffix}    ${value}
    ${idx}=    Evaluate JavaScript
    ...    ${None}
    ...    () => { const t=document.getElementById('${grid_id}'); if(!t) return -1;
    ...    const m=t.querySelectorAll("input[id$='${cell_suffix}']");
    ...    for (const e of m) { if ((e.value||'')==='${value}') { const r=e.id.match(/:T:(\\d+):/); if(r) return parseInt(r[1]); } }
    ...    return -1; }
    RETURN    ${idx}

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
