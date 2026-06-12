*** Settings ***
Documentation       EC IUD Test - Pipeline Segment (Configuration > Assets > Dispatching Objects > Pipeline Segment).
...                 OV-GM behaviour: navigator Business Unit + GO gates the grid; insert
...                 references "Pipeline Name" = TS5 Gas Pipeline so the row is visible
...                 under the TS5 BU filter. DELETE = End Date = Start Date (ov_pipeline_segment).
...                 NEVER touch existing data: unique AUTOTEST_PSEG_<timestamp> code per run;
...                 the referenced parent objects are READ-ONLY seed data.

Resource            ../../../../pageobjects/Configuration/Assets/Dispatching_Objects/pipeline_segment_page.resource

Suite Setup         Set Up Pipeline Segment Suite
Suite Teardown      Close EC

Test Tags           iud    pipeline_segment


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE_REFDD}
${END_DATE}         ${TEST_START_DATE_REFDD}
${NAV_BU}           TS5 BU
${PARENT_VALUE}     TS5 Gas Pipeline


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test pipeline segment does not exist before inserting.
    [Tags]    clean-state
    Pipeline Segment Row Should Not Exist    ${TEST_CODE}
    Capture Step    pipeline_segment_tc01_clean

TC02 Insert New Pipeline Segment
    [Documentation]    Insert a new pipeline segment and confirm it appears in the BU-filtered list.
    [Tags]    insert
    Insert Pipeline Segment Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}    ${PARENT_VALUE}
    Pipeline Segment Row Should Exist    ${TEST_CODE}
    Pipeline Segment Should Exist In DB    ${TEST_CODE}
    Capture Step    pipeline_segment_tc02_inserted

TC03 Update Pipeline Segment Name
    [Documentation]    Edit the pipeline segment name and confirm the list reflects the change.
    [Tags]    update
    Update Pipeline Segment Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Pipeline Segment Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    pipeline_segment_tc03_updated

TC04 Delete Pipeline Segment
    [Documentation]    Delete via End Date = Start Date and confirm the pipeline segment is gone.
    [Tags]    delete    cleanup
    Delete Pipeline Segment    ${TEST_CODE}    ${END_DATE}
    Pipeline Segment Row Should Not Exist    ${TEST_CODE}
    Pipeline Segment Should Not Exist In DB    ${TEST_CODE}
    Capture Step    pipeline_segment_tc04_deleted


*** Keywords ***
Set Up Pipeline Segment Suite
    [Documentation]    Generate a unique test code/name, then open the Pipeline Segment screen
    ...    with the ${NAV_BU} navigator context.
    Prepare IUD Object Data    AUTOTEST_PSEG_    Pipeline Segment
    Open Pipeline Segment Screen    ${NAV_BU}
