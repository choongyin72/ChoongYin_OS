*** Settings ***
Documentation       T1 area — the in-screen Navigator (the "Navigator can be configured"
...                 screen area): set cascading filter dropdowns and apply (Go).
...                 Distinct from screen.resource, which only navigates TO a screen.

Library             Browser


*** Keywords ***
Set Navigator Filter
    [Documentation]    Set a cascading autocomplete-dd navigator filter: click the
    ...    chevron, wait for the panel, then click the exact option (typing is unreliable).
    [Arguments]    ${group}    ${value}
    Click    css=[id="nav:form:${group}:R:1:C:0:dd_button"]
    Wait For Elements State    css=[id="nav:form:${group}:R:1:C:0:dd_panel"]    visible    timeout=10s
    Click    css=[id="nav:form:${group}:R:1:C:0:dd_panel"] >> text="${value}"
    Wait For Load State    networkidle    timeout=12s
    Sleep    0.9s

Apply Navigator
    [Documentation]    Click the navigator Go button to (re)load the list.
    Click    css=[id="button:form:B"]
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.2s
