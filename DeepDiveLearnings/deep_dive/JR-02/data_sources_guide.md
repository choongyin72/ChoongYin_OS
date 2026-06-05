# JR-02: Data Sources Guide — JasperReports 7.0.3+

## Overview

JasperReports separates the report design from data retrieval. The engine calls `JasperFillManager.fillReport(dataSource, parameters)` where `dataSource` can be any of the types below. EC uses **JDBC** (Oracle database) as the primary data source.

---

## 1. JDBC Data Source (Primary for EC)

### Configuration in JRXML
```xml
<queryString language="sql">
    <![CDATA[
    SELECT
        o.object_code,
        s.daytime,
        NVL(s.net_oil_vol_sm3, 0) AS net_oil_vol_sm3
    FROM rv_pwel_day_status s
    JOIN object o ON o.object_id = s.object_id
    WHERE TRUNC(s.daytime) = TRUNC($P{P_DAYTIME})
    ORDER BY o.object_code
    ]]>
</queryString>
```

### How JasperReports Iterates JDBC
1. Executes the SQL query against the JDBC connection
2. Creates a `JRResultSetDataSource` wrapping the `ResultSet`
3. Calls `next()` on the ResultSet for each detail band iteration
4. Maps column names to `<field>` declarations by name (case-insensitive in Oracle)

### Parameter Syntax
```xml
<!-- Safe parameterised binding — prevents SQL injection -->
WHERE daytime = $P{P_DAYTIME}
AND object_code = $P{P_OBJECT_CODE}

<!-- Multi-value IN clause — use $X{} for lists -->
WHERE object_code IN ($X{IN, OBJECT_CODE, P_OBJECT_LIST})
<!-- P_OBJECT_LIST must be java.util.Collection -->

<!-- Raw SQL injection — ONLY for ORDER BY or controlled values -->
ORDER BY $P!{P_SORT_COLUMN}
```

### EC-Specific JDBC Setup in Jasper Studio
1. Window → Data Adapters → New → Database JDBC Connection
2. Driver: `oracle.jdbc.OracleDriver`
3. URL: `jdbc:oracle:thin:@db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev`
4. Username: `ECKERNEL_EC`, Password: `energy`
5. Add JAR: `ojdbc17.jar` (from EC Java tools folder)

### Common Errors
| Error | Cause | Resolution |
|---|---|---|
| `ClassNotFoundException: oracle.jdbc.OracleDriver` | ojdbc JAR not in classpath | Add ojdbc17.jar to Jasper Studio project classpath |
| `ORA-00942: table or view does not exist` | Wrong schema or view name | Prefix with schema: `ECKERNEL_EC.rv_pwel_day_status` |
| `Field type mismatch` | Java class doesn't match Oracle type | Check Oracle NUMBER → Double, VARCHAR2 → String, DATE → java.util.Date |

---

## 2. JREmptyDataSource

### When to Use
- Reports that don't need database data (parameter-driven calculations, static content)
- Master reports that only contain subreports
- Testing report layout without a database connection

### JRXML Configuration
```xml
<!-- No queryString needed -->
<!-- No fields needed -->
<!-- In Java: JasperFillManager.fillReport(jasper, params, new JREmptyDataSource()) -->
```

**EC use case:** Cover page reports, summary dashboards that call subreports for each section.

---

## 3. JRBeanCollectionDataSource

### When to Use
- Java application passes a list of objects directly to the report
- REST API integration — deserialise JSON to Java beans, pass to report

### Field Mapping
Fields map to getter methods on the Java bean:
```xml
<field name="objectCode" class="java.lang.String"/>
<!-- Maps to bean.getObjectCode() -->

<field name="netOilVolSm3" class="java.lang.Double"/>
<!-- Maps to bean.getNetOilVolSm3() -->
```

**EC use case:** EC's REST API endpoints could return `List<ProductionDataDTO>` for programmatic report generation without database queries.

---

## 4. JRCsvDataSource

### When to Use
- Import/export files in EC (ECIS file imports, exported data)
- Testing with flat file data without a database

### JRXML Configuration
```xml
<queryString language="csv">
    <![CDATA[objectCode,daytime,netOilVol]]>
</queryString>
<field name="objectCode" class="java.lang.String">
    <!-- Maps to column 0 (index-based) or column name -->
    <fieldDescription><![CDATA[objectCode]]></fieldDescription>
</field>
```

### In Java
```java
JRCsvDataSource ds = new JRCsvDataSource(new File("data.csv"));
ds.setColumnNames(new String[]{"objectCode","daytime","netOilVol"});
ds.setFirstRowAsHeader(true);
JasperFillManager.fillReport(jasper, params, ds);
```

---

## 5. JRJsonDataSource

### When to Use
- REST API responses consumed directly by reports
- EC GraphQL/REST API data piped into reports

### JRXML Configuration
```xml
<queryString language="json">
    <![CDATA[wells]]>
    <!-- Selects the "wells" array from the JSON root -->
</queryString>
<field name="objectCode" class="java.lang.String">
    <fieldDescription><![CDATA[code]]></fieldDescription>
    <!-- Maps to wells[].code in JSON -->
</field>
```

---

## 6. JRXmlDataSource

### When to Use
- XML configuration exports from EC
- Legacy data exchange formats

### JRXML Configuration
```xml
<queryString language="xpath">
    <![CDATA[/wells/well]]>
</queryString>
<field name="objectCode" class="java.lang.String">
    <fieldDescription><![CDATA[code]]></fieldDescription>
</field>
```

---

## `whenNoDataType` Options

| Value | Behaviour |
|---|---|
| `NoPages` | Report generates no pages (default) |
| `BlankPage` | One blank page |
| `AllSectionsNoDetail` | title, pageHeader, pageFooter, summary — no detail |
| `NoData` | Renders the `<noData>` band (**recommended for EC reports**) |

---

## SQL Query Best Practices for EC Reports

```sql
-- Always use NVL/COALESCE for nullable columns
SELECT
    NVL(s.net_oil_vol_sm3, 0)  AS net_oil_vol,

-- Always TRUNC daytime for date comparisons (EC stores with time component)
WHERE TRUNC(s.daytime) = TRUNC($P{P_DAYTIME})

-- Use proper joins — never implicit joins
JOIN object o ON o.object_id = s.object_id

-- Sort in SQL — JasperReports cannot re-sort data
ORDER BY o.object_code, s.daytime

-- For group reports — sort by the group field FIRST
ORDER BY facility_code, object_code
```
