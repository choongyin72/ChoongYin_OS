*** Settings ***
Documentation       T3 (screen) - Calculation Library page object.
...                 Screen: Configuration > Assets > Calculation_Objects > Calculation Library (CO.1060). Manage-Object (OV) screen.
...                 OV object-config: Code / Name / Start Date mandatory (optional dropdowns skipped).
...                 NO hardcoded field ids: grid = shared T2 ${SCREEN_GRID};
...                 fields resolved by LABEL via T2 (Fill OV * By Label). Thin IUD wrappers over T2 + T1.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${SCREEN_NAME}          Calculation Library
${SCREEN_GRID}          nav:form:T_data
# NO hardcoded ids: grid = shared T2 ${SCREEN_GRID}; fields resolved by LABEL (T2 Fill OV * By Label).
# Field labels (from recon): Code="Calc Library Code" Name="Calc Library Name" Date="Start Date" End="End Date".


*** Keywords ***
Open Calculation Library Screen
    [Documentation]    Suite Setup: launch, login, open Calculation Library, load the list (GO).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCREEN_NAME}    ${user}    ${pass}
    Refresh Screen    # custom-URL OV: no GO; grid loads on open, toolbar Refresh after writes

Calculation Library Row Should Exist
    [Documentation]    Assert a calculation_library with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${SCREEN_GRID}    ${code}

Calculation Library Row Should Not Exist
    [Documentation]    Assert a calculation_library with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${SCREEN_GRID}    ${code}

Calculation Library Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_CALC_LIBRARY.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_CALC_LIBRARY    ${code}

Calculation Library Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_CALC_LIBRARY.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_CALC_LIBRARY    ${code}

Calculation Library Row Should Show Name
    [Documentation]    Assert the Calculation Library row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${SCREEN_GRID}    ${code}    ${name}

Insert Calculation Library Record
    [Documentation]    Insert a new calculation_library: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label    objectForm    Calc Library Code    ${code}
    Fill OV Field By Label    objectForm    Calc Library Name    ${name}
    Fill OV Date By Label    objectForm    Start Date    ${start_date}
    Save And Refresh List

Update Calculation Library Name
    [Documentation]    Select the calculation_library, confirm it loaded (code id resolved by label), edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${SCREEN_GRID}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    Calc Library Code
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill OV Field By Label    updateAttributes    Calc Library Name    ${new_name}
    Save And Refresh List

Delete Calculation Library
    [Documentation]    Select the calculation_library, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${SCREEN_GRID}    ${code}
    Fill OV Date By Label    objectdates    End Date    ${date}
    Save And Refresh List
