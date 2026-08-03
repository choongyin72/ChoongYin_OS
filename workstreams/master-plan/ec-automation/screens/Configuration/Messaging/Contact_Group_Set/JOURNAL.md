# JOURNAL - Contact Group Set (CO.0225) OV-GM IUD

## 2026-08-03
- **Branch:** `feature/build-contact-group-set-iud`. New screen, never attempted before - discovered
  via a database-first coverage audit (`SELECT class_name FROM CLASS_CNFG WHERE CLASS_TYPE='OBJECT'`,
  295 total OBJECT-type classes, cross-referenced against every tracking doc to find genuinely
  unautomated classes with a real live screen).
- **Real screen title differs from the class's own LABEL property** - `class_property_cnfg` stores
  the LABEL as "Contact Group Set", but the live treeview menu item is titled "Maintain Contact Group
  Set" (Configuration > Messaging). A search for the exact LABEL text alone does not find a clickable
  screen; confirmed the real title via a live menu search first, then verified via `scan_ec_screen.py`
  using that real title before committing to build.
- **Simple, low-risk build - matches Message Group's exact pattern (same folder, same family):**
  navigator = Functional Area (single mandatory dropdown, first-available resolved to
  "Administration") + GO, OV-GM, grid `manageObject:form:T_data`. Insert form: Contact Group Set Code
  (mandatory) + Name (mandatory) + Start Date + Functional Area (parent_dd, bound to the nav-captured
  value so the new row lists under the correct scope - the exact mechanism Message Group's own park
  history proved necessary).
- Built via `gen_ovgm.py` (`parent_dd="Functional Area"`, `nav_levels=1`, `start_date="2020-01-01"` per
  the owner's simplified standing default for reference-dropdown screens). **First live run: ALL PASS**
  (nav_pu/insert_ui/insert_db/update_ui/update_db/delete_ui/delete_db/self_clean), no fixes needed -
  confirms the gen_ovgm.py template + Message Group precedent transferred cleanly to a sibling screen
  in the same folder/family.
- Confirmed live + DB-verified via `verify_screen.py` (OVERALL PASS: robocop 0, hygiene 0, dryrun 4/4,
  live RF 4/4, Playwright driver 8/8). Full I-U-D, 0 residual.

## Lessons
- **A class's `class_property_cnfg` LABEL property does not always match the live menu's displayed
  screen title** - confirmed again here (LABEL="Contact Group Set", real title="Maintain Contact
  Group Set"). When doing a coverage audit from the DB outward (class -> label -> hoped-for screen),
  always confirm the real clickable title via a live menu search before running `resolve_ec_screen.py`
  or `scan_ec_screen.py` with an assumed title - several other candidates from the same audit batch
  (Split Key, Project, Revenue Contract, Sale Contract, Scenario) failed an exact-title match for
  exactly this reason and need the same live-search-first treatment before being ruled in or out.
