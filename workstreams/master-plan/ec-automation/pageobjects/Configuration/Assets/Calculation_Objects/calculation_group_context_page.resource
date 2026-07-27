*** Settings ***
Documentation       T3 (screen) - Calculation Group Context page object.
...                 Screen: Configuration > Assets > Calculation_Objects > Calculation Group Context (CO.0245). Manage-Object (OV) screen.
...                 OV object-config: Code / Name / Start Date mandatory (optional dropdowns skipped).
...                 NO hardcoded field ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE};
...                 fields resolved by LABEL via T2 (Fill OV * By Label). Thin IUD wrappers over T2 + T1.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${SCREEN_NAME}          Calculation Group Context
# NO hardcoded ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE}; fields resolved by LABEL (T2 Fill OV * By Label).
# Field labels (from recon): Code="Calculation Group Context Code" Name="Calculation Group Context Name" Date="Start Date" End="End Date".


*** Keywords ***
Open Calculation Group Context Screen
    [Documentation]    Suite Setup: launch, login, open Calculation Group Context, load the list (GO).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCREEN_NAME}    ${user}    ${pass}
    Apply Navigator    # grid needs GO to populate (no default rows on open)

Calculation Group Context Row Should Exist
    [Documentation]    Assert a calculation_group_context with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Calculation Group Context Row Should Not Exist
    [Documentation]    Assert a calculation_group_context with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Calculation Group Context Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_CALC_GRP_CONTEXT.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_CALC_GRP_CONTEXT    ${code}

Calculation Group Context Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_CALC_GRP_CONTEXT.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_CALC_GRP_CONTEXT    ${code}

Calculation Group Context Row Should Show Name
    [Documentation]    Assert the Calculation Group Context row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${OV_MANAGE_OBJECT_TABLE}    ${code}    ${name}

Insert Calculation Group Context Record
    [Documentation]    Insert a new calculation_group_context: New Object form -> Code/Name/Start Date (+ mandatory dropdowns/extra fields) -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label    objectForm    Calculation Group Context Code    ${code}
    Fill OV Field By Label    objectForm    Calculation Group Context Name    ${name}
    Fill OV Date By Label    objectForm    Start Date    ${start_date}
    Fill Calculation Group Context Mandatory Extras
    Save
    Apply Navigator

Fill Calculation Group Context Mandatory Extras
    [Documentation]    Fill the mandatory dropdown(s) + extra field(s) for Calculation Group Context, split out of Insert to keep
    ...    the Insert keyword within the keyword-count limit. All label-driven (no hardcoded ids).
    Fill OV Dropdown By Label    objectForm    Calculation Group Object Class    __FIRST__
    Fill OV Dropdown By Label    objectForm    Calculation Group List Class    __FIRST__

Update Calculation Group Context Name
    [Documentation]    Select the calculation_group_context, confirm it loaded (code id resolved by label), edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    Calculation Group Context Code
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill OV Field By Label    updateAttributes    Calculation Group Context Name    ${new_name}
    Save
    Apply Navigator

Delete Calculation Group Context
    [Documentation]    Select the calculation_group_context, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    Fill OV Date By Label    objectdates    End Date    ${date}
    Save
    Apply Navigator
