# JasperReports 7.0.3+ — Cheatsheet

## JRXML Skeleton
```xml
<?xml version="1.0" encoding="UTF-8"?>
<jasperReport xmlns="http://jasperreports.sourceforge.net/jasperreports"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://jasperreports.sourceforge.net/jasperreports
        http://jasperreports.sourceforge.net/xsd/jasperreport.xsd"
    name="ReportName" pageWidth="842" pageHeight="595" orientation="Landscape"
    columnWidth="782" leftMargin="30" rightMargin="30" topMargin="20" bottomMargin="20"
    whenNoDataType="NoData">
  <style name="Def" isDefault="true" fontName="Helvetica" pdfFontName="Helvetica"
         isPdfEmbedded="false" pdfEncoding="Cp1252" fontSize="9"/>
  <parameter name="P_PARAM" class="java.util.Date"/>
  <queryString language="sql"><![CDATA[SELECT ... FROM ... WHERE col=$P{P_PARAM}]]></queryString>
  <field name="col_name" class="java.lang.String"/>
  <variable name="VAR" class="java.lang.Double" calculation="Sum" resetType="Report">
    <variableExpression><![CDATA[$F{col_name}]]></variableExpression>
  </variable>
  <title><band height="30">...</band></title>
  <pageHeader><band height="0"/></pageHeader>
  <columnHeader><band height="18">...</band></columnHeader>
  <detail><band height="14">...</band></detail>
  <columnFooter><band height="2"/></columnFooter>
  <pageFooter><band height="16">...</band></pageFooter>
  <lastPageFooter><band height="24">...</band></lastPageFooter>
  <summary><band height="0"/></summary>
  <noData><band height="30"><!-- No data message --></band></noData>
</jasperReport>
```

## 9 Band Names (in render order)
`title` → `pageHeader` → `columnHeader` → `detail` → `columnFooter` → `pageFooter`
Last page: `lastPageFooter` replaces `pageFooter`
After all: `summary`
Zero rows: `noData`

## Variable Calculation Types
`Nothing` `Count` `DistinctCount` `Sum` `Average` `Lowest` `Highest` `StandardDeviation` `Variance` `First` `System`

## resetType / incrementType Options
`Report` `Page` `Column` `Group` (+ `resetGroup="GROUP_NAME"`) `None`

## pdfFontName Mappings
| Screen Font | Style | pdfFontName |
|---|---|---|
| Helvetica | Regular | `Helvetica` |
| Helvetica | Bold | `Helvetica-Bold` |
| Helvetica | Italic | `Helvetica-Oblique` |
| Helvetica | Bold+Italic | `Helvetica-BoldOblique` |

Always: `isPdfEmbedded="false"` `pdfEncoding="Cp1252"`

## Top 10 Most-Used Properties
```xml
<property name="net.sf.jasperreports.export.pdf.compressed" value="true"/>
<property name="net.sf.jasperreports.export.pdf.tagged" value="true"/>
<property name="net.sf.jasperreports.export.xls.detect.cell.type" value="true"/>
<property name="net.sf.jasperreports.export.xls.remove.empty.space.between.rows" value="true"/>
<property name="net.sf.jasperreports.export.xls.remove.empty.space.between.columns" value="true"/>
<property name="net.sf.jasperreports.export.xls.freeze.row" value="3"/>
<property name="net.sf.jasperreports.export.xls.collapse.row.span" value="true"/>
<property name="net.sf.jasperreports.export.xls.sheet.names.all" value="Data"/>
<property name="net.sf.jasperreports.export.xls.one.page.per.sheet" value="false"/>
<property name="com.jaspersoft.studio.data.defaultdataadapter" value="LocalEC"/>
```

## Most Common Expression Patterns
```xml
<!-- Null-safe string -->
$F{f} != null ? $F{f} : ""
java.util.Objects.toString($F{f}, "")

<!-- Null-safe number format -->
$F{n} != null ? new java.text.DecimalFormat("#,##0.000").format($F{n}) : "0.000"

<!-- Null-safe date format -->
$F{d} != null ? new java.text.SimpleDateFormat("dd-MMM-yyyy").format($F{d}) : ""

<!-- Page footer -->
"Page " + $V{PAGE_NUMBER} + " of " + $V{PAGE_COUNT}

<!-- Status code to label -->
$F{s}.equals("V") ? "Verified" : ($F{s}.equals("A") ? "Approved" : "Provisional")

<!-- printWhenExpression — show only when not null -->
$F{f} != null && !$F{f}.isEmpty()
```

## Built-in Variables
`$V{PAGE_NUMBER}` `$V{PAGE_COUNT}` `$V{COLUMN_NUMBER}` `$V{REPORT_COUNT}` `$V{COLUMN_COUNT}`

## Oracle → Java Type Mapping
| Oracle | Java class |
|---|---|
| VARCHAR2 | `java.lang.String` |
| NUMBER | `java.lang.Double` |
| DATE | `java.util.Date` |
| TIMESTAMP | `java.sql.Timestamp` |
| NUMBER(p,0) | `java.lang.Integer` or `java.lang.Long` |

## Local EC DB Connection
```
Driver: oracle.jdbc.OracleDriver
URL: jdbc:oracle:thin:@localhost:1521/ORCL
User: ECKERNEL_EC  Password: energy
```
