# Pluto Hub As-Built (DDS) series — index (found 2026-06-13 via SharePoint)

Location: qbsol SharePoint `GlobalServices/.../12839 - 2024 - ECaaS - Implementation - TM/`
`02 EC Delivery and Acceptance/02 Product Configuration & Integration (PCI)/As-Built/`
Title block: "Pluto Hub Production Allocation System — Detailed Design Specification".
**The system's official name = Production Allocation System → Pluto's EC = above all a
PRODUCTION ALLOCATION implementation (confirms domain priority #1).**

| Vol | File | Modified | Read? |
|---|---|---|---|
| 01 SystemConfig | WSPLU_EC_AsBuilt01_SystemConfig_v1.0.xlsx (Archived/) | 2026-04-23 | ☐ |
| 02 ScreenConfig | WSPLU_EC_AsBuilt02_ScreenConfig_v1.0.docx | 2026-06-11 | ✅ catalog read → ASBUILT02-SCREENS.md (Pluto screen list by code + SI units) |
| 03 ObjectConfig | WSPLU_EC_AsBuilt03_ObjectConfig_v1.2.xlsx | **2026-06-12** | ☐ |
| 05 Interfaces | WSPLU_EC_AsBuilt05_Interfaces_v1.0.docx | **2026-06-12** | ☐ ← ECIS task! |
| 06 Calculations | WSPLU_EC_AsBuilt06_Calculations_v1.0.docx | 2026-06-11 | ☐ ← allocation design |
| 07 Reports | WSPLU_EC_AsBuilt07_Reports_v1.0.docx (+ANNEX folder with report mappings, e.g. r_blp_daily_prod_alloc_pluto) | 2026-06-10 | ☐ |
| 11 Notification | WSPLU_EC_AsBuilt11_Notification_v1.0.docx | 2026-05-19 | ☐ |
| 14 BusinessProcesses | WSPLU_EC_AsBuilt14_BusinessProcesses_v1.2.docx | 2026-05-18 | 🔵 PARTIAL — §1 + §2.1.1 daily allocation done → ASBUILT14-BUSINESS-PROCESSES.md; §2.1.3-2.4 (monthly/deferment/emissions) pending |

Gaps in numbering (04, 08-10, 12-13) — enumerate the folder next session (folder may hold
more; also an ANNEX subfolder per volume). Several volumes ACTIVELY EDITED this week
(03/05 touched 2026-06-12) → the As-Built is a LIVING document set; check dates when citing.

**Reading order for the curriculum (Pluto lens):**
1. **14 BusinessProcesses** — the business flows EC supports for Pluto (maps to my flow
   syntheses; validates/corrects them + tells which generic flows are IN SCOPE).
2. **06 Calculations** — Pluto allocation network design (production.md deep pass).
3. **05 Interfaces** — directly feeds the real ECIS task (what interfaces exist, incl.
   ZWP_INTERIM_DATA_UPLOAD design rationale + PHD interface).
4. 03 ObjectConfig (xlsx) — master-data scope = which Assets screens matter.
5. 02/07/11 as needed per domain.
Access via mcp sharepoint read_resource on the URIs (search 'WSPLU Energy Components
Detailed Design Specification' folderName='As-Built' re-surfaces them).
