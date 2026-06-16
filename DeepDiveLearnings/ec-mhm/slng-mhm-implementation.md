# SLNG (Singapore LNG) — Notification / MHM implementation (SME deep-dive)

Read-only recon of the client repo `C:\DEV\GIT\ecaas_slng_singapore` (READ-ONLY — see
[[reference_slng_project_sources]]). Verified against the source 2026-06-15 (grep-confirmed the table,
package, and Java business action below). Fourth MHM flavor studied alongside CLP, AOPA, Pluto.

## Verdict — HYBRID (custom queue table → stock MHM), bridged by a **Java business action**

SLNG is a **custom-table + stock-MHM hybrid**, and the distinctive trait vs the other clients is that
the bridge from the custom layer into EC's stock MHM is a **Java business action**, not pure PL/SQL.

```
business events ──(ZP_NOTIFICATIONS.*)──▶ Z_NOTIFICATION (status=NEW)   ← custom queue table
                                               │
                              EC Scheduler job "SendNotifications" (a Java business action)
                                               │  com.ec.slng.messages.outbound.SendNotifications
                                               ▼
                    MESSAGE_OUT  +  RECIPIENT      ← stock EC MHM tables (INSERT from Java)
                                               │   recipients/delivery from COMPANY_CONTACT_VERSION
                                               ▼
                    MHM framework → MHM_MSG journal → SMTP delivery
                                               │
                                  Z_NOTIFICATION.status = PROCESSED
```

## Components (verified file paths, repo-root relative)

**Custom queue table — `Z_NOTIFICATION`** (status NEW/SENT/PROCESSED; notification_code, send_date,
contract_id, notification_text, confirm_needed, recipient_list):
- `extensions/z/z/.../db/migration/1.0.0/0100_Data_Model_Changes/V1.0.0.0101.0112__Z_TABLE_TRIGGER.sql`

**Producer package — `ZP_NOTIFICATIONS`** (PL/SQL; inserts rows into Z_NOTIFICATION on business events:
`scheduleNotifications`, `changeSubmitNotification`, `fcstSubmitNotification`, `blPublishNotification`,
`freetextNotification`, + pipeline/tranche/cargo procedures; `dlPreCheck('DLCHECK')` pre-hook):
- spec: `extensions/z/z/.../0200_Package_definitions/V1.0.0.0200.0053__ZP_NOTIFICATIONS_head.sql`
- body: `extensions/z/z/.../common/packages/R__0200_ZP_NOTIFICATIONS_body.sql` (~6.3k lines)

**Bridge — Java business action `SendNotifications`** (polls Z_NOTIFICATION WHERE status='NEW', resolves
distribution via MESSAGE_DISTRIBUTION/DISTRIBUTION_SET_CONTACT, `INSERT INTO message_out` (line 258) +
RECIPIENT rows from COMPANY_CONTACT_VERSION delivery_method/address):
- `extensions/zxapp/zxapp/src/main/java/com/ec/slng/messages/outbound/SendNotifications.java`

**MHM broker customization — `SLNGMessageBrokerAdapter`** (extends stock IMessageBroker; caps rows
returned from MHM_MSG to avoid EC crashes):
- `extensions/zxapp/zxapp/src/main/java/com/ec/slng/mhm/SLNGMessageBrokerAdapter.java`
- stock broker registered: `extensions/z/z/.../0900_Extension_Scripts/V1.0.0.0900.0004__USE_STD_MESSAGE_BROKER.sql`

**Config seed (dataload):**
- message types → `OV_MESSAGE_DEFINITION` (I_NOMINATION, I_PIPELINE_NOMINATION, I_45DAY_SUBMIT, …; maps
  inbound loads to `com.ec.slng.messages.inbound.*`):
  `extensions/z/z/.../0900_Extension_Scripts/V1.0.0.0900.0005__OV_MESSAGE_DEFINITION.sql`
- distribution sets (TV_DISTRIBUTION_SET / _CONTACT, e.g. `N_STPUT_PCI`):
  `extensions/zmd/zmd/.../0900_Extension_Scripts/V1.0.0.0900.2307061804__STPUT_PCI_Notification_Message_Config.sql`
- scheduler jobs (incl. "SendNotifications" — disabled in this snapshot):
  `extensions/z/z/.../0900_Extension_Scripts/V1.0.0.0900.0032__Disabled_EC_Scheduled_Jobs.sql`

## Client prefix
`Z` (core extensions: `Z_*` tables, `ZP_*` packages). Domain modules carry their own folder prefixes
(`zmd`, `zxapp`, `zdp`, `zjr`, …). No single 3-letter object prefix like CLP `ZXC` / AOPA `ZWA` /
Pluto `ZWP`.

## Compared to the other flavors

| Client | Store | Bridge to delivery | Channel | Closest trait |
|---|---|---|---|---|
| **SLNG** | custom `Z_NOTIFICATION` queue → stock `MESSAGE_OUT`/`MHM_MSG` | **Java business action** (`SendNotifications`) | SMTP via COMPANY_CONTACT_VERSION | hybrid, Java-bridged |
| CLP | custom `ZXC_T_NOTIFICATION` | EIP | AWS SES | fully custom |
| AOPA | stock `MESSAGE_OUT` | PL/SQL `ZWA_P_NOTIFICATIONS` | SMTP | stock + PL/SQL |
| Pluto | stock `MHM_MSG` | `ZWP_P_MAIL_UTIL` | SMTP | stock MHM |

**Closest match: AOPA** (custom notification package + stock MESSAGE_OUT + SMTP). **Key differences:**
SLNG interposes its own `Z_NOTIFICATION` queue table before MESSAGE_OUT (AOPA writes MESSAGE_OUT more
directly), and SLNG does the Z_NOTIFICATION→MESSAGE_OUT mapping in **Java** (a business-action class)
rather than PL/SQL. SLNG is NOT AWS-SES/custom-table-terminal like CLP, and does not use MHM_MSG as the
primary store like Pluto (MHM_MSG is downstream/journal only).

## Implications for an EC-test (N-notify) of SLNG
- **Oracle options:** (a) `Z_NOTIFICATION` row created with status=NEW after a business event (tests the
  producer `ZP_NOTIFICATIONS`); (b) status transition NEW→PROCESSED + a new `MESSAGE_OUT`/`MHM_MSG` row
  after the `SendNotifications` scheduler action runs (tests the bridge). The append-only +delta pattern
  (as in the Pluto MHM_MSG suite) applies to all three tables.
- **Trigger:** the bridge needs the "SendNotifications" scheduler job enabled + a node firing it
  (recall the generic-sandbox finding: status/send jobs don't advance with no scheduler node). Producer
  procedures fire on business events (submit/publish), so a producer-only test can be screen-driven.
- **Safety:** same outbound-email caution as the generic sandbox — verify recipient domains in the
  configured TV_DISTRIBUTION_SET_CONTACT before any live send.

## Deeper-dive next steps (when picked up)
1. Read `R__0200_ZP_NOTIFICATIONS_body.sql` to map each `*Notification` producer → its business event +
   notification_code → distribution.
2. Read `SendNotifications.java` end-to-end (recipient resolution + MESSAGE_OUT/RECIPIENT insert shape).
3. Inventory the SLNG message types in `OV_MESSAGE_DEFINITION` + their distribution sets.
4. Confirm whether SLNG runs in our reachable sandbox or only in an SLNG env (decides if a live N-notify
   test is even possible here).
