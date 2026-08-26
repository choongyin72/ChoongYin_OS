*** Settings ***
Documentation       T3 (screen) - External Location page object.
...                 Screen: Configuration > Assets > Facility_Objects > External Location.
...                 OV-GM (manage-object, groupmodel): the grid loads on GO ALONE - the navigator has
...                 no mandatory scope (fields are optional filters). Fields resolved BY LABEL (no
...                 hardcoded rows).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${SCR}              External Location
${TBL}              manageObject:form:T_data
${DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
${GM_PU}            ${EMPTY}
# 2026-08-26: navigator fill now goes through the shared T2 "Apply Navigator From Properties"
# (resources/manage_object.resource, added for Area 2026-08-26), driven by an INTENTIONALLY EMPTY
# testdata/external_location_navigator.properties - see that file for why. This is an edge-case
# test of the shared keyword (zero properties lines -> zero fills -> GO alone), not a behaviour
# change: External Location's navigator fields remain optional filters only, no mandatory scope.
${EL_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/external_location_navigator.properties


*** Keywords ***
Open External Location Screen
    [Documentation]    Suite Setup: launch, login, navigate, GO alone (no mandatory nav scope on
    ...    this screen); RETURN the top-parent PU, which is legitimately ${EMPTY} here. Navigator
    ...    fill delegates to the shared T2 "Apply Navigator From Properties" with an empty
    ...    properties file (see ${EL_NAVIGATOR_PROPERTIES}) - degrades to a bare GO, same as before.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCR}    ${user}    ${pass}
    Apply Navigator From Properties    ${EL_NAVIGATOR_PROPERTIES}
    VAR    ${pu}    ${EMPTY}    # optional filters only - no scope value to capture
    RETURN    ${pu}

External Location Row Should Exist
    [Documentation]    Assert ${code} is present (await lazy OV-GM redraw first).
    [Arguments]    ${code}
    Wait For Elements State
    ...    xpath=//tbody[@id='${TBL}']//span[normalize-space(text())='${code}']
    ...    visible    timeout=20s
    Row Should Exist    ${TBL}    ${code}

External Location Row Should Not Exist
    [Documentation]    Assert ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${TBL}    ${code}

External Location Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} persisted in OV_EXTERNAL_LOCATION.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_EXTERNAL_LOCATION    ${code}

External Location Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} deleted from OV_EXTERNAL_LOCATION.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_EXTERNAL_LOCATION    ${code}

External Location Row Should Show Name
    [Documentation]    Assert the row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${TBL}    ${code}    ${name}

Insert External Location Record
    [Documentation]    Insert (all fields BY LABEL) + Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label       objectForm    External Location Code    ${code}
    Fill OV Field By Label       objectForm    External Location Name    ${name}
    Fill OV Date By Label        objectForm    Start Date    ${start_date}
    Save And Refresh List

Update External Location Name
    [Documentation]    Select the row, edit Name (by label), save + reload.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${TBL}    ${code}
    Fill OV Field By Label    updateAttributes    External Location Name    ${new_name}
    Save And Refresh List

Delete External Location
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${TBL}    ${DEL_ENDDATE}    ${code}    ${date}
    Apply Navigator
