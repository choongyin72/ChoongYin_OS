# EFK Phase-2 — EC Framework / EC Technology cohort + the **Database Sanity** rules
Read 2026-06-14 from EC Knowledge (EFK). **EC Framework** `1854410` and **EC Technology** `1853250`
are thin parent pages; most Framework children are 2014 empty stubs. The one high-value page is
**Database Sanity** `1851734` (2018) — a list of EC config/extension patterns that are **NOT
supported**. Captured because it's a direct guardrail for the coverage track + any hands-on config
(ECPR deploys, ZWP extensions, group-model work).

## ⭐ Database Sanity — unsupported config/coding rules (the "don't do this" list)
EC is highly flexible with unclear lines on what's allowed; this page lists cases known to cause
problems (the intent was to grow these into automated sanity checks + a real framework-API contract).

| Rule | What | Severity | Why it bites |
|---|---|---|---|
| **Object_id uniqueness across classes** | `object_id` is unique **system-wide**, also across object classes — two different object classes must NOT share the same row (object_id). If classes share a physical table, their class WHERE must be **mutually exclusive**. (Does NOT apply to Interfaces, Data classes, Table classes.) | Medium | Breaks access control + `ecdp_objects.GetObjClassName(p_object_id)` (ambiguous class for a shared id). |
| **Group model must be loop-free** | A group model (hierarchy among object classes) assumes **one path between any two nodes** — no loops. Known exceptions with special logic: **FCTY_CLASS_1, Well_Hookup, Well**. For *project* group models the no-loop rule is essential. | Medium | Loops break correct **data-replication synchronization + version splitting**. |
| **Class Trigger actions discipline** | EC's viewlayer uses INSTEAD-OF triggers; you can inject PL/SQL in *Class trigger actions* (folded into generated triggers). Injected code should target the **physical table layer**, not interfere with transaction handling in a for-each-row trigger. Oracle's **mutating-trigger** limits are the guideline. | **High** | Referring to other generated views/packages → **circular dependencies** + more build steps. Separate DML on the *same table* the INSTEAD-OF trigger works on → corrupts **audit trails / sync**. |
| **No order/group by in class DB Where Condition** | A class's `db_where_condition` **cannot contain `ORDER BY` or `GROUP BY`**. | Low | Such classes **won't build**. |

### How this connects to what I've already seen
- The **group-model loop-free rule + the FCTY_CLASS_1 / Well_Hookup / Well exceptions** is the
  architectural reason the **N1 daily-status nav cascade** is shaped the way it is (Date → PU → Area →
  Facility Class 1 → Well Hookup → Well) — those exception nodes carry special hierarchy logic. Ties to
  [[reference_ec_navigator_go_button]] and the N1 pattern.
- **object_id uniqueness across classes** underpins why my DbVerify resolves OBJECT_ID per name-source
  view (WELL_VERSION / OV_STREAM) and why allocation/day-status tables key cleanly on (OBJECT_ID,
  DAYTIME) — the id is globally unique. Reinforces the [[reference_db_design]] picture.
- **Class trigger / DB-where constraints** are guardrails for any ZWP/PL-SQL extension or class-config
  change (e.g. ECPR work, validation rules): keep injected trigger code at the physical-table layer,
  no circular view/package refs, no order/group-by in class WHEREs. Worth checking against before
  proposing any class-level config change. Pairs with [[feedback_clone_full_row_diff]].

## Thin / empty siblings (noted, not deep-read)
- **EC Framework `1854410`** + **EC Technology `1853250`** — parent stubs only.
- **Calculation Framework `1852084`** (2020) — body is an empty placeholder (`---`). The real calc
  depth I already hold is in `calc-engine-insights.md` + `vcf-calculation.md`.
- **EC Timezone `1853989`** (2020) — empty body. (Relevant topic for DAYTIME correctness if it ever
  gets content — revisit on demand.)
- 2014 empty stubs: **BPM, EC Core, ECIS, JSF, Logging, Messaging, Reporting, Jboss, To Do's for JSF**.
  (BPM stub ≠ the held BPM/Process-Automation deep dive; ECIS stub ≠ my deep ECIS notes; JSF stub ≠ the
  JSF/PrimeFaces id grammar I already field-guide.)
- **ARJUNA016027 in server log** `1835991` (2016) — ops fix: WildFly/Oracle **XA recovery** grants to
  silence a 2-min server-log warning. Filed for ops reference only.
- **EC Technology → Presentations `1853267`** (2021) — slide decks; low text value, skipped.

## Phase-2 status / next
Framework cohort done (Database Sanity = the keeper). Phase-2 calc/framework depth now covered by:
calc-engine-insights, vcf-calculation, framework-db-sanity (+ framework-calculation/ecis from the
earlier setup). Remaining series value is mostly **Phase-3 reference** (EC Vocabulary cross-check vs my
GLOSSARY; EC Talks newest topics) and **Phase-4 on-demand ops** (schedule-job / stuck-service — pull
when the scheduler misbehaves). Next idle item: **EC Vocabulary `1844980`** (Phase-3, cross-check
acronyms against `business-domains/GLOSSARY.md`).
