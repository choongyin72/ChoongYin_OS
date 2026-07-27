*** Settings ***
Documentation       T3 (screen) - Task Process page object.
...                 Screen: Configuration > Task_List > Task Process (CO.0191). Manage-Object (OV) screen.
...                 OV object-config: Code / Name / Start Date mandatory (optional dropdowns skipped).
...                 NO hardcoded field ids: grid = shared T2 ${SCREEN_GRID};
...                 fields resolved by LABEL via T2 (Fill OV * By Label). Thin IUD wrappers over T2 + T1.

Library             Browser
Library             ../../../libraries/DbVerify.py
Resource            ../../../resources/common.resource
Resource            ../../../resources/manage_object.resource


*** Variables ***
${SCREEN_NAME}          Task Process
${SCREEN_GRID}          nav:form:T_data
# NO hardcoded ids: grid = shared T2 ${SCREEN_GRID}; fields resolved by LABEL (T2 Fill OV * By Label).
# Field labels (from recon): Code="Task Process Code" Name="Task Process Name" Date="Start date" End="End date".


*** Keywords ***
Open Task Process Screen
    [Documentation]    Suite Setup: launch, login, open Task Process, load the list (GO).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCREEN_NAME}    ${user}    ${pass}
    Refresh Screen    # custom-URL OV: no GO; grid loads on open, toolbar Refresh after writes

Task Process Row Should Exist
    [Documentation]    Assert a task_process with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${SCREEN_GRID}    ${code}

Task Process Row Should Not Exist
    [Documentation]    Assert a task_process with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${SCREEN_GRID}    ${code}

Task Process Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_TASK_PROCESS.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_TASK_PROCESS    ${code}

Task Process Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_TASK_PROCESS.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_TASK_PROCESS    ${code}

Task Process Row Should Show Name
    [Documentation]    Assert the Task Process row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${SCREEN_GRID}    ${code}    ${name}

Insert Task Process Record
    [Documentation]    Insert a new task_process: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label    objectForm    Task Process Code    ${code}
    Fill OV Field By Label    objectForm    Task Process Name    ${name}
    Fill OV Date By Label    objectForm    Start date    ${start_date}
    Save And Refresh List

Update Task Process Name
    [Documentation]    Select the task_process, confirm it loaded (code id resolved by label), edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${SCREEN_GRID}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    Task Process Code
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill OV Field By Label    updateAttributes    Task Process Name    ${new_name}
    Save And Refresh List

Delete Task Process
    [Documentation]    Select the task_process, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${SCREEN_GRID}    ${code}
    Fill OV Date By Label    objectdates    End date    ${date}
    Save And Refresh List
