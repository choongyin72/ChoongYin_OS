*** Settings ***
Documentation       T3 (screen) - Cargo Planning Forecast page object.
...                 Screen: EC Transport > Cargo Planning > Forecast > Cargo Planning Forecast (CP.0030).
...                 Custom layout: navigator = PER-FIELD groups nav:form:G:1..G:4:R:1:C:0 (PU ->
...                 Area -> FC1 -> Storage), SPECIFIC P1 values; grid fcst:form:T_data; the
...                 new_fcst panel + COPY buttons = the copy-existing dialog (owner-confirmed,
...                 NOT used) - the standard objectForm is the insert form. Mandatory extra:
...                 END DATE (row must SPAN the nav date to list). Storage Name = nav Storage.
...                 View OV_FCST_MNGR_FCST_LIST (resolved empirically; row also lands in
...                 OV_FORECAST_TRAN_CP - both over base FORECAST). DELETE = End Date = Start Date.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Resource            ../../../../resources/navigator.resource


*** Variables ***
${SCR}              Cargo Planning Forecast
${TBL}              fcst:form:T_data
${DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
${CPF_NAV_PU}       P1 Production Unit
${CPF_NAV_AREA}     P1 Area
${CPF_NAV_FC1}      P1 Facility 1
${CPF_NAV_STORAGE}    P1_CRUDE_STOR
${CPF_END_DATE}     2026-12-31


*** Keywords ***
Open Cargo Planning Forecast Screen
    [Documentation]    Suite Setup: launch, login, open the screen, apply the SPECIFIC 4-level
    ...    P1 navigator scope (per-field groups incl. Storage) + GO.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCR}    ${user}    ${pass}
    Apply Cargo Planning Forecast Navigator

Apply Cargo Planning Forecast Navigator
    [Documentation]    Fill nav groups G:1..G:4 (each R:1:C:0) with the owner-provided P1 values
    ...    incl. Storage, then GO. Layout differs from the standard single-row cascade.
    Select EC Dropdown Option    nav:form:G:1:R:1:C:0:dd    ${CPF_NAV_PU}
    Sleep    0.7s
    Select EC Dropdown Option    nav:form:G:2:R:1:C:0:dd    ${CPF_NAV_AREA}
    Sleep    0.7s
    Select EC Dropdown Option    nav:form:G:3:R:1:C:0:dd    ${CPF_NAV_FC1}
    Sleep    0.7s
    Select EC Dropdown Option    nav:form:G:4:R:1:C:0:dd    ${CPF_NAV_STORAGE}
    Sleep    0.7s
    Apply Navigator

Cargo Planning Forecast Row Should Exist
    [Documentation]    Assert ${code} is present (await lazy redraw first).
    [Arguments]    ${code}
    Wait For Elements State
    ...    xpath=//tbody[@id='${TBL}']//span[normalize-space(text())='${code}']
    ...    visible    timeout=20s
    Row Should Exist    ${TBL}    ${code}

Cargo Planning Forecast Row Should Not Exist
    [Documentation]    Assert ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${TBL}    ${code}

Cargo Planning Forecast Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} persisted in OV_FCST_MNGR_FCST_LIST.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_FCST_MNGR_FCST_LIST    ${code}

Cargo Planning Forecast Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} deleted from OV_FCST_MNGR_FCST_LIST.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_FCST_MNGR_FCST_LIST    ${code}

Cargo Planning Forecast Row Should Show Name
    [Documentation]    Assert the row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${TBL}    ${code}    ${name}

Insert Cargo Planning Forecast Record
    [Documentation]    Insert (all fields BY LABEL) + Save: mandatory End Date (spans the nav date)
    ...    + Storage Name = nav Storage (parent-matching). COPY buttons untouched.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label       objectForm    Cargo Planning Forecast Code    ${code}
    Fill OV Field By Label       objectForm    Cargo Planning Forecast Name    ${name}
    Fill OV Date By Label        objectForm    Start Date    ${start_date}
    Fill OV Date By Label        objectForm    End Date    ${CPF_END_DATE}
    Fill OV Dropdown By Label    objectForm    Storage Name    ${CPF_NAV_STORAGE}
    Save And Refresh List

Update Cargo Planning Forecast Name
    [Documentation]    Select the row, edit Name (by label), save + reload.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${TBL}    ${code}
    Fill OV Field By Label    updateAttributes    Cargo Planning Forecast Name    ${new_name}
    Save And Refresh List

Delete Cargo Planning Forecast
    [Documentation]    Delete via End Date = Start Date (proven true delete on this screen despite
    ...    the mandatory insert End Date), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${TBL}    ${DEL_ENDDATE}    ${code}    ${date}
