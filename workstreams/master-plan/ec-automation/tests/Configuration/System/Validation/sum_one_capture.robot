*** Settings ***
Documentation       Issue_1052 SUM check — ONE isolated screen capture per run (fresh grid).
...                 Parameterize via --variable GRP/FROM/TO/MATCH/SHOT. Run headless for full
...                 1920x1080 resolution. One Message filter per fresh load (cascading-filter safe).

Library             Browser
Resource            ../../../../pageobjects/Configuration/System/Validation/validation_overview_pluto_scarborough.resource

Suite Setup         Open Validation Overview Screen
Suite Teardown      Close EC
Test Tags           sum    evidence    issue_1052


*** Variables ***
${GRP}      Stream Gas Component Analysis - Daily Sampling Validations
${FROM}     2026-05-01
${TO}       2026-05-31
${MATCH}    sum of mole percentage
${SHOT}     sum_capture
${PAGE}     2


*** Test Cases ***
Capture One Filtered View
    Set Validation Date Range And Go    ${FROM}    ${TO}
    Go To Groups Tree Page    ${PAGE}
    ${idx}=    Find Group Row Index    ${GRP}
    Should Be True    ${idx} >= 0    msg=Group not found: ${GRP}
    Select Validation Group    ${GRP}
    Sleep    1s
    Show Only Log Messages By Ticking    ${MATCH}
    ${c}=    Evaluate JavaScript    ${None}
    ...    () => { const tb=document.querySelector('[id="logs:form:T_data"]'); const txt=tb?(tb.innerText||''):''; return { mole:(txt.match(/sum of mole percentage/g)||[]).length, molwt:(txt.match(/molecular weight percentage/g)||[]).length }; }
    Log    COUNTS[${SHOT}] :: ${c}    console=True
    Take Screenshot    filename=${OUTPUT DIR}/${SHOT}.png    fullPage=True
