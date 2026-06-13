*** Settings ***
Documentation       T3 (screen) — Pipeline page object.
...                 Screen: Configuration > Assets > Dispatching Objects > Pipeline.
...                 Full OV-GM on the OPERATIONAL groupmodel (like Area): grid loads after navigator Production Unit + GO. 30-row
...                 insert form with Latitude/Longitude FIRST — Code at R2, Name at R3,
...                 Start Date R5, End Date R6, Op Production Unit dd at R21 (set = nav PU for grid visibility). updateAttributes mirrors the same row layout.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${PIPE_SCREEN}          Pipeline
${PIPE_TABLE}           manageObject:form:T_data
# navigator: Production Unit dropdown (cascading Area/FacilityClass follow) — MANDATORY
${PIPE_NAV_PU}          nav:form:G:0:R:1:C:1:dd
# objectForm field IDs (Insert — NOTE shifted rows: lat/long occupy R0/R1)
${PIPE_INS_CODE}        tab:tabPanel:objectForm:form:G:0:R:2:C:1:in
${PIPE_INS_NAME}        tab:tabPanel:objectForm:form:G:0:R:3:C:1:in
${PIPE_INS_DATE}        tab:tabPanel:objectForm:form:G:0:R:5:C:1:da_input
${PIPE_INS_OP_PU}       tab:tabPanel:objectForm:form:G:0:R:21:C:1:dd
# updateAttributes field IDs (Update — assumed same shifted layout; verified by the
# loaded-code safety check in Update Object Name)
${PIPE_UPD_CODE}        tab:tabPanel:updateAttributes:form:G:0:R:2:C:1:in
${PIPE_UPD_NAME}        tab:tabPanel:updateAttributes:form:G:0:R:3:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${PIPE_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Pipeline Screen
    [Documentation]    Suite Setup: launch, login, navigate, pick the Business Unit
    ...    Production Unit navigator context and apply it (grid is empty until then).
    [Arguments]    ${production_unit}    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${PIPE_SCREEN}    ${user}    ${pass}
    Select EC Dropdown Option    ${PIPE_NAV_PU}    ${production_unit}
    Apply Navigator

Pipeline Row Should Exist
    [Documentation]    Assert a pipeline with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${PIPE_TABLE}    ${code}

Pipeline Row Should Not Exist
    [Documentation]    Assert a pipeline with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${PIPE_TABLE}    ${code}

Pipeline Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in ov_pipeline.
    [Arguments]    ${code}
    Code Should Be Present In View    ov_pipeline    ${code}

Pipeline Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from ov_pipeline.
    [Arguments]    ${code}
    Code Should Be Absent In View    ov_pipeline    ${code}

Pipeline Row Should Show Name
    [Documentation]    Assert the Pipeline row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${PIPE_TABLE}    ${code}    ${name}

Insert Pipeline Record
    [Documentation]    Insert a new pipeline: New Object form -> Code/Name/Start Date +
    ...    Op Production Unit = ${op_pu} (grid-visibility link) -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}    ${op_pu}
    Fill New Object Form    ${PIPE_INS_CODE}    ${PIPE_INS_NAME}    ${PIPE_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Select EC Dropdown Option    ${PIPE_INS_OP_PU}    ${op_pu}
    ${picked}=    Get Property    css=[id="${PIPE_INS_OP_PU}_input"]    value
    Should Be Equal    ${picked}    ${op_pu}    msg=Op PU dd did not commit (shows '${picked}')
    # force blur so the cell's EC.bf onchange stages the dd value before Save
    Click    css=[id="${PIPE_INS_OP_PU}_input"]
    Keyboard Key    press    Tab
    Wait For Load State    networkidle    timeout=12s
    Sleep    0.6s
    Save And Refresh List

Update Pipeline Name
    [Documentation]    Select the pipeline, confirm it loaded, edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${PIPE_TABLE}    ${PIPE_UPD_CODE}    ${PIPE_UPD_NAME}    ${code}    ${new_name}

Delete Pipeline
    [Documentation]    Select the pipeline, set End Date = Start Date (true delete), Save.
    ...    Versioned GM grids redraw lazily — one extra Apply Navigator before asserting.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${PIPE_TABLE}    ${PIPE_DEL_ENDDATE}    ${code}    ${date}
    Apply Navigator
