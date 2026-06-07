*** Settings ***
Documentation       T1 area — Toolbar actions (the icon row). Currently Save;
...                 Refresh / Insert / Delete / Export land here as they are needed.

Library             Browser


*** Keywords ***
Save
    [Documentation]    Click the Save toolbar button (only when enabled).
    Click    xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.2s

Refresh Screen
    [Documentation]    Click the Refresh toolbar button to reload the grid from the DB
    ...    (so verification reads persisted data, not stale optimistic client state).
    Click    xpath=//a[@title='Refresh [Ctrl+r]']
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.2s
