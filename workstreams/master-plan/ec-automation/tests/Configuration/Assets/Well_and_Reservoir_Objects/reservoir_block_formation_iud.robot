*** Settings ***
Documentation       EC IUD Test - Reservoir Block Formation (CO.0137) - MULTI-OBJECT.
...                 RBF is a junction OV whose Reservoir Block + Reservoir Formation are dependent dropdowns.
...                 This suite creates a fresh Block + Formation, links them via RBF (full I-U-D), then tears
...                 down in reverse dependency order (RBF -> Formation -> Block). All DB-verified, self-cleaning.
...                 Layered: this test -> reservoir_block_formation_page (T3) -> manage_object (T2) + common (T1).

Resource            ../../../../pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/reservoir_block_formation_page.resource

Suite Setup         Open Reservoir Block Formation Suite
Suite Teardown      Tear Down Reservoir Block Formation Suite

Test Tags           iud    reservoir_block_formation


*** Variables ***
${SD}               ${TEST_START_DATE}
${BLK_CODE}         AUTOTEST_RFB_001
${BLK_NAME}         AUTOTEST RF Block 001
${FRM_CODE}         AUTOTEST_RFF_001
${FRM_NAME}         AUTOTEST RF Formation 001
${RBF_CODE}         AUTOTEST_RFR_001
${RBF_NAME}         AUTOTEST RF RBF 001
${RBF_NAME_UPD}     AUTOTEST RF RBF 001 UPDATED


*** Test Cases ***
TC01 Create Parent Block And Formation
    [Documentation]    Insert a fresh Reservoir Block + Reservoir Formation; confirm both in DB.
    [Tags]    setup
    Insert Plain Object    Reservoir Block Code    Reservoir Block Name    ${BLK_CODE}    ${BLK_NAME}    ${SD}
    Row Present    ${BLK_CODE}
    Code Should Be Present In View    OV_RESV_BLOCK    ${BLK_CODE}
    Go To Screen    Reservoir Formation
    Insert Plain Object    Reservoir Formation Code    Reservoir Formation Name    ${FRM_CODE}    ${FRM_NAME}    ${SD}
    Row Present    ${FRM_CODE}
    Code Should Be Present In View    OV_RESV_FORMATION    ${FRM_CODE}

TC02 Insert Reservoir Block Formation Linking Both
    [Documentation]    On RBF: select the new Block (populates Formation), then the new Formation; confirm in list + DB.
    [Tags]    insert
    Go To Screen    Reservoir Block Formation
    Insert Reservoir Block Formation    ${RBF_CODE}    ${RBF_NAME}    ${SD}    ${BLK_NAME}    ${FRM_CODE}
    Row Present    ${RBF_CODE}
    Code Should Be Present In View    OV_RESV_BLOCK_FORMATION    ${RBF_CODE}

TC03 Update Reservoir Block Formation
    [Documentation]    Edit RBF Name; confirm DB ground truth.
    [Tags]    update
    Update Object Name By Label    Resv Block Formation Code    Resv Block Formation Name    ${RBF_CODE}    ${RBF_NAME_UPD}
    Field Should Equal In View    OV_RESV_BLOCK_FORMATION    ${RBF_CODE}    NAME    ${RBF_NAME_UPD}

TC04 Delete Reservoir Block Formation
    [Documentation]    Delete RBF via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete
    Delete Object By End Date    ${RBF_CODE}    ${SD}
    Row Absent    ${RBF_CODE}
    Code Should Be Absent In View    OV_RESV_BLOCK_FORMATION    ${RBF_CODE}

TC05 Tear Down Parents In Reverse Order
    [Documentation]    Delete Formation then Block (reverse dependency order); confirm both gone from DB.
    [Tags]    cleanup
    Go To Screen    Reservoir Formation
    Delete Object By End Date    ${FRM_CODE}    ${SD}
    Code Should Be Absent In View    OV_RESV_FORMATION    ${FRM_CODE}
    Go To Screen    Reservoir Block
    Delete Object By End Date    ${BLK_CODE}    ${SD}
    Code Should Be Absent In View    OV_RESV_BLOCK    ${BLK_CODE}


*** Keywords ***
Tear Down Reservoir Block Formation Suite
    [Documentation]    Best-effort cleanup (reverse order) in case a TC failed mid-run, then close EC.
    Run Keyword And Ignore Error    Go To Screen    Reservoir Block Formation
    Run Keyword And Ignore Error    Delete Object By End Date    ${RBF_CODE}    ${SD}
    Run Keyword And Ignore Error    Go To Screen    Reservoir Formation
    Run Keyword And Ignore Error    Delete Object By End Date    ${FRM_CODE}    ${SD}
    Run Keyword And Ignore Error    Go To Screen    Reservoir Block
    Run Keyword And Ignore Error    Delete Object By End Date    ${BLK_CODE}    ${SD}
    Close EC
