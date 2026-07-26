*** Settings ***
Documentation       T3 (screen) - Port page object.
...                 Screen: Configuration > Assets > Transport Objects > Port (CO.2003). Manage-Object (OV) screen.
...                 OV object-config: Code / Name / Start Date mandatory (Country/Canal/Time Zone/Carrier
...                 dropdowns all optional). NO hardcoded field ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE};
...                 fields resolved by LABEL via T2 (Fill OV * By Label). Thin IUD wrappers over T2 + T1.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${PORT_SCREEN}          Port
# NO hardcoded ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE}; fields resolved by LABEL (T2 Fill OV * By Label).
# Field labels (from recon): Code="Port Code" Name="Port Name" Date="Start Date" End="End Date".


*** Keywords ***
Open Port Screen
    [Documentation]    Suite Setup: launch, login, open Port, load the list (GO).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${PORT_SCREEN}    ${user}    ${pass}
    Apply Navigator    # grid needs GO to populate (no default rows on open)

Port Row Should Exist
    [Documentation]    Assert a port with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Port Row Should Not Exist
    [Documentation]    Assert a port with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Port Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_PORT.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_PORT    ${code}

Port Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_PORT.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_PORT    ${code}

Port Row Should Show Name
    [Documentation]    Assert the Port row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${OV_MANAGE_OBJECT_TABLE}    ${code}    ${name}

Insert Port Record
    [Documentation]    Insert a new port: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label    objectForm    Port Code    ${code}
    Fill OV Field By Label    objectForm    Port Name    ${name}
    Fill OV Date By Label    objectForm    Start Date    ${start_date}
    Save
    Apply Navigator

Update Port Name
    [Documentation]    Select the port, confirm it loaded (code id resolved by label), edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    Port Code
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill OV Field By Label    updateAttributes    Port Name    ${new_name}
    Save
    Apply Navigator

Delete Port
    [Documentation]    Select the port, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    Fill OV Date By Label    objectdates    End Date    ${date}
    Save
    Apply Navigator
