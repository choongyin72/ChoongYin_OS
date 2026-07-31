*** Settings ***
Documentation       T3 (screen) - Chemical Stream page object.
...                 Screen: Configuration > Assets > Chemical_Objects > Chemical Stream (CO.0258).
...                 OV-GM with a mandatory Pick-from-EC-Object POPUP (From Connection). The popup
...                 (stream_node_ref_popup) differs from the standard object_popup: it has its own
...                 inner navigator + an Object Type dd (nav:form:G:4, empty on open) + inner GO,
...                 and its list grid id is manage_object_nav_nav:form:T_data (NOT PopupList) -
...                 hence the screen-local popup keyword below (shared T1 popup.resource untouched).
...                 Navigator uses SPECIFIC P1 values: the popup source is EMPTY under the
...                 first-available AS1 scope (the original park reason; owner screenshot proved
...                 the P1 scope populates it). Fields BY LABEL. DELETE = End Date = Start Date.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Resource            ../../../../resources/navigator.resource


*** Variables ***
${SCR}                  Chemical Stream
${TBL}                  manageObject:form:T_data
${DEL_ENDDATE}          tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# owner-provided working nav scope (popup source empty under first-available AS1)
${CHS_NAV_PU}           P1 Production Unit
${CHS_NAV_AREA}         P1 Area
${CHS_NAV_FC1}          P1 Facility 1
# From Connection popup internals (recon-verified 2026-07-30)
${CHS_POPUP_OBJTYPE}    CHEM_TANK
${CHS_POPUP_OBJTYPE_DD}    nav:form:G:4:R:1:C:0:dd
${CHS_POPUP_GRID}       manage_object_nav_nav:form:T_data


*** Keywords ***
Open Chemical Stream Screen
    [Documentation]    Suite Setup: launch, login, open the screen, apply the SPECIFIC 3-level
    ...    P1 navigator scope + GO - the grid AND the From Connection popup source are scoped by it.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCR}    ${user}    ${pass}
    Apply Chemical Stream Navigator

Apply Chemical Stream Navigator
    [Documentation]    Fill the 3-column cascade (row 1) with the owner-provided P1 values, then GO.
    Select EC Dropdown Option    nav:form:G:0:R:1:C:1:dd    ${CHS_NAV_PU}
    Sleep    0.7s
    Select EC Dropdown Option    nav:form:G:0:R:1:C:2:dd    ${CHS_NAV_AREA}
    Sleep    0.7s
    Select EC Dropdown Option    nav:form:G:0:R:1:C:3:dd    ${CHS_NAV_FC1}
    Sleep    0.7s
    Apply Navigator

Open From Connection Popup List
    [Documentation]    Open the stream_node_ref_popup behind ${pin_prefix} and drive it to the list
    ...    state: select Object Type = CHEM_TANK in the popup's inner dd, click the popup's inner GO,
    ...    wait for the popup grid (manage_object_nav_nav:form:T_data). The generic T1 popup keywords
    ...    do not fit this popup type: they wait for PopupList:form:T_data and drive no inner steps.
    [Arguments]    ${pin_prefix}
    Evaluate JavaScript    ${None}    () => document.getElementById('${pin_prefix}B').click()
    Wait For Elements State    css=[id="popupIFrame"]    visible    timeout=15s
    Sleep    2s
    Click    css=[id="popupIFrame"] >>> css=[id="${CHS_POPUP_OBJTYPE_DD}_button"]
    Click    css=[id="popupIFrame"] >>> xpath=//*[@id='${CHS_POPUP_OBJTYPE_DD}_panel']//tr[normalize-space(@data-item-label)='${CHS_POPUP_OBJTYPE}']
    Sleep    1s
    Click    css=[id="popupIFrame"] >>> css=[id="button:form:B"]
    Wait For Elements State    css=[id="popupIFrame"] >>> css=[id="${CHS_POPUP_GRID}"]    visible    timeout=15s
    Sleep    1s

Pick From Connection Popup
    [Documentation]    Screen-LOCAL first-available picker: drive the popup to its list state
    ...    (Open From Connection Popup List), click the FIRST row, verify the popup closed and
    ...    the pin input took a value.
    [Arguments]    ${pin_prefix}
    Open From Connection Popup List    ${pin_prefix}
    ${found}=    Evaluate JavaScript
    ...    css=[id="popupIFrame"] >>> css=[id="${CHS_POPUP_GRID}"]
    ...    (tbody) => { const tr = tbody.querySelector('tr'); const td = tr ? tr.querySelector('td') : null; if (td) { td.click(); return true; } return false; }
    Should Be True    ${found}    msg=From Connection popup has no rows (check the P1 navigator scope)
    Wait For Elements State    css=[id="popupIFrame"]    hidden    timeout=15s
    Sleep    1s
    ${val}=    Get Property    css=[id="${pin_prefix}"]    value
    Should Not Be Empty    ${val}    msg=From Connection pick did not fill the pin field

Chemical Stream Row Should Exist
    [Documentation]    Assert ${code} is present (await lazy OV-GM redraw first).
    [Arguments]    ${code}
    Wait For Elements State
    ...    xpath=//tbody[@id='${TBL}']//span[normalize-space(text())='${code}']
    ...    visible    timeout=20s
    Row Should Exist    ${TBL}    ${code}

Chemical Stream Row Should Not Exist
    [Documentation]    Assert ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${TBL}    ${code}

Chemical Stream Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} persisted in OV_CHEM_STREAM.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_CHEM_STREAM    ${code}

Chemical Stream Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} deleted from OV_CHEM_STREAM.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_CHEM_STREAM    ${code}

Chemical Stream Row Should Show Name
    [Documentation]    Assert the row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${TBL}    ${code}    ${name}

Insert Chemical Stream Record
    [Documentation]    Insert (fields BY LABEL): Start Date FIRST (it precedes Code on this form),
    ...    Chemical Stream Type first-available, then the From Connection popup (screen-local picker).
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Date By Label        objectForm    Start Date    ${start_date}
    Fill OV Field By Label       objectForm    Chemical Stream Code    ${code}
    Fill OV Field By Label       objectForm    Chemical Stream Name    ${name}
    Fill OV Dropdown By Label    objectForm    Chemical Stream Type    __FIRST__
    ${pin}=    Get Attribute
    ...    xpath=//span[contains(@class,'ECCell') and contains(@id,':objectForm:form:') and normalize-space(text())='From Connection']/ancestor::div[contains(@class,'tableCell')][1]/following-sibling::div[contains(@class,'tableCell')][1]//input[substring(@id, string-length(@id) - 3) = ':pin']
    ...    id
    Pick From Connection Popup    ${pin}
    Save And Refresh List

Update Chemical Stream Name
    [Documentation]    Select the row, edit Name (by label), save + reload.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${TBL}    ${code}
    Fill OV Field By Label    updateAttributes    Chemical Stream Name    ${new_name}
    Save And Refresh List

Delete Chemical Stream
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${TBL}    ${DEL_ENDDATE}    ${code}    ${date}
