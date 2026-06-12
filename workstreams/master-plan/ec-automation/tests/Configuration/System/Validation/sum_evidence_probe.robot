*** Settings ***
Documentation       Stream WT% as the FIRST/ONLY filter on a fresh grid (first filter always
...                 applies). Verify molwt-only via row counts, screenshot.

Library             Browser
Resource            ../../../../pageobjects/Configuration/System/Validation/validation_overview_pluto_scarborough.resource

Suite Setup         Open Validation Overview Screen
Suite Teardown      Close EC
Test Tags           probe


*** Test Cases ***
Stream WT Only First
    [Documentation]    Probe: apply the WT% Message filter as the FIRST filter on a fresh grid
    ...    and verify only molwt rows remain (cascading-filter behavior check).
    Set Validation Date Range And Go    2026-05-01    2026-05-31
    Go To Groups Tree Page    2
    Select Validation Group    Stream Gas Component Analysis - Daily Sampling Validations
    Sleep    1s
    Show Only Log Messages By Ticking    weight percentage
    ${after}=    Evaluate JavaScript    ${None}
    ...    () => { const tb=document.querySelector('[id="logs:form:T_data"]'); const txt=tb?(tb.innerText||''):''; return { mole:(txt.match(/sum of mole percentage/g)||[]).length, molwt:(txt.match(/molecular weight percentage/g)||[]).length }; }
    Log    WT_FIRST :: ${after}    console=True
    Take Screenshot    filename=${OUTPUT DIR}/sum_stream_WT_pct.png    fullPage=True
