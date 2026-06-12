*** Settings ***
Documentation       T1 area — Screen navigation: find/load a screen, expand to full page.

Library             Browser


*** Variables ***
# Screen min/max toggle — hides/restores the left treeview (expands the loaded screen)
${SCREEN_MINMAX_BTN}    css=[id="screenToolbar:form:minmaxMenu"]
${TREEVIEW_SEARCH}      css=[id="menu:searchForm:searchTxt"]


*** Keywords ***
Navigate To Screen
    [Documentation]    Open a screen via the sidebar search, confirm it loaded, then
    ...    expand it to full page (hide the treeview). Restores the treeview first if
    ...    a previous expand left it hidden, so repeated navigation keeps working.
    [Arguments]    ${screen_name}
    Restore Treeview If Hidden
    Type Text    ${TREEVIEW_SEARCH}    ${screen_name}    delay=60ms    clear=Yes
    Wait For Load State    networkidle    timeout=8s
    Sleep    0.5s
    Click
    ...    xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='${screen_name}']
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.5s
    ${label}=    Get Text    css=[id="screenToolbar:form:screenLabel"]
    Should Contain    ${label}    ${screen_name}    msg=Failed to navigate to ${screen_name}
    Expand Screen To Full Page

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
