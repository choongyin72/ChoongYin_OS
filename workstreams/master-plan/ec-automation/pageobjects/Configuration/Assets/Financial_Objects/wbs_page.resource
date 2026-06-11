*** Settings ***
Documentation       T3 (screen) — WBS page object.
...                 Screen: Configuration > Assets > Financial Objects > WBS.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${WBS_SCREEN}    WBS
${WBS_TABLE}    nav:form:T_data
# objectForm field IDs (Insert — new object); rows derived from recon LABELS
${WBS_INS_CODE}    tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${WBS_INS_NAME}    tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${WBS_INS_DATE}    tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
# updateAttributes field IDs (Update — existing object)
${WBS_UPD_CODE}    tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${WBS_UPD_NAME}    tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${WBS_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open WBS Screen
    [Documentation]    Suite Setup: launch, login, navigate to the WBS screen.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Open EC Browser
    Login To EC    ${user}    ${pass}
    Navigate To Screen    ${WBS_SCREEN}

WBS Row Should Exist
    [Documentation]    Assert a wbs with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${WBS_TABLE}    ${code}

WBS Row Should Not Exist
    [Documentation]    Assert a wbs with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${WBS_TABLE}    ${code}

WBS Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_FIN_WBS.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_FIN_WBS    ${code}

WBS Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_FIN_WBS.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_FIN_WBS    ${code}

WBS Row Should Show Name
    [Documentation]    Assert the WBS row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${WBS_TABLE}    ${code}    ${name}

Insert WBS Record
    [Documentation]    Insert a new wbs: Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${WBS_INS_CODE}    ${WBS_INS_NAME}    ${WBS_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Save And Refresh List

Update WBS Name
    [Documentation]    Select the wbs, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${WBS_TABLE}    ${WBS_UPD_CODE}    ${WBS_UPD_NAME}    ${code}    ${new_name}

Delete WBS
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${WBS_TABLE}    ${WBS_DEL_ENDDATE}    ${code}    ${date}
