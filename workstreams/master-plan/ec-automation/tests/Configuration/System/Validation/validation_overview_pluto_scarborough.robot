*** Settings ***
Documentation       EC PHD Check Group validation — front-end run via Validation Overview -
...                 Pluto Scarborough, verified against the database (ground truth).
...                 Runs the 3 new PHD check groups on 2026-05-26 and asserts EC's result
...                 matches an INDEPENDENT per-object oracle computed from the source views
...                 using each rule's own deployed WHERE_FORMULA. EC logs one violation per
...                 object (e.g. per stream), so the oracle counts DISTINCT OBJECT_ID.
...                 Tank GRS_VOL & AVG_TEMP are clean (0) on 2026-05-26, so they are also run
...                 on a 2nd date (2026-06-07) where they DO fire, to positively exercise them.
...                 Layered: this test -> validation_overview_pluto_scarborough (T3) ->
...                 common (T1) + DbVerify. The run writes to CTRL_CHECK_LOG (EC's output),
...                 which EC overwrites per group/day, so the suite is re-runnable.

Resource            ../../../../pageobjects/Configuration/System/Validation/validation_overview_pluto_scarborough.resource

Suite Setup         Set Up And Run PHD Groups
Suite Teardown      Close EC

Test Tags           validation_overview_pluto_scarborough    phd    issue_1052


*** Variables ***
${TEST_DATE}            2026-05-26
# 2nd date: Tank GRS_VOL & AVG_TEMP are clean (0) on TEST_DATE; they DO fire on this date,
# so we positively exercise them here (5 tanks each).
${TANK_DATE2}           2026-06-07
${GROUP_COMP}           Stream Gas Component Analysis (Composition) - PHD Validations
${GROUP_ANALYSIS}       Stream Gas Component Analysis (Analysis) - PHD Validations
${GROUP_TANK}           Daily Tank Status - VCF Calc - PHD Validations
# rule CHECK_IDs (per-instance values confirmed on COPS DEV)
${MOL_PCT}              1142
${WT_PCT}               1143
${DENSITY}              1144
${GCV}                  1145
${GRS_VOL}              1146
${GRS_MASS}             1147
${AVG_TEMP}             1148
${STD_DENSITY}          1149


*** Test Cases ***
TC_UI_01 Composition MOL_PCT — EC Matches DB Oracle
    [Documentation]    Rule ${MOL_PCT}: EC's CTRL_CHECK_LOG count equals the independent oracle.
    [Tags]    tc_ui_01    stream_comp
    Rule Log Matches Oracle    ${MOL_PCT}    ${TEST_DATE}

TC_UI_02 Composition WT_PCT — EC Matches DB Oracle
    [Documentation]    Rule ${WT_PCT}: EC's CTRL_CHECK_LOG count equals the independent oracle.
    [Tags]    tc_ui_02    stream_comp
    Rule Log Matches Oracle    ${WT_PCT}    ${TEST_DATE}

TC_UI_03 Analysis DENSITY — EC Matches DB Oracle
    [Documentation]    Rule ${DENSITY}: EC's CTRL_CHECK_LOG count equals the independent oracle.
    [Tags]    tc_ui_03    stream_analysis
    Rule Log Matches Oracle    ${DENSITY}    ${TEST_DATE}

TC_UI_04 Analysis GCV — EC Matches DB Oracle
    [Documentation]    Rule ${GCV}: EC's CTRL_CHECK_LOG count equals the independent oracle.
    [Tags]    tc_ui_04    stream_analysis
    Rule Log Matches Oracle    ${GCV}    ${TEST_DATE}

TC_UI_05 Tank GRS_VOL — EC Matches DB Oracle
    [Documentation]    Clean on 2026-05-26 (oracle 0) — asserts no false positives.
    [Tags]    tc_ui_05    tank_dip
    Rule Log Matches Oracle    ${GRS_VOL}    ${TEST_DATE}

TC_UI_06 Tank GRS_MASS — EC Matches DB Oracle
    [Documentation]    Rule ${GRS_MASS}: EC's CTRL_CHECK_LOG count equals the independent oracle.
    [Tags]    tc_ui_06    tank_dip
    Rule Log Matches Oracle    ${GRS_MASS}    ${TEST_DATE}

TC_UI_07 Tank AVG_TEMP — EC Matches DB Oracle
    [Documentation]    Clean on 2026-05-26 (oracle 0) — asserts no false positives.
    [Tags]    tc_ui_07    tank_dip
    Rule Log Matches Oracle    ${AVG_TEMP}    ${TEST_DATE}

TC_UI_08 Tank STD_DENSITY — EC Matches DB Oracle
    [Documentation]    Rule ${STD_DENSITY}: EC's CTRL_CHECK_LOG count equals the independent oracle.
    [Tags]    tc_ui_08    tank_dip
    Rule Log Matches Oracle    ${STD_DENSITY}    ${TEST_DATE}

TC_UI_09 Composition UI Summary Matches DB Total
    [Documentation]    UI Summary "Errors" for the Composition group equals the summed oracles.
    [Tags]    tc_ui_09    stream_comp    ui-summary
    ${total}=    Group Oracle Total    ${TEST_DATE}    ${MOL_PCT}    ${WT_PCT}
    Group Summary Errors Should Be On Date    ${TEST_DATE}    ${GROUP_COMP}    ${total}

TC_UI_10 Analysis UI Summary Matches DB Total
    [Documentation]    UI Summary "Errors" for the Analysis group equals the summed oracles.
    [Tags]    tc_ui_10    stream_analysis    ui-summary
    ${total}=    Group Oracle Total    ${TEST_DATE}    ${DENSITY}    ${GCV}
    Group Summary Errors Should Be On Date    ${TEST_DATE}    ${GROUP_ANALYSIS}    ${total}

TC_UI_11 Tank UI Summary Matches DB Total
    [Documentation]    UI Summary "Errors" for the Tank group equals the summed oracles.
    [Tags]    tc_ui_11    tank_dip    ui-summary
    ${total}=    Group Oracle Total    ${TEST_DATE}    ${GRS_VOL}    ${GRS_MASS}    ${AVG_TEMP}    ${STD_DENSITY}
    Group Summary Errors Should Be On Date    ${TEST_DATE}    ${GROUP_TANK}    ${total}

TC_UI_12 Tank GRS_VOL Positively Fires (2nd date)
    [Documentation]    On TEST_DATE this rule is clean (0); on TANK_DATE2 it has real
    ...    violations. Assert oracle > 0 AND EC's log matches it.
    [Tags]    tc_ui_12    tank_dip    second-date
    Rule Should Positively Fire    ${GRS_VOL}    ${TANK_DATE2}

TC_UI_13 Tank AVG_TEMP Positively Fires (2nd date)
    [Documentation]    On TEST_DATE this rule is clean (0); on TANK_DATE2 it has real
    ...    violations. Assert oracle > 0 AND EC's log matches it.
    [Tags]    tc_ui_13    tank_dip    second-date
    Rule Should Positively Fire    ${AVG_TEMP}    ${TANK_DATE2}

TC_UI_14 Tank UI Summary Matches DB Total (2nd date)
    [Documentation]    UI Summary "Errors" for the Tank group equals the summed oracles on TANK_DATE2.
    [Tags]    tc_ui_14    tank_dip    ui-summary    second-date
    ${total}=    Group Oracle Total    ${TANK_DATE2}    ${GRS_VOL}    ${GRS_MASS}    ${AVG_TEMP}    ${STD_DENSITY}
    Group Summary Errors Should Be On Date    ${TANK_DATE2}    ${GROUP_TANK}    ${total}


*** Keywords ***
Set Up And Run PHD Groups
    [Documentation]    Open the screen; run the 3 PHD groups on TEST_DATE, then run the Tank
    ...    group again on TANK_DATE2 (so GRS_VOL & AVG_TEMP are positively exercised).
    ...    Each run: set date + GO -> select group -> Run Selected Groups -> GO to refresh.
    Open Validation Overview Screen
    Set Validation Date Range And Go    ${TEST_DATE}    ${TEST_DATE}
    Run Check Group    ${GROUP_COMP}
    Run Check Group    ${GROUP_ANALYSIS}
    Run Check Group    ${GROUP_TANK}
    Set Validation Date Range And Go    ${TANK_DATE2}    ${TANK_DATE2}
    Run Check Group    ${GROUP_TANK}
