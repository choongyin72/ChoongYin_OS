*** Settings ***
Documentation       T3 (screen) — "Send Freetext Message" (MHM) page object — the N-notify pattern
...                 (the FIRST messaging/notification test, vs the N1/N2/N3 data-grid/run patterns).
...                 Send a freetext message via stock EC MHM, then DB-verify it journaled to MHM_MSG.
...                 Stock-MHM model (present in this sandbox); the same pattern maps to client
...                 implementations by swapping the table/action (AOPA stock MESSAGE_OUT, CLP custom
...                 ZXC_T_NOTIFICATION). See docs/pattern_n_notify_mhm_design.md.
...
...                 Real screen model (verified live 2026-06-15): nav = Date + Functional Area (EC) +
...                 Message Type (FRMW Test Msg 1 for message body) + Subject (Testing of Message Body)
...                 → GO → edit Template body → SEND. There is NO distribution/recipient selector;
...                 recipients are fixed by the message type's wiring.
...
...                 ⚠️ LIVE SEND GATED (outbound email): the FRMW free-text message type routes to
...                 receiver_1/2/3@energycomponents.com (a REAL domain). The sandbox is journal-only
...                 (outbound MHM_MSG = PREPARED, no sender node), but a synchronous send can't be 100%
...                 ruled out. A safe live run requires the message type first be wired to a
...                 non-deliverable (.invalid) distribution (a reversible MESSAGE_DISTRIBUTION change),
...                 or explicit approval. Oracle = MHM_MSG journal delta (DbVerify message_journal_*).
...                 Layered: this test → this T3 → message_send (T2) + common (T1) + DbVerify.

Library             Browser
Library             ../../libraries/DbVerify.py
Resource            ../../resources/message_send.resource


*** Variables ***
${MSG_SCREEN}             Send Freetext Message
# nav scope (FA -> Message Type cascade; Subject is a fixed-list popup)
${MSG_FA}                 EC
${MSG_TYPE_LABEL}         FRMW Test Msg 1 for message body
${MSG_SUBJECT_OPT}        Testing of Message Body
${MSG_DATE}               2024-02-06
${MSG_BODY}               AUTOTEST N-notify freetext — automated MHM journal test.
# MHM_MSG journal MSG_TYPE for this send (message-def code FRMW_TEST_MSG_1).
# ⚠️ CONFIRM on the first live send — the exact MSG_TYPE written to MHM_MSG is unverified
# (no live send has run yet; the suite is build-ready/gated).
${MSG_JOURNAL_TYPE}       FRMW_TEST_MSG_1
${MSG_BASELINE}           ${0}


*** Keywords ***
Open Send Freetext Screen
    [Documentation]    Suite Setup: launch, login, open the Send Freetext Message screen.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${MSG_SCREEN}    ${user}    ${pass}

Capture Journal Baseline
    [Documentation]    Record the current MHM_MSG outbound count for the message type (append-only
    ...    journal → a +1 delta after the send proves a fresh message was journaled).
    ${n}=    Message Journal Count    ${MSG_JOURNAL_TYPE}    O
    VAR    ${MSG_BASELINE}    ${n}    scope=SUITE

Send Freetext Notification
    [Documentation]    Drive nav (FA + Message Type + Subject) → GO → edit body → SEND.
    ...    ⚠️ Live send routes to the message type's wired (currently REAL-domain) distribution —
    ...    gate on a .invalid wiring or approval first.
    Set Message Send Navigator    ${MSG_DATE}    ${MSG_FA}    ${MSG_TYPE_LABEL}    ${MSG_SUBJECT_OPT}
    Fill Message Body    ${MSG_BODY}
    Send Message

Journal Should Have New Message
    [Documentation]    DB ground truth: MHM_MSG gained a new outbound row for the message type
    ...    (delta over the captured baseline) — the send was journaled.
    Message Journal New Row Should Exist    ${MSG_JOURNAL_TYPE}    ${MSG_BASELINE}    O
