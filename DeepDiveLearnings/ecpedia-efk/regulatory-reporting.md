# EFK Phase-1 — EC Regulatory Reporting (the *why* behind EC's controls) + Phase-1 close
Read 2026-06-14 from EC Knowledge (EFK): **EC Regulatory Reporting** `1845940` (2014). Plus the
three remaining Phase-1 pages, which are **link-outs** (noted, not deep-read). This closes Phase-1.

## EC Regulatory Reporting — SOX/SEC governance (grounds EC's validation + audit machinery)
A governance/compliance frame, not a screen module. The takeaway for *why EC has the validation,
freeze, and audit-trail features I've been automating*:

- **SOX (Sarbanes-Oxley Act 2002)** + SEC: enacted after the early-2000s corporate scandals; mandates
  US registrants **evaluate and report on the effectiveness of internal financial controls**.
  **Section 404** is the big one — documenting critical operational controls, assessing their
  effectiveness, and submitting that assessment to **independent auditor** scrutiny.
- Oil & gas faces this acutely: multi-regulatory / multi-tax regimes, long-term high-risk projects,
  complex JV/stakeholder relationships → heavy pressure to comply with international financial
  reporting standards. SOX assumes management ensures all financial reporting (incl. **future cash-flow
  inflows from production and sale of oil & gas**) is reliable enough for investors to depend on.
- **Three upstream business needs** the hydrocarbon-accounting data flow must serve:
  1. Management & elimination of **losses (downtime)**.
  2. **Reliability of production data** for reservoir analysis.
  3. **Government & internal-control requirements**.
- **Pre-SOX → Post-SOX org change:** reporting structure moves **out of the E&P line into the
  financial organisation (CFO)**; the board + financial committee set corporate-governance standards;
  an **independent board audit committee** has authority over and direct responsibility for the
  internal-audit process (an *independent internal reserves review process*). SOX prescribes no single
  procedure, so implementations differ.
- **EC's pitch:** component-based assembly + built-in SOX compliance → full **traceability,
  auditability, SOX404 compliance at all levels** (the same phrase appears in EC Revenue).

### Why this matters for the test work (the series' point)
This is the business justification for the control features I automate/validate:
- The **validation framework** (CTRL_CHECK_* — Validation Overview, Issue_1052 rules, the frozen-PHD
  check) IS the "documented, effective internal control over production/financial data" SOX-404 wants.
  A validation rule that fires (or fails to) is a *control test* — so a meaningful test asserts the
  control behaves per its documented intent, with an auditable log (CTRL_CHECK_LOG = the evidence).
  See [[reference_ec_frozen_check_business_flow]] and [[reference_ec_check_group_rule_linkage]].
- "Reliability of production data" + "elimination of downtime losses" = exactly the N1 daily-status
  grids (ON_STREAM_HRS, measured rates) and N2 allocation conservation I've been proving at the DB.
  The conservation/no-neg oracle is, in SOX terms, a control over data integrity.
- "Transferring quantities into monetary value" (EC Revenue) under audit = why revenue tests need
  Σ(qty×price) + JV/royalty split oracles, not CRUD ([[../ecpedia-efk/sales-revenue.md]]).

## Phase-1 link-out pages (noted, not deep-read — external/other spaces)
- **EC Chemistry Management** `1853912` → link to space **ECCM**. (Chemical/corrosion mgmt extension.)
- **EC Environment Management** `1851143` → link to **ecpedia.eu.tieto.com / XEM** (the env/emissions
  extension). I already hold the GHG/emissions frame in `environment-ghg.md`; the Tieto-internal
  ecpedia URL may be dead/internal — don't chase unless a real emissions task needs it.
- **EC IAM (Integrated Asset Modelling)** `1850998` → link to **ECIAMD** space (reservoir-to-surface
  asset modelling; upstream of EC, feeds production planning). Reference only.

## Phase-1 status: ✅ COMPLETE
All 8 Phase-1 domain pages now read: EC Production (diagram-only parent), Hydrocarbon Accounting,
EC Sales, EC Revenue, EC Regulatory Reporting (this note), + the 3 link-outs (Chemistry/Environment/
IAM). The reservoir→revenue value chain is mapped end-to-end with the SOX/governance "why" layered on.
**Next:** Phase-2 (calc/framework depth) — start with **VCF Calculation in EC** `1853432` (2023,
recent + concrete: tank volume correction, API Ch.12.1 5-step GSV) since it's a calculation oracle
in the same family as the N2 allocation work.
