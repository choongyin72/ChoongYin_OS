*** Settings ***
Documentation       T3 (screen) -- Calendar Collection page object.
...                 Screen: Configuration > Assets > Date Objects > Calendar Collection (CD.0105).
...                 Manage-Object (OV, date-effective) screen. Plain Bank-family OV:
...                 the New-Object form mandatory set is just Code/Name/Start Date; the
...                 7 weekday indicator cells (R:6-R:12, MONDAY_IND..SUNDAY_IND) are
...                 optional checkboxes left at default. DELETE = End Date = Start Date.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${CC_SCREEN}           Calendar Collection
# Calendar Collection is a custom-URL OV: grid is nav:form:T_data and there is NO navigator GO
# (Save And Refresh List falls back to toolbar Refresh) -- cf. Account / Regulatory Permits.
${CC_TABLE}            nav:form:T_data
${CC_VIEW}             ov_calendar_collection
# objectForm field IDs (Insert -- new object)
${CC_INS_CODE}         tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${CC_INS_NAME}         tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${CC_INS_DATE}         tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
# updateAttributes field IDs (Update -- Code read-only after creation)
${CC_UPD_CODE}         tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${CC_UPD_NAME}         tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete -- End Date = Start Date)
${CC_DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Calendar Collection Screen
    [Documentation]    Suite Setup: launch, login as ${user} (defaults to env user), open Calendar Collection.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${CC_SCREEN}    ${user}    ${pass}

Calendar Collection Row Should Exist
    [Documentation]    Assert a Calendar Collection with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${CC_TABLE}    ${code}

Calendar Collection Row Should Not Exist
    [Documentation]    Assert a Calendar Collection with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${CC_TABLE}    ${code}

Calendar Collection Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in ov_calendar_collection.
    [Arguments]    ${code}
    Code Should Be Present In View    ${CC_VIEW}    ${code}

Calendar Collection Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from ov_calendar_collection.
    [Arguments]    ${code}
    Code Should Be Absent In View    ${CC_VIEW}    ${code}

Calendar Collection Row Should Show Name
    [Documentation]    Assert the Calendar Collection row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${CC_TABLE}    ${code}    ${name}

Insert Calendar Collection Record
    [Documentation]    Insert a new Calendar Collection: New Object form -> Code/Name/Start Date -> Save + reload.
    ...    Weekday indicator checkboxes are optional -> left at default.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${CC_INS_CODE}    ${CC_INS_NAME}    ${CC_INS_DATE}    ${code}    ${name}    ${start_date}
    Save And Refresh List

Update Calendar Collection Name
    [Documentation]    Select the object by code (proves it loaded), edit Name, Save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${CC_TABLE}    ${CC_UPD_CODE}    ${CC_UPD_NAME}    ${code}    ${new_name}

Delete Calendar Collection
    [Documentation]    Select the object, set End Date = Start Date (true delete), Save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${CC_TABLE}    ${CC_DEL_ENDDATE}    ${code}    ${date}
