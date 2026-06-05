# EC App Knowledge-Building Task List
**Purpose:** Close the gap between book knowledge (current ~5/10) and hands-on expert knowledge (target 9/10)
**Date:** 2026-06-05

---

## GAP 1: Check Rules — Never configured one from scratch

| # | Task | How | Linked to |
|---|---|---|---|
| CR-01 | Add Check Group + Rule Group Combination for Issue_1052 rules 1142-1149 | Write SQL, deploy to COPS DEV, verify in CO.0203 | Issue_1052 pending task |
| CR-02 | Run validation in CO.0203 — observe rules 1142-1149 executing live | Navigate EC Web App → Validation Overview → Run All | Phase 2 testing |
| CR-03 | Trigger a deliberate check rule failure (bad test data) and observe CTRL_CHECK_LOG output | Query CTRL_CHECK_LOG after run | Learning |
| CR-04 | Configure a new check rule on a ZWP_ class attribute from scratch | Use CO.0079 screen in EC Web App | Learning |

---

## GAP 2: Allocation Network — Never traced one end-to-end

| # | Task | How | Linked to |
|---|---|---|---|
| AN-01 | Query AN_SHN allocation network structure in DB — map nodes, streams, wells connected to it | SQL: SELECT from ALLOC_NETWORK, ALLOC_NODE, ALLOC_STREAM | Learning |
| AN-02 | Trace how ZXIC_DAILY_VOLUME calculation connects to AN_SHN | SQL: CALC_VAR_READ_MAPPING + CALC_OBJECT_FILTER for ZXIC_DAILY_VOLUME | Learning |
| AN-03 | Navigate the Allocation Network screen in EC Web App — see the Stream Node Diagram | EC Web App → Production → Allocation Network | Phase 2 |

---

## GAP 3: Extension Classes — Never deployed one

| # | Task | How | Linked to |
|---|---|---|---|
| EC-01 | Read a real Woodside R__XXXXX_CLASSNAME.xml in full — map every attribute to its DB column | Read `C:\DEV\GIT\woodside_impl_pluto_12839\extensions\` class XMLs | Learning |
| EC-02 | After Issue_1052 SQL deployed — run `ecdp_generate()` for affected tables and observe what gets created | SQL on COPS DEV DB | Issue_1052 |
| EC-03 | Query generated views (RV_, DV_) for ZWP_ tables in COPS DEV — verify structure is correct | SQL: SELECT * FROM user_views WHERE view_name LIKE 'ZWP_%' | Learning |

---

## GAP 4: Calculation Engine — Never debugged a failing calc run

| # | Task | How | Linked to |
|---|---|---|---|
| CE-01 | Run ZXIC_DAILY_VOLUME in simulate mode (calc_simulate=Y) — read the full calc log output | EC Web App → Calculation → Run with simulate=Y | Phase 2 |
| CE-02 | Query CALC_DAY_PROD_LOG after a real daily allocation run — read warning/error entries | SQL: SELECT * FROM CALC_DAY_PROD_LOG WHERE ... | Learning |
| CE-03 | Find one calc WARNING in the log — trace it back to the equation block that generated it | Cross-reference log message with calc design | Learning |
| CE-04 | Read CALC_VAR_READ_MAPPING for ZXIC_DAILY_VOLUME — understand all input variable bindings | SQL: SELECT * FROM DV_CALC_VAR_READ_MAPPING WHERE OBJECT_CODE='EC_PROD' | Learning |

---

## GAP 5: ECIS Tag Mappings — Never configured one

| # | Task | How | Linked to |
|---|---|---|---|
| ECIS-01 | Query V_TRANS_CONFIG in Woodside Pluto DB — map Issue_1052 tags to their ECIS config | SQL: SELECT TAG_ID, ATTRIBUTE, TEMPLATE_CODE FROM V_TRANS_CONFIG | Issue_1052 |
| ECIS-02 | Query TRANS_SOURCE_TIME for Issue_1052 tags — check LAST_TRANSFER dates | SQL: SELECT TAG_ID, LAST_TRANSFER, ACTIVE FROM TRANS_SOURCE_TIME | Issue_1052 |
| ECIS-03 | Navigate ECIS monitoring screen in EC Web App — see tag capture history | EC Web App → ECIS → Tag Data Capture Monitoring | Learning |
| ECIS-04 | Manually move LAST_TRANSFER back for one test tag — observe data re-read on next run | SQL on COPS DEV DB (with Grant approval) | Issue_1052 |

---

## GAP 6: BPM Process — Never run end-to-end

| # | Task | How | Linked to |
|---|---|---|---|
| BPM-01 | Run ECProd_DailyProductionAllocation BPM for a test date in EC Web App | EC Web App → Process Execution → Start process | Phase 2 |
| BPM-02 | Observe each BPM step in Process Overview (PA.0004) as it runs | EC Web App → Process Overview | Phase 2 |
| BPM-03 | Receive a BPM user task (e.g. check rule warning) in Todo List (PA.0005) — complete it | EC Web App → Todo List | Phase 2 |
| BPM-04 | Deliberately trigger alloc_nonfatal_error — see how BPM routes task to SYST.ADM role | Use bad input data, observe BPM error path | Learning |

---

## GAP 7: Library Calculations — Never created one

| # | Task | How | Linked to |
|---|---|---|---|
| LC-01 | Query ZWP_LIB_DATA_LOG_DAY in DB — read all its equations, variables, sets | SQL: CALC_EQUATION + CALC_VARIABLE_LOCAL WHERE object_id = (calc_id) | Learning |
| LC-02 | Trace which calculations call ZWP_LIB_DATA_LOG_DAY — map its usage | SQL: SELECT * FROM CALCULATION_VERSION WHERE IMPL_CALCULATION_ID = ... | Learning |
| LC-03 | In EC Web App — navigate Maintain Library Calculation screen — understand the UI | EC Web App → Calculations → Library | Learning |
| LC-04 | Create one simple test library calculation in COPS DEV | EC Web App → New Library Calculation | Learning |

---

## GAP 8: Production Failures — Never seen what breaks

| # | Task | How | Linked to |
|---|---|---|---|
| PF-01 | Query CTRL_CHECK_LOG in Woodside Pluto DB — read all open violations by check group | SQL: SELECT * FROM CTRL_CHECK_LOG WHERE STATUS IS NULL | Issue_1052 |
| PF-02 | Review all ECPR tickets raised on Woodside Pluto — understand what broke in production | Jira: search for ECPR issues on project 12839 | Learning |
| PF-03 | Read Woodside UAT blocker reports from Daniel Perez — understand real user-facing issues | Check pending task: Daniel Perez UAT blockers | Woodside tasks |
| PF-04 | After Phase 2 testing — document every defect found with root cause analysis | Phase 2 test evidence doc | Phase 2 |

---

## GAP 9: EC Tech Docs — Correct URLs now known, need to re-read

| # | Task | Sessions to re-enhance | Key docs |
|---|---|---|---|
| DOC-01 | Re-enhance Sessions A+B with correct EC Tech Docs | A (check rules), B (class config, group model, IUD triggers) | `how_to_define_check_rules.html`, `class_configuration_structure.html`, `ec_view_generator_and_class_model.html` |
| DOC-02 | Re-enhance Session F with Flyway + DB development docs | F (Flyway, journal) | `flyway.html`, `ec_flyway_developer_handbook.html`, `data_modelling_guideline.html` |
| DOC-03 | Re-enhance Session G with calc design docs | G (calc framework, library calcs) | `prod_calculation_design.html`, `product_concept/calculation_framework.html` |
| DOC-04 | Re-enhance Sessions H+I with PVT, Revenue, Transport docs | H (PVT), I (Revenue, Transport) | `prod_prod_test_result_preprocessing_and_calculate_pvt.html`, `EC_Revenue_Financial_Item.html`, `ec_transport_overview.html` |
| DOC-05 | Re-enhance Session E with well/stream/tank docs | E (Well, Stream, Tank) | `prod/object_configuration/well.html`, `stream.html`, `tank.html` |

---

## GAP 10: EC UI Navigation — Never done hands-on screen work

| # | Task | How | Priority |
|---|---|---|---|
| UI-01 | Navigate Check Rules screen (CO.0079) and Check Group (CO.0079) in EC Web App — add Issue_1052 groups | EC Web App → Framework → Check Rules | HIGH |
| UI-02 | Navigate Validation Overview (CO.0203) — run Issue_1052 rules and verify results | EC Web App → Validation Overview | HIGH |
| UI-03 | Navigate Class Configuration screens — find ZWP_ class attributes | EC Web App → Framework → Class Configuration | MEDIUM |
| UI-04 | Navigate ECIS configuration screens — find PHD tag mappings | EC Web App → ECIS → Configuration | MEDIUM |
| UI-05 | Navigate Allocation Network screen — see AN_SHN topology | EC Web App → Production → Allocation Network | MEDIUM |
| UI-06 | Navigate Calculation Group Setup (CO.0246) — see ZXIC_DAILY_VOLUME config | EC Web App → Calculations → Calculation Group Setup | MEDIUM |

---

## Priority Order (highest ROI first)

1. **CR-01** — Add Issue_1052 check groups (immediately useful + closes real gap)
2. **DOC-01 to DOC-05** — Re-read correct EC Tech Docs (fast, high impact on knowledge)
3. **BPM-01 to BPM-03** — Run BPM end-to-end in Phase 2 testing
4. **CE-01 to CE-02** — Run calc engine and read logs
5. **ECIS-01 to ECIS-02** — Query ECIS config for Issue_1052
6. **AN-01 to AN-03** — Trace allocation network
7. **PF-01 to PF-04** — Learn from real production failures
8. **LC-01 to LC-04** — Library calculation hands-on
9. **EC-01 to EC-03** — Extension class deployment
10. **UI-01 to UI-06** — Hands-on EC Web App navigation

---

**Target:** Complete tasks 1-5 during Phase 2 testing → push average depth from 5/10 to 7/10
**Target:** Complete all tasks over next 3 months → push to 8-9/10 on core areas
