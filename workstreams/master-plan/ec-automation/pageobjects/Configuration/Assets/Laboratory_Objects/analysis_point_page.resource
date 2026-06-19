*** Settings ***
Documentation       T3 (screen) — Analysis Point page object.
...                 Screen: Configuration > Assets > Laboratory Objects > Analysis Point.
...                 OV-GM (groupmodel, 3-level cascade): the grid (manageObject:form:T_data) loads only
...                 after the PU → Area → Facility-Class-1 navigator cascade (dds at G:0 C:1/C:2/C:3) + GO.
...                 The inserted object's Op Production Unit / Op Area / Op Facility Class 1 must equal the
...                 nav scope or the filtered grid never lists it. Insert also needs a mandatory Analysis
...                 Point Type dd. DELETE = End Date = Start Date (true delete from ov_analysis_point).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${AP_SCREEN}            Analysis Point
${AP_TABLE}             manageObject:form:T_data
# navigator cascade dds (mandatory) — PU C:1 -> Area C:2 -> Facility Class 1 C:3 (Date is C:0, optional)
${AP_NAV_PU}            nav:form:G:0:R:1:C:1:dd
${AP_NAV_AREA}          nav:form:G:0:R:1:C:2:dd
${AP_NAV_FCTY}          nav:form:G:0:R:1:C:3:dd
# objectForm field IDs (Insert) — Start Date at R:0, Code R:2, Name R:3, Type R:4 (recon order)
${AP_INS_DATE}          tab:tabPanel:objectForm:form:G:0:R:0:C:1:da_input
${AP_INS_CODE}          tab:tabPanel:objectForm:form:G:0:R:2:C:1:in
${AP_INS_NAME}          tab:tabPanel:objectForm:form:G:0:R:3:C:1:in
${AP_INS_TYPE}          tab:tabPanel:objectForm:form:G:0:R:4:C:1:dd
# groupmodel link dds (mandatory-in-effect for grid visibility) — set = nav scope
${AP_INS_OP_PU}         tab:tabPanel:objectForm:form:G:0:R:10:C:1:dd
${AP_INS_OP_AREA}       tab:tabPanel:objectForm:form:G:0:R:11:C:1:dd
${AP_INS_OP_FCTY}       tab:tabPanel:objectForm:form:G:0:R:12:C:1:dd
# updateAttributes field IDs (Update)
${AP_UPD_CODE}          tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${AP_UPD_NAME}          tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${AP_DEL_ENDDATE}       tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Analysis Point Screen
    [Documentation]    Suite Setup: launch, login, navigate, set the PU/Area/Facility cascade and apply
    ...    (grid empty until the cascade + GO).
    [Arguments]    ${pu}    ${area}    ${facility}    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${AP_SCREEN}    ${user}    ${pass}
    Select EC Dropdown Option    ${AP_NAV_PU}    ${pu}
    Select EC Dropdown Option    ${AP_NAV_AREA}    ${area}
    Select EC Dropdown Option    ${AP_NAV_FCTY}    ${facility}
    Apply Navigator

Analysis Point Row Should Exist
    [Documentation]    Assert an analysis point with ${code} is present. The OV-GM grid redraws lazily
    ...    after Save+GO, so wait for the row span before the instant first-cell read (R17).
    [Arguments]    ${code}
    Wait For Elements State
    ...    xpath=//tbody[@id='${AP_TABLE}']//span[normalize-space(text())='${code}']
    ...    visible    timeout=20s
    Row Should Exist    ${AP_TABLE}    ${code}

Analysis Point Row Should Not Exist
    [Documentation]    Assert an analysis point with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${AP_TABLE}    ${code}

Analysis Point Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in ov_analysis_point.
    [Arguments]    ${code}
    Code Should Be Present In View    ov_analysis_point    ${code}

Analysis Point Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from ov_analysis_point.
    [Arguments]    ${code}
    Code Should Be Absent In View    ov_analysis_point    ${code}

Analysis Point Row Should Show Name
    [Documentation]    Assert the Analysis Point row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${AP_TABLE}    ${code}    ${name}

Insert Analysis Point Record
    [Documentation]    Insert: New Object → Code/Name/Start Date + Type (first option) + Op PU/Area/Facility
    ...    = the nav scope (groupmodel link — required for the row to list) → Save.
    [Arguments]    ${code}    ${name}    ${start_date}    ${pu}    ${area}    ${facility}    # robocop: off=LEN07
    Fill New Object Form    ${AP_INS_CODE}    ${AP_INS_NAME}    ${AP_INS_DATE}    ${code}    ${name}    ${start_date}
    Select First EC Dropdown Option    ${AP_INS_TYPE}
    Select EC Dropdown Option    ${AP_INS_OP_PU}    ${pu}
    Select EC Dropdown Option    ${AP_INS_OP_AREA}    ${area}
    Select EC Dropdown Option    ${AP_INS_OP_FCTY}    ${facility}
    Save And Refresh List

Update Analysis Point Name
    [Documentation]    Select the analysis point, confirm it loaded, edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${AP_TABLE}    ${AP_UPD_CODE}    ${AP_UPD_NAME}    ${code}    ${new_name}

Delete Analysis Point
    [Documentation]    Select the analysis point, set End Date = Start Date (true delete), Save.
    ...    Versioned GM grids redraw lazily — one extra Apply Navigator before asserting.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${AP_TABLE}    ${AP_DEL_ENDDATE}    ${code}    ${date}
    Apply Navigator
