// Compile / fill / export a downgraded JRXML using JasperReports 6.17.0.
//
// The 6.17.0 compiler is the authority on whether the downgrade is valid - it validates against
// the 6.x XSD, so any leftover JR7 construct surfaces here as a concrete SAXParseException
// naming the attribute, rather than as a guess.
//
//   Jr6Build compile <jrxml>                       -> validate only
//   Jr6Build fill    <jrxml> <out.pdf>             -> compile + fill from the local Oracle
import java.sql.Connection;
import java.sql.DriverManager;
import java.util.HashMap;
import java.util.Map;

import net.sf.jasperreports.engine.JasperCompileManager;
import net.sf.jasperreports.engine.JasperExportManager;
import net.sf.jasperreports.engine.JasperFillManager;
import net.sf.jasperreports.engine.JasperPrint;
import net.sf.jasperreports.engine.JasperReport;

public class Jr6Build {
    public static void main(String[] args) throws Exception {
        String mode = args[0];
        String jrxml = args[1];

        System.out.println("JasperReports on classpath: "
                + net.sf.jasperreports.engine.JRPropertiesUtil.class
                    .getPackage().getImplementationVersion());

        JasperReport report;
        try {
            report = JasperCompileManager.compileReport(jrxml);
            System.out.println("COMPILE OK: " + report.getName());
        } catch (Throwable t) {
            System.out.println("COMPILE FAILED");
            System.out.println("  " + t.getClass().getName());
            String m = t.getMessage();
            if (m != null) {
                for (String line : m.split("\n")) {
                    System.out.println("  " + line);
                }
            }
            System.exit(1);
            return;
        }

        if ("jasper".equals(mode)) {
            // Produce the deployable artifact, so it can be tested against EC's legacy 6.21.4
            // engine - a 6.17 build is only useful if 6.21.4 can actually deserialise it.
            JasperCompileManager.compileReportToFile(jrxml, args[2]);
            System.out.println("JASPER WRITTEN: " + args[2]);
            return;
        }

        if ("fillempty".equals(mode)) {
            // Layout-only reports (R07.001-006) have no <query>; their 7.x PDFs were produced
            // with JREmptyDataSource(N). Match N exactly or the page count differs and the
            // comparison is meaningless.
            int n = Integer.parseInt(args[3]);
            Map<String, Object> p = new HashMap<>();
            p.put("P_BASE_URL", "");
            JasperPrint print = JasperFillManager.fillReport(
                    report, p, new net.sf.jasperreports.engine.JREmptyDataSource(n));
            System.out.println("FILL OK (JREmptyDataSource(" + n + ")): "
                    + print.getPages().size() + " page(s)");
            JasperExportManager.exportReportToPdfFile(print, args[2]);
            System.out.println("EXPORT OK: " + args[2]);
            return;
        }

        if (!"fill".equals(mode)) {
            return;
        }

        // P_BASE_URL is overridden to "" for the local run: the report's default targets EC's
        // extension path (/extension/ZREP/reports/), which does not exist off-server.
        Map<String, Object> params = new HashMap<>();
        params.put("P_BASE_URL", "");

        Class.forName("oracle.jdbc.OracleDriver");
        try (Connection conn = DriverManager.getConnection(
                "jdbc:oracle:thin:@localhost:1521/ORCL", "ECKERNEL_EC", "energy")) {
            JasperPrint print = JasperFillManager.fillReport(report, params, conn);
            System.out.println("FILL OK: " + print.getPages().size() + " page(s)");
            JasperExportManager.exportReportToPdfFile(print, args[2]);
            System.out.println("EXPORT OK: " + args[2]);
        }
    }
}
