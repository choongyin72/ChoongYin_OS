# EC deployment — state at end of 2026-09-03

## ✅ DONE TODAY
1. **Logo references normalised** — R07.001-006 -> `logo.png` (wide INPEX wordmark, 127x22
   box), R07.011-025 -> `ichthys-logo.png` (Ichthys Project tile, 144x75 box). Root cause was
   a NAME COLLISION: both families asked for `logo.png` but need different artwork, and one
   flat extension folder cannot serve that. Cleared R07.002/003/004 on EC.
2. **R07.016's internal name fixed** — was `name="R07_014_LPG_Lifting_Report"` (clone
   leftover). Audited all 122 live JRXMLs under `C:\Projects\INPEX`: it was the ONLY genuine
   case. Propagated to all 8 live copies + both `.jasper` recompiled.
3. **`<group>` drop FIXED in `jr7_to_jr6.py`** — the parked R07.017-022 blocker. The converter
   never emitted `<group>` at all (not in `BAND_ORDER`, no handler), so `G_MONTH` vanished.
   Now emitted after variables per the 6.x XSD, with a group-only `is`-prefix rename table.
   **Full sweep is now 21/21 IDENTICAL** (was 15/21).
4. **Guard added so that class of bug cannot recur** — `ROOT_CHILDREN` allowlist hard-fails on
   any unhandled root child. `<group>` only failed LOUDLY by luck (a variable referenced it);
   a report with a group but no group-reset variable would have lost its page breaks silently.
5. **Converter appends `_6_17` to the internal name** — so each 6.17/V7 pair is
   distinguishable in EC's logs, which are the only place EC uses the report name. Does NOT
   affect fidelity: the name never reaches the PDF (tested, not assumed).
6. **Both Studio workspaces refreshed** — 21 reports in each `R07.XXX` project.
7. **R07.001 unblocked on EC** — `Jasper Definition Url` switched to the `.jrxml`, bypassing
   the `jdk.serialFilter` rejection of its 995KB `.jasper`. Owner confirmed it generates.

## 🔴 STILL OPEN
### A. R07.001 and R07.003 render SHORT on EC — the only wrong output
| Report | Expected | On EC | Missing pages live in |
|---|---|---|---|
| R07.001 | 7 pages | **1** | `<detail>`, gated `REPORT_COUNT == 1..6` |
| R07.003 | 5 pages | **1** | `<detail>`, gated `REPORT_COUNT == 1..4` |

**Mechanism — band choice, nothing else.** These reports have no `<query>` and no `<field>`, so
nothing supplies records. A `<detail>` band prints once per record; with 0 records and
`whenNoDataType="AllSectionsNoDetail"` (print every section EXCEPT detail) only title +
pageFooter survive. The local harness passed `JREmptyDataSource(6)`, which is exactly the input
EC does not provide - so the reports were never wrong, their page count depended on the caller.

**Fix, proven on R07.001 (7 pages, render byte-identical to the owner-approved PDF):**
```xml
<query language="SQL"><![CDATA[
SELECT LEVEL AS RECNO FROM DUAL CONNECT BY LEVEL <= 6
]]></query>
```
after the last `</parameter>`. R07.003 needs `<= 4`. No tables involved.

⚠️ **I first claimed FIVE reports were affected (001-005). WRONG - only 001 and 003.** I
inferred from harness record counts; R07.002/004/005 put their second page in `<summary>`,
which `AllSectionsNoDetail` does NOT skip, so they print fine with zero records. Owner
challenged the list and was right. **Rule: `detail`-band pages vanish without records;
`summary`-band pages do not.**

### B. R07.017-022 have NO artifacts deployed
0 files in the extension folder. Their 6.x JRXMLs now exist and 24 registration scripts are in
place, but nothing is deployed and there is no evidence the scripts were ever run. These six
have never generated on EC.

### C. Extension tree stale for all 21
`sources/CrystalReports/*/output/jr6/` holds the current copies; the
`ecaas_inpex_ichthys` working copy does not. NOT propagated - it is the owner's client git repo
on `feature/MS_upgrade` and writing 40+ files into it needs their say-so.

### D. Stale duplicates in both Studio workspaces
`R07.012/` and `R07.014/` projects hold their own older copies (missing the `_6_17` name
suffix); the 7.0.3 workspace also has `R07_012_FC_Lifting_Report_6_13.jrxml`. Awaiting a
refresh-or-delete decision.

---

# NEXT: SQL query binding (owner, 2026-09-04) — make the reports fully executable
Facts already established that bear on it:
- **Reports WITHOUT a query:** R07.001-006, R07.023-025. R07.001/003 additionally need the
  record-generating query above regardless of real data binding.
- **Reports WITH a query:** R07.011-022, all `SELECT ... FROM TV_<product>_<purpose>_REPORT`.
- **Only 2 of those tables have DDLs** (`sources/SQLs/DDLs/`): `TV_FC_LIFTING_REPORT` and
  `TV_LPG_LIFTING_REPORT` - and they are `CREATE TABLE`, not views. Those are exactly
  R07.012/R07.014, the two reports that worked first.
- ⚠️ **The other table names have UNVERIFIED provenance.** They predate any of my edits (diff
  proves only the `WHERE` line changed, never the `FROM`) but appear nowhere in `sources/SQLs`.
  The uniform naming is equally consistent with a real convention or a pattern extrapolated
  from the two that exist. **Authoritative source = the Crystal `.rpt` originals. Check before
  creating anything.**
- **EC passes a report parameter under its OWN name, no prefix** (`JasperReportGenerator`
  default branch is `reportParams.put(key, value)`). That is why `REPORT_DATE` never reached
  `$P{P_REPORT_DATE}` and had to be renamed. Registered params must match the JRXML exactly.
- **EC supplies a Connection** to any report that declares a query - proven by R07.012/014.
- **Date window pattern in use:** `WHERE DAYTIME BETWEEN TRUNC($P{P_START_DATE}, 'MM') AND
  LAST_DAY($P{P_END_DATE})`, with `P_START_DATE`/`P_END_DATE` parsed from `P_REPORT_DATE`.
  Applied to R07.011/013/015/016 (single-month). R07.017-022 deliberately span FOUR months
  (2025-08-01..2025-11-30) - that is why they carry `G_MONTH` - so do NOT collapse them to one
  month.

---

# Earlier state (kept for the diagnostic method)

## ✅ CURRENT STATE (owner-confirmed 2026-09-03)
**13 of 15 reports now generate on EC.** Two fixes cleared everything:
1. **Logo references normalised** — R07.001-006 -> `logo.png` (wide INPEX wordmark, 127x22
   box), R07.011-025 -> `ichthys-logo.png` (Ichthys Project tile, 144x75 box). The root cause
   was that `logo.png` had to mean two different images for two report families, which one flat
   extension folder cannot serve. Applied to `sources/CrystalReports` and BOTH Studio
   workspaces (7.0.3 and 6.17.0); verified logo-lines-only, line endings preserved.
2. **The invalid table fixed by the owner** — cleared R07.011/013/015/016.

### Still open
- **R07.001** — the only remaining EC failure. `jdk.serialFilter` rejects its 995KB `.jasper`.
  Fix is confirmed and unused so far: point `Jasper Definition Url` at the `.jrxml`. Note its
  6.17 `.jasper` is 1.1MB, so that registration needs the same treatment.
- **R07.017-022** — cannot be downgraded to 6.17 at all: `jr7_to_jr6.py` drops their `<group>`
  element. Their V7 registrations are unaffected. Owner parked this ("revisit those 6 later").

### Deployed artifacts are STALE after the logo change
The `.jasper` files in the extension folder and both workspaces still reference the OLD logo
filenames. The 6.17 copies need reconverting and both `.jasper` sets recompiling before the
logo change takes effect on EC.

---

# Original trace (kept for the diagnostic method)

Owner will action these one at a time and will ping. **Nothing has been fixed or changed** —
this is a trace only. Every cause below was REPRODUCED locally with a real error, not inferred.

## Method (re-runnable)
`tmp/trace_ec.sh` compiles each **deployed** `.jrxml` with EC's own JasperReports **7.0.1** and
fills it with the parameters the scheduler log shows EC sending, with `P_BASE_URL` pointed at
the real extension folder — so asset resolution fails exactly as it does on EC.

Deployment folder:
`C:\Projects\INPEX\DEV\ecaas_inpex_ichthys\extensions\zrep\zrep\src\main\webapp\reports`

## Result — matches the owner's own EC observations

| Report | Local | Cause |
|---|---|---|
| R07.005, R07.006 | OK | — owner confirmed these work on EC |
| R07.001 | **OK, 7 pages** | ① serialFilter (only on EC, via the `.jasper` path) |
| R07.012, R07.014 | OK | — already working on EC |
| R07.023, R07.024, R07.025 | **OK** | ❓ unexplained — report is fine, so likely registration not loaded |
| R07.002, R07.003, R07.004 | FAIL | ② `Byte data not found at: .../logo.jpg` |
| R07.011, R07.013, R07.015, R07.016 | FAIL | ③ `ORA-00942` — **local sandbox only; EC cause UNKNOWN** |

## ① R07.001 — `jdk.serialFilter` rejects the .jasper (EC-side only)
```
jasper7.JasperReportGenerator -> JRLoader.loadObject(JRLoader.java:229)
  -> java.io.InvalidClassException: filter status: REJECTED   (at ObjectInputStream.readArray)
```
**No class name** before "filter status" — a pattern rejection reports
`InvalidClassException: <classname>; filter status: REJECTED`, so this is a filter LIMIT
(`maxarray`/`maxrefs`/`maxdepth`), not a blocked class. R07.001's `.jasper` is 995,786 bytes /
2,688 elements — ~10x every other report (R07.012 = 57,125). Neither EC's code nor either of
its `jasperreports.properties` sets a filter, and JasperReports' own defaults to
`report.class.filter.enabled=false`, so the filter is JVM-level in the EC server's JAVA_OPTS.

**The artifact is NOT at fault** — the deployed `.jasper` loads cleanly under EC's own 7.0.1 on
a JVM without a filter, and Jaspersoft Studio 7.0.3 renders the report fine.

**Confirmed fix:** point `Jasper Definition Url` at the **`.jrxml`** instead of the `.jasper`.
Per `JasperReportGenerator.java:179-184` EC branches on the extension — `.jrxml` goes through
`JRXmlLoader.load` + `compileReport` and never touches `ObjectInputStream`. The local trace
proves this path renders all 7 pages. Cost: a compile on every run. Alternative is relaxing
`jdk.serialFilter` on the EC server (platform team).

## ② logo.jpg is not deployed
R07.002/003/004 reference `$P{P_BASE_URL} + "logo.jpg"`; the extension folder holds only
`logo.png` and `logo_ref.png`. Source exists and all three copies are identical:
`R07.002/output/logo.jpg`, 116,392 bytes, md5 `8cb635167b95f61eb6cc2b2f63e8f2ee`.
Fix = copy it into the extension folder.

## ③ RESOLVED for R07.016 (2026-09-03) — the invalid table WAS the real EC cause
Owner fixed the invalid table and **R07.016 now generates on EC**: status `GENERATED`,
format `pdf`, 2026-09-03 05:35:27, on the `(Template)` / JASPER_V7 row. Two earlier attempts
that day are logged as `ERROR`.

So the table problem was genuine on EC as well — though note my own evidence for it had been
sandbox-only (see the correction below, which still stands as a reasoning lesson: the owner's
fix confirmed it, my trace did not).

**Apply the same fix to R07.011 / R07.013 / R07.015** — same shape, same cause class.

Also confirmed by that screen: both registrations coexist as separate rows
(`...(Template 6.17)` and `...(Template)`), validating the distinct-TEMPLATE_CODE change — with
the shared code they would have deleted one another. And `P_REPORT_DATE` plumbs end-to-end
(`2025-07-01` in REPORT PARAMETERS, `2025-07-01T00:00:00` in PARAMETER VALUES).

⚠️ **R07.016's internal name defect is now LIVE and no longer masked** — its JRXML still
declares `name="R07_014_LPG_Lifting_Report"`. Worth fixing now that the report actually runs.

## ⚠️ Reasoning correction (kept) — the ORA-00942 I observed was MY SANDBOX
**Owner correction 2026-09-03, and they were right.** My trace connects to the LOCAL SANDBOX
(`localhost:1521/ORCL`), while EC runs against **ECDS**. So the `ORA-00942` proves only that
those objects are missing from my sandbox — it is NOT a diagnosis of the EC failure.

What the local sandbox actually holds (queried `all_objects`):

| Object | Local sandbox |
|---|---|
| `TV_FC_LIFTING_REPORT` | **TABLE** |
| `TV_LPG_LIFTING_REPORT` | **TABLE** |
| `TV_FC_PRODUCTION_REPORT` | ABSENT |
| `TV_LPG_PRODUCTION_REPORT` | ABSENT |
| `TV_PC_PRODUCTION_REPORT` | ABSENT |
| `TV_PC_LIFTING_REPORT` | ABSENT |
| `TV_FC_PLP_PRODUCTION_FORECAST_REPORT` | ABSENT |
| `TV_FC_PROVISIONAL_LIFTING_PROGRAM` | ABSENT |

The two present ones are TABLES, created locally by `DDLs/TV_FC_LIFTING_REPORT.sql` /
`TV_LPG_LIFTING_REPORT.sql` (both `CREATE TABLE`). They exist locally purely because those two
DDLs were run — which is exactly why only R07.012/R07.014 render in my trace.

**Status of R07.011/013/015/016 on EC: UNKNOWN.** They do fail there (owner observed it), but
the cause is unverified and needs an EC scheduler log. Do NOT act on "create four views" — see
the open question below.

**Open question, unresolved:** are those table names even correct? They were present in the
JRXMLs before any of my edits (proven by diff against `.backup_20260902_paramwork`: only the
`WHERE` line changed, never the `FROM`), but they originate from earlier build sessions and
appear nowhere in `sources/SQLs`. The uniform `TV_<product>_<purpose>_REPORT` naming is equally
consistent with a real convention or with a pattern extrapolated from the two that do exist.
Authoritative source = the Crystal `.rpt` originals. Settle that before creating anything.

## New defect — R07.016 carries R07.014's identity
`R07_016_PC_Lifting_Report.jrxml` declares `name="R07_014_LPG_Lifting_Report"` — a leftover
from cloning it off R07.014. Audited all 15; it is the only one. Its compiled `.jasper` loads
under the wrong internal name. Masked for now because R07.016 fails earlier on ③.

## Other verified state
- All 15 deployed `.jrxml` are byte-identical to source, EXCEPT R07.012's `_6_17.jrxml`, which
  is stale (36,377 bytes from an older converter revision vs the current 39,839). It works, but
  is not the conversion verified IDENTICAL.
- All 30 deployed `.jasper` load cleanly (15 on 7.0.1, 15 on 6.21.4). Caveat: this JVM has no
  serialFilter, so the test finds corrupt/version-wrong artifacts, NOT filter rejections.
- **EC runs JasperReports 7.0.1**, not 7.0.3 (`ec701/net.sf.jasperreports-jasperreports-7.0.1.jar`
  extracted from EC). Any `.jasper` deployed to a V7 registration should be compiled with 7.0.1.
  The `.jrxml` route sidesteps this entirely — EC compiles in-process with its own version.
- `P_REPORT_DATE` now reaches the report: the scheduler log shows
  `"P_REPORT_DATE":"2025-07-01T00:00:00"` being passed, confirming the `REPORT_DATE` ->
  `P_REPORT_DATE` rename works.

## ⚠️ .jasper files are NOT byte-comparable
These JRXMLs carry zero `uuid=` attributes, so JasperReports mints fresh UUIDs on every compile:
two compiles of the SAME file by the SAME version differ by ~42KB. Byte-diff cannot identify a
compiler version or validate an artifact — only loading it can. (I briefly drew a version
conclusion from a byte-diff before testing this; it was wrong.)

## Pending actions (all need owner go-ahead)
1. Copy `logo.jpg` into the extension folder — clears R07.002/003/004
2. Fix R07.016's `name=` attribute, then reconvert + recompile
3. Point R07.001's `Jasper Definition Url` at `.jrxml` — clears R07.001
4. ~~Create the four missing views~~ — **do NOT act on this yet.** The ORA-00942 was my
   sandbox, not EC. First get an EC log for one of R07.011/013/015/016, and confirm the table
   names against the Crystal `.rpt` originals.
5. Get an EC log for R07.023 AND for one of R07.011/013/015/016 — two unexplained groups
6. Refresh R07.012's stale deployed `_6_17.jrxml`
