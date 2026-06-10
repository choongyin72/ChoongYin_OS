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

Show Only Log Messages By Ticking
    [Documentation]    Show ONLY rows whose message contains ${match_text}, by unticking
    ...    toggle-all (clear all) then clicking EACH matching option checkbox individually
    ...    (avoids the toggle-all-reselects-all bug). Closes to apply.
    [Arguments]    ${match_text}
    ${trig}=    Set Variable    css=[id="logs:form:T:sfilter3_cb_filter"] .ui-selectcheckboxmenu-trigger
    ${panel}=   Set Variable    css=[id="logs:form:T:sfilter3_cb_filter_panel"]
    ${hdr}=     Set Variable    css=[id="logs:form:T:sfilter3_cb_filter_panel"] .ui-selectcheckboxmenu-header .ui-chkbox-box
    Click    ${trig}
    Wait For Elements State    ${panel}    visible    timeout=10s
    Sleep    0.5s
    # Step 1: clear ALL currently-ticked items (re-query inside JS)
    Evaluate JavaScript    ${None}
    ...    () => { document.querySelectorAll('[id="logs:form:T:sfilter3_cb_filter_panel"] li.ui-selectcheckboxmenu-item .ui-chkbox-box.ui-state-active').forEach(b=>b.click()); }
    Sleep    3s
    # re-open the panel if the clear-all AJAX collapsed it, so the tick step sees the items
    ${vis}=    Get Element States    ${panel}    then    bool(value & visible)
    IF    not $vis
        Click    ${trig}
        Wait For Elements State    ${panel}    visible    timeout=10s
        Sleep    1s
    END
    # Step 2: tick only items matching ${match_text} (fresh re-query, avoids stale refs)
    ${ticked}=    Evaluate JavaScript    ${None}
    ...    () => { let c=0; document.querySelectorAll('[id="logs:form:T:sfilter3_cb_filter_panel"] li.ui-selectcheckboxmenu-item').forEach(li=>{ const t=(li.textContent||'').trim(); const b=li.querySelector('.ui-chkbox-box'); if(t.includes('${match_text}') && b && !b.classList.contains('ui-state-active')){ b.click(); c++; } }); return c; }
    Log    TICKED_ITEMS :: ${ticked}    console=True
    Sleep    0.8s
    Sleep    1s
    Click    ${panel} .ui-selectcheckboxmenu-close
    Wait For Load State    networkidle    timeout=20s
    Sleep    1.5s

Show Only Log Messages Matching
    [Documentation]    Filter the result detail grid's Message column (multi-select sfilter3)
    ...    to show ONLY rows whose message contains ${match_text}. Correct PrimeFaces sequence:
    ...    open -> clear search -> UNTICK toggle-all (clear all) -> type ${match_text} ->
    ...    TICK toggle-all (selects just the filtered messages) -> close.
    ...    e.g. 'mole percentage' (1156/1157 MOL%) or 'molecular weight percentage'.
    [Arguments]    ${match_text}
    ${trig}=      Set Variable    css=[id="logs:form:T:sfilter3_cb_filter"] .ui-selectcheckboxmenu-trigger
    ${panel}=     Set Variable    css=[id="logs:form:T:sfilter3_cb_filter_panel"]
    ${search}=    Set Variable    css=[id="logs:form:T:sfilter3_cb_filter_filter"]
    ${hdr}=       Set Variable    css=[id="logs:form:T:sfilter3_cb_filter_panel"] .ui-selectcheckboxmenu-header .ui-chkbox-box
    Click    ${trig}
    Wait For Elements State    ${panel}    visible    timeout=10s
    Sleep    0.5s
    Fill Text    ${search}    ${EMPTY}
    Sleep    0.5s
    # clear ALL selections first (untick toggle-all only if it is currently active)
    ${cls}=    Get Attribute    ${hdr}    class
    IF    'ui-state-active' in $cls
        Click    ${hdr}
        Sleep    0.5s
    END
    # narrow the list to the wanted text, then tick toggle-all -> selects the filtered set
    Fill Text    ${search}    ${match_text}
    Sleep    1s
    Click    ${hdr}
    Sleep    1s
    Click    ${panel} .ui-selectcheckboxmenu-close
    Wait For Load State    networkidle    timeout=20s
    Sleep    1.5s

Go To Groups Tree Page
    [Documentation]    The group tree is paginated; click the paginator page link with the
    ...    given number (e.g. the "Daily Sampling Validations" groups live on page 2).
    [Arguments]    ${page_num}
    Click
    ...    xpath=//*[contains(@id,"groups:form")]//*[contains(@class,"ui-paginator-page") and normalize-space(.)='${page_num}']
    Wait For Load State    networkidle    timeout=20s
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

Rule Should Positively Fire
    [Documentation]    Stronger than Rule Log Matches Oracle: assert the rule has REAL
    ...    violations on ${daytime} (oracle > 0) AND that EC's CTRL_CHECK_LOG matches that
    ...    oracle. Use to positively exercise a rule (not just assert "no false positives").
    [Arguments]    ${check_id}    ${daytime}
    ${oracle}=    Distinct Violation Objects For Rule    ${check_id}    ${daytime}
    Should Be True    ${oracle} > 0
    ...    msg=No violations on ${daytime} - cannot positively exercise rule ${check_id}
    Check Log Count Should Be    ${check_id}    ${daytime}    ${oracle}

Get Group Summary Warnings
    [Documentation]    Read the Summary cell for ${group_desc} and return the integer count
    ...    before " Warnings" (e.g. "0 Errors, 6 Warnings, ..." -> 6). Frozen rules log WARNINGs.
    [Arguments]    ${group_desc}
    ${idx}=    Find Group Row Index    ${group_desc}
    Should Be True    ${idx} >= 0    msg=Group not found in tree: ${group_desc}
    ${summary}=    Get Text    css=[id="groups:form:T:${idx}:C2_la"]
    ${m}=    Get Regexp Matches    ${summary}    (\\d+)\\s+Warnings    1
    Should Not Be Empty    ${m}    msg=Could not parse Warnings from summary: ${summary}
    RETURN    ${{int(${m}[0])}}

Group Summary Warnings Should Be Positive On Date
    [Documentation]    Set date + GO, then assert the group's UI Summary shows Warnings > 0
    ...    (visual confirmation that the frozen WARNINGs surfaced on screen for that date).
    [Arguments]    ${daytime}    ${group_desc}
    Set Validation Date Range And Go    ${daytime}    ${daytime}
    ${warns}=    Get Group Summary Warnings    ${group_desc}
    Should Be True    ${warns} > 0
    ...    msg=Expected frozen WARNINGs > 0 for ${group_desc} on ${daytime}, UI showed ${warns}

Frozen Rule Should Positively Fire
    [Documentation]    Frozen equivalent of Rule Should Positively Fire: independent oracle via
    ...    getValFrozenValue (Frozen Distinct Violation Objects), assert oracle > 0 AND EC's
    ...    CTRL_CHECK_LOG (populated by the UI group run) equals it. Proves UI run == DB truth.
    [Arguments]    ${check_id}    ${daytime}
    ${oracle}=    Frozen Distinct Violation Objects    ${check_id}    ${daytime}
    Should Be True    ${oracle} > 0
    ...    msg=No frozen violations on ${daytime} - cannot positively exercise rule ${check_id}
    Check Log Count Should Be    ${check_id}    ${daytime}    ${oracle}

Group Summary Errors Should Be On Date
    [Documentation]    Set the date window + GO (so the Summary reflects THAT date), then assert
    ...    the group's UI Summary "Errors". Self-contained, so multiple test dates don't interfere.
    [Arguments]    ${daytime}    ${group_desc}    ${expected}
    Set Validation Date Range And Go    ${daytime}    ${daytime}
    Group Summary Errors Should Be    ${group_desc}    ${expected}
