# Woodside AOPA — Notification/MHM Implementation (SME deep-dive, 2026-06-15)

2nd real client MHM implementation (after CLP), studied **read-only** from the client repo
`C:\DEV\GIT\ecaas_woodside_aopa` — never committed to ([[feedback_never_commit_without_permission]]);
synthesis lives in MY repo. AOPA is the most valuable example because it uses the **stock EC MHM
tables that also exist in my sandbox** → closest to a *buildable* notification test.

## Headline: AOPA = STOCK EC MHM data model + CUSTOM orchestration (a hybrid)
Where CLP built a fully-custom table (`ZXC_T_NOTIFICATION` + AWS SES), AOPA keeps the **stock MHM
schema** (`MESSAGE_OUT`, `MESSAGE_DEFINITION`, `DISTRIBUTION_SET`, `dv_message_distribution`,
`tv_distribution_set_contact`, `dv_RECIPIENT`) and wraps it with a custom PL/SQL package + a custom
Java sender + a daily schedule.

## Architecture (stock tables, custom glue)
```
business logic / report-ready event
  └─ ZWA_P_NOTIFICATIONS (PL/SQL)
       ├─ findRecipientList(msg_type, recipient_type, object_id)  ← from dv_message_distribution + tv_distribution_set_contact
       ├─ findDistributionList(role)                              ← comma-delim TO addresses by ROLE
       ├─ findAssignedEmailAddress(assignee)                      ← for Todo-task notifications
       └─ storeMessage(...)  → INSERT into stock MESSAGE_OUT (TRANSMIT_STATUS='N', ACKNOWLEDGE_IND='N')   ← QUEUE + ORACLE
            └─ [daily schedule 'ZWA_SEND_NOTICATIONS' on ECDS] → SendNotifications (AbstractBusinessAction)
                 ├─ SELECT … FROM message_out WHERE TRANSMIT_STATUS=? AND ACKNOWLEDGE_IND='N'
                 ├─ recipients from dv_RECIPIENT (TO/CC/FROM); attach REPORT / message_attachment
                 ├─ send via **GenericSMTPClient** (ENDPOINT_CONFIG 'default-smtp-endpoint')
                 └─ updateNotification(): UPDATE message_out SET TRANSMIT_STATUS=? (sent)
```
Also a `ZWA_Update_Text_MHM_Msg` action (`GenericRunSqlAction` → `ZWA_P_NOTIFICATIONS.updateMsgOriginal`).
Stock config deployed via Flyway: `MESSAGE_DEFINITION`, `MESSAGE_FORMAT`, `DISTRIBUTION_SET(+_CONTACT)`,
`MESSAGE_DISTRIBUTIONS`, `MESSAGE_CONTACT`, `MESSAGE_CONFIG` + packages `ZWA_P_NOTIFICATIONS`/`ZWA_P_MAIL_UTIL`.

## The test oracle — stock `MESSAGE_OUT`
Key cols (from `ec-mhm-sme.md`): `MESSAGE_NO`, `SUBJECT`, `MESSAGE`, `MESSAGE_DISTRIBUTION_NO`,
**`TRANSMIT_STATUS`** ('N' queued → flipped after send), `ACKNOWLEDGE_IND`. A notification test:
- **generate half:** call the trigger (or `ZWA_P_NOTIFICATIONS.storeMessage`) → assert a new
  `MESSAGE_OUT` row (TRANSMIT_STATUS='N', right subject + `MESSAGE_DISTRIBUTION_NO`/recipients).
- **send half:** run `SendNotifications` (or the schedule) → assert `TRANSMIT_STATUS` flips to sent.
DbVerify: `message_out_count(status)` + `message_out_status(message_no)`.

## 3-client SME contrast (the reusable lesson)
| Client | MHM flavor | Generate (trigger) | Queue/oracle table | Send + delivery |
|---|---|---|---|---|
| **CLP** | fully custom | `NotificationAction.generateNotification()` | **`ZXC_T_NOTIFICATION`** (status NEW→SENT) | `SendNotifications` → **AWS SES** + EIP |
| **AOPA** | **stock schema + custom glue** | `ZWA_P_NOTIFICATIONS.storeMessage()` | **`MESSAGE_OUT`** (TRANSMIT_STATUS) | `SendNotifications` → **`GenericSMTPClient`** SMTP |
| **Pluto** | stock MHM | (stock MHM + `ZWP_P_MAIL_UTIL`) | **`MHM_MSG`** / `MESSAGE_OUT` | SMTP *(on hold)* |
**Pattern (all three):** *event → notification row (a status field) → scheduled sender business action
→ delivery → status transition.* Only the **table + sender action + delivery channel** differ. So my
"N-notify" test shape is client-agnostic — point it at the right table + action per client.

## Why AOPA is the best build target
The stock tables AOPA uses (`MESSAGE_OUT`, `MESSAGE_DEFINITION`, `DISTRIBUTION_SET`, `dv_RECIPIENT`)
**are present in my generic sandbox** — so a stock-MHM notification test (seed/generate a `MESSAGE_OUT`
row → run a send action → assert `TRANSMIT_STATUS` flip) is **buildable here** as a pattern, then the
AOPA-specific message types/distributions swap in at the AOPA env. The schedule runs on **ECDS** (the
same scheduler/ec-worker model as N3) — so the scheduled send needs the worker, or call the action directly.

## Status + next
SME on AOPA's notification implementation: architecture + oracle + trigger + send + config understood
from the git source. Building/verifying needs an AOPA env (or seeding the stock MHM config locally).
Next options: (a) read `ZWA_P_NOTIFICATIONS.storeMessage` for the exact INSERT (what populates
MESSAGE_OUT) + the message types AOPA defines; (b) prototype the generic stock-MHM "N-notify" test in
the sandbox (MESSAGE_OUT + a send action) since those tables are present; (c) hold for an env.
