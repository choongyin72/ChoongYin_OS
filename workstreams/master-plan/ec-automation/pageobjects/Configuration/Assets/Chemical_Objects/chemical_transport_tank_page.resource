*** Settings ***
Documentation       T3 (screen) - Chemical Transport Tank page object.
...                 Screen: Configuration > Assets > Chemical_Objects > Chemical Transport Tank (CO.0257). Manage-Object (OV) screen.
...                 OV object-config: Code / Name / Start Date mandatory (optional dropdowns skipped).
...                 NO hardcoded field ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE};
...                 fields resolved by LABEL via T2 (Fill OV * By Label). Thin IUD wrappers over T2 + T1.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${CHEMICAL_TRANSPORT_TANK_SCREEN}          Chemical Transport Tank
# NO hardcoded ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE}; fields resolved by LABEL (T2 Fill OV * By Label).
# Field labels (from recon): Code="Transport Tank Code" Name="Transport Tank Name" Date="Start Date" End="End Date".


*** Keywords ***
Open Chemical Transport Tank Screen
    [Documentation]    Suite Setup: launch, login, open Chemical Transport Tank, load the list (GO).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${CHEMICAL_TRANSPORT_TANK_SCREEN}    ${user}    ${pass}
    Apply Navigator    # grid needs GO to populate (no default rows on open)

Chemical Transport Tank Row Should Exist
    [Documentation]    Assert a chemical_transport_tank with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Chemical Transport Tank Row Should Not Exist
    [Documentation]    Assert a chemical_transport_tank with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Chemical Transport Tank Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_CHEM_TRANS_TANK.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_CHEM_TRANS_TANK    ${code}

Chemical Transport Tank Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_CHEM_TRANS_TANK.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_CHEM_TRANS_TANK    ${code}

Chemical Transport Tank Row Should Show Name
    [Documentation]    Assert the Chemical Transport Tank row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${OV_MANAGE_OBJECT_TABLE}    ${code}    ${name}

Insert Chemical Transport Tank Record
    [Documentation]    Insert a new chemical_transport_tank: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label    objectForm    Transport Tank Code    ${code}
    Fill OV Field By Label    objectForm    Transport Tank Name    ${name}
    Fill OV Date By Label    objectForm    Start Date    ${start_date}
    Save
    Apply Navigator

Update Chemical Transport Tank Name
    [Documentation]    Select the chemical_transport_tank, confirm it loaded (code id resolved by label), edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    Transport Tank Code
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill OV Field By Label    updateAttributes    Transport Tank Name    ${new_name}
    Save
    Apply Navigator

Delete Chemical Transport Tank
    [Documentation]    Select the chemical_transport_tank, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    Fill OV Date By Label    objectdates    End Date    ${date}
    Save
    Apply Navigator
