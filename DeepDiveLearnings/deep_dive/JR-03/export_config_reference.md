# Export Configuration Reference — JasperReports 7.0.3+

## PDF Export Properties

| Property | Default | Recommended for EC | Notes |
|---|---|---|---|
| `net.sf.jasperreports.export.pdf.compressed` | `false` | `true` | Reduces file size ~30-50% |
| `net.sf.jasperreports.export.pdf.encrypted` | `false` | `false` | Enable only if report contains sensitive data |
| `net.sf.jasperreports.export.pdf.owner.password` | (none) | (none) | Set if encrypted=true |
| `net.sf.jasperreports.export.pdf.user.password` | (none) | (none) | Password to open the PDF |
| `net.sf.jasperreports.export.pdf.tagged` | `false` | `true` | Accessibility — PDF/UA compliance |
| `net.sf.jasperreports.export.pdf.tag.language` | (none) | `EN-US` | Required when tagged=true |
| `net.sf.jasperreports.export.pdf.javascript` | (none) | (none) | Avoid in EC — security risk |
| `net.sf.jasperreports.export.pdf.pdfa.conformance` | `NONE` | `NONE` | Set to PDFA1A for archiving |

### Set in JRXML (report-level)
```xml
<property name="net.sf.jasperreports.export.pdf.compressed" value="true"/>
<property name="net.sf.jasperreports.export.pdf.tagged" value="true"/>
<property name="net.sf.jasperreports.export.pdf.tag.language" value="EN-US"/>
```

### Set in Java (runtime)
```java
SimplePdfExporterConfiguration config = new SimplePdfExporterConfiguration();
config.setCompressed(true);
config.setTagged(true);
config.setTagLanguage("EN-US");
JRPdfExporter exporter = new JRPdfExporter();
exporter.setConfiguration(config);
```

---

## Excel (XLSX) Export Properties

| Property | Default | Recommended for EC | Notes |
|---|---|---|---|
| `net.sf.jasperreports.export.xls.one.page.per.sheet` | `false` | `false` | true = one sheet per report page |
| `net.sf.jasperreports.export.xls.remove.empty.space.between.rows` | `false` | `true` | Critical — removes blank rows between bands |
| `net.sf.jasperreports.export.xls.remove.empty.space.between.columns` | `false` | `true` | Removes blank columns |
| `net.sf.jasperreports.export.xls.detect.cell.type` | `false` | `true` | Numeric fields become numbers not strings |
| `net.sf.jasperreports.export.xls.white.page.background` | `true` | `true` | Keep white background |
| `net.sf.jasperreports.export.xls.ignore.graphics` | `false` | `false` | Set true to skip charts/images for faster export |
| `net.sf.jasperreports.export.xls.freeze.row` | (none) | `3` | Freeze header rows (set to row AFTER headers) |
| `net.sf.jasperreports.export.xls.freeze.column` | (none) | (none) | Freeze left columns |
| `net.sf.jasperreports.export.xls.sheet.names.all` | (auto) | `"Production Data"` | Name all sheets with this value |
| `net.sf.jasperreports.export.xls.collapse.row.span` | `false` | `true` | Prevents merged cell issues |

### Standard EC Excel Export Config Block
```xml
<property name="net.sf.jasperreports.export.xls.remove.empty.space.between.rows" value="true"/>
<property name="net.sf.jasperreports.export.xls.remove.empty.space.between.columns" value="true"/>
<property name="net.sf.jasperreports.export.xls.detect.cell.type" value="true"/>
<property name="net.sf.jasperreports.export.xls.freeze.row" value="3"/>
<property name="net.sf.jasperreports.export.xls.collapse.row.span" value="true"/>
<property name="net.sf.jasperreports.export.xls.sheet.names.all" value="Production Data"/>
```

---

## HTML Export Properties

| Property | Default | Recommended for EC | Notes |
|---|---|---|---|
| `net.sf.jasperreports.export.html.use.background.image.to.align` | `true` | `false` | Avoid background images for clean HTML |
| `net.sf.jasperreports.export.html.frames.as.nested.tables` | `true` | `true` | Better layout in browsers |

---

## Common Export Pitfalls

| Problem | Cause | Fix |
|---|---|---|
| Numbers in Excel as text (left-aligned) | `detect.cell.type` not set | Add `xls.detect.cell.type=true` |
| Blank rows between data rows in Excel | `remove.empty.space.between.rows` not set | Add both empty space properties |
| PDF blank text / boxes | Font not found | Use Helvetica with `isPdfEmbedded=false` |
| Merged cells break Excel formulas | Band height merges cells | Set `xls.collapse.row.span=true` |
| Page headers repeat in Excel | Multi-page PDF exported to Excel | Use `xls.one.page.per.sheet=false` + remove page headers |
