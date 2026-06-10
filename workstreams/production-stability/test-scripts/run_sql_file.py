"""Run an EC .sql file (anonymous PL/SQL block + trailing verify SELECTs) against COPS DEV.
Splits on a line containing only '/'. First chunk = PL/SQL block (executed as one stmt,
the block COMMITs itself). Remaining chunks: strip -- comments, split on ';', run SELECTs
and print rows. Read-only for SELECTs; the block's own COMMIT persists writes.
Usage: py run_sql_file.py <path-to-sql>
"""
import sys, re
import oracledb

def run(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    # split into chunks on a line that is just "/"
    chunks = re.split(r'(?m)^\s*/\s*$', text)
    conn = oracledb.connect(user='ECKERNEL_EC', password='energy',
        dsn=oracledb.makedsn('db.plutodev.woodside-pluto.tieto-og.cloud',1521,service_name='plutodev'),
        tcp_connect_timeout=25)
    cur = conn.cursor()
    print(f"=== RUN {path} ===")
    for ci, chunk in enumerate(chunks):
        # strip full-line comments
        lines = [ln for ln in chunk.splitlines() if not ln.strip().startswith('--')]
        body = '\n'.join(lines).strip()
        if not body:
            continue
        if body.upper().startswith('DECLARE') or body.upper().startswith('BEGIN'):
            print("  -> executing PL/SQL block ...")
            cur.execute(body)
            print("     OK (block ran; COMMIT inside).")
        else:
            # one or more SQL statements separated by ;
            for stmt in body.split(';'):
                s = stmt.strip()
                if not s:
                    continue
                if s.upper().startswith('SELECT'):
                    print("  -> verify SELECT:")
                    cur.execute(s)
                    cols = [d[0] for d in cur.description]
                    rows = cur.fetchall()
                    print("     ", cols)
                    if not rows:
                        print("      (0 rows)")
                    for r in rows:
                        print("      ", r)
                else:
                    cur.execute(s)
                    print(f"  -> ran: {s[:60]}...")
    cur.close(); conn.close()
    print("=== DONE ===\n")

if __name__ == '__main__':
    run(sys.argv[1])
