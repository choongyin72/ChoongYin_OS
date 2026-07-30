*** Settings ***
Documentation       Diagnostic: does the RF (Browser-library) dropdown gesture COMMIT + persist?
Resource            ../../workstreams/master-plan/ec-automation/pageobjects/Configuration/Assets/Revenue_Lists/input_list_page.resource
Suite Setup         Open Input List Screen
Suite Teardown      Close EC

*** Test Cases ***
Diag Insert With Dropdown
    Open New Object Form
    Fill OV Field By Label    objectForm    Code    AUTOTEST_DIAG_DD
    Fill OV Field By Label    objectForm    Name    AUTOTEST Diag DD
    Fill OV Date By Label    objectForm    Start Date    2000-01-01
    Fill OV Dropdown By Label    objectForm    List Category    INPUT
    ${v}=    Get Property    css=[id="tab:tabPanel:objectForm:form:G:0:R:6:C:1:dd_input"]    value
    Log To Console    \nDDVAL=${v}
    Save
    Sleep    1s
    Apply Navigator
    ${present}=    Run Keyword And Return Status    Code Should Be Present In View    ov_stream_item_collection    AUTOTEST_DIAG_DD
    Log To Console    DB_PRESENT=${present}
    [Teardown]    Run Keyword And Ignore Error    Delete Input List    AUTOTEST_DIAG_DD    2000-01-01
