# DOC-02 — General Configuration A (Class Model & View Layer)
**Source:** EC 14.2.4 `frmw/general-config` (pages 1–25 of 50)
**Read:** 2026-06-06 · pages 1–12 in depth; 13–25 by title (how-to/styling)

> 🔑 **This session explains the DB layer my IUD automation was working against** (OV_BANK / OV_EQPM, the date-effective columns, the INSTEAD OF triggers). Big cross-link payoff.

## 1. The Class Model & View Generator (the foundation)
EC separates **business objects from physical storage** via a metadata-driven **View Layer** ("EC Data Services"). Object-class definitions are used to **auto-generate a set of DB views** (the `OV_`/`DV_`/`TV_` views) plus their **INSTEAD OF IUD triggers**.
- This is *why* I read/wrote banks via `OV_BANK` and equipment via `OV_EQPM` — **those are generated object-class views**, and my inserts/updates/deletes fired the generated **INSTEAD OF INSERT/UPDATE/DELETE triggers**.
- Generic capabilities (locking, row-level security, four-eyes approval, journaling) are offered transparently from the DB layer, configurable per class.
- Grouped by **App_Space_Cntx**: `EC_FRMW, EC_PROD, EC_TRAN, EC_SALE, EC_REVN, EC_ECDM, EC_BPM` (product spaces). Generic access layer = **GenAppSpace** (every object has a global id).

## 2. 🔑 Required object-class attributes (explains the OV_ columns I saw)
The hard-enforced rule **`RequiredObjectClassAttributes`** — a **versioned** object class MUST have:
`OBJECT_ID, CODE, OBJECT_START_DATE, OBJECT_END_DATE, DAYTIME, NAME, END_DATE`
(invariant classes: same minus DAYTIME/END_DATE).
- **This is exactly the column set I queried in `OV_BANK`/`OV_EQPM`** (CODE, NAME, OBJECT_START_DATE, OBJECT_END_DATE, REV_NO…).
- It confirms *why* delete = **End Date = Start Date**: object classes are **versioned by `OBJECT_START_DATE`/`OBJECT_END_DATE`**; a zero-length window removes the object from the view. The data model *mandates* these date columns.

## 3. Class types & config rules (hard-enforced on extensions)
Class types: `OBJECT, DATA, TABLE, INTERFACE, REPORT, META`. Migration **fails** if rules break. Key rules:
- DbObjectName = main table; DbObjectAttribute = attribute table (versioned objects need it).
- Object key can only be `OBJECT_ID`; Data classes must have an `OWNER` class + `OBJECT_ID`.
- `TimeScopeCode`: OBJECT = VERSIONED|INVARIANT; DATA/TABLE = NONE|EVENT|DAY|WEEK|MTH|QTR|YR|HR_1|HR_2|SAMPLE (← the data-grid "keyed by day" maps here).
- DbMappingType ∈ ATTRIBUTE|COLUMN|EXTENSION|FUNCTION|INNER_JOIN|LEFT_JOIN|EXT_JOIN.

## 4. Class config structure — domain vs property tables, owner context
- **5 domain-model tables** (classes, attributes, relations, dependencies, trigger actions) + **4 property tables** (overridable settings).
- **Override by OWNER_CNTX (numeric): highest wins.** Product = 0; templates/projects insert higher values to override — upgrade-safe per level. Product rows (EC_* app spaces) must NOT be edited by others; define your own in `Z_`-prefixed tables/own owner context.
- Presentation properties: prefer **static over dynamic**, and **individual properties over the legacy semicolon `PresentationSyntax`** string (avoids upgrade ambiguity).

## 5. Group Model config (why the Equipment navigator cascades)
Group Model = redundant denormalized parent→child relations stored on lower objects for **Allocation-read performance** (20-yr-old concept). A named set of class relations. Object classes are **versioned**, so relations change over time → group model sync happens in the generated **IUD triggers** + ECTP trigger packages. New model (EC 12.2.9+, off by default) vs traditional. *(This is the Production Unit → Area → Facility Class hierarchy that drove the Equipment cascading navigator.)*

## 6. 🔑 Date integrity check — `ENFORCE_DATE_CHECK` (parent/child relations)
Configurable property on object relations:
| Value | Meaning |
|---|---|
| `STRICT` | parent must be valid across child's whole lifespan |
| `IGNORE_NULL` | STRICT but child NULL end-date allowed |
| `OVERLAP` | parent & child just need to overlap |
| `NONE` | no lifespan check |
Relevant to date-effective objects in a Group Model (and to my End=Start deletes on hierarchy members).

## 7. Object-class IUD trigger internals (EC 13.0.0+)
Generated `INSTEAD OF INSERT OR UPDATE OR DELETE ON OV_<class>` triggers. Old `n_`/`o_`/`vt` vars replaced by **`nct` (new class table) / `oct` (old class table)** structures. `nct` may have several rows (group-model version alignment); `oct` always 1 row (all NULL on insert). Journal rules use `p_nct(1)`/`p_oct(1)` not `:NEW`/`:OLD`. *(This is the machinery my saves triggered.)*

## 8. General relations (EC 13.1+) — logical keys
New relation type so external callers (config tools, **REST API**, SQL scripts) operate via **logical keys** instead of surrogate keys (which differ per DB instance). Relation types: OBJECT, OWNER, REF_CODE, GENERAL, CODE_REF.

## 9. EC Codes simplified (CODE_REF) — popup attributes
EC 12.0+: a class relation `RELATION_TYPE = CODE_REF` auto-renders an attribute as a **popup dropdown** (no manual Popup* props), REST-API-aware. Ref classes: `EC_CODES, UNIT_REF, COMPONENT_SET_REF, HYDROCARBONCOMPONENT_REF, TRANS_TEMPLATE_REF`, or a TABLE class with CODE/NAME/SORT_ORDER. *(These are the dropdowns I drive in navigators/forms.)*

## 10. Smart Journaling
Reduces journal "noise": skip journaling for system-user instantiated rows (`JOUR_USER_EXCL_OLD` e.g. SYSTEM/INSTANTIATE) and repeated same-system-user updates (`JOUR_USER_EXCL_NEW` e.g. TRANSFER); always journal deletes with rev_text (`JN_OPERATION=DEL`). Configured in `CTRL_SYSTEM_ATTRIBUTE`; needs view-layer regen. *(Explains the REV_NO / journal behaviour I saw — e.g. BNK_001 staying rev 1.1 when its update failed.)*

## 11. Pages 13–25 (by title — how-to/styling, lighter)
verificationStatus cell colouring · `IGNORE_IND` · `INTERFACE_ALIAS` · custom-Java app-layer data sourcing · Expressions & Scripting in the domain model · Screen Tree-view menu config · Unit of Measure support · **System of Measurement** · get Users & roles · Exclude Synonyms · **Four Eyes Approval** · User Exit packages · **Calculation Group configuration**. Font Awesome icons (`icon-fa`, EC colour classes ECGreen/ECRed/ECYellow/ECOrange/ECBlue/ECPurple). → revisit on demand.

---

## Cross-links to my work
- **`OV_BANK`/`OV_EQPM` = generated object-class views**; my IUD fired their INSTEAD OF triggers (nct/oct).
- **Required versioned attributes** (OBJECT_START_DATE/OBJECT_END_DATE/CODE/NAME…) = the columns in my DB checks, and the reason **End=Start = true delete**. `[[reference_ec_object_delete]]`
- Group Model = the cascading navigator pattern (Equipment). `[[project_ec_iud_learning_track]]`
- CODE_REF popups = the EC-code dropdowns in screens.
- Next: **DOC-03 General Config B** (general-config pages 26–50: system attributes, EC codes admin, etc.).
