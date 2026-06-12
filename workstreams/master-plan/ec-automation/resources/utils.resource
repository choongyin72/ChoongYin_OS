*** Settings ***
Documentation       T1 area — cross-cutting helpers: unique code generation, evidence capture.

Library             DateTime
Library             Browser


*** Keywords ***
Generate Unique Code
    [Documentation]    Return ${prefix} + a YYYYMMDDHHMMSS timestamp (unique per second)
    ...    so re-runs never collide with codes that linger in the DB after a delete.
    [Arguments]    ${prefix}
    ${ts}=    Get Current Date    result_format=%Y%m%d%H%M%S
    RETURN    ${prefix}${ts}

Prepare IUD Object Data
    [Documentation]    Standard IUD suite-setup data step: generate a unique AUTOTEST
    ...    code from ${prefix} and publish the conventional suite variables
    ...    ${TEST_CODE} / ${OBJ_NAME} ("${label} <code>") / ${OBJ_NAME_UPD} (...UPD).
    ...    Returns the code for suites that need it directly.
    [Arguments]    ${prefix}    ${label}
    ${code}=    Generate Unique Code    ${prefix}
    VAR    ${TEST_CODE}    ${code}    scope=SUITE
    VAR    ${OBJ_NAME}    ${label} ${code}    scope=SUITE
    VAR    ${OBJ_NAME_UPD}    ${label} ${code} UPD    scope=SUITE
    RETURN    ${code}

Capture Step
    [Documentation]    Take a screenshot into the output dir with a step label.
    [Arguments]    ${label}
    Take Screenshot    filename=${OUTPUT_DIR}/${label}
