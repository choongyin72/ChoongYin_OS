# Platform Ops — Context (as of 2026-06-02)

## Current version
- Active snapshot: `1.1.0-SNAPSHOT` on `develop`
- Last production release: `PROD_RELEASE_1.0.36`
- Next planned release: Wave 03 bundle (UAT fixes + report changes)

## Change Requests
- **CR-028 (High Priority)** — Variation Order dated 1-June-2026. Woodside has requested Quorum retain current project resources. WIP draft in SharePoint (`06 Change Management/`).
- **CR-029 (Low Priority)** — change request in change management

## CI pipeline
- Tool: Jenkins
- Build: `JAVA_HOME=/home/jenkins/agent/.../jdk17 mvn clean verify`
- Global Maven settings config ID: `40bc3356-a008-48fb-a709-b5f4cc803537`
- No concurrent builds (`disableConcurrentBuilds`)

## Key SharePoint docs (qbsol.sharepoint.com)
- Weekly SteerCo decks: `Project Management (PMO)/...Governance SteerCo Meetings/Woodside/Woodside Pluto/`
  - Latest: Project Delivery Progress 05 June 2026 (updated 2026-05-29)
- Org chart: `01 EC Project Management/03 Communication/EC 12839 - Woodside Pluto - ORG CHART.pptx`
- CR docs: `01 EC Project Management/06 Change Management/`
- TM project folder: `12839 - 2024 - ECaaS - Implementation - TM`

## Sources
- Git: `C:/DEV/GIT/woodside_impl_pluto_12839`
- SharePoint: 1,725 documents in project (qbsol.sharepoint.com/sites/GlobalServices)
- Jenkins: CI via Bitbucket webhooks
