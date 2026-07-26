*** Settings ***
Documentation       T3 (screen) - Calculation Context page object.
...                 Screen: Configuration > Assets > Calculation_Objects > Calculation Context (CO.1059). Manage-Object (OV) screen.
...                 OV object-config: Code / Name / Start Date mandatory (optional dropdowns skipped).
...                 NO hardcoded field ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE};
...                 fields resolved by LABEL via T2 (Fill OV * By Label). Thin IUD wrappers over T2 + T1.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${CALCULATION_CONTEXT_SCREEN}          Calculation Context
# NO hardcoded ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE}; fields resolved by LABEL (T2 Fill OV * By Label).
# Field labels (from recon): Code="Calc Context Code" Name="Calc Context Name" Date="Start Date" End="End Date".


*** Keywords ***
Open Calculation Context Screen
    [Documentation]    Suite Setup: launch, login, open Calculation Context, load the list (GO).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${CALCULATION_CONTEXT_SCREEN}    ${user}    ${pass}
    Apply Navigator    # grid needs GO to populate (no default rows on open)

Calculation Context Row Should Exist
    [Documentation]    Assert a calculation_context with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Calculation Context Row Should Not Exist
    [Documentation]    Assert a calculation_context with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Calculation Context Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_CALC_CONTEXT.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_CALC_CONTEXT    ${code}

Calculation Context Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_CALC_CONTEXT.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_CALC_CONTEXT    ${code}

Calculation Context Row Should Show Name
    [Documentation]    Assert the Calculation Context row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${OV_MANAGE_OBJECT_TABLE}    ${code}    ${name}

Insert Calculation Context Record
    [Documentation]    Insert a new calculation_context: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label    objectForm    Calc Context Code    ${code}
    Fill OV Field By Label    objectForm    Calc Context Name    ${name}
    Fill OV Date By Label    objectForm    Start Date    ${start_date}
    Save
    Apply Navigator

Update Calculation Context Name
    [Documentation]    Select the calculation_context, confirm it loaded (code id resolved by label), edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    Calc Context Code
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill OV Field By Label    updateAttributes    Calc Context Name    ${new_name}
    Save
    Apply Navigator

Delete Calculation Context
    [Documentation]    Select the calculation_context, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    Fill OV Date By Label    objectdates    End Date    ${date}
    Save
    Apply Navigator
