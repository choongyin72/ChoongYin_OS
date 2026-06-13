# EFK Phase A1 — EC Test Automation Framework (TAF) — 2026-06-13

**Outcome: low yield — the "TAF Competency trainings" pages are EMPTY STUBS** (all 10 modules
return the identical placeholder "Session-I: Arquillian / Core / DBRestHelper-TestAgent / POM /
Utilities / Others"; authored 2020, never filled). Checked #1 Core Architecture, #8 Best
Practices, #4 Jenkins Pipeline — all the same placeholder.

## The one useful signal (the module TITLES + the placeholder stack)
EC's OFFICIAL Test Automation Framework is a **Java/Arquillian backend-integration** stack:
- **Arquillian** (in-container Java integration tests) + **POM** (Maven) + **DBRestHelper /
  TestAgent** (DB + REST assertions) + **Docker** + **Jenkins** pipeline + **Cucumber** (BDD).
- Training module list: 1 Core Architecture · 2 Role of Docker · 3 Chart Utilities · 4 Jenkins
  Pipeline · 5 Package Automation setup · 6 Stream Node Diagram · 7 Cucumber · 8 Best Practices ·
  9 Regression Testing · 10 Online help/page load.

## Implication for OUR framework (ec-automation)
EC's TAF is **backend/integration** (Arquillian in-container + DB/REST), whereas mine is
**UI/black-box** (Playwright + Robot Framework driving the real screens + DB ground-truth).
Complementary, not competing — ours tests the deployed app as a user; theirs tests Java units
in-container. Two takeaways worth adopting if/when relevant:
- **Cucumber/BDD** style = the business-readable layer; my RF suites already read declaratively
  (TC01..04, domain-keyword names) — a fair equivalent. Could map TEST-CASE-BACKLOG items to
  Gherkin-ish scenarios for business review.
- **Jenkins pipeline** = matches my roadmap's deferred CI item (run Robocop + suite, Pabot
  parallel). When Jenkins lands, mirror this structure.
No content to mine further here. Detail (if ever filled) would live on these page IDs.

## Decision
Mark TAF DONE (stub). Move to Phase A2 (Calculation Framework — substantive, underpins
Issue_1052 validations + As-Built allocation/NGER calcs).
