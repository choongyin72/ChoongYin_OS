*** Settings ***
Documentation       T2 pattern — N-notify: send a message via the EC MHM "Send Freetext Message"
...                 screen, to be DB-verified in the Message Journal (MHM_MSG). Cross-screen MHM
...                 send mechanics live here; the screen NAME + scope (message type, distribution,
...                 body) + the journal oracle live in the T3.
...
...                 Send gesture (DB-/UI-cracked 2026-06-15, mirrors EC's own SendFreetextMessagePage):
...                 navigator `nav:form` (Date G:0:C:0 + Message Type G:0:C:1:dd + Distribution
...                 G:0:C:2:dd) → GO `button:form:B` → compose in `template:form` → click
...                 `SendButton:form`. The send JOURNALS to MHM_MSG (the existing sandbox outbound
...                 rows sit STATUS=PREPARED → journaled-not-transmitted; the journal row is the oracle).
...
...                 ⚠️ SAFETY: only ever target a distribution whose recipients are NON-DELIVERABLE
...                 test addresses (e.g. an `@example.invalid` test distribution). NEVER send through a
...                 distribution that resolves to a real domain (the stock FRMW free-text set points at
...                 @energycomponents.com). See DeepDiveLearnings/ec-mhm/.

Library             Browser
Resource            common.resource


*** Variables ***
${MSG_DATE_FIELD}          nav:form:G:0:R:1:C:0:da_input
${MSG_TYPE_DD}             nav:form:G:0:R:1:C:1:dd
${MSG_DISTRIBUTION_DD}     nav:form:G:0:R:1:C:2:dd
${MSG_GO_BUTTON}           button:form:B
${MSG_SEND_BUTTON}         SendButton:form


*** Keywords ***
Set Message Send Navigator
    [Documentation]    Set the Send-Freetext navigator: Date + Message Type + Distribution, then GO to
    ...    load the compose panel. Use a SAFE (non-deliverable) distribution only.
    [Arguments]    ${date}    ${message_type}    ${distribution}
    Fill EC Date    ${MSG_DATE_FIELD}    ${date}
    Select EC Dropdown Option    ${MSG_TYPE_DD}    ${message_type}
    Select EC Dropdown Option    ${MSG_DISTRIBUTION_DD}    ${distribution}
    Apply Navigator

Fill Freetext Body
    [Documentation]    Fill the freetext compose form (template:form) with a subject/body. The exact
    ...    cell ids are resolved live on first run (template:form composite); kept here as the
    ...    single place the compose gesture lives.
    [Arguments]    ${subject}    ${body}
    Fill EC Field    template:form:subject    ${subject}
    Fill EC Field    template:form:body    ${body}

Send Message
    [Documentation]    Click the Send button. The message is journaled to MHM_MSG (assert the journal
    ...    delta next). Send only after a SAFE distribution + body are set.
    Click    css=[id="${MSG_SEND_BUTTON}"]
    Wait For Load State    networkidle    timeout=30s
    Sleep    1.0s
