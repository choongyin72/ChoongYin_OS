# DOC-11 — IAM + Database Development + Containers
**Source:** EC 14.2.4 `iam` (9) + `databasedevelopment` (4) + `containers` (10) + `flyway`/`blobstorage`/`tools` (5) = 28 pages · **Read:** 2026-06-06
**(Final session — 11 of 11)**

## A. Container topology (the EC deployment architecture) 🔑
EC is deployed as a set of **Docker images** (Kubernetes/OpenShift/Docker-Swarm), each env-configured via an env-file. The full stack:

| Image | Role | Notes / DB user |
|---|---|---|
| **ec-app** | EC Application (WildFly) | `ENERGYX_EC`; `EC_SESSION_TIMEOUT` |
| **ec-bpm** | jBPM engine / BPM Console (DOC-08) | separate server group |
| **ec-keycloak** | **Identity manager (Keycloak)** | `KCKERNEL_EC`; `KC_HOSTNAME` |
| **ec-keycloak-migration** | Keycloak config (realms/clients/service-accounts) | **init-container**, Flyway-driven (versioned + repeatable) |
| **ec-ra** | Reporting & Analytics (**Yellowfin**) | `YFKERNEL_EC` + `ANALYTICS_EC`; SAML to Keycloak |
| **ec-messaging** | Message broker (events/MHM, DOC-07) | `ENERGYX_EC`; durable msgs dropped after **10 days**; JMS paging to DB |
| **ec-clam-av** | **Antivirus** (ClamAV) | scans ALL uploads (screens + REST); never expose port |
| **ec-analytics-manager** (+ `-runner`) | external-simulator analytics jobs (DOC-04) | `AMKERNEL_EC`; OIDC client `analytics-manager` |
| **db** | Oracle | the schemas from DOC-03 |

DB connection via `DB_URL=jdbc:oracle:thin:@//host:1521/ORCL` (or DB_HOSTNAME/PORT/SERVICENAME).

## B. IAM (Keycloak) 🔑
**Keycloak = authentication + authorization master.**
- **Users / roles / groups** managed in Keycloak or EC business functions. **EC 14.0.0+: `T_BASIS_USER`/`T_BASIS_USERROLE` removed → now META classes** reading from Keycloak (visible in app/REST/BPM, **not in the DB**).
- **Roles** exist in both Keycloak and EC (**Keycloak is master**); sync via **Role Maintenance** screen (the Keycloak-sync button I saw in recon!). Object access defined in Object Maintenance.
- **Identity brokering** (OIDC/SAML to Azure AD / Okta / Google — recommended: OIDC) + **user federation** (LDAP/AD). 
- **Session timeout**: `EC_SESSION_TIMEOUT` must equal Keycloak "SSO Session Idle".
- Keycloak realm settings: **audit logging** (login/admin events), **Brute Force Protection**, **Password Policy**, **User Account Service** (`/auth/realms/energyx/account`).
- **`jbpmengine`** = service account for the `bpm-client` client (runs BPM, DOC-08).
- 🔑 **Service Accounts for external integration**: each integration gets its own Keycloak **client + service account**, assigned **minimum** EC roles (access configured in Role/Object Maintenance). **Client Credential Flow** (M2M: client id + secret → access token) — for CLIs/daemons/backends. `created_by`/`last_updated_by` = the service-account username. Delivered accounts: `ecworker` (`service-account-ecworker`), etc. *(This is how an external automation — or a fixed morning-briefing-style integration against EC's own APIs — should authenticate: a dedicated service account + client-credentials, not a user login.)*

## C. Database Development
- **Data Modelling Guideline** — standards for EC data model design.
- **EC Flyway Developer Handbook** + **Flyway in EC**: migrations are **versioned** (one-time, e.g. table changes) vs **repeatable** (re-applied on change, e.g. packages/views/triggers) — the model used by product, extensions (DOC-09) and Keycloak-migration.
- **PL/SQL Coding Standard & Style**; **Custom Oracle Error Messages**.

## D. Tools & misc
- **Online Help**: context-sensitive per screen; stored in `business_function` + `bf_description` tables (+ images); editable in-app (onlinehelp access object, DOC-01); extractable for cross-DB import.
- **PKI** (Public Key Infrastructure): screens can require **digital signing** of insert/update/delete (smart-card certificate, e.g. Buypass; PIN to confirm) — the signed data is wrapped and stored with the user's signature. *(A signing-enabled screen would change the IUD save flow — relevant if a future target screen requires PKI.)*
- **Password Encryption Tool** (`password-encryption-tool-14.2.4.jar`, WildFly Elytron): ENCRYPT / MIGRATE plaintext or legacy-encrypted passwords (replaces `encrypt_pw.bat`).
- **Blob Storage Service**: multi-provider (AWS S3 / Azure Blob / Local Folder) via Java ServiceLoader (`@ServiceProvider`), `BLOBSTORAGE_*` env config; `BlobStorageProvider` (upload/download/delete) + `BlobStorageMgr.getService()`.

---

## Cross-links
- Keycloak IAM = the auth layer behind DOC-01 Users/Roles/Access + Role Maintenance recon; `jbpmengine` (DOC-08); service accounts (DOC-07/09 REST/integration).
- Container topology shows where every prior module physically runs; DB users tie to DOC-03.
- 🔑 **Service account + client-credentials** is the correct pattern for an unattended integration hitting EC's own REST/GraphQL APIs — far cleaner than UI automation for future EC-IUD work.
- Flyway versioned/repeatable migrations = DOC-09 extension rules.

## 🎉 Deep dive COMPLETE — all 11 sessions, 230 technical pages of EC 14.2.4 documentation synthesized into `DeepDiveLearnings/ec-docs/`.
