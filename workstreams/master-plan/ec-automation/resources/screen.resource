*** Settings ***
Documentation       T1 area — Screen navigation: find/load a screen, expand to full page.

Library             Browser


*** Variables ***
# Screen min/max toggle — hides/restores the left treeview (expands the loaded screen)
${SCREEN_MINMAX_BTN}    css=[id="screenToolbar:form:minmaxMenu"]
${TREEVIEW_SEARCH}      css=[id="menu:searchForm:searchTxt"]


*** Keywords ***
Dismiss Unsaved Changes Dialog If Present
    [Documentation]    EC shows its own "UNSAVED CHANGES" Yes/No/Cancel confirm when navigating
    ...    away from a dirty New Object form. If an earlier step failed mid-fill (e.g. a
    ...    dependent-dropdown timeout), this dialog can be left open and its overlay mask
    ...    (#confirmationForm:confirmation_modal) then intercepts every click for the rest of
    ...    the run - the whole suite silently stalls behind it. Detect + discard via No, so a
    ...    single earlier failure can't cascade into the entire suite hanging.
    ${present}=    Get Element Count    css=[id="confirmationForm:confirmation_modal"]:visible
    IF    ${present} > 0
        Log    Unsaved-changes dialog detected - discarding via No to unblock navigation    level=WARN
        Click    css=[id="confirmationForm:nobtn"]
        Wait For Load State    networkidle    timeout=10s
        Sleep    0.5s
    END

Navigate To Screen
    [Documentation]    Open a screen via the sidebar search, confirm it loaded, then
    ...    expand it to full page (hide the treeview). Restores the treeview first if
    ...    a previous expand left it hidden, so repeated navigation keeps working.
    [Arguments]    ${screen_name}
    Dismiss Unsaved Changes Dialog If Present
    Restore Treeview If Hidden
    Type Text    ${TREEVIEW_SEARCH}    ${screen_name}    delay=60ms    clear=Yes
    # The search-results list renders incrementally/async (verified via DOM probe, #237 item 4
    # TC05): a fuzzy superset match (e.g. "Reservoir Block Formation" for query "Reservoir
    # Formation") can appear before the exact match does. Wait for the EXACT target link itself,
    # not a fixed sleep, so a slow-to-render exact match is never clicked past.
    Wait For Elements State
    ...    xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='${screen_name}']
    ...    visible    timeout=10s
    Click
    ...    xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='${screen_name}']
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.5s
    Confirm Screen Loaded    ${screen_name}
    Expand Screen To Full Page

Confirm Screen Loaded
    [Documentation]    Assert the loaded screen's toolbar label matches ${screen_name}.
    [Arguments]    ${screen_name}
    ${label}=    Get Text    css=[id="screenToolbar:form:screenLabel"]
    Should Contain    ${label}    ${screen_name}    msg=Failed to navigate to ${screen_name}

Expand Screen To Full Page
    [Documentation]    Click the screen min/max toggle to hide the treeview so the
    ...    loaded EC screen takes the full page width (more data columns visible).
    Wait For Elements State    ${SCREEN_MINMAX_BTN}    visible    timeout=15s
    Click    ${SCREEN_MINMAX_BTN}
    Wait For Load State    networkidle    timeout=15s
    Sleep    0.5s

Restore Treeview If Hidden
    [Documentation]    If a previous expand hid the treeview, toggle it back so the
    ...    sidebar search box is usable again. No-op when the treeview is visible.
    ${visible}=    Get Element Count    css=[id="menu:searchForm:searchTxt"]:visible
    IF    ${visible} == 0
        ${toggle}=    Get Element Count    css=[id="screenToolbar:form:minmaxMenu"]:visible
        IF    ${toggle} > 0
            Click    ${SCREEN_MINMAX_BTN}
            Wait For Elements State    ${TREEVIEW_SEARCH}    visible    timeout=15s
            Sleep    0.5s
        END
    END
