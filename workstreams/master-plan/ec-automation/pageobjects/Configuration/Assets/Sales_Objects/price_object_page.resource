*** Settings ***
Documentation       T3 (screen) - Price Object page object.
...                 Screen: Configuration > Assets > Sales_Objects > Price Object.
...                 OV-GM (manage-object, groupmodel): the grid loads ONLY after the navigator's
...                 single mandatory Business Unit dropdown + GO (NOT a multi-level cascade - the
...                 2 other nav dropdown columns are unrelated optional filters, not children).
...                 Fields resolved BY LABEL (no hardcoded rows). Extra dropdowns first-available.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${SCR}              Price Object
${TBL}              manageObject:form:T_data
${DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
${GM_PU}            ${EMPTY}
${NAV_DD}            nav:form:G:0:R:1:C:1:dd


*** Keywords ***
Open Price Object Screen
    [Documentation]    Suite Setup: launch, login, navigate, fill the navigator's ONE mandatory
    ...    Business Unit dropdown first-available + GO, RETURN it. NOT a real cascade (the shared
    ...    "Apply OV-GM Navigator First Available" keyword tries columns 2/3 too, which exist on
    ...    this screen as unrelated OPTIONAL filters with 0 options, not cascade children - same
    ...    class of gap as Service/CO.2103) - fill the single dropdown directly instead.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCR}    ${user}    ${pass}
    Select First EC Dropdown Option    ${NAV_DD}
    ${pu}=    Get Property    css=[id="${NAV_DD}_input"]    value
    Apply Navigator
    RETURN    ${pu}

Price Object Row Should Exist
    [Documentation]    Assert ${code} is present (await lazy OV-GM redraw first).
    [Arguments]    ${code}
    Wait For Elements State
    ...    xpath=//tbody[@id='${TBL}']//span[normalize-space(text())='${code}']
    ...    visible    timeout=20s
    Row Should Exist    ${TBL}    ${code}

Price Object Row Should Not Exist
    [Documentation]    Assert ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${TBL}    ${code}

Price Object Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} persisted in OV_PRICE_OBJECT.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_PRICE_OBJECT    ${code}

Price Object Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} deleted from OV_PRICE_OBJECT.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_PRICE_OBJECT    ${code}

Price Object Row Should Show Name
    [Documentation]    Assert the row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${TBL}    ${code}    ${name}

Insert Price Object Record
    [Documentation]    Insert (all fields BY LABEL) + Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label       objectForm    Price Object Code    ${code}
    Fill OV Field By Label       objectForm    Price Object Name    ${name}
    Fill OV Date By Label        objectForm    Start Date    ${start_date}
    Fill OV Dropdown By Label    objectForm    Product Name    __FIRST__
    Fill OV Dropdown By Label    objectForm    Price Concept    __FIRST__
    Fill OV Dropdown By Label    objectForm    UOM    __FIRST__
    Fill OV Dropdown By Label    objectForm    Price Rounding Rule    __FIRST__
    Fill OV Dropdown By Label    objectForm    Business Unit    ${GM_PU}
    Save And Refresh List

Update Price Object Name
    [Documentation]    Select the row, edit Name (by label), save + reload.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${TBL}    ${code}
    Fill OV Field By Label    updateAttributes    Price Object Name    ${new_name}
    Save And Refresh List

Delete Price Object
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${TBL}    ${DEL_ENDDATE}    ${code}    ${date}
    Apply Navigator
