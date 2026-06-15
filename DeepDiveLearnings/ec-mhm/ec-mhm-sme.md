# EC Notification / MHM — SME Knowledge + Test-Pattern Design (2026-06-15)

Phase-1 (learn) + Phase-2 (feasibility recon) of the SME deep-dive into EC's notification layer, so a
client SOW notification requirement can be turned into DB-verified automation. Sources: Pluto As-Built
11 (`business-domains/ASBUILT11-NOTIFICATION.md`), live sandbox DB recon (`tmp/scripts/mhm_recon*.py`).

## 1. The domain model (how EC notifies a human)
EC raises **two** notification kinds, usually together:
1. **Email** via the **Message Handling Module (MHM)** — manual or BPM/trigger-fired.
2. **To-do task** — appears on the TODO screen + the menu bell (jBPM-backed work queue).

Flow: **event** (validation fail, approval gate, threshold) → **Message Type** resolves the template +
recipients → **Message Distribution** binds Type → **Distribution List** (role→mailbox) → message is
sent and **logged in the Message Journal**. The Journal is the audit trail = the **test oracle**.

## 2. Config layer (screens → tables) — DB-confirmed
| Concept | Screen | Table (sandbox-confirmed) |
|---|---|---|
| Message Type / Definition | CO.0142 / Maintain Message Type | **`MESSAGE_DEFINITION`** (key `OBJECT_CODE`, date-effective) |
| Message Format | CO.0143 | `MESSAGE_FORMAT` |
| Freetext body template | CO.0144 | `MESSAGE_TEMPLATE` |
| Distribution List | MHM.0001 | **`DISTRIBUTION_SET`** (`DISTRIBUTION_SET_CODE`,`NAME`) + `DISTRIBUTION_SET_CONTACT` |
| Message Distribution (bind Type→List) | MHM.0004 | `MESSAGE_DISTRIBUTION` (+`MESSAGE_DISTR_CONN`/`_PARAM`) |
| Actor / Message Contact | MHM.0012 | (contact registry; Contact Code 1:1 with User ID) |
| **Message Journal (audit log)** | MHM.0007 | **`MHM_MSG`** ← THE ORACLE |
| Outbound queue | — | `MESSAGE_OUT` |
| SMTP endpoint | Remote Endpoint Config (event-route layer) | (config, not OV) |

## 3. The oracle — `MHM_MSG` (Message Journal), 34 cols
Audit columns that matter for a notification test:
`DIRECTION` (I/O), `MESSAGE_ID`, `MSG_TYPE` (→ the Message Type code), `STATUS`
(PREPARED/ACCEPTED/SENT/…), `SUBJECT`, `SENDER`, `RECIPIENT`, `RECEIVED_DATE`, `EXTERNAL_REF`,
`ACKNOWLEDGED`, `TRANSPORT`. A notification test asserts: **after the trigger, a new `MHM_MSG` row
exists for the expected `MSG_TYPE`/`RECIPIENT` with the right `SUBJECT`/`STATUS`** (delta over a
captured baseline — `MHM_MSG` is append-only like `STAT_PROCESS_STATUS`).
The **Todo/task half** lives in the jBPM tables (`EC_JBPM_TASK` / `JBPM_TASK` / `TASK` / `TASK_DETAIL`).

## 4. ⛔ Feasibility verdict — NOT testable in THIS sandbox (wrong environment)
Ground truth (`mhm_recon3.py`):
- **`MESSAGE_DEFINITION` = 8 codes, all generic** (`MHM13_DNA/DNM/EDIGAS/FREETEXT/TEST_IN`,
  `FRMW_TEST_MSG_1`, `P3_MESSAGE_DEF`, `TEST_MSG_1`). **`N_R_D_VALIDATION_REVIEW` is absent** (0 codes
  match VALID/N_R).
- **`DISTRIBUTION_SET` = 4 generic lists** (`EC111_DIST_LIST`, `FRMW_DISTR_SET_FREE_TEXT`,
  `MHM13_OCH_WL`, `TEST_LIST`) — **NOT** the 8 Pluto `DL_PLU_DL_*` from As-Built 11.
- **`MHM_MSG` = 16 rows, all old MHM13 dispatching test messages** (2019–2025); `MESSAGE_OUT` = 0,
  `JBPM_NOTIFICATION` = 0 → nothing has ever fired a business notification here.
⇒ **This is a generic EC dev/test sandbox, not the Pluto COPS DEV** where the As-Built 11 MHM config
lives. The Pluto live notification can't be triggered or journal-verified here. (Consistent with the
multi-client nature of EC — [[reference_ec_multiclient_asbuilt]] — and the COPSDEV-is-separate note.)
**Phase-3 (build the live notification test) is blocked on environment, not knowledge.**

## 5. Ready-to-execute test design (for the real client env, when available)
When run against an env that HAS the client MHM config (e.g. Pluto COPS DEV with `N_R_D_VALIDATION_REVIEW`):
1. **Baseline:** capture `SELECT COUNT(*) FROM MHM_MSG WHERE MSG_TYPE=:t` (+ the jBPM task count) for
   the target Message Type, on the scope date.
2. **Trigger:** run the upstream event — for `N_R_D_VALIDATION_REVIEW` that's a daily-validation
   review task creation (ties to the Validation Overview suite + Issue_1052). Reuse
   `validation_overview_*` to raise the validation, which creates the review Todo.
3. **Oracle (DB ground truth):** assert a NEW `MHM_MSG` row (delta +1) for the Type with the expected
   `RECIPIENT` (the role DL) + `SUBJECT` (after PARAM substitution), AND a new jBPM task for the
   assignee. New DbVerify helpers: `message_journal_count(msg_type, date)` +
   `message_journal_latest(msg_type, date)` (mirror the `STAT_PROCESS_STATUS` delta pattern).
4. **Self-clean:** notifications/journal are append-only audit rows — do NOT delete; instead scope the
   assertion to the test's own trigger (delta), and (if a Todo was created) complete/cancel it via the
   reverse task action, or leave the audit row (it's a log, not state). Decide per env policy.
5. **Pattern name:** "N-notify" (event→message-journal oracle) — a new pattern type alongside N1/N2/N3.

## 6. SME status
Domain model + config→table map + the `MHM_MSG` oracle + the trigger chain are **understood
(reference-grade)**. The only gap is environmental (no client MHM config in this sandbox). When a
client SOW notification requirement lands WITH its environment, this design drops straight in. Next
depth (optional): EC Tech Docs 14.2.5 MHM module + the event-route/SMTP layer for the delivery-side
detail; not needed for the journal-oracle test.
