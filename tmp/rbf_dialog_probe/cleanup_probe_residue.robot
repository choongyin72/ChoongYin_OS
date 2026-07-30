*** Settings ***
Documentation       Self-clean residue left by probe_dropdown_labels.robot (AUTOTEST_PROBE_BLK /
...                 AUTOTEST_PROBE_FRM saved as parents but never torn down). Delete via
...                 End Date = Start Date, the standard pattern for this screen family.

Library             Browser
Resource            ../../workstreams/master-plan/ec-automation/resources/common.resource
Resource            ../../workstreams/master-plan/ec-automation/resources/manage_object.resource
Resource            ../../workstreams/master-plan/ec-automation/resources/screen.resource
Resource            ../../workstreams/master-plan/ec-automation/pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/reservoir_block_formation_page.resource

Suite Teardown      Close Browser


*** Variables ***
${SD}    2000-01-01


*** Test Cases ***
Clean Up Probe Residue
    Launch EC And Open Screen    Reservoir Formation
    Apply Navigator
    Delete Object By End Date    AUTOTEST_PROBE_FRM    ${SD}
    Row Should Not Exist    ${OV_MANAGE_OBJECT_TABLE}    AUTOTEST_PROBE_FRM
    Navigate To Screen    Reservoir Block
    Apply Navigator
    Delete Object By End Date    AUTOTEST_PROBE_BLK    ${SD}
    Row Should Not Exist    ${OV_MANAGE_OBJECT_TABLE}    AUTOTEST_PROBE_BLK
