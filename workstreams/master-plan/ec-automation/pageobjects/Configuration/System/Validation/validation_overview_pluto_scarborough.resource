*** Settings ***
Documentation       T3 (screen) — Validation Overview - Pluto Scarborough page object.
...                 Screen: Configuration > System > Validation (framework screen
...                 /com.ec.frmw.co.screens/tt_validation_overview, root V_VALIDATIONS).
...                 NOT an IUD screen: it RUNS check groups and shows results. Flow per EC:
...                 set From/To date -> click GO (navigator reload, MANDATORY) -> select a
...                 group row -> [Run Selected Groups] -> click GO again to refresh Summary.
...                 Verifies against CTRL_CHECK_LOG (EC's validation output) via DbVerify.
...                 Folder is 4 deep -> imports use ../../../../ to reach root.

Library             Browser
Library             String
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource


*** Variables ***
${VO_SCREEN}        Validation Overview - Pluto Scarborough
${VO_FROM}          nav:form:G:0:R:1:C:0:da_input
${VO_TO}            nav:form:G:0:R:1:C:1:da_input
${VO_GO}            navButton:form:B
# Run Selected Groups button (PrimeFaces commandButton wrapping a span)
${VO_RUN_SELECTED}      xpath=//*[self::button or self::a or contains(@class,'ui-button')][.//*[normalize-space()='Run Selected Groups'] or normalize-space(.)='Run Selected Groups']
# group tree: label cell groups:form:T:{idx}:C0_la , summary cell ...:C2_la


*** Keywords ***
Open Validation Overview Screen
    [Documentation]    Suite Setup: launch, login (default env user), open the screen.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Open EC Browser
    Login To EC    ${user}    ${pass}
    Navigate To Screen    ${VO_SCREEN}

Set Validation Date Range And Go
    [Documentation]    Set From/To date then click GO (mandatory navigator reload, filters
    ...    the group tree to the date window).
    [Arguments]    ${from_date}    ${to_date}
    Fill Text    css=[id="${VO_FROM}"]    ${from_date}
    Fill Text    css=[id="${VO_TO}"]    ${to_date}
    Keyboard Key    press    Escape
    Reload Validation Screen

Reload Validation Screen
    [Documentation]    Click the navigator GO button and wait for the screen to reload.
    Click    css=[id="${VO_GO}"]
    Wait For Load State    networkidle    timeout=30s
    Sleep    1.5s

Find Group Row Index
    [Documentation]    Return the groups:form:T:{idx} index whose C0 label contains
    ...    ${group_desc}, or -1. Located by text so it is robust to row reordering.
    [Arguments]    ${group_desc}
    ${idx}=    Evaluate JavaScript    ${None}
    ...    () => { let r=-1; document.querySelectorAll('[id^="groups:form:T:"][id$=":C0_la"]').forEach(la=>{ if((la.textContent||'').includes('${group_desc}')){const m=la.id.match(/groups:form:T:(\\d+):C0_la/); if(m) r=parseInt(m[1]);}}); return r; }
    RETURN    ${idx}

Select Validation Group
    [Documentation]    Click the group row label to select it.
    [Arguments]    ${group_desc}
    ${idx}=    Find Group Row Index    ${group_desc}
    Should Be True    ${idx} >= 0    msg=Group not found in tree: ${group_desc}
    Click    css=[id="groups:form:T:${idx}:C0_la"]
    Sleep    0.6s
    RETURN    ${idx}

Run Selected Validation Groups
    [Documentation]    Click [Run Selected Groups] and wait for the run to complete.
    Click    ${VO_RUN_SELECTED}
    Wait For Load State    networkidle    timeout=60s
    Sleep    2s

Run Check Group
    [Documentation]    Full run gesture for ONE group: select it, Run Selected Groups,
    ...    then GO to refresh the Summary. Leaves the screen showing the refreshed result.
    [Arguments]    ${group_desc}
    Select Validation Group    ${group_desc}
    Run Selected Validation Groups
    Reload Validation Screen

Get Group Summary Errors
    [Documentation]    Read the Summary cell for ${group_desc} and return the integer
    ...    count before " Errors" (e.g. "50 Errors, 0 Warnings, ..." -> 50).
    [Arguments]    ${group_desc}
    ${idx}=    Find Group Row Index    ${group_desc}
    Should Be True    ${idx} >= 0    msg=Group not found in tree: ${group_desc}
    ${summary}=    Get Text    css=[id="groups:form:T:${idx}:C2_la"]
    ${m}=    Get Regexp Matches    ${summary}    (\\d+)\\s+Errors    1
    Should Not Be Empty    ${m}    msg=Could not parse Errors from summary: ${summary}
    ${errors}=    Convert To Integer    ${m}[0]
    RETURN    ${errors}

Group Summary Errors Should Be
    [Documentation]    Assert the UI Summary "Errors" for ${group_desc} equals ${expected}.
    [Arguments]    ${group_desc}    ${expected}
    ${errors}=    Get Group Summary Errors    ${group_desc}
    Should Be Equal As Integers    ${errors}    ${expected}
    ...    msg=UI Summary Errors mismatch for ${group_desc}: got ${errors}, expected ${expected}

Rule Log Count Should Be
    [Documentation]    DB ground-truth: assert CTRL_CHECK_LOG rows for ${check_id} on
    ...    ${daytime} equals ${expected} (DbVerify -> live DB).
    [Arguments]    ${check_id}    ${daytime}    ${expected}
    Check Log Count Should Be    ${check_id}    ${daytime}    ${expected}

Rule Log Matches Oracle
    [Documentation]    Compute the independent per-object oracle from the rule's own
    ...    WHERE_FORMULA, then assert EC's CTRL_CHECK_LOG count equals it (UI run == DB).
    [Arguments]    ${check_id}    ${daytime}
    ${oracle}=    Distinct Violation Objects For Rule    ${check_id}    ${daytime}
    Check Log Count Should Be    ${check_id}    ${daytime}    ${oracle}

Group Oracle Total
    [Documentation]    Sum the per-object oracles of a group's rules — the expected UI
    ...    Summary "Errors" total for the group.
    [Arguments]    ${daytime}    @{check_ids}
    ${total}=    Set Variable    ${0}
    FOR    ${id}    IN    @{check_ids}
        ${n}=    Distinct Violation Objects For Rule    ${id}    ${daytime}
        ${total}=    Evaluate    ${total} + ${n}
    END
    RETURN    ${total}
