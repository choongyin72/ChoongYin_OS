*** Settings ***
Documentation       T3 (screen) — Pipeline Segment page object.
...                 Screen: Configuration > Assets > Dispatching Objects > Pipeline Segment.
...                 OV-GM behaviour: the grid (manageObject:form:T_data) loads ONLY after
...                 a Business Unit is picked in the navigator + GO. The inserted object's
...                 "Pipeline Name" must be consistent with that BU or the filtered grid
...                 will never list it (recon 2026-06-12).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${PIPESEG_SCREEN}          Pipeline Segment
${PIPESEG_TABLE}           manageObject:form:T_data
# navigator: Business Unit dropdown — MANDATORY before the grid loads
${PIPESEG_NAV_BU}          nav:form:G:0:R:1:C:1:dd
# objectForm field IDs (Insert — new object)
${PIPESEG_INS_CODE}        tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${PIPESEG_INS_NAME}        tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${PIPESEG_INS_DATE}        tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
# Insert form's "Pipeline Name" dropdown (mandatory / grid-visibility parent)
${PIPESEG_INS_PARENT}      tab:tabPanel:objectForm:form:G:0:R:6:C:1:dd
# updateAttributes field IDs (Update — existing object)
${PIPESEG_UPD_CODE}        tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${PIPESEG_UPD_NAME}        tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${PIPESEG_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Pipeline Segment Screen
    [Documentation]    Suite Setup: launch, login, navigate, pick the Business Unit
    ...    navigator context and apply it (grid is empty until then).
    [Arguments]    ${business_unit}    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${PIPESEG_SCREEN}    ${user}    ${pass}
    Select EC Dropdown Option    ${PIPESEG_NAV_BU}    ${business_unit}
    Apply Navigator

Pipeline Segment Row Should Exist
    [Documentation]    Assert a pipeline segment with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${PIPESEG_TABLE}    ${code}

Pipeline Segment Row Should Not Exist
    [Documentation]    Assert a pipeline segment with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${PIPESEG_TABLE}    ${code}

Pipeline Segment Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in ov_pipeline_segment.
    [Arguments]    ${code}
    Code Should Be Present In View    ov_pipeline_segment    ${code}

Pipeline Segment Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from ov_pipeline_segment.
    [Arguments]    ${code}
    Code Should Be Absent In View    ov_pipeline_segment    ${code}

Pipeline Segment Row Should Show Name
    [Documentation]    Assert the Pipeline Segment row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${PIPESEG_TABLE}    ${code}    ${name}

Insert Pipeline Segment Record
    [Documentation]    Insert a new pipeline segment: New Object form -> Code/Name/Start Date +
    ...    "Pipeline Name" = ${parent} (mandatory / BU-visibility link) -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}    ${parent}
    Fill New Object Form    ${PIPESEG_INS_CODE}    ${PIPESEG_INS_NAME}    ${PIPESEG_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Select EC Dropdown Option    ${PIPESEG_INS_PARENT}    ${parent}
    Save And Refresh List

Update Pipeline Segment Name
    [Documentation]    Select the pipeline segment, confirm it loaded, edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${PIPESEG_TABLE}    ${PIPESEG_UPD_CODE}    ${PIPESEG_UPD_NAME}    ${code}    ${new_name}

Delete Pipeline Segment
    [Documentation]    Select the pipeline segment, set End Date = Start Date (true delete), Save.
    ...    Versioned GM grids redraw lazily — one extra Apply Navigator before asserting.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${PIPESEG_TABLE}    ${PIPESEG_DEL_ENDDATE}    ${code}    ${date}
    Apply Navigator
