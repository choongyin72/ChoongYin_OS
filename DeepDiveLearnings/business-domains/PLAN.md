# EC Business-Domain Deep Dive — plan (user-assigned 2026-06-12)

Choong-Yin: "do self deep dive into ec in other areas... business domain (production,
transport, sales, revenue & etc)". Goal feeds [[project_ec_coverage_goal]]: domain
understanding → better test design for business test-case suites (the final phase).

## Method per domain (production / transport / sales / revenue / chemistry / messaging)
1. **Menu walk** (local EC, read-only): expand the EC <Domain> treeview branch, inventory
   screens by section (same scan style as the Assets scan).
2. **Docs**: ec-docs KB (DeepDiveLearnings/ec-docs/) + EC Tech Docs 14.2.5 domain chapters
   (use reference_ec_tech_doc_url_map) + ECpedia search per domain.
3. **DB**: domain table families (PWEL_/PFCTY_ production; CARGO_/LIFT_ transport;
   CNTR_/SALE_ sales; FIN_/DOC_ revenue) — row counts on local sandbox = which flows
   have seed data to learn from.
4. **Business flow synthesis**: per domain, write THE core daily flow (e.g. production:
   InitiateDay → daily statuses → allocation → approval) with screens + tables + scheduler
   jobs involved. The May-29 history rows (InitiateDay, DailyProductionAllocation) are live
   evidence on the sandbox.
5. Output: one `<domain>.md` per domain in this folder; update coverage-goal memory.

## Status
- [ ] Production (start here — richest seed data: AS1 wells, PWEL_DAY_STATUS 282 rows/well,
      InitiateDay + DailyProductionAllocation schedules ran 2026-05-29)
- [ ] Transport (Cargo/Lifting — big OTHER bucket in Assets scan)
- [ ] Sales (contracts, nominations — links to Nomination Point work in Dispatching)
- [ ] Revenue (DocProcess schedules, FIN_* — links to Financial Objects)
- [ ] Chemistry (ChemGen* CRON schedules visible)

NOTE: prior session today completed the ECIS learning build (see
DeepDiveLearnings/ecis-deep-dive/AUDREY-EXAMPLE-NOTES.md) and Dispatching slice 1.
Dispatching slice 2 (Pipeline/Meter/Nomination Cycle) is queued after this dive.
