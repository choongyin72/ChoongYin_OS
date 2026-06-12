*** Settings ***
Documentation       Issue_1052 FROZEN check rules — Layer-2 (front-end) validation via the
...                 Validation Overview - Pluto Scarborough screen, verified against the DB.
...                 Runs the frozen-bearing check groups through the UI, then asserts EC's
...                 CTRL_CHECK_LOG (the UI run's output) matches an INDEPENDENT oracle computed
...                 from getValFrozenValue on the source rows (Frozen Distinct Violation Objects).
...                 So a PASS = the UI-triggered run really detected the frozen values, not just
...                 that the screen looked right.
...
...                 Scope = the 4 ACTIVE frozen rules that fire on natural data:
...                   V_PHD_STREAM_ANALYSIS  -> 1152 DENSITY, 1153 GCV   (2025-12-13: 6 each)
...                   V_PHD_STREAM_WATER     -> 1154 ZWT_OILINWAT        (2026-05-24: 1)
...                 Excluded: 1155 AVG_GAS_RATE (empty data, can't fire); 1150/1151 (ON HOLD).
...                 Reuses the validation_overview_pluto_scarborough (T3) page object + DbVerify.

Resource            ../../../../pageobjects/Configuration/System/Validation/validation_overview_pluto_scarborough.resource

Suite Setup         Set Up And Run Frozen Groups
Suite Teardown      Close EC

Test Tags           validation_overview    frozen    phd    issue_1052


*** Variables ***
${ANALYSIS_DATE}        2025-12-13
${WATER_DATE}           2026-05-24
${GROUP_ANALYSIS}       Stream Gas Component Analysis (Analysis) - PHD Validations
${GROUP_WATER}          Daily Stream Water Status - PHD Validations
# frozen rule CHECK_IDs (active set, confirmed on COPS DEV)
${DENSITY_FRZ}          1152
${GCV_FRZ}              1153
${OILINWAT_FRZ}         1154


*** Test Cases ***
TC_FRZ_01 Analysis DENSITY Frozen — UI Run Matches DB Oracle
    [Documentation]    Frozen rule ${DENSITY_FRZ}: oracle > 0 AND EC's CTRL_CHECK_LOG matches it.
    [Tags]    tc_frz_01    stream_analysis
    Frozen Rule Should Positively Fire    ${DENSITY_FRZ}    ${ANALYSIS_DATE}

TC_FRZ_02 Analysis GCV Frozen — UI Run Matches DB Oracle
    [Documentation]    Frozen rule ${GCV_FRZ}: oracle > 0 AND EC's CTRL_CHECK_LOG matches it.
    [Tags]    tc_frz_02    stream_analysis
    Frozen Rule Should Positively Fire    ${GCV_FRZ}    ${ANALYSIS_DATE}

TC_FRZ_03 Water Oil-in-Water Frozen — UI Run Matches DB Oracle
    [Documentation]    Frozen rule ${OILINWAT_FRZ}: oracle > 0 AND EC's CTRL_CHECK_LOG matches it.
    [Tags]    tc_frz_03    stream_water
    Frozen Rule Should Positively Fire    ${OILINWAT_FRZ}    ${WATER_DATE}

TC_FRZ_04 Analysis Group UI Shows Frozen WARNINGs
    [Documentation]    Visual confirmation the frozen WARNINGs surface in the UI Summary
    ...    (Warnings > 0) for the analysis group on the frozen date.
    [Tags]    tc_frz_04    stream_analysis    ui-summary
    Group Summary Warnings Should Be Positive On Date    ${ANALYSIS_DATE}    ${GROUP_ANALYSIS}


*** Keywords ***
Set Up And Run Frozen Groups
    [Documentation]    Open the screen; run the analysis group on ANALYSIS_DATE and the water
    ...    group on WATER_DATE (each: set date + GO -> select -> Run Selected Groups -> GO).
    ...    These runs write the frozen WARNINGs to CTRL_CHECK_LOG for the assertions below.
    Open Validation Overview Screen
    Set Validation Date Range And Go    ${ANALYSIS_DATE}    ${ANALYSIS_DATE}
    Run Check Group    ${GROUP_ANALYSIS}
    Set Validation Date Range And Go    ${WATER_DATE}    ${WATER_DATE}
    Run Check Group    ${GROUP_WATER}
