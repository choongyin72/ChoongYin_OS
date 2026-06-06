# DOC-09 — EC Extensions & Application Development
**Source:** EC 14.2.4 `ec-extensions` (17) + `appdev` (2) + `rest-api` (1) + `expression` (1) = 21 pages · **Read:** 2026-06-06

> How to extend EC **without modifying the product** — the supported customization path (vs the project-config/owner-context path in DOC-02).

## EC REST API
The entry point for new integrations/clients. Features:
- **Domain model REST API** — full query + **modify** of the EC Class Concept (insert/update/delete domain objects via REST). *(Another path to manipulate Bank/Equipment besides UI/DB — and it fires `DomainObjectChanged`, DOC-07.)*
- ECIS Agent support, **job scheduling** (trigger async jobs via scheduler), BPM config import/export.
- Design: HATEOAS; auto-generated **OpenAPI 3.0.3** (+ Swagger 2.0) docs served from the EC install.
- **Java SDK client**: maven `com.ec.frmw:frmw-core-api` (RestEasy client + EC authenticators). Examples in EC-SDK `examples/rest`.

## EC Extensions — concept & lifecycle
Extensions = **software projects (source → binary WAR)** deployed on top of EC, managed by EC. Full lifecycle control (start/stop/disable/update/db-migrate) via the **Extensions Manager** screen (Configuration → System → Develop). "Run on startup" = auto-start at EC boot (downloads from DB, verifies no pending migration). Quorum ships extensions (e.g. **EC Chemistry XCH**); customers can build their own. Multiple extensions run simultaneously.

## Creating an extension
- **Maven archetype** generates a skeleton project (correct file structure + pom with extensionID/name/description), or copy an existing one.
- Build: **`mvn clean install`** / `mvn clean package` → WAR artifact in `target/`.
- Can contain: Flyway DB scripts, custom business functions, business actions, Jasper reports, classes, Java, screens, online help, datamodel, PL/SQL, views, triggers, calculation libraries.
- **Maven project params:** `groupId` (com.ec.extension), `artifactId`, `package`, **`extensionId`** (≤5 letters — eats into the 100-char name budget), **`ownerContext`** (**≥1000** for customer), `ecVersion`, `version`.

## Install options (4)
1. **Extensions Manager** web UI (Select File → Upload → Start). 2. At **EC boot**. 3. **Maven** `ecextension-maven-plugin`. 4. **REST API**. (Stop + disable the old version before installing a new one.)

## 🔑 Strict rules for data-model changes (extensions)
- **Product tables/packages/views/triggers CANNOT be modified.**
- **Name prefixing** by extension id: tables `TPL_<name>`, packages `TPL_/ZP_TPL_/UEI_TPL_<name>`, views `TPL_V_<name>`, triggers `TPL_IU_<name>` (≤100 chars incl. id).
- Migration type: **table changes = versioned**; **packages/views/triggers = repeatable** (Flyway, in `src/main/webapp/WEB-INF/db`, **UTF-8**). Views/triggers depending on generated objects need `FORCE`.
- **Class changes** (extending a product class): new attributes/relations prefixed with ext id; `APP_SPACE_CNTX` = extension id; **`OWNER_CNTX ≥ 1000`**; never disable product attrs (use **`IGNORE_IND`**, DOC-02); `DB_MAPPING_TYPE = EXTENSION`; don't map to existing columns. *(All consistent with the owner-context override model in DOC-02.)*

## Dev environment (EC 14.x)
16 GB RAM / 4 cores / 200 GB; Docker + Java JDK (version-matched) + Maven + Eclipse/IntelliJ. Maven `settings.xml` configured for **EC Hub Nexus** (`hub.energycomponents.com`, your EC community login). EC-SDK has worked examples (`energycomponents-sdk/examples/...`).

## Create-EC-Extension artifact guides (pages 9–18, by title)
Classes · Java · Screens · Online Help · Reports (Jasper) · Datamodel · PL/SQL Package · Views · Triggers · Calculation Libraries — each a how-to for that artifact type within an extension.

## AppDev + Expression
- **Expression & Scripting support** — EC's expression language used across config (dynamic presentation, conditions, dashboard text, event payloads).
- **AppDev / `DomainEntityMgr`** — programmatic Java access to the domain model (the API layer over classes).

---

## Cross-links
- Extension class rules (prefix, `OWNER_CNTX≥1000`, `APP_SPACE_CNTX`, `IGNORE_IND`, `DB_MAPPING_TYPE=EXTENSION`) extend the **DOC-02** class/owner-context model.
- **REST domain API** = a 3rd way to do IUD (UI / direct-DB / REST) — all fire `DomainObjectChanged` (DOC-07). A REST-based EC-IUD automation is feasible (vs my Playwright UI approach).
- Flyway DB migration → DOC-11 databasedevelopment.
- Next: **DOC-10 GraphQL + Reporting + eDAC**.
