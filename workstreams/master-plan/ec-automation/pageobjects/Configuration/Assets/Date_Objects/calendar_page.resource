*** Settings ***
Documentation       T3 (screen) -- Calendar page object.
...                 Screen: Configuration > Assets > Date Objects > Calendar (CD.0024).
...                 Manage-Object (OV, date-effective) screen. Plain Bank-family OV:
...                 the New-Object form mandatory set is just Code/Name/Start Date; the
...                 7 weekday indicator cells (R:6-R:12, MONDAY_IND..SUNDAY_IND) are
...                 optional checkboxes left at default. DELETE = End Date = Start Date.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${CAL_SCREEN}           Calendar
# Calendar is a custom-URL OV: grid is nav:form:T_data and there is NO navigator GO
# (Save And Refresh List falls back to toolbar Refresh) -- cf. Account / Regulatory Permits.
${CAL_TABLE}            nav:form:T_data
${CAL_VIEW}             ov_calendar
# objectForm field IDs (Insert -- new object)
${CAL_INS_CODE}         tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${CAL_INS_NAME}         tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${CAL_INS_DATE}         tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
# updateAttributes field IDs (Update -- Code read-only after creation)
${CAL_UPD_CODE}         tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${CAL_UPD_NAME}         tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete -- End Date = Start Date)
${CAL_DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Calendar Screen
    [Documentation]    Suite Setup: launch, login as ${user} (defaults to env user), open Calendar.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${CAL_SCREEN}    ${user}    ${pass}

Calendar Row Should Exist
    [Documentation]    Assert a Calendar with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${CAL_TABLE}    ${code}

Calendar Row Should Not Exist
    [Documentation]    Assert a Calendar with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${CAL_TABLE}    ${code}

Calendar Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in ov_calendar.
    [Arguments]    ${code}
    Code Should Be Present In View    ${CAL_VIEW}    ${code}

Calendar Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from ov_calendar.
    [Arguments]    ${code}
    Code Should Be Absent In View    ${CAL_VIEW}    ${code}

Calendar Row Should Show Name
    [Documentation]    Assert the Calendar row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${CAL_TABLE}    ${code}    ${name}

Insert Calendar Record
    [Documentation]    Insert a new Calendar: New Object form -> Code/Name/Start Date -> Save + reload.
    ...    Weekday indicator checkboxes are optional -> left at default.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${CAL_INS_CODE}    ${CAL_INS_NAME}    ${CAL_INS_DATE}    ${code}    ${name}    ${start_date}
    Save And Refresh List

Update Calendar Name
    [Documentation]    Select the object by code (proves it loaded), edit Name, Save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${CAL_TABLE}    ${CAL_UPD_CODE}    ${CAL_UPD_NAME}    ${code}    ${new_name}

Delete Calendar
    [Documentation]    Select the object, set End Date = Start Date (true delete), Save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${CAL_TABLE}    ${CAL_DEL_ENDDATE}    ${code}    ${date}
