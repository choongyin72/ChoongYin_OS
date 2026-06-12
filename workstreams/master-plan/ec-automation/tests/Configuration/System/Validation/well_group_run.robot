*** Settings ***
Documentation       Run the Well Gas Component Analysis daily-sampling group on a date and
...                 (optionally) capture the mole% sum errors. Used for the well MOL% fake-data
...                 PASS evidence: run after patch (capture), and again after revert (restore log).

Library             Browser
Resource            ../../../../pageobjects/Configuration/System/Validation/validation_overview_pluto_scarborough.resource

Suite Setup         Open Validation Overview Screen
Suite Teardown      Close EC
Test Tags           evidence    issue_1052


*** Variables ***
${WELL_GRP}     Well Gas Component Analysis - Daily Sampling Validations
${DAY}          2026-06-01
${CAPTURE}      no
${SHOT}         well_run


*** Test Cases ***
Run Well Group
    [Documentation]    Run the well daily-sampling group on ${DAY}; if CAPTURE=yes, isolate the
    ...    mole% errors and screenshot as ${SHOT}.
    Set Validation Date Range And Go    ${DAY}    ${DAY}
    Go To Groups Tree Page    2
    Run Check Group    ${WELL_GRP}
    Go To Groups Tree Page    2
    Select Validation Group    ${WELL_GRP}
    Sleep    1.5s
    IF    '${CAPTURE}' == 'yes'
        Show Only Log Messages By Ticking    sum of mole percentage
        ${c}=    Evaluate JavaScript    ${None}
        ...    () => { const tb=document.querySelector('[id="logs:form:T_data"]'); const t=tb?(tb.innerText||''):''; return (t.match(/sum of mole percentage/g)||[]).length; }
        Log    MOLE_ERRORS :: ${c}    console=True
        Take Screenshot    filename=${OUTPUT DIR}/${SHOT}.png    fullPage=True
    END
