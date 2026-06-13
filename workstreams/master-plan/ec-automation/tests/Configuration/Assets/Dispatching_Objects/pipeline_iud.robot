*** Settings ***
Documentation       EC IUD Test - Pipeline (Configuration > Assets > Dispatching Objects).
...                 Full OV-GM: navigator Production Unit + GO gates the grid (operational groupmodel, like Area); insert sets Op Production Unit = nav PU so the row is visible. DELETE = End Date
...                 = Start Date (ov_pipeline). Form quirk: Latitude/Longitude rows FIRST
...                 (Code R2/Name R3/Start R5). Unique AUTOTEST_PIPE_<ts> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Dispatching_Objects/pipeline_page.resource

Suite Setup         Set Up Pipeline Suite
Suite Teardown      Close EC

Test Tags           iud    pipeline


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE_REFDD}
${END_DATE}         ${TEST_START_DATE_REFDD}
${NAV_PU}           P1 Production Unit


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test pipeline does not exist before inserting.
    [Tags]    clean-state
    Pipeline Row Should Not Exist    ${TEST_CODE}
    Capture Step    pipeline_tc01_clean

TC02 Insert New Pipeline
    [Documentation]    Insert a new pipeline and confirm it appears in the BU-filtered list.
    [Tags]    insert
    Insert Pipeline Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}    ${NAV_PU}
    Pipeline Row Should Exist    ${TEST_CODE}
    Pipeline Should Exist In DB    ${TEST_CODE}
    Capture Step    pipeline_tc02_inserted

TC03 Update Pipeline Name
    [Documentation]    Edit the pipeline name and confirm the list reflects the change.
    [Tags]    update
    Update Pipeline Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Pipeline Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    pipeline_tc03_updated

TC04 Delete Pipeline
    [Documentation]    Delete via End Date = Start Date and confirm the pipeline is gone.
    [Tags]    delete    cleanup
    Delete Pipeline    ${TEST_CODE}    ${END_DATE}
    Pipeline Row Should Not Exist    ${TEST_CODE}
    Pipeline Should Not Exist In DB    ${TEST_CODE}
    Capture Step    pipeline_tc04_deleted


*** Keywords ***
Set Up Pipeline Suite
    [Documentation]    Generate a unique test code/name, then open the Pipeline screen
    ...    with the ${NAV_PU} navigator context.
    Prepare IUD Object Data    AUTOTEST_PIPE_    Pipeline
    Open Pipeline Screen    ${NAV_PU}
