"""READ-ONLY recon of the MHM distribution model in the sandbox DB. Goal: understand DISTRIBUTION_SET +
its contacts/recipients, and find whether ANY distribution already resolves only to non-deliverable /
internal addresses (which would let the N-notify live send run safely with no config write at all).
NO writes. Creds via env (EC_DB_PWD), default 'energy'."""
import os
import oracledb

# Same connection contract as DbVerify.py (sandbox reached via localhost tunnel).
USER = os.environ.get("EC_DB_USER", "ECKERNEL_EC")
PWD = os.environ.get("EC_DB_PASS", "energy")
DSN = os.environ.get("EC_DB_DSN", "localhost:1521/ORCL")


def connect():
    c = oracledb.connect(user=USER, password=PWD, dsn=DSN, tcp_connect_timeout=15)
    print(f"CONNECTED via {DSN}")
    return c


def main():
    con = connect()
    cur = con.cursor()

    def show(title, sql, binds=None):
        print(f"\n=== {title} ===")
        try:
            cur.execute(sql, binds or {})
            cols = [d[0] for d in cur.description]
            print(" | ".join(cols))
            for r in cur.fetchall()[:40]:
                print(" | ".join("" if v is None else str(v)[:34] for v in r))
        except Exception as e:
            print("ERR:", str(e)[:160])

    # 1) distribution set master
    show("DISTRIBUTION_SET cols", """
        SELECT column_name, data_type FROM all_tab_columns
        WHERE table_name='DISTRIBUTION_SET' ORDER BY column_id""")
    show("DISTRIBUTION_SET rows", """
        SELECT * FROM DISTRIBUTION_SET WHERE ROWNUM<=20""")

    # 2) any contact / recipient child tables referencing distribution
    show("candidate contact tables", """
        SELECT table_name FROM all_tables
        WHERE (table_name LIKE '%DISTRIBUTION%' OR table_name LIKE '%CONTACT%'
               OR table_name LIKE '%RECIPIENT%' OR table_name LIKE 'MHM%')
        ORDER BY table_name""")

    con.close()
    print("\nDONE")


if __name__ == "__main__":
    main()
