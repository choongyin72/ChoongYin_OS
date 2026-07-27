*** Settings ***
Documentation       T3 (screen) - Conversion Group page object.
...                 Screen: Configuration > System > Units > Conversion Group (CO.1049). Manage-Object (OV) screen.
...                 OV object-config: Code / Name / Start Date mandatory (optional dropdowns skipped).
...                 NO hardcoded field ids: grid = shared T2 ${SCREEN_GRID};
...                 fields resolved by LABEL via T2 (Fill OV * By Label). Thin IUD wrappers over T2 + T1.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${SCREEN_NAME}          Conversion Group
${SCREEN_GRID}          nav:form:T_data
# NO hardcoded ids: grid = shared T2 ${SCREEN_GRID}; fields resolved by LABEL (T2 Fill OV * By Label).
# Field labels (from recon): Code="Conversion Group Code" Name="Conversion Group Name" Date="Start Date" End="End Date".


*** Keywords ***
Open Conversion Group Screen
    [Documentation]    Suite Setup: launch, login, open Conversion Group, load the list (GO).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCREEN_NAME}    ${user}    ${pass}
    Refresh Screen    # custom-URL OV: no GO; grid loads on open, toolbar Refresh after writes

Conversion Group Row Should Exist
    [Documentation]    Assert a conversion_group with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${SCREEN_GRID}    ${code}

Conversion Group Row Should Not Exist
    [Documentation]    Assert a conversion_group with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${SCREEN_GRID}    ${code}

Conversion Group Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_CONVERSION_GROUP.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_CONVERSION_GROUP    ${code}

Conversion Group Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_CONVERSION_GROUP.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_CONVERSION_GROUP    ${code}

Conversion Group Row Should Show Name
    [Documentation]    Assert the Conversion Group row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${SCREEN_GRID}    ${code}    ${name}

Insert Conversion Group Record
    [Documentation]    Insert a new conversion_group: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label    objectForm    Conversion Group Code    ${code}
    Fill OV Field By Label    objectForm    Conversion Group Name    ${name}
    Fill OV Date By Label    objectForm    Start Date    ${start_date}
    Save And Refresh List

Update Conversion Group Name
    [Documentation]    Select the conversion_group, confirm it loaded (code id resolved by label), edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${SCREEN_GRID}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    Conversion Group Code
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill OV Field By Label    updateAttributes    Conversion Group Name    ${new_name}
    Save And Refresh List

Delete Conversion Group
    [Documentation]    Select the conversion_group, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${SCREEN_GRID}    ${code}
    Fill OV Date By Label    objectdates    End Date    ${date}
    Save And Refresh List
