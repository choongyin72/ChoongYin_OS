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

Capture Step
    [Documentation]    Take a screenshot into the output dir with a step label.
    [Arguments]    ${label}
    Take Screenshot    filename=${OUTPUT_DIR}/${label}
