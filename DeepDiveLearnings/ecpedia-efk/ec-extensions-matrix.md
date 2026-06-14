# EFK Phase-3 — EC Extensions Compatibility Matrix (the extension catalog + Pluto-relevant versions)
Read 2026-06-14 from EC Knowledge (EFK): **EC Extensions Compatibility Matrix** `1851205` (updated
daily; the live source for EC↔extension version compatibility, owned by CPD for ECaaS deployment).
The other two Phase-3 reference pages were low-yield: **EC Talks** `1837692` = purpose/team stub (talk
recordings live in children/SharePoint, no text); **EC Releases and live assets** `1853526` = a
template with only "test row" placeholder data. **EC Product Trainings** `1853607` = a training index
(skip). The Matrix is the keeper.

## ⭐ Resolves part of the parked Chemistry question
The matrix footnotes + pipeline notes state **XCH (Chemistry) and XLM are DISCONTINUED as extensions —
"Not available as extension / moved into EC as module/feature"**, specifically **"Module from EC
13.1.2"**. So on Pluto's **EC 14.2.x**, **Chemistry is a built-in EC core module** (licensing-
dependent), NOT the old XCH extension. That sharpens the parked "jump back to Chemistry later" item
([[link-out-extensions.md]]): the question for the user becomes *"is the Chemistry module licensed/
enabled for Woodside?"* — not *"is the XCH extension installed?"*. (Emissions XEM is still a separate
extension — see below.)

## EC extension catalog (codes decoded from the matrix)
| Code | Extension (inferred) | Notes for us |
|---|---|---|
| **XEM** | Environment Management (**Emissions**) | Still a live extension; rides EC calc+allocation framework → N2-family. v4.x pairs with EC 14.2.x. |
| **XCH** | Chemistry | **DISCONTINUED as extension → EC core module from 13.1.2.** |
| **XLM** | (Lab Mgmt?) | Discontinued (with XCH). |
| **XMS** | Mobile / Measurement Solution | Mobile task-list pairing (with ECME). |
| **ECME** | EC Mobile | High business-relevance with XMS/XTO/FDC. |
| **XTO** | Terminal Operations | v2.0.0 on EC 14.x. |
| **XGH** | (GHG / Greenhouse?) | v2.0.3 on EC 14.2.x. |
| **TAP / XTAP** | (Test Automation Platform?) | v1.3.0 on EC 14.2.x. |
| **FDC** | (Field Data Capture?) | v1.0.0. |
| **ECSM** | EC Smart | Discontinued; couldn't combine with other extensions (except EC Mobile). |
| **ECCT** | (EC ?) | v2.2.1 on EC 14.2.x. |
| **CME** | (?) | v3.3.1 on EC 14.2.x. |
| **XRPCA / XRRCA** | Reporting Package / Royalty — **Canada** | Regional reporting packages. |
| **XRPNO / XRRNO** | Reporting / Royalty — **Norway** | Pairs High with each other. |
| **XRPUS** | Reporting — **US** | |
| **XRREU** | Reporting — **EU** | |
| **XUM** | (Upgrade/Migration?) | High relevance with ECME/ECSM. |

(Decodes are inferred from context + my As-Built knowledge; confirm exact long-names against an
extension details child page if it ever matters for a real task.)

## Pluto-relevant slice (EC 14.2.x rows)
For Pluto's **EC 14.2.x**, the matrix shows verified-compatible extension versions around:
**ECME-1.5.6, TAP-1.3.0, XTO-2.0.0, XGH-2.0.3, ECCT-2.2.1, CME-3.3.1** (14.2.2/14.2.5/14.2.6), and
**XEM-4.1.2** at 14.2.3 (the emission extension version for Pluto's branch). Reporting packages
(XRP*/XRR*) are mostly "None verified" on 14.2.x in this table.
- Status values used: **N/A** (no dependency), **NC/Not Compatible** (tested, fails), **NV/Not
  Verified** (untested), **DC/Discontinued**.

## Why this matters / how to use it
- **Before planning coverage of any add-on screen** (emissions, chemistry, terminal ops, mobile),
  check this matrix for the extension version that's verified against Pluto's EC version, and whether
  it's even live — answers the recurring "is it installed/licensed for Woodside?" question.
- **Cross-extension overlap:** extensions that extend the *same EC-Core-owned objects* must be
  compatibility-tested; the page tracks this (e.g. XCA overlaps 49 ECSM objects). Relevant if a
  Woodside config change touches a Core object an extension also extends.
- **CPD uses this to structure ECaaS deployment scripts** — so it's the authority on what ships
  together, complementing the Database Sanity config-guardrails ([[framework-db-sanity.md]]).

## Phase-3 status
Reference phase essentially done: Vocabulary (→ GLOSSARY), Extensions Matrix (this note). EC Talks /
Releases / Product Trainings = thin/template/index, noted + skipped. Remaining series = **Phase-4
on-demand ops** (schedule-job / stuck-service — pull when the scheduler misbehaves) and **Phase-5
skip**. The EFK series is now effectively complete for value; deeper drills are on-demand.
