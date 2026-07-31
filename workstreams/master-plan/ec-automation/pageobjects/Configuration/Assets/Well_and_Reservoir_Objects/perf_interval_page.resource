*** Settings ***
Documentation       T3 (screen) - Perforation Interval page object.
...                 Screen: Configuration > Assets > Well_and_Reservoir_Objects > Perforation Interval (CO.0153).
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
${SCR}              Perforation Interval
${TBL}              manageObject:form:T_data
${DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
${PI_NAV_PU}        P1 Production Unit
${PI_NAV_AREA}      P1 Area
${PI_NAV_FC1}       P1 Facility 1
${PI_NAV_WELL}      P1 W008 OP
${PI_NAV_WB}        P1 W008 WB001
${PI_NAV_WBI}       P1 W008 WB001 WBI001
${PI_POPUP_GRID}    Objects:form:T_data


*** Keywords ***
Open Perforation Interval Screen
    [Documentation]    Suite Setup: launch, login, open the screen, apply the SPECIFIC 4-level
    ...    navigator (per-field groups) + GO.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCR}    ${user}    ${pass}
    Apply Perforation Interval Navigator

Select Nav Group Value
    [Documentation]    Set one per-field navigator group (nav:form:G:<g>:R:1:C:0:dd) to ${value}.
    [Arguments]    ${group}    ${value}
    Select EC Dropdown Option    nav:form:G:${group}:R:1:C:0:dd    ${value}
    Sleep    0.8s

Apply Perforation Interval Navigator
    [Documentation]    Fill nav groups G:1..G:4 + G:6 (each R:1:C:0) with the verified P1 values -
    ...    a REAL well in G:4 and the WELL BORE in G:6 - then GO. G:5 is skipped (zero options
    ...    under every scope tried).
    Select Nav Group Value    1    ${PI_NAV_PU}
    Select Nav Group Value    2    ${PI_NAV_AREA}
    Select Nav Group Value    3    ${PI_NAV_FC1}
    Select Nav Group Value    4    ${PI_NAV_WELL}
    Select Nav Group Value    6    ${PI_NAV_WB}
    Select Nav Group Value    7    ${PI_NAV_WBI}
    Apply Navigator

Open Well Bore Interval Popup List
    [Documentation]    Open the well_bore_interval_gm_popup behind ${pin_prefix} and click its OWN
    ...    inner GO (button:form:B): the popup inherits the outer nav scope but its list grid
    ...    `Objects:form:T_data` stays EMPTY until that inner GO runs (recon-verified). The generic
    ...    T1 helpers wait on PopupList and never drive GO -> false 'empty source' report.
    [Arguments]    ${pin_prefix}
    Evaluate JavaScript    ${None}    () => document.getElementById('${pin_prefix}B').click()
    Wait For Elements State    css=[id="popupIFrame"]    visible    timeout=15s
    Sleep    2s
    Click    css=[id="popupIFrame"] >>> css=[id="button:form:B"]
    Sleep    2.5s

Pick Well Bore Interval Popup
    [Documentation]    Screen-LOCAL picker: drive the popup to its list state, click the row whose
    ...    value starts with ${want} (the nav-scope well bore interval), verify the pin took a value.
    [Arguments]    ${pin_prefix}    ${want}=${PI_NAV_WBI}
    Open Well Bore Interval Popup List    ${pin_prefix}
    ${found}=    Evaluate JavaScript
    ...    css=[id="popupIFrame"] >>> css=[id="${PI_POPUP_GRID}"]
    ...    (tbody) => { let hit = false; tbody.querySelectorAll('tr').forEach(tr => { const inp = tr.querySelector('td input'); const v = inp ? inp.value.trim() : (tr.innerText || '').trim(); if (!hit && v.startsWith('${want}')) { hit = true; tr.querySelector('td').click(); } }); return hit; }
    Should Be True    ${found}    msg=Well Bore Interval popup row '${want}' not found in ${PI_POPUP_GRID} after inner GO
    Wait For Elements State    css=[id="popupIFrame"]    hidden    timeout=15s
    Sleep    1s
    ${val}=    Get Property    css=[id="${pin_prefix}"]    value
    Should Not Be Empty    ${val}    msg=Well Bore Interval popup pick did not fill the pin field

Perforation Interval Row Should Exist
    [Documentation]    Assert ${code} is present (await lazy OV-GM redraw first).
    [Arguments]    ${code}
    Wait For Elements State
    ...    xpath=//tbody[@id='${TBL}']//span[normalize-space(text())='${code}']
    ...    visible    timeout=20s
    Row Should Exist    ${TBL}    ${code}

Perforation Interval Row Should Not Exist
    [Documentation]    Assert ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${TBL}    ${code}

Perforation Interval Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} persisted in OV_PERF_INTERVAL.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_PERF_INTERVAL    ${code}

Perforation Interval Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} deleted from OV_PERF_INTERVAL.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_PERF_INTERVAL    ${code}

Perforation Interval Row Should Show Name
    [Documentation]    Assert the row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${TBL}    ${code}    ${name}

Insert Perforation Interval Record
    [Documentation]    Insert (fields BY LABEL) + the mandatory Well Bore Interval popup
    ...    (screen-local, inner-GO picker) + the mandatory Reservoir Block Formation dd + Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label    objectForm    Perforation Interval Code    ${code}
    Fill OV Field By Label    objectForm    Perforation Interval Name    ${name}
    Fill OV Date By Label     objectForm    Start Date    ${start_date}
    ${pin}=    Get Attribute
    ...    xpath=//span[contains(@class,'ECCell') and contains(@id,':objectForm:form:') and normalize-space(text())='Well Bore Interval']/ancestor::div[contains(@class,'tableCell')][1]/following-sibling::div[contains(@class,'tableCell')][1]//input[substring(@id, string-length(@id) - 3) = ':pin']
    ...    id
    Pick Well Bore Interval Popup    ${pin}
    Fill OV Dropdown By Label    objectForm    Reservoir Block Formation    __FIRST__
    Save And Refresh List

Update Perforation Interval Name
    [Documentation]    Select the row, edit Name (by label), save + reload.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${TBL}    ${code}
    Fill OV Field By Label    updateAttributes    Perforation Interval Name    ${new_name}
    Save And Refresh List

Delete Perforation Interval
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${TBL}    ${DEL_ENDDATE}    ${code}    ${date}
