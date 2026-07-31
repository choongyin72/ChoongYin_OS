*** Settings ***
Documentation       T3 (screen) - Well Bore page object.
...                 Screen: Configuration > Assets > Well_and_Reservoir_Objects > Well Bore (CO.0054).
...                 OV-GM, PER-FIELD nav groups nav:form:G:1..G:4:R:1:C:0 (PU / Area / Facility
...                 Class 1 / 'Well & Well Hookup') with SPECIFIC values: the first-available G:4
...                 option is 'P1 Graph 001' (a graph object with no bores), so G:4 = a REAL well
...                 (P1 W008 OP). A 5th group G:5 ('Well') is scan-flagged mandatory but offers ZERO
...                 options under every scope tried - unusable filter, skipped; the grid loads on 4
...                 levels (verified: P1 W008 WB001 lists).
...                 Mandatory form field: 'Well' POPUP whose list grid is `Objects:form:T_data`
...                 (NOT PopupList:form:T_data) - screen-local picker below; picks the nav-scope
...                 well by value (the popup's FIRST row is the graph object). DELETE = End=Start.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Resource            ../../../../resources/navigator.resource


*** Variables ***
${SCR}              Well Bore
${TBL}              manageObject:form:T_data
${DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
${WB_NAV_PU}        P1 Production Unit
${WB_NAV_AREA}      P1 Area
${WB_NAV_FC1}       P1 Facility 1
${WB_NAV_WELL}      P1 W008 OP
${WB_POPUP_GRID}    Objects:form:T_data


*** Keywords ***
Open Well Bore Screen
    [Documentation]    Suite Setup: launch, login, open the screen, apply the SPECIFIC 4-level
    ...    navigator (per-field groups) + GO.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCR}    ${user}    ${pass}
    Apply Well Bore Navigator

Apply Well Bore Navigator
    [Documentation]    Fill nav groups G:1..G:4 (each R:1:C:0) with the verified P1 values incl. a
    ...    REAL well in G:4, then GO. G:5 is skipped (zero options under every scope tried).
    Select EC Dropdown Option    nav:form:G:1:R:1:C:0:dd    ${WB_NAV_PU}
    Sleep    0.8s
    Select EC Dropdown Option    nav:form:G:2:R:1:C:0:dd    ${WB_NAV_AREA}
    Sleep    0.8s
    Select EC Dropdown Option    nav:form:G:3:R:1:C:0:dd    ${WB_NAV_FC1}
    Sleep    0.8s
    Select EC Dropdown Option    nav:form:G:4:R:1:C:0:dd    ${WB_NAV_WELL}
    Sleep    0.8s
    Apply Navigator

Pick Well Popup
    [Documentation]    Screen-LOCAL picker for the 'Well' popup behind ${pin_prefix}: waits for the
    ...    real list grid `Objects:form:T_data` (the generic T1 helpers wait for PopupList and thus
    ...    report a false 'empty source'), then clicks the row whose value equals ${want} (default
    ...    the nav-scope well; the popup's first row is a graph object, deliberately not used).
    [Arguments]    ${pin_prefix}    ${want}=${WB_NAV_WELL}
    Evaluate JavaScript    ${None}    () => document.getElementById('${pin_prefix}B').click()
    Wait For Elements State    css=[id="popupIFrame"]    visible    timeout=15s
    Wait For Elements State    css=[id="popupIFrame"] >>> css=[id="${WB_POPUP_GRID}"]    visible    timeout=15s
    Sleep    1.5s
    ${found}=    Evaluate JavaScript
    ...    css=[id="popupIFrame"] >>> css=[id="${WB_POPUP_GRID}"]
    ...    (tbody) => { let hit = false; tbody.querySelectorAll('tr').forEach(tr => { const inp = tr.querySelector('td input'); const v = inp ? inp.value.trim() : (tr.innerText || '').trim(); if (!hit && v.startsWith('${want}')) { hit = true; tr.querySelector('td').click(); } }); return hit; }
    Should Be True    ${found}    msg=Well popup row '${want}' not found in ${WB_POPUP_GRID}
    Wait For Elements State    css=[id="popupIFrame"]    hidden    timeout=15s
    Sleep    1s
    ${val}=    Get Property    css=[id="${pin_prefix}"]    value
    Should Not Be Empty    ${val}    msg=Well popup pick did not fill the pin field

Well Bore Row Should Exist
    [Documentation]    Assert ${code} is present (await lazy OV-GM redraw first).
    [Arguments]    ${code}
    Wait For Elements State
    ...    xpath=//tbody[@id='${TBL}']//span[normalize-space(text())='${code}']
    ...    visible    timeout=20s
    Row Should Exist    ${TBL}    ${code}

Well Bore Row Should Not Exist
    [Documentation]    Assert ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${TBL}    ${code}

Well Bore Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} persisted in OV_WELL_BORE.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_WELL_BORE    ${code}

Well Bore Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} deleted from OV_WELL_BORE.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_WELL_BORE    ${code}

Well Bore Row Should Show Name
    [Documentation]    Assert the row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${TBL}    ${code}    ${name}

Insert Well Bore Record
    [Documentation]    Insert (fields BY LABEL) + the mandatory Well popup (screen-local picker) + Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label    objectForm    Well Bore Code    ${code}
    Fill OV Field By Label    objectForm    Well Bore Name    ${name}
    Fill OV Date By Label     objectForm    Start Date    ${start_date}
    ${pin}=    Get Attribute
    ...    xpath=//span[contains(@class,'ECCell') and contains(@id,':objectForm:form:') and normalize-space(text())='Well']/ancestor::div[contains(@class,'tableCell')][1]/following-sibling::div[contains(@class,'tableCell')][1]//input[substring(@id, string-length(@id) - 3) = ':pin']
    ...    id
    Pick Well Popup    ${pin}
    Save And Refresh List

Update Well Bore Name
    [Documentation]    Select the row, edit Name (by label), save + reload.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${TBL}    ${code}
    Fill OV Field By Label    updateAttributes    Well Bore Name    ${new_name}
    Save And Refresh List

Delete Well Bore
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${TBL}    ${DEL_ENDDATE}    ${code}    ${date}
