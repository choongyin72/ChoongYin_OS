# JOURNAL - Lifting Account (CO.2004) OV-GM 4-level-nav IUD

## 2026-07-30
- **Branch:** `feature/lifting-account-iud-v2`. Previously PARKED: original scan found a 4th mandatory
  nav dropdown that timed out empty under the first-available AS1 path (grid never loaded).
- **UNPARKED by owner walk-through:** owner provided the working scope with a screenshot -
  **P1 Production Unit -> P1 Area -> P1 Facility 1 -> Storage P1_CRUDE_STOR** (the Storage dd sits on
  a SECOND navigator row below Date; flagged by owner as required).
- **Recon** (read-only id dump): cascade at `nav:form:G:0:R:1:C:1..3`, Storage at
  `nav:form:G:0:R:3:C:0:dd_input` - the second-row position is why the generic single-row
  `apply_ovgm_navigator` never reached it.
- **DB pre-checks (real facts):** BF CO.2004 (DefaultScreenTreeview); OV_LIFTING_ACCOUNT live (34 rows);
  P1_CRUDE_STOR effective 2010-01-01; 146 companies effective at 2020-01-01 -> Start Date 2020-01-01.
- **Built HAND-WRITTEN (no generator):** generator supports neither a second nav row nor specific nav
  values. Thin driver with screen-local `apply_lifting_account_navigator` (specific values + GO);
  T3 with screen-local `Apply Lifting Account Navigator` on T1 `Select EC Dropdown Option` +
  `Apply Navigator`. Insert: Company Name first-available + **Storage Name = nav Storage**
  (parent-matching rule - row never lists otherwise).
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4 pass,
  Playwright 8/8. DB residual 0.
- **#265 lesson applied:** registry/scorecard rows column-diffed against the Channel sibling row;
  nav column corrected to state SPECIFIC P1 values + 2nd-row Storage (not the template cascade text).

## Lessons
- A "deep cascade with an empty level" park can be a DATA-SCOPE gap, not a structural blocker: the
  level was empty only under the first-available path. One owner-provided working scope unblocked it.
- Second-row navigator fields (G:0:R:3) are invisible to the single-row engine helper - dump ALL
  `nav:form` input ids when a scan reports more mandatory dds than the standard 3.
