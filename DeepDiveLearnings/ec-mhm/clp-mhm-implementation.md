# CLP (Hong Kong) — Notification/MHM Implementation (SME deep-dive, 2026-06-15)

Real client MHM implementation studied to deepen SME (CLP genuinely uses MHM). **Read-only** study of
the CLP client repo — I never commit to it ([[feedback_never_commit_without_permission]]); this synthesis
lives in MY repo (ChoongYin_OS).

## Sources (for reference; recorded here since DATA_SOURCES.MD is another session's working file)
- **CLP git (local clone):** `C:\DEV\GIT\ecaas_clp_hongkong` ← authoritative ("the one source for
  understanding the code and functionality" — per its readme; uses Git Flow: develop / feature/<jira> / release).
- **CLP Bitbucket:** https://bitbucket.org/energycomponents/clp_icms_ec_implementation/src/
- **CLP SharePoint:** https://qbsolapc.sharepoint.com/:f:/s/CLPECImplementationProject/... (separate
  tenant `qbsolapc` — not fetched here; the git source is authoritative anyway).

## Headline: CLP uses a CUSTOM notification framework, not stock EC MHM screens
Unlike Pluto (which configures the stock MHM: `MESSAGE_DEFINITION`/`MHM_MSG`), CLP built its OWN
notification layer in the **`zxapp`/`zxc` extensions** (`com.ec.extension.zxapp`), integrating
**AWS SES** (email) + **EIP** (enterprise integration platform / message broker). This is a key SME
lesson: **clients often REPLACE or EXTEND stock MHM** — so for any SOW, first determine which they use.

## Architecture (custom CLP notification flow)
```
business event (nomination/forecast/…)
  └─ NotificationAction (NominationNotificationAction / ForecastNotificationAction).generateNotification()
       └─ INSERT into ZXC_T_NOTIFICATION  (status = NEW/PENDING)        ← the queue + audit + ORACLE
            └─ [scheduled] SendNotifications (AbstractBusinessAction)
                 ├─ ZXC_P_NOTIFICATION.checkDistribution()  (PL/SQL — resolve recipients/distribution)
                 └─ processNotifications():  SELECT … FROM zxc_t_notification WHERE status=?
                      ├─ build email (email_to/cc/bcc_list), attach REPORT (report_no) / FILE_ATTACHMENT
                      ├─ send via **Amazon SES** (SMTP endpoint/port/user/pass)
                      └─ updateNotification(id, status = SENT)          ← status transition = the oracle
```
Other channels in `zxapp/mhm/`: **outbound** `SubmitMessageToEIP` / `TransferProcessor(+Schedule)` /
`GetTagsFromPI` (PI tag data → EIP); **inbound** `LoadInboundMessage`. Custom screens
`notification.xml` / `notification_detail.xml`.

## The test oracle — `ZXC_T_NOTIFICATION` (custom table)
Cols: `id`, **`msg_type`** (indexed), **`status`** (NEW→SENT), `production_day`, `send_date`,
`object_id`, `notification_text` (CLOB), `subject`, `email_to_list`/`cc`/`bcc`, `sender`, `report_no`,
`attachment_no`, + standard audit (`record_status`, `created_*`, `approval_*`).
**A CLP notification test would:** trigger the business event (or the NotificationAction) → assert a
`ZXC_T_NOTIFICATION` row exists (status NEW, right `msg_type`/`subject`/recipients) → run
`SendNotifications` → assert **status → SENT + `send_date` set** (delta-scoped; append-only audit).
DbVerify helpers: `zxc_notification_count(msg_type, day)` + `zxc_notification_status(id)`.

## SME takeaways (reusable for a CLP notification SOW)
1. **Identify the framework first.** CLP = custom (`ZXC_T_NOTIFICATION` + AWS SES + EIP). Pluto = stock
   MHM (`MHM_MSG`). The oracle table + trigger differ per client — never assume stock MHM.
2. **The pattern generalises** though: *event → notification row (status) → scheduled sender → delivery
   → status transition*. My "N-notify" oracle (row + status-delta) applies to BOTH; only the table +
   sender business-action name change.
3. **Triggers are Business Actions** (`AbstractBusinessAction.execute(Connection)`) wired to schedules —
   same scheduler/ec-worker execution model as N3 status processes. So a CLP notification test that
   uses the scheduled `SendNotifications` needs the worker running (or call the action directly).
4. **Delivery is AWS SES** (not classic SMTP relay) — verifying actual email receipt is out of scope;
   the **`ZXC_T_NOTIFICATION` status = SENT** is the trustworthy in-DB oracle.

## Status + next
SME on CLP's notification implementation: **architecture + oracle + trigger + delivery understood**
from the git source (authoritative). To BUILD a CLP notification test I'd need a CLP env/DB with the
`zxapp` extension + `ZXC_T_NOTIFICATION` data (the local generic sandbox is neither CLP nor Pluto).
Next options: (a) deeper read of `ZXC_P_NOTIFICATION` + the NotificationActions for the exact trigger
conditions; (b) the CLP SharePoint design docs (if access provided) for the SOW intent behind each
`msg_type`; (c) wait for a CLP env to build/verify against.
