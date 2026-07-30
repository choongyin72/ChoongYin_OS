*** Settings ***
Documentation       ONE-OFF diagnostic - inspect the REAL data-item-label values rendered in the
...                 dependent Reservoir Formation dropdown panel on the RBF screen, to prove
...                 whether TC02's timeout is a timing race or a label-text mismatch.

Library             Browser
Resource            ../../workstreams/master-plan/ec-automation/resources/common.resource
Resource            ../../workstreams/master-plan/ec-automation/resources/manage_object.resource
Resource            ../../workstreams/master-plan/ec-automation/resources/screen.resource
Resource            ../../workstreams/master-plan/ec-automation/resources/table.resource

Suite Teardown      Close Browser


*** Variables ***
${SD}               ${TEST_START_DATE}
${BLK_CODE}         AUTOTEST_PROBE_BLK
${BLK_NAME}         AUTOTEST Probe Block
${FRM_CODE}         AUTOTEST_PROBE_FRM
${FRM_NAME}         AUTOTEST Probe Formation


*** Test Cases ***
Probe Dropdown Labels
    Launch EC And Open Screen    Reservoir Block
    Apply Navigator
    Open New Object Form
    Fill OV Field By Label    objectForm    Reservoir Block Code    ${BLK_CODE}
    Fill OV Field By Label    objectForm    Reservoir Block Name    ${BLK_NAME}
    Fill OV Date By Label    objectForm    Start Date    ${SD}
    Save
    Apply Navigator
    Navigate To Screen    Reservoir Formation
    Apply Navigator
    Open New Object Form
    Fill OV Field By Label    objectForm    Reservoir Formation Code    ${FRM_CODE}
    Fill OV Field By Label    objectForm    Reservoir Formation Name    ${FRM_NAME}
    Fill OV Date By Label    objectForm    Start Date    ${SD}
    Save
    Apply Navigator
    Navigate To Screen    Reservoir Block Formation
    Apply Navigator
    Open New Object Form
    Fill OV Field By Label    objectForm    Resv Block Formation Code    AUTOTEST_PROBE_RBF
    Fill OV Field By Label    objectForm    Resv Block Formation Name    AUTOTEST Probe RBF
    Fill OV Date By Label    objectForm    Start Date    ${SD}
    Fill OV Dropdown By Label    objectForm    Reservoir Block    ${BLK_NAME}
    Wait For Load State    networkidle    timeout=15s
    Sleep    1s
    # Now open the Formation dropdown WITHOUT selecting - just dump what's really there
    ${id}=    Get Attribute
    ...    xpath=//span[contains(@class,'ECCell') and contains(@id,':objectForm:form:') and normalize-space(text())='Reservoir Formation']/ancestor::div[contains(@class,'tableCell')][1]/following-sibling::div[contains(@class,'tableCell')][1]//input[contains(@id,'dd_input')]
    ...    id
    ${dd}=    Set Variable    ${id.replace('_input', '')}
    Click    css=[id="${dd}_button"]
    Sleep    2s
    ${rows}=    Evaluate JavaScript    ${None}
    ...    () => Array.from(document.querySelectorAll('[id$="${dd}_panel"] tr[data-item-label]')).map(e=>({label:e.getAttribute('data-item-label'), text:e.textContent.trim()}))
    Log    ROWS FOUND: ${rows}    console=True
    Take Screenshot
