*** Settings ***
Documentation       T3 (screen) — Country page object.
...                 Screen: Configuration > Assets > Basic Objects > Country.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${COUNTRY_SCREEN}           Country
${COUNTRY_TABLE}            manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert — new object)
${COUNTRY_INS_CODE}         tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${COUNTRY_INS_NAME}         tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${COUNTRY_INS_DATE}         tab:tabPanel:objectForm:form:G:0:R:5:C:1:da_input
# updateAttributes field IDs (Update — existing object)
${COUNTRY_UPD_CODE}         tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${COUNTRY_UPD_NAME}         tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${COUNTRY_DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Country Screen
    [Documentation]    Suite Setup: launch, login as ${user} (defaults to the env
    ...    user), navigate to the Country screen. Pass a different user for role tests.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${COUNTRY_SCREEN}    ${user}    ${pass}

Country Row Should Exist
    [Documentation]    Assert a country with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${COUNTRY_TABLE}    ${code}

Country Row Should Not Exist
    [Documentation]    Assert a country with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${COUNTRY_TABLE}    ${code}

Country Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_COUNTRY.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_COUNTRY    ${code}

Country Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_COUNTRY.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_COUNTRY    ${code}

Country Row Should Show Name
    [Documentation]    Assert the Country row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${COUNTRY_TABLE}    ${code}    ${name}

Insert Country Record
    [Documentation]    Insert a new country: Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${COUNTRY_INS_CODE}    ${COUNTRY_INS_NAME}    ${COUNTRY_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Save And Refresh List

Update Country Name
    [Documentation]    Select the country, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${COUNTRY_TABLE}    ${COUNTRY_UPD_CODE}    ${COUNTRY_UPD_NAME}    ${code}    ${new_name}

Delete Country
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${COUNTRY_TABLE}    ${COUNTRY_DEL_ENDDATE}    ${code}    ${date}
