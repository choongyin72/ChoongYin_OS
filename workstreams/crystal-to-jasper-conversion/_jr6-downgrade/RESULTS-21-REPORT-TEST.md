# JR 7.0.3 → 6.17.0 downgrade sweep — R07.001–006, R07.011–025

Run 2026-09-02 22:06–22:11. **TEST ONLY** per owner: *"no fix code... only test its able to
downgrade and have same report for both version"*.

Reproduce: `py test_all.py` (all 21) or `py test_all.py R07.017` (one).

## No report source was modified
Verified, not assumed: a `find` for any main JRXML modified during the batch window returns
nothing. Everything written went to `<report>/output/jr6/` (converted JRXML, 2 PDFs, `.jasper`)
and `_jr6-downgrade/_testwork/`. R07.001's JRXML carries a 19:32:43 stamp from the earlier
owner-approved defect-fix build, 2h34m before this batch started.

The two things that would otherwise have required editing a report were handled in **copies of
the Java harness**, applied identically to both engines so they cannot bias the comparison:
- the 7.x-only `net.sf.jasperreports.pdf.JRPdfExporter` (moved out of `engine.export` in 7.0)
- R07.012/014's `P_BASE_URL`, which defaults to the EC path `/extension/ZREP/reports/` and on a
  local disk resolves to the drive root where the logo is not present

## Result: 15 pass, 6 fail

| Verdict | Reports |
|---|---|
| **IDENTICAL** + EC 6.21.4 loads the `.jasper` | R07.001 002 003 004 005 006 011 012 013 014 015 016 023 024 025 |
| **COMPILE-FAIL** on real 6.17.0 | R07.017 018 019 020 021 022 |

Identical means every text span, every drawing rect and every font family matches exactly —
e.g. R07.001 = 1263 spans / 1442 rects, R07.012 = 385 / 1438, R07.005 = 637 / 2397.

## The 6 failures — one shared root cause (PARKED, owner will revisit)

`jr7_to_jr6.py` **drops the `<group>` element entirely.** All six reports have exactly one
group — `G_MONTH`, their page-per-month break — and the converted 6.x file has zero. The
variables that reference it survive, so 6.17.0 rejects the design:

```
Report design not valid :
     1. Unknown reset group 'G_MONTH' for variable : V_PRODUCTION_TOTAL
```

(R07.019/020 name `V_PRODUCTION_PROPANE_TOTAL`; otherwise identical.) Confirmed by grep:
7.x has `<group name="G_MONTH" startNewPage="true">`, the 6.x output has no `<group ` at all,
while all nine `resetGroup="G_MONTH"` variables are still emitted.

### ⚠️ It failed loudly only by luck
The validation error fires *because* a group-reset variable exists. A report with a `<group>`
but no such variable would lose its grouping and page breaks **silently** — correct page count,
wrong data boundaries, no error. Audited all 21 for this: only R07.017–022 declare a group, so
none of the 15 passes is hiding a silent loss.

## Two method points worth keeping

1. **Run each report's own harness under both engines**, not a generic fill. R07.017–022 fill
   from a hand-built 2-month `JRMapCollectionDataSource` with a per-report `rowAt()` helper;
   reimplementing that would have meant guessing field names, and a fill that differs from the
   baseline produces span differences unrelated to the downgrade. Both PDFs are generated fresh
   in the same run, so there is also no question of which stale artifact in `output/` is the
   right baseline — which mattered, since the newest PDF is `R07_002_refresh_test.pdf` for
   R07.002 and `*_generated.pdf` for R07.012/014.
2. **Put the Arial fonts jar on the 7.x classpath too.** R07.012's and R07.014's own `cp.txt`
   omit it, so the *baseline* silently fell back to Helvetica and dropped bold/italic — both
   reports first reported DIFFERS in the wrong direction, with the 6.x output being the correct
   one (rects were already 1438=1438). Same trap the README documents, on the side I wasn't
   watching. `cp7()` now appends it unconditionally.

## Scope limit — state this whenever quoting these results
`EC-LOAD-OK` proves EC's legacy 6.21.4 engine **deserialises** the 6.17.0-compiled `.jasper`.
It does **not** prove EC generates the report end-to-end; that needs a report definition per
report plus an extension deploy. R07.012 is the only report proven that far
(`Report number 22 is generated successfully`, `P_BASE_URL = /extension/ZREP/reports/`).

Full failure output per report: `_testwork/<report>/fail.log`.
