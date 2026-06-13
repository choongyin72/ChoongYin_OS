# EFK Phase A3 — ECIS framework + PI DAS setup — 2026-06-13

Read: "How to Set up PI DAS and ECIS" (1851186, updated 2025) — substantive. (The EC Framework
› ECIS landing page itself is a thin wrapper; the how-to carries the detail.)

## 🔑 ECIS has PLUGGABLE source adapters (the architecture insight)
ECIS isn't just the Excel importer I learned — it's a framework with swappable **source
adapters**, selected per interface:
- **PI JDBC adapter** `com.ec.frmw.is.engine.adapter.pi.jdbc.PiAdapter` — pulls from an
  **OSIsoft PI** historian via **PI DAS** (Data Access Server) over PI JDBC/OLEDB.
- **OPC UA adapter** — pulls tag data over OPC UA (the Pluto I_IN_PHD_DAILY path from Honeywell
  PHD; As-Built 05).
- **Advanced Excel / file** job actions — Excel/CSV/XML file import (AUDREY + my CLAUDE_WELL_TEST).
- **REST** — `POST /services/ecis/interfaces/<code>/files` (As-Built 05).
Two config modes: **ecisconfig.xml** (file, `<config><sourceadapter><class>+<parameters>`) OR
**DB config** (`ecis_db_config=Y` business-action param → Mapping Configuration screen — what
AUDREY/my build use). So ECIS = one engine, many adapters, file-OR-db configured.

## PI DAS setup essentials (OSIsoft PI path — NOT Pluto's, but completes the picture)
- Prereqs: WildFly app server with open ports to the PI server; install **PI OLEDB Enterprise +
  PI DAS + PI JDBC** (OSIsoft); EC ear must bundle the matching `PIJDBCDriver.jar`; redeploy +
  restart after.
- ecisconfig.xml `<config name="ECIS_SIGMA_PI">` → PiAdapter, `dbdriver=com.osisoft.jdbc.Driver`,
  `connecturl=jdbc:pisql://<host>/Data Source=SIGMAFINE_PI;Integrated Security=SSPI;`, user/pwd
  (pwd can be `encrypted="true"`), logfile, timezone.
- Needs a **server trust** between PI server and PI DAS server; else explicit PI login in the
  connecturl. `PI_RDSA_LIB64` env var must point to RDSAWrapper64.dll.
- Troubleshooting table: 403 Forbidden (OS creds), "Unable to open session" (PI creds),
  -10431 (auth method disabled → use network trust), connection refused (PI DAS service down),
  "Native Library Version wrong" (PIJDBCDriver.jar version mismatch in the ear).

## Vendor note (clears a confusion)
Two historian families seen: **OSIsoft PI** (this how-to, Sigmafine PI, PI DAS/JDBC) vs
**Honeywell PHD** (Pluto, OPC UA via the ECIS Agent). Both are "tag data" historians; EC has a
distinct ECIS adapter for each. Pluto = PHD/OPC UA. So this PI DAS how-to is reference for
OTHER clients, not Pluto's path — but confirms the adapter-pluggability that frames the
ECIS-backup design choices.

## For the ECIS real task
Reinforces As-Built 05: the PHD feed is a historian/tag adapter (automated); a manual Excel
backup uses the Advanced-Excel adapter (my proven build). The adapter architecture means the
backup is genuinely a separate interface, not a modification of the PHD adapter.

## Decision
A3 DONE. Phase A near-complete; A4 = Environment/GHG (XEM + NGER calc training) next block.
Good session checkpoint here.
