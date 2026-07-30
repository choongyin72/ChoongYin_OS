*** Settings ***
Documentation       ONE-OFF diagnostic - from the Reservoir Block Formation screen, search
...                 "Reservoir Formation" and dump every matching tv-link element's real text/id,
...                 to see exactly why the click lands on the wrong node (#237 item 4, TC05).

Library             Browser
Resource            ../../workstreams/master-plan/ec-automation/resources/common.resource
Resource            ../../workstreams/master-plan/ec-automation/resources/screen.resource

Suite Teardown      Close Browser


*** Test Cases ***
Probe Tv Link Collision
    Launch EC And Open Screen    Reservoir Block Formation
    Restore Treeview If Hidden
    Type Text    ${TREEVIEW_SEARCH}    Reservoir Formation    delay=60ms    clear=Yes
    Wait For Load State    networkidle    timeout=8s
    Sleep    0.5s
    ${links}=    Evaluate JavaScript    ${None}
    ...    () => Array.from(document.querySelectorAll('.tv-link')).map(e=>({id:e.id, text:e.textContent.trim(), tooltip:e.getAttribute('data-tooltip')}))
    Log    TV-LINKS FOUND: ${links}    console=True
    Take Screenshot
