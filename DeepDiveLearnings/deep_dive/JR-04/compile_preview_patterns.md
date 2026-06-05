# JasperReports — Compile & Preview Patterns

## Jasper Studio 7.0.3 — Workflow

### Step 1: Configure Local EC Data Adapter
1. Window → Preferences → Jaspersoft Studio → Data Adapters → Add
2. Type: Database JDBC Connection
3. Name: `LocalEC`
4. Driver: `oracle.jdbc.OracleDriver`
5. URL: `jdbc:oracle:thin:@localhost:1521/ORCL`
6. Username: `ECKERNEL_EC`, Password: `energy`
7. Add JAR: `C:\Tools\java\zulu21.36.17-ca-jdk21.0.4-win_x64\lib\ojdbc17.jar`
8. Test Connection → should show "Connection successful"

### Step 2: Preview Report
1. Open `.jrxml` in Jasper Studio
2. Switch to Preview tab
3. Select data adapter: `LocalEC`
4. Fill in parameter values (P_DAYTIME, P_FACILITY_CODE, etc.)
5. Click Run Report

### Step 3: Export to PDF / Excel
- Right-click in Preview → Export as PDF / Excel

---

## Command-Line Compilation (Maven)

EC extensions use Maven to compile JRXML files as part of the build:

```xml
<!-- In pom.xml — JasperReports Maven plugin -->
<plugin>
    <groupId>com.alexnederlof</groupId>
    <artifactId>jasperreports-plugin</artifactId>
    <version>2.9</version>
    <executions>
        <execution>
            <phase>process-sources</phase>
            <goals><goal>jasper</goal></goals>
        </execution>
    </executions>
    <configuration>
        <sourceDirectory>src/main/resources/reports</sourceDirectory>
        <outputDirectory>${project.build.directory}/reports</outputDirectory>
        <compiler>net.sf.jasperreports.engine.design.JRJdtCompiler</compiler>
    </configuration>
</plugin>
```

```bash
# Compile all JRXML in extension
mvn process-sources

# Output: target/reports/*.jasper
```

---

## VS Code tasks.json — Compile on Save

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Compile JRXML",
            "type": "shell",
            "command": "mvn process-sources -pl extensions/ZWP_Reports",
            "group": "build",
            "presentation": {
                "reveal": "always",
                "panel": "shared"
            },
            "problemMatcher": []
        }
    ]
}
```
