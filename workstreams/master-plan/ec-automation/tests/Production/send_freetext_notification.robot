*** Settings ***
Documentation       EC N-notify Test — "Send Freetext Message" (MHM) → Message Journal oracle. The
...                 first messaging/notification pattern (alongside N1 edit-grids, N2 calc-runs, N3
...                 status-processes). Sends a freetext message via stock EC MHM and DB-verifies it
...                 journaled to MHM_MSG (append-only delta). Stock-MHM mechanism is present in this
...                 sandbox; the same pattern maps to client implementations (AOPA stock MESSAGE_OUT,
...                 CLP custom ZXC_T_NOTIFICATION) by swapping the oracle table. See DeepDiveLearnings/ec-mhm/.
...
...                 ⚠️ STATUS: BUILD-READY — the LIVE send is GATED. Real screen model (verified live):
...                 nav = Date + Functional Area (EC) + Message Type (FRMW Test Msg 1) + Subject
...                 (Testing of Message Body) → GO → edit Template body → SEND. There is NO distribution
...                 selector — recipients are fixed by the message type's wiring, which routes the stock
...                 FRMW free-text type to a REAL domain (@energycomponents.com). The sandbox is
...                 journal-only (outbound MHM_MSG = PREPARED, no sender node), but a synchronous send
...                 can't be 100% ruled out, so a safe live run needs the message type first wired to a
...                 non-deliverable (.invalid) distribution, or explicit approval. Outbound email is an
...                 external action — run live only when safe/approved.
...                 Layered: this test → send_freetext_message_page (T3) → message_send (T2) + DbVerify.
...                 Pattern + verified posture + paths to the live proof: docs/pattern_n_notify_mhm_design.md.

Resource            ../../pageobjects/Production/send_freetext_message_page.resource

Suite Setup         Open Send Freetext Screen
Suite Teardown      Close EC

Test Tags           n_notify    mhm    send_freetext


*** Test Cases ***
TC01 Freetext Send Journals To MHM_MSG
    [Documentation]    Capture the MHM_MSG baseline for the message type, send a freetext message, and
    ...    DB-verify a NEW outbound journal row appeared (delta) — proving the send→journal mechanism
    ...    end to end. The journal row is the trustworthy oracle (the sandbox journals as PREPARED — no
    ...    real transmission). ⚠️ Live send GATED — recipients are the message type's wired distribution
    ...    (currently the REAL-domain FRMW set); wire a .invalid distribution or get approval first.
    [Tags]    send
    Capture Journal Baseline
    Send Freetext Notification
    Journal Should Have New Message
    Capture Step    nnotify_tc01_freetext_journaled
