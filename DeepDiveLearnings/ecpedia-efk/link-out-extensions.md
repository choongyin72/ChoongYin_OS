# EFK Phase-1 link-outs followed — Chemistry (ECCM), Emissions (XEM), IAM (ECIAMD)
Followed 2026-06-14 (user-directed) the three EFK Phase-1 link-out pages to their real spaces on
energycomponents.atlassian.net (the old `ecpedia.eu.tieto.com` URLs were migrated here). These are
**EC product add-on / extension** spaces (not Woodside/Pluto client config), so they're reference —
but one tie-in is directly actionable for my calc/allocation test track.

## EC Chemical Management — space **ECCM** (homepage `2326530`, "Chemistry and Environmental technical hub")
A hub for two add-ons (SharePoint: `qbsol.sharepoint.com/sites/oilfieldchemistry`):
- **EC Chemical & Laboratory Management ("EC Chemistry")** — features for operators to **monitor +
  report chemical use**: volumes, dosages, performance. (Shape = data capture + reporting; akin to the
  N1 daily-status grids — measured values per object/day.)
- **EC Emission Management ("EC Environmental")** — an extension that **transforms EC Production into
  an emission calculation + data-management solution**: adds configuration, data storage, and default
  library calculations that can be expanded. (This is the XEM extension below.)
- Owners: John-Arne Stokkan (Sr Product Mgr), Yannick Tollenaere (PO), Atul Gaigol (Tech PO).

## EC Environment Management Extension — space **XEM** (homepage `5734405`, "XEM: Emission Tracking")
- **EC Environmental Management 1.0.0** = an extension for EC / EC Production for **emission data
  management with standard calculation libraries for hydrocarbon emission accounting**.
- ⭐ **KEY ARCHITECTURAL TIE:** it *"integrates seamlessly with EC Production using the **calculation
  and allocation framework** in EC to easily add calculation flows with **production allocation** and
  production data updates."* → **Emissions are computed by the SAME calc/allocation engine I just
  automated for N2** (HA.0002 RUN CALCULATIONS). A GHG result screen is a feature (sprint item
  ECAP-23083 "Create GHG result screen"); v1 = emission config + emission data storage + industry-
  standard emission calc library. Roadmap track = FRMW-3.
- Space contents are mostly **Scrum/Kanban dev-admin** (sprints, groomings, kanban commitments); the
  one technical page "XEM Calculations" (`5734852`) is an **empty placeholder** — the actual emission-
  calc detail lives in external SharePoint (`ECchemistrydevteam/Emission tracking`), not chased.

## EC Integrated Asset Modelling Documentation — space **ECIAMD** (homepage `4489220`)
- The **EC IAM product manual** (© 2020 TietoEVRY; `eciam@tietoevry.com`, `tietoevry.com/EC-IAM`).
  Integrated Asset Modelling = reservoir-to-surface asset modelling (upstream of EC; feeds production
  planning/forecasting). Overview is just a manual cover; depth is in the manual's child pages.
  **Reference only** — revisit only if an IAM-integration question arises.

## Actionable takeaway for the test track
**Emissions/GHG is an N2-family target.** Because XEM rides EC's calculation + allocation framework,
an emission calc RUN should surface the same way as HA.0002 (a calc job → result rows + a GHG result
screen), so the **N2 RUN-verify pattern + conservation oracle generalize to emissions**: run the
emission calc, assert the run's Exit Status, then DB-assert no-negative / mass-balance invariants on
the GHG result table. Filed as a candidate when an emissions screen is in Pluto scope (would need the
XEM extension installed in the sandbox + the GHG result table name — neither confirmed here). Chemistry
(volumes/dosages) is an **N1-family** data-entry candidate. Both are add-ons → confirm they're licensed
/installed for Woodside before planning real coverage (open question for the user).

## Phase-1 link-outs: ✅ followed + closed. No deeper crawl (product-dev admin + external SharePoint).
