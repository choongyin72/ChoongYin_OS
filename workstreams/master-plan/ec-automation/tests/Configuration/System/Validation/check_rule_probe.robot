*** Settings ***
Documentation       DIAGNOSTIC — open the Check Rule maintenance screen, screenshot it, dump
...                 navigator/filter inputs so we can filter to a specific rule by name/id.

Library             Browser
Resource            ../../../../resources/common.resource

Suite Setup         Open And Login
Suite Teardown      Close EC
Test Tags           probe


*** Test Cases ***
Open Check Rule Screen
    [Documentation]    Diagnostic: open the Check Rule screen, dump candidate filter inputs and
    ...    screenshot it (used to find the Check Name column filter id).
    Navigate To Screen    Check Rule
    Wait For Load State    networkidle    timeout=30s
    Sleep    2s
    ${title}=    Evaluate JavaScript    ${None}
    ...    () => [...document.querySelectorAll('span,div,label')].map(e=>(e.textContent||'').trim()).filter(t=>t && t.length<40 && /Check Rule/i.test(t)).slice(0,5)
    Log    TITLES :: ${title}    console=True
    ${inputs}=    Evaluate JavaScript    ${None}
    ...    () => [...document.querySelectorAll('input,select')].map(e=>e.id).filter(id=>id && (id.includes('nav')||id.toLowerCase().includes('check')||id.toLowerCase().includes('rule')||id.toLowerCase().includes('filter'))).slice(0,30)
    Log    INPUTS :: ${inputs}    console=True
    Take Screenshot    filename=${OUTPUT DIR}/check_rule_screen.png    fullPage=True


*** Keywords ***
Open And Login
    [Documentation]    Suite Setup: launch the browser and authenticate.
    Open EC Browser
    Login To EC    ${EC_USER}    ${EC_PASS}
