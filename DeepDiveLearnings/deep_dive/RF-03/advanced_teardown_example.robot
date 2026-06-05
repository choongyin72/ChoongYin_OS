*** Settings ***
Documentation    Advanced Teardown Patterns — EC Robot Framework
...              Demonstrates: screenshot path pattern, suite+test teardown,
...              Set Test Metadata, custom log messages
Library          Browser
Library          OperatingSystem
Resource         ../RF-02/ec_project_scaffold/resources/variables/common_variables.robot
Variables        ../RF-02/ec_project_scaffold/vars/local.py

Suite Setup      Log    Suite starting: ${SUITE_NAME}    INFO
Suite Teardown   Suite Level Cleanup
Test Teardown    Standard EC Test Teardown

*** Test Cases ***

TC_Teardown_01 Example With Metadata
    [Documentation]    Demonstrates Set Test Metadata for custom report info
    [Tags]    teardown_demo
    Set Test Metadata    Environment    ${EC_URL}
    Set Test Metadata    DB    ${DB_URL}
    Log    Test executing on ${EC_URL}    INFO
    # ... actual test steps would go here ...

TC_Teardown_02 Deliberate Failure For Screenshot Demo
    [Documentation]    This test intentionally fails to show screenshot teardown
    [Tags]    teardown_demo    negative
    Log    About to fail intentionally    WARN
    Should Be Equal    PASS    FAIL    msg=Intentional failure for demo

*** Keywords ***

Standard EC Test Teardown
    [Documentation]    Standard teardown for ALL EC tests.
    ...                Screenshots saved to ${OUTPUT_DIR} with suite+test name.
    ...                Run Keyword And Continue On Failure ensures all cleanup runs
    ...                even if one teardown step fails.
    Run Keyword And Continue On Failure
    ...    Run Keyword If Test Failed
    ...    Take Screenshot    ${OUTPUT_DIR}${/}${SUITE_NAME}_${TEST_NAME}_failure
    Log    Test '${TEST_NAME}' finished with status: ${TEST_STATUS}    INFO

Suite Level Cleanup
    [Documentation]    Suite teardown — close browser and log summary.
    Run Keyword And Continue On Failure    Close Browser
    Log    Suite '${SUITE_NAME}' complete    INFO

Log Custom Message With Level
    [Documentation]    Example of structured logging with semicolon format for Excel.
    ...                Full log: "INFO = [block_index] ; node ; stream ; value1 ; value2"
    [Arguments]    ${block}    ${node}    ${stream}    ${value}
    Log    INFO = ${block} ; ${node} ; ${stream} ; ${value}    INFO
    # In Full log level, semicolon-separated format → copy-paste to Excel for analysis
