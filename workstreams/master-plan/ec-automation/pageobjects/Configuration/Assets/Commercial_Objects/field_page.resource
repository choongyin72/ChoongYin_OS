*** Settings ***
Documentation       T3 (screen) — Field page object.
...                 Screen: Configuration > Assets > Commercial Objects > Field.
...                 Manage-Object (OV-GM groupmodel) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${FIELD_SCREEN}         Field
${FIELD_TABLE}          manageObject:form:T_data
# groupmodel navigator dropdown — MANDATORY before the grid loads
${FIELD_NAV0}           nav:form:G:0:R:1:C:1:dd
# objectForm field IDs (Insert — new object); rows derived from recon LABELS
${FIELD_INS_CODE}       tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${FIELD_INS_NAME}       tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${FIELD_INS_DATE}       tab:tabPanel:objectForm:form:G:0:R:6:C:1:da_input
# Geo Area links the object into the groupmodel/navigator context
${FIELD_INS_VDD0}       tab:tabPanel:objectForm:form:G:0:R:11:C:1:dd
# updateAttributes field IDs (Update — existing object)
${FIELD_UPD_CODE}       tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${FIELD_UPD_NAME}       tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${FIELD_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Field Screen
    [Documentation]    Suite Setup: launch, login, navigate to the Field screen and set the groupmodel navigator context.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${FIELD_SCREEN}    ${user}    ${pass}
    Select EC Dropdown Option    ${FIELD_NAV0}    Offshore area
    Apply Navigator

Field Row Should Exist
    [Documentation]    Assert a field with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${FIELD_TABLE}    ${code}

Field Row Should Not Exist
    [Documentation]    Assert a field with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${FIELD_TABLE}    ${code}

Field Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_FIELD.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_FIELD    ${code}

Field Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_FIELD.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_FIELD    ${code}

Field Row Should Show Name
    [Documentation]    Assert the Field row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${FIELD_TABLE}    ${code}    ${name}

Insert Field Record
    [Documentation]    Insert a new field: Code/Name/Start Date + mandatory extras -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${FIELD_INS_CODE}    ${FIELD_INS_NAME}    ${FIELD_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Select EC Dropdown Option    ${FIELD_INS_VDD0}    Offshore area
    Save And Refresh List

Update Field Name
    [Documentation]    Select the field, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${FIELD_TABLE}    ${FIELD_UPD_CODE}    ${FIELD_UPD_NAME}    ${code}    ${new_name}

Delete Field
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${FIELD_TABLE}    ${FIELD_DEL_ENDDATE}    ${code}    ${date}
    # versioned groupmodel grids redraw lazily after a delete
    Apply Navigator
