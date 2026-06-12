*** Settings ***
Documentation       Capture the Check Rule maintenance screen filtered to a rule-name pattern
...                 (proves the rule is configured/deployed). Parameterize NAME / SHOT.

Library             Browser
Resource            ../../../../resources/common.resource

Suite Setup         Open And Login
Suite Teardown      Close EC
Test Tags           evidence    issue_1052


*** Variables ***
${NAME}     COMP_MOL_PCT
${SHOT}     check_rule_capture


*** Test Cases ***
Filter Check Rule List
    [Documentation]    Filter the Check Rule list to ${NAME} and screenshot the matching rows
    ...    (evidence the rule is configured/deployed).
    Navigate To Screen    Check Rule
    Wait For Load State    networkidle    timeout=30s
    Sleep    1.5s
    # free-text filter on the Check Name column
    Fill Text    css=[id="check_rules:form:T:sfilter1_ft_filter"]    ${NAME}
    Keyboard Key    press    Enter
    Wait For Load State    networkidle    timeout=20s
    Sleep    2s
    ${rows}=    Evaluate JavaScript    ${None}
    ...    () => { const tb=document.querySelector('[id="check_rules:form:T_data"]'); return tb?tb.querySelectorAll('tr').length:-1; }
    Log    RULE_ROWS :: ${rows}    console=True
    Take Screenshot    filename=${OUTPUT DIR}/${SHOT}.png    fullPage=True


*** Keywords ***
Open And Login
    [Documentation]    Suite Setup: launch the browser and authenticate.
    Open EC Browser
    Login To EC    ${EC_USER}    ${EC_PASS}
