# JR-02: Expression Language Deep Dive — JasperReports 7.0.3+

## Expression Language Overview

All JasperReports expressions are **Java expressions** inside `<![CDATA[...]]>` blocks. They must return the correct Java type for the element they are used in.

```
$F{fieldName}     — field value (from data source row)
$P{paramName}     — parameter value (passed at runtime)
$V{varName}       — variable value (calculated by engine)
```

---

## Expression Locations

| Element | Expression tag | Expected return type |
|---|---|---|
| `<textField>` | `<textFieldExpression>` | `java.lang.String` (or any — auto-converted) |
| `<image>` | `<imageExpression>` | `java.lang.String` (file path or URL) |
| `<variable>` | `<variableExpression>` | Same as variable's `class` |
| `<variable>` | `<initialValueExpression>` | Same as variable's `class` |
| `<parameter>` | `<defaultValueExpression>` | Same as parameter's `class` |
| `<group>` | `<groupExpression>` | Any comparable type (usually String) |
| `<reportElement>` | `<printWhenExpression>` | `java.lang.Boolean` |
| `<conditionalStyle>` | `<conditionExpression>` | `java.lang.Boolean` |

---

## 15+ Practical Expression Examples

### 1. Simple Field Output
```xml
<![CDATA[$F{OBJECT_CODE}]]>
```

### 2. Null-Safe String Field
```xml
<![CDATA[$F{OBJECT_CODE} != null ? $F{OBJECT_CODE} : "N/A"]]>
```

### 3. Null-Safe via Objects.toString()
```xml
<![CDATA[java.util.Objects.toString($F{OBJECT_CODE}, "")]]>
```

### 4. Number Formatting — 3 Decimal Places
```xml
<![CDATA[$F{NET_OIL_VOL_SM3} != null ?
    new java.text.DecimalFormat("#,##0.000").format($F{NET_OIL_VOL_SM3}) :
    "0.000"]]>
```

### 5. Number Formatting — Integer with Thousands Separator
```xml
<![CDATA[$F{RECORD_COUNT} != null ?
    new java.text.DecimalFormat("#,##0").format($F{RECORD_COUNT}) :
    "0"]]>
```

### 6. Date Formatting — Oracle Date Field
```xml
<![CDATA[$F{DAYTIME} != null ?
    new java.text.SimpleDateFormat("dd-MMM-yyyy").format($F{DAYTIME}) :
    ""]]>
```

### 7. Date Formatting — With Time
```xml
<![CDATA[$F{DAYTIME} != null ?
    new java.text.SimpleDateFormat("dd-MMM-yyyy HH:mm").format($F{DAYTIME}) :
    ""]]>
```

### 8. String Concatenation
```xml
<![CDATA[$F{OBJECT_CODE} + " — " + ($F{OBJECT_NAME} != null ? $F{OBJECT_NAME} : "")]]>
```

### 9. Conditional Label (Status Code → Human-Readable)
```xml
<![CDATA[$F{RECORD_STATUS} != null ?
    ($F{RECORD_STATUS}.equals("P") ? "Provisional" :
    ($F{RECORD_STATUS}.equals("V") ? "Verified" :
    ($F{RECORD_STATUS}.equals("A") ? "Approved" : $F{RECORD_STATUS}))) :
    "Unknown"]]>
```

### 10. Percentage Calculation with Division-by-Zero Protection
```xml
<![CDATA[($F{TOTAL_PROD} != null && $F{TOTAL_PROD} != 0.0) ?
    new java.text.DecimalFormat("##0.0").format(
        $F{WELL_PROD} / $F{TOTAL_PROD} * 100) + "%" :
    "0.0%"]]>
```

### 11. Running Total Variable in Expression
```xml
<!-- In the detail band — shows running total at this row -->
<![CDATA[$V{RUNNING_OIL_TOTAL} != null ?
    new java.text.DecimalFormat("#,##0.000").format($V{RUNNING_OIL_TOTAL}) :
    "0.000"]]>
```

### 12. Page Number Footer
```xml
<![CDATA["Page " + $V{PAGE_NUMBER} + " of " + $V{PAGE_COUNT}]]>
```

### 13. Combined Parameter + Field
```xml
<![CDATA["Production for " + $F{OBJECT_CODE} +
    " on " + new java.text.SimpleDateFormat("dd-MMM-yyyy").format($P{P_DAYTIME})]]>
```

### 14. printWhenExpression — Conditional Element Visibility
```xml
<printWhenExpression>
    <![CDATA[$F{NET_OIL_VOL_SM3} != null && $F{NET_OIL_VOL_SM3} > 0]]>
</printWhenExpression>
```

### 15. String Truncation with Ellipsis
```xml
<![CDATA[$F{OBJECT_NAME} != null ?
    ($F{OBJECT_NAME}.length() > 30 ?
        $F{OBJECT_NAME}.substring(0, 30) + "…" :
        $F{OBJECT_NAME}) :
    ""]]>
```

### 16. Upper/Lower Case
```xml
<![CDATA[$F{STATUS_CODE} != null ? $F{STATUS_CODE}.toUpperCase() : ""]]>
```

### 17. Boolean Flag Display
```xml
<![CDATA[Boolean.TRUE.equals($F{IS_ACTIVE}) ? "Active" : "Inactive"]]>
```

---

## Null-Safety Reference Table

| Scenario | Safe Pattern |
|---|---|
| String field | `$F{f} != null ? $F{f} : ""` |
| Number field | `$F{f} != null ? $F{f} : 0.0` |
| Number + format | `$F{f} != null ? new DecimalFormat("...").format($F{f}) : "0.000"` |
| Date field | `$F{f} != null ? new SimpleDateFormat("...").format($F{f}) : ""` |
| Null-safe join | `java.util.Objects.toString($F{f}, "")` |
| Division | `$F{denom} != null && $F{denom} != 0.0 ? $F{num}/$F{denom} : 0.0` |

---

## Variable Calculation Types

| Calculation | What it computes |
|---|---|
| `Nothing` | No calculation — use with `System` for manual control |
| `Count` | Count of non-null values |
| `DistinctCount` | Count of distinct non-null values |
| `Sum` | Sum of values |
| `Average` | Arithmetic mean |
| `Lowest` | Minimum value |
| `Highest` | Maximum value |
| `StandardDeviation` | Statistical SD |
| `Variance` | Statistical variance |
| `First` | First value encountered |
| `System` | Manually managed — expression evaluated each row |

---

## Variable resetType and incrementType

| Value | Resets/increments when |
|---|---|
| `Report` | Once per report (grand total) |
| `Page` | Each new page |
| `Column` | Each new column |
| `Group` | Group expression changes |
| `None` | Never resets (running total across entire report) |

---

## Group Declaration

```xml
<!-- Sort the SQL query by this field first! -->
<group name="FACILITY_GROUP" isStartNewPage="false" isResetPageNumber="false">
    <groupExpression><![CDATA[$F{FACILITY_CODE}]]></groupExpression>

    <groupHeader>
        <band height="18">
            <!-- Facility header row -->
            <textField>
                <reportElement x="0" y="2" width="300" height="14"/>
                <textElement><font isBold="true" pdfFontName="Helvetica-Bold" isPdfEmbedded="false"/></textElement>
                <textFieldExpression>
                    <![CDATA["Facility: " + ($F{FACILITY_CODE} != null ? $F{FACILITY_CODE} : "")]]>
                </textFieldExpression>
            </textField>
        </band>
    </groupHeader>

    <groupFooter>
        <band height="18">
            <!-- Group subtotal -->
            <textField>
                <reportElement x="250" y="2" width="100" height="14"/>
                <textElement textAlignment="Right">
                    <font isBold="true" pdfFontName="Helvetica-Bold" isPdfEmbedded="false"/>
                </textElement>
                <textFieldExpression>
                    <![CDATA[$V{FACILITY_OIL_SUBTOTAL} != null ?
                        new java.text.DecimalFormat("#,##0.000").format($V{FACILITY_OIL_SUBTOTAL}) :
                        "0.000"]]>
                </textFieldExpression>
            </textField>
        </band>
    </groupFooter>
</group>

<!-- Matching variable for group subtotal -->
<variable name="FACILITY_OIL_SUBTOTAL" class="java.lang.Double"
          calculation="Sum" resetType="Group" resetGroup="FACILITY_GROUP">
    <variableExpression><![CDATA[$F{NET_OIL_VOL_SM3}]]></variableExpression>
    <initialValueExpression><![CDATA[0.0]]></initialValueExpression>
</variable>
```

**Critical rule:** Data MUST be sorted by the group expression field in the SQL query. JasperReports does not sort data — it only detects when the group expression value changes.
