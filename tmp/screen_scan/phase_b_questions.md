# Phase B — deep-dive findings & clarification questions (before real work)

Screens: Area, Sub Area, Production Sub Unit (groupmodel OV) + Object List Setup (parent-child).
Recon: read-only; nothing saved. Evidence: phase_b_recon.json, shots/phaseb_*.png.

---

## Findings per screen

### 1. Area  (`manage_object_groupmodel_nav/GROUPMODEL/AREA`)
- Navigator: Date + **Production Unit** (mandatory, yellow) + GO — grid loads only after a PU is picked.
- Insert form: Area Code + Area Name mandatory; optional dropdowns incl. **Op Production Unit**,
  Cp Production Unit, Business Unit, System of Measurement, Conversion Context, Time Zone.
- PU dropdown options (21): AS1/AS2/AS3 EC Exploration Norway, AS4_Diluent, AS5_Injection,
  **EC-UT-GENERIC Production Unit**, ECP Norway, FRMW PU, MID, P1, P3, Production Unit 1/2, RBS, SS2…
- Working assumption (verify live): the new Area must set Op Production Unit = the navigator PU,
  or it won't appear in the PU-filtered grid for row-verify.

### 2. Sub Area  (`…/GROUPMODEL/SUB_AREA`)
- Navigator: Date + **Production Unit** + **Area** (cascading: Area list fills after PU picked) + GO.
- Cascade verified: EC-UT-GENERIC PU → "EC-UT-GENERIC Area"; Production Unit 1 → "Area 1"; AS1 → "AS1_Area".
- Insert form: Sub Area Code/Name mandatory; optional dd: Op Production Unit, Op Area, SoM.
- `OV_SUB_AREA` currently 0 rows (clean slate, like State/County were).

### 3. Production Sub Unit  (`…/GROUPMODEL/PROD_SUB_UNIT`)
- NO navigator dropdowns visible; grid `manageObject:form:T_data` present, currently empty
  (`OV_PROD_SUB_UNIT` = 0 rows).
- Insert form fully standard: PSU Code/Name mandatory, Master System, Start/End Date, SoM dd.
- Looks like the plain phase-A template should work as-is.

### 4. Object List Setup  (`com.ec.revn.cd/manage_object_list`)
- Different pattern: **parent-child setup screen**. Navigator: Daytime + **List Class** + **Object List**
  (both mandatory) + GO → shows the chosen list's ITEMS. Toolbar Insert = "Object List Item",
  Delete = "Object List Item".
- List Class options = all EC classes; Object List options = existing lists (e.g. ALL_DIM, GB_ALL…).
- DB note: `OV_OBJECT_LIST_SETUP` does not exist — the right verify view/table to be located in
  implementation (grid recon will reveal the base table).

---

## Questions (recommendation first — "approve all" is enough)

**Q1 (Area):** Which Production Unit as the test's navigator context (and as Op Production Unit
on the inserted AUTOTEST area)? → **Recommend: EC-UT-GENERIC Production Unit** (purpose-built generic).

**Q2 (Sub Area):** Which PU + Area pair? → **Recommend: EC-UT-GENERIC Production Unit + EC-UT-GENERIC Area**
(pair verified to exist).

**Q3 (Production Sub Unit):** No special inputs found — OK to attempt with the standard phase-A
template directly? → **Recommend: yes, try-first.**

**Q4 (Object List Setup):** Approve the self-contained flow?
1. Suite creates its own AUTOTEST Object List (Class = BANK — your earlier approval) reusing the
   Object List page object;
2. selects it in Setup (List Class=BANK, Object List=AUTOTEST list), GO;
3. Insert "Object List Item" referencing an EXISTING bank object (read-only reference, list-membership
   row only);
4. DB-verify item, delete item, delete the AUTOTEST list (leaves zero trace).
Fallback if no bank exists in sandbox: suite creates + deletes its own AUTOTEST bank too.
→ **Recommend: yes.**
