# DOC-07 — ECIS (Integration Services) + Events
**Source:** EC 14.2.4 `frmw/event` (15) + `frmw/ecis` (10) = 25 pages · **Read:** 2026-06-06

## A. EC EVENTS (publish-subscribe)
Generic pub-sub on **Apache Camel** + **Apache ActiveMQ** (durable/persisted events). Async, concurrent, **no ordering guarantee**, subscribers must be thread-safe.

### Publishing
- **Automatic** (no config): `JobCompleted` (allocation/report done), `TaskStatus` (BPM status change), `ExtensionRunning/Stopping`, `CheckRuleIncident`, **`DomainObjectChanged`**.
- 🔑 **`DomainObjectChanged`**: set class property **`PUBLISH_EVENTS_IND=Y`** + regenerate view → an event fires on **any insert/update/delete** of that class, regardless of source (web, calc, ECIS, **direct DB**, REST). *(So my Bank/Equipment IUD operations would each publish a DomainObjectChanged event.)*
- **Programmatic:** Java (`EventMgr.getService().publish(channel, event)`), DB, or REST.
- **Inbound:** external systems POST `/rest/v1/services/event/types/{eventType}/events`.

### Subscribing
- **Config** (no code): **Schedules (CO.0130)** → Event Subscriptions tab, or **Event Route Configuration (CO.1081)**. Filter by event params (e.g. `className=TANK_DAY_INV_OIL`) → triggers a job. *(E.g. tank level changes → auto-run a calc/report.)*
- **Code:** `@SubscribeToEvent` annotation / `subscribe(...)`.
- **Execution modes:** Stateful Off = **Parallel**, On = **Serial**; `@Execution`: `Tx` (REQUIRED / REQUIRES_NEW / IGNORE), `redelivery` (maxRedeliveries/delay), `throttle` (maxRequestCount/timePeriod), `skipConcurrentEvents`.

### Event types & history
- Valid types in EC code **`CTRL_EVENT_TYPE`**; list via REST `/rest/v1/services/event/types`. Custom types: past-tense names (`orderShipped`); attrs `allowExternal`, `saveHistory`.
- History persisted in **`CTRL_EVENT_HISTORY`** (off by default for all; on for external; config in Maintain System Settings; batch size/timeout tuning).

### Outbound bridges (Event Routes, CO.1081)
- **WebHooks** → Azure LogicApp / MuleSoft etc. (POST full event JSON; auth: none/basic/OIDC; redelivery + throttle policies).
- **AWS SNS** (platform-specific payloads sns.default/apns/gcm/adm; expression language `${event.payload[...]}`).
- **Firebase Cloud Messaging** (service-account JSON).
- New systems: implement `EventRoute` (Camel `RouteBuilder`) or a custom subscriber.

## B. ECIS — EC Integration Services (data capture)
The module integrating EC with external parties: **SCADA/Tag-based** (metering) + **File integration** (row-based: Excel/CSV/Fixed/XML).

### Architecture
Two halves isolated by a **message queue**: **Source** (read external → write to queue) + **Target** (read queue → transform → store in EC). Scheduler triggers `SourceAction(config-id)` → reads adapter config → creates **DTOs** → queue.
- **TagService**: a tag = {tag id (meter), timestamp, value, quality}. **RowService**: arbitrary rows → `PackageService`/`ECClassService` on target.

### Components
- **ECIS Agent** (v12.0+): lightweight standalone **Java jar** placed near the data source (SCADA / file-drop), pushes to EC; all config lives in EC (Agent only needs the EC URI); client-credential auth (v13.2.9+). Download from Agent Configuration screen.
- **Advanced File Import**: framework for Excel (multi-sheet/crosstab/table/form), CSV, Fixed Width, XML. 4 steps: read source (source mappings) → staging → target mappings → store EC class. Interface Type = INSERT / "insert then update" / UPDATE. Drop-folder pickup.
- **Staging Table Extension**: for timestamp-grouped tag sets (e.g. well-test tags where one tag = well no, others = measurements — can't write until full set arrives; grouped by identical timestamp).
- **Source Adapter Configuration**: `config name` (must be EC code type **`DT_SOURCE_ID`**), `class` (adapter impl), `Sequential`, **`DEFAULT_RECORD_STATUS` = P/V/A** (must also set `trans_template.overwrite_status`), failover (multiple same-name configs + `RetryTimeout`). Adapters: OPC Classic/UA, `TagFileAdapter`, `RowFileAdapter` (DropFolder/CompletedFolder/ErrorFolder/BadFolder).
- **Sample Periods**: aggregation intervals (30min/1hr/2hr/1day) across time zones.

### Remote Endpoint Configuration (shared)
Generic config for EC "calling out" to 3rd-party systems (WebHooks, ECIS, mail). Credentials stored in a **Secret Storage** (environment-dependent, **NOT the EC DB**). `ClientConfigurationMgr.getService().getConfiguration(name)`; VALIDATE ENDPOINT button.

---

## Cross-links
- 🔑 **`DomainObjectChanged`** fires on every IUD — my Bank/Equipment inserts/updates/deletes would each emit one; a subscription could trigger downstream calc/report.
- ECIS writes via the **`TRANSFER_<op>`** Oracle user (DOC-03) into staging tables; `DEFAULT_RECORD_STATUS` ties to P/V/A (DOC-01/04).
- ECIS is the **data-capture path** feeding the data-grid screens (Daily Equipment Status, DOC-01 data classes).
- Remote Endpoint secret storage + WebHook/mail integration relate to the morning-briefing/messaging path (DOC-03 MHM).
- This was a flagged priority (Production/Calc/**ECIS**/Config) — now covered.
- Next: **DOC-08 BPM** (workflow engine behind the allocation BPMs in DOC-04).
