*** Settings ***
Documentation       EC IUD Test - Cargo Planning Forecast (EC Transport > Cargo Planning > Forecast).
...                 Custom layout: per-field nav groups (PU/Area/FC1/Storage, SPECIFIC P1 values),
...                 grid fcst:form:T_data, mandatory End Date at insert (row spans the nav date),
...                 Storage Name = nav Storage. COPY buttons (copy-existing dialog) untouched.
...                 DELETE = End Date = Start Date (proven true delete in OV_FCST_MNGR_FCST_LIST).
...                 NEVER touch existing data; unique AUTOTEST_CPF_<timestamp> code per run.

Resource            ../../../../pageobjects/EC_Transport/Cargo_Planning/Forecast/cargo_planning_forecast_page.resource

Suite Setup         Set Up Cargo Planning Forecast Suite
Suite Teardown      Close EC

Test Tags           iud    cargo-planning-forecast


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2026-01-01
${END_DATE}         2026-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test object does not exist before inserting.
    [Tags]    clean-state
    Cargo Planning Forecast Row Should Not Exist    ${TEST_CODE}
    Capture Step    cargo_planning_forecast_tc01_clean

TC02 Insert New Cargo Planning Forecast
    [Documentation]    Insert under the P1+Storage navigator scope (incl. mandatory End Date) and confirm it lists.
    [Tags]    insert
    Insert Cargo Planning Forecast Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Cargo Planning Forecast Row Should Exist    ${TEST_CODE}
    Cargo Planning Forecast Should Exist In DB    ${TEST_CODE}
    Capture Step    cargo_planning_forecast_tc02_inserted

TC03 Update Cargo Planning Forecast Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Cargo Planning Forecast Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Cargo Planning Forecast Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    cargo_planning_forecast_tc03_updated

TC04 Delete Cargo Planning Forecast
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Cargo Planning Forecast    ${TEST_CODE}    ${END_DATE}
    Cargo Planning Forecast Row Should Not Exist    ${TEST_CODE}
    Cargo Planning Forecast Should Not Exist In DB    ${TEST_CODE}
    Capture Step    cargo_planning_forecast_tc04_deleted


*** Keywords ***
Set Up Cargo Planning Forecast Suite
    [Documentation]    Generate a unique test code/name, open the screen, apply the P1+Storage nav scope.
    Prepare IUD Object Data    AUTOTEST_CPF_    Cargo Planning Forecast
    Open Cargo Planning Forecast Screen
