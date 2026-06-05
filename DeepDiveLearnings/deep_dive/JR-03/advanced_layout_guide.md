# JR-03: Advanced Layout Guide — JasperReports 7.0.3+

## 1. Subreports

### What Subreports Are
A subreport is a separate `.jasper` file called from within a parent (master) report. Each subreport runs its own query, has its own bands, and renders independently inside the master's band.

### When to Use Subreports
- Master-detail layouts: facility header + well detail rows per facility
- Multi-section reports: each section has a different query
- Reusable report components: a standard footer shared across reports

### `<subreport>` Element Anatomy
```xml
<subreport>
    <reportElement x="0" y="20" width="535" height="200"/>

    <!-- Parameters to pass TO the subreport -->
    <subreportParameter name="P_OBJECT_ID">
        <subreportParameterExpression>
            <![CDATA[$F{OBJECT_ID}]]>
        </subreportParameterExpression>
    </subreportParameter>

    <!-- Pass all parameters from master to subreport -->
    <parametersMapExpression><![CDATA[$P{REPORT_PARAMETERS_MAP}]]></parametersMapExpression>

    <!-- JDBC connection (same connection as master) -->
    <connectionExpression><![CDATA[$P{REPORT_CONNECTION}]]></connectionExpression>

    <!-- Path to compiled subreport — relative to master -->
    <subreportExpression>
        <![CDATA["well_detail_subreport.jasper"]]>
    </subreportExpression>
</subreport>
```

### Returning Values from Subreport
```xml
<!-- In subreport: define a variable to export -->
<variable name="SUBRPT_TOTAL" class="java.lang.Double" calculation="Sum">
    <variableExpression><![CDATA[$F{net_oil_vol}]]></variableExpression>
</variable>

<!-- In master: receive the returned value -->
<returnValue subreportVariable="SUBRPT_TOTAL"
             toVariable="MASTER_SUBTOTAL"
             calculation="Sum"/>
```

### Compilation Order
Subreports MUST be compiled BEFORE the master report. Build order:
```
1. Compile subreport_detail.jrxml → subreport_detail.jasper
2. Compile master_report.jrxml → master_report.jasper
3. Both .jasper files must be in the same directory (or use absolute path)
```

### Common Pitfall: JRException Subreport Not Found
**Symptom:** `net.sf.jasperreports.engine.JRException: Subreport not found`
**Cause:** The `subreportExpression` path is wrong at runtime
**Resolution:**
1. Use relative path: `"subreport_detail.jasper"` (same folder as master)
2. Or use absolute path via parameter: `$P{SUBREPORT_DIR} + "subreport_detail.jasper"`
3. In EC: pass the subreport base path as a report parameter from Java

---

## 2. Crosstabs

### What Crosstabs Are
A crosstab (pivot table) aggregates data across two dimensions (row groups × column groups) and displays measures at intersections.

### Crosstab Structure
```xml
<crosstab isRepeatColumnHeaders="true" isRepeatRowHeaders="true">

    <!-- Dataset — subset of the main data source -->
    <crosstabDataset>
        <dataset>
            <datasetRun subDataset="CROSSTAB_DATASET"/>
        </dataset>
    </crosstabDataset>

    <!-- Row group: e.g. Stream name down the left -->
    <rowGroup name="STREAM_GROUP" width="120" totalPosition="End">
        <bucket class="java.lang.String">
            <bucketExpression><![CDATA[$F{stream_code}]]></bucketExpression>
        </bucket>
        <crosstabRowHeader>
            <cellContents>
                <textField>
                    <reportElement x="0" y="0" width="120" height="14"/>
                    <textFieldExpression><![CDATA[$V{STREAM_GROUP}]]></textFieldExpression>
                </textField>
            </cellContents>
        </crosstabRowHeader>
        <crosstabTotalRowHeader>
            <cellContents>
                <staticText>
                    <reportElement x="0" y="0" width="120" height="14"/>
                    <text><![CDATA[TOTAL]]></text>
                </staticText>
            </cellContents>
        </crosstabTotalRowHeader>
    </rowGroup>

    <!-- Column group: e.g. Month across the top -->
    <columnGroup name="MONTH_GROUP" height="20" totalPosition="End">
        <bucket class="java.lang.String">
            <bucketExpression>
                <![CDATA[new java.text.SimpleDateFormat("MMM-yy").format($F{daytime})]]>
            </bucketExpression>
        </bucket>
        <crosstabColumnHeader>
            <cellContents>
                <textField>
                    <reportElement x="0" y="0" width="60" height="20"/>
                    <textElement textAlignment="Center"/>
                    <textFieldExpression><![CDATA[$V{MONTH_GROUP}]]></textFieldExpression>
                </textField>
            </cellContents>
        </crosstabColumnHeader>
        <crosstabTotalColumnHeader>
            <cellContents>
                <staticText>
                    <reportElement x="0" y="0" width="60" height="20"/>
                    <textElement textAlignment="Center"/>
                    <text><![CDATA[TOTAL]]></text>
                </staticText>
            </cellContents>
        </crosstabTotalColumnHeader>
    </columnGroup>

    <!-- Measure: Sum of oil volumes at each intersection -->
    <measure name="OIL_SUM" class="java.lang.Double" calculation="Sum">
        <measureExpression><![CDATA[$F{net_oil_vol}]]></measureExpression>
    </measure>

    <!-- Detail cell (stream × month) -->
    <crosstabCell width="60" height="14">
        <cellContents>
            <textField>
                <reportElement x="0" y="0" width="60" height="14"/>
                <textElement textAlignment="Right"/>
                <textFieldExpression>
                    <![CDATA[$V{OIL_SUM} != null ?
                        new java.text.DecimalFormat("#,##0.0").format($V{OIL_SUM}) : "0.0"]]>
                </textFieldExpression>
            </textField>
        </cellContents>
    </crosstabCell>

</crosstab>
```

### Crosstab Conditional Styles (Zebra Striping)
```xml
<crosstabCell width="60" height="14">
    <cellContents>
        <!-- Conditional background on even rows -->
        <rectangle>
            <reportElement x="0" y="0" width="60" height="14" mode="Opaque">
                <printWhenExpression>
                    <![CDATA[$V{ROW_COUNT} % 2 == 0]]>
                </printWhenExpression>
            </reportElement>
            <graphicElement>
                <pen lineWidth="0"/>
            </graphicElement>
        </rectangle>
    </cellContents>
</crosstabCell>
```

---

## 3. Charts

### Bar Chart Example
```xml
<barChart>
    <chart>
        <reportElement x="0" y="0" width="535" height="200"/>
        <chartTitle>
            <titleExpression><![CDATA["Daily Oil Production by Well"]]></titleExpression>
        </chartTitle>
    </chart>
    <categoryDataset>
        <categorySeries>
            <seriesExpression><![CDATA["Oil Volume"]]></seriesExpression>
            <categoryExpression><![CDATA[$F{OBJECT_CODE}]]></categoryExpression>
            <valueExpression><![CDATA[$F{NET_OIL_VOL_SM3}]]></valueExpression>
        </categorySeries>
    </categoryDataset>
    <barPlot isShowLabels="true">
        <plot orientation="Vertical"/>
        <itemLabel>
            <font size="8" pdfFontName="Helvetica" isPdfEmbedded="false"/>
        </itemLabel>
    </barPlot>
</barChart>
```

### Chart Types Available (v7.0.3)
`barChart`, `bar3DChart`, `lineChart`, `areaChart`, `pieChart`, `pie3DChart`, `xyBarChart`, `xyLineChart`, `scatterChart`, `bubbleChart`, `ganttChart`, `thermometerChart`, `meterChart`, `stackedBarChart`

---

## 4. Export Configuration — PDF & Excel

### PDF Export Properties
```xml
<!-- Set in report root or via JasperExportManager -->
<property name="net.sf.jasperreports.export.pdf.compressed" value="true"/>
<property name="net.sf.jasperreports.export.pdf.encrypted" value="false"/>
<property name="net.sf.jasperreports.export.pdf.owner.password" value=""/>

<!-- Accessibility -->
<property name="net.sf.jasperreports.export.pdf.tagged" value="true"/>
<property name="net.sf.jasperreports.export.pdf.tag.language" value="EN-US"/>
```

### Excel Export Properties
```xml
<!-- One sheet per band group -->
<property name="net.sf.jasperreports.export.xls.one.page.per.sheet" value="false"/>

<!-- Remove blank rows between detail bands -->
<property name="net.sf.jasperreports.export.xls.remove.empty.space.between.rows" value="true"/>
<property name="net.sf.jasperreports.export.xls.remove.empty.space.between.columns" value="true"/>

<!-- Auto-detect cell type (number vs string) -->
<property name="net.sf.jasperreports.export.xls.detect.cell.type" value="true"/>

<!-- Sheet name -->
<property name="net.sf.jasperreports.export.xls.sheet.names.all" value="Production Data"/>

<!-- Freeze header row -->
<property name="net.sf.jasperreports.export.xls.freeze.row" value="3"/>
```

### Key Excel Pitfall: Numeric Cells as Text
**Symptom:** Numbers in Excel cells are left-aligned and cannot be summed
**Cause:** `detect.cell.type` not enabled
**Resolution:** Add `net.sf.jasperreports.export.xls.detect.cell.type=true` property

---

## 5. Conditional Styles

```xml
<!-- Define style at report level -->
<style name="DataRow">
    <conditionalStyle>
        <conditionExpression><![CDATA[$V{REPORT_COUNT} % 2 == 0]]></conditionExpression>
        <style backcolor="#F5F5F5" mode="Opaque"/>
    </conditionalStyle>
    <conditionalStyle>
        <!-- Highlight negative values in red -->
        <conditionExpression>
            <![CDATA[$F{NET_OIL_VOL_SM3} != null && $F{NET_OIL_VOL_SM3} < 0]]>
        </conditionExpression>
        <style forecolor="#CC0000" isBold="true" pdfFontName="Helvetica-Bold"/>
    </conditionalStyle>
</style>

<!-- Apply to reportElement -->
<textField>
    <reportElement style="DataRow" .../>
    ...
</textField>
```

---

## 6. `isTitleNewPage` & PAGE_COUNT Behaviour

When `isTitleNewPage="true"`:
- Title is rendered on page 1
- Data starts on page 2
- `PAGE_COUNT` includes the title page

**Resolution patterns:**

```xml
<!-- Option A: Subtract 1 from PAGE_COUNT -->
<![CDATA["Page " + $V{PAGE_NUMBER} + " of " + ($V{PAGE_COUNT} - 1)]]>

<!-- Option B: Don't use isTitleNewPage — put title in a group header -->
<!-- Set isTitleNewPage="false" (default) and control layout with bands -->

<!-- Option C: Suppress footer on title page -->
<pageFooter>
    <band height="20">
        <textField>
            <reportElement x="0" y="1" width="535" height="14">
                <printWhenExpression><![CDATA[$V{PAGE_NUMBER} > 1]]></printWhenExpression>
            </reportElement>
            ...
        </textField>
    </band>
</pageFooter>
```
