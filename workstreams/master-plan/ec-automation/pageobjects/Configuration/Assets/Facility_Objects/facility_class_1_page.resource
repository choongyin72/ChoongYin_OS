*** Settings ***
Documentation       T3 (screen) - Facility Class 1 page object.
...                 Screen: Configuration > Assets > Facility_Objects > Facility Class 1.
...                 OV-GM (manage-object, groupmodel): the grid loads ONLY after the navigator
...                 cascade + GO. Genuine 2-level PU->Area cascade (C:1/C:2 same row, C:3 absent -
...                 confirmed live 2026-08-26, tmp/recon_fc1_navigator_cascade.py). Navigator fill
...                 delegates to the shared T2 "Apply Navigator From Properties"
...                 (resources/manage_object.resource, added 2026-08-26), driven by
...                 testdata/facility_class_1_navigator.properties, instead of the previous
...                 "Apply OV-GM Navigator First Available" - same live-confirmed values
...                 first-available already picked (AS1 EC Exploration Norway -> AS1_Area), now
...                 EXPLICIT. Form fields resolved BY LABEL (no hardcoded rows). No Op Production
...                 Unit field or extra dropdowns on this screen's insert/update forms (confirmed
...                 live) - the ${GM_PU} suite variable this keyword still returns is not read by
...                 Insert/Update Facility Class 1 keywords, kept only so
...                 tests/.../facility_class_1_iud.robot's existing `${pu}= Open Facility Class 1
...                 Screen` call (out of scope for this task) keeps working unchanged.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${SCR}              Facility Class 1
${TBL}              manageObject:form:T_data
${DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
${GM_PU}            ${EMPTY}
${FC1_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/facility_class_1_navigator.properties


*** Keywords ***
Open Facility Class 1 Screen
    [Documentation]    Suite Setup: launch, login, navigate, fill the 2-level PU->Area navigator
    ...    cascade with the EXPLICIT values from testdata/facility_class_1_navigator.properties
    ...    (via the shared T2 "Apply Navigator From Properties") + GO, RETURN the top-parent PU
    ...    (grid empty until then) - same return contract as before this conversion.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCR}    ${user}    ${pass}
    ${data}=    Read Properties    ${FC1_NAVIGATOR_PROPERTIES}
    Apply Navigator From Properties    ${FC1_NAVIGATOR_PROPERTIES}
    RETURN    ${data}[Op Production Unit]

Facility Class 1 Row Should Exist
    [Documentation]    Assert ${code} is present (await lazy OV-GM redraw first).
    [Arguments]    ${code}
    Wait For Elements State
    ...    xpath=//tbody[@id='${TBL}']//span[normalize-space(text())='${code}']
    ...    visible    timeout=20s
    Row Should Exist    ${TBL}    ${code}

Facility Class 1 Row Should Not Exist
    [Documentation]    Assert ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${TBL}    ${code}

Facility Class 1 Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} persisted in OV_FCTY_CLASS_1.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_FCTY_CLASS_1    ${code}

Facility Class 1 Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} deleted from OV_FCTY_CLASS_1.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_FCTY_CLASS_1    ${code}

Facility Class 1 Row Should Show Name
    [Documentation]    Assert the row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${TBL}    ${code}    ${name}

Insert Facility Class 1 Record
    [Documentation]    Insert (all fields BY LABEL) + Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label       objectForm    Facility Class 1 Code    ${code}
    Fill OV Field By Label       objectForm    Facility Class 1 Name    ${name}
    Fill OV Date By Label        objectForm    Start Date    ${start_date}
    Save And Refresh List

Update Facility Class 1 Name
    [Documentation]    Select the row, edit Name (by label), save + reload.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${TBL}    ${code}
    Fill OV Field By Label    updateAttributes    Facility Class 1 Name    ${new_name}
    Save And Refresh List

Delete Facility Class 1
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${TBL}    ${DEL_ENDDATE}    ${code}    ${date}
    Apply Navigator
