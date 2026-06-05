# JasperReports 7.0.3+ — World-Class Best Practices

## Naming Conventions

```
File names:     EC_<Domain>_<ReportName>.jrxml     e.g. EC_Prod_DailyWellStatus.jrxml
Report name:    Same as file (without .jrxml)
Parameter names: P_<UPPERCASE>                     e.g. P_DAYTIME, P_FACILITY_CODE
Field names:    <lowercase_with_underscore>         e.g. net_oil_vol, object_code
Variable names: <UPPERCASE_WITH_UNDERSCORE>         e.g. TOTAL_OIL, ROW_COUNT
Style names:    <PascalCase>                        e.g. HeaderStyle, DataRow
```

## Version Control

**Commit `.jrxml` files — not `.jasper` files**
- `.jrxml` is the source of truth (XML, diff-able)
- `.jasper` is compiled output — regenerate from `.jrxml`
- Add `*.jasper` to `.gitignore`
- Exception: if Jasper Studio cannot access the DB at CI time, commit `.jasper` alongside `.jrxml`

## Design Rules (Actionable)

1. **Every report has a `noData` band** — no exceptions
2. **Every field expression has null-safety** — no raw `$F{}` without null check
3. **All styles defined once at report level** — never set fontName/size inline on reportElement
4. **Parameterise everything that might change** — dates, object codes, colour thresholds
5. **Push aggregation to SQL** — use database SUM/COUNT, not report variables, for large datasets
6. **Sort in SQL, not in the report** — JasperReports does not sort; group expression field must be first in ORDER BY
7. **Never use `$P!{}` in WHERE clause** — only for ORDER BY with developer-controlled values
8. **Use Helvetica family with `isPdfEmbedded=false`** — no font JARs needed
9. **Add XML comment block at report top** — document: data source, parameters, audience, owner
10. **Keep detail band height tight** — y + height of ALL elements ≤ band height - 2px buffer

## Testing Strategy

```
Level 1 — Jasper Studio Preview: test with real EC local DB (localhost:1521/ORCL)
Level 2 — Export to PDF: verify fonts, layout, totals
Level 3 — Export to Excel: verify cell types, no merged cells, freeze rows
Level 4 — Edge cases: empty result set, single row, NULL values in all fields
Level 5 — Large dataset: 1000+ rows — verify performance and pagination
```

## Documentation Standard (XML Comment in JRXML)
```xml
<!-- ============================================================
     Report: EC_Prod_DailyWellStatus
     Owner: Choong-Yin Lee
     Data Source: Oracle ECKERNEL_EC — rv_pwel_day_status
     Parameters:
       P_DAYTIME (Date) — production date, defaults to today
       P_FACILITY_CODE (String) — facility filter, "ALL" = no filter
     Audience: Production Operations team
     Format: PDF (A4 landscape) + Excel
     Version History:
       2026-06-05 CYL: Initial version
     ============================================================ -->
```

## PR Code Review Checklist

- [ ] All field expressions have null-safety
- [ ] noData band present with meaningful message
- [ ] No hardcoded URLs, usernames, or passwords in parameters
- [ ] `net.sf.jasperreports.export.xls.detect.cell.type=true` if Excel output needed
- [ ] `net.sf.jasperreports.export.xls.remove.empty.space.between.rows=true` if Excel output
- [ ] Fonts use Helvetica family with `isPdfEmbedded=false`
- [ ] No `$P!{}` in WHERE clause
- [ ] SQL ORDER BY matches group expression field order
- [ ] XML comment block at report top documents purpose, parameters, owner
- [ ] Tested with empty result set (noData renders correctly)
- [ ] `.jasper` file NOT committed (only `.jrxml`)
