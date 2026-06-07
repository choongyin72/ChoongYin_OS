*** Settings ***
Documentation       T1 area — Screen navigation: find/load a screen.

Library             Browser


*** Keywords ***
Navigate To Screen
    [Documentation]    Open a screen via the sidebar search and confirm it loaded.
    [Arguments]    ${screen_name}
    Type Text    css=[id="menu:searchForm:searchTxt"]    ${screen_name}    delay=60ms    clear=Yes
    Wait For Load State    networkidle    timeout=8s
    Sleep    0.5s
    Click
    ...    xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='${screen_name}']
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.5s
    ${label}=    Get Text    css=[id="screenToolbar:form:screenLabel"]
    Should Contain    ${label}    ${screen_name}    msg=Failed to navigate to ${screen_name}
