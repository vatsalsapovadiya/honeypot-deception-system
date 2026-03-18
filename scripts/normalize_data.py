import sqlite3
from datetime import datetime

DB = "../database/attacks.db"

def normalize(table):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    rows = c.execute(f"SELECT id, timestamp FROM {table}").fetchall()

    for row_id, ts in rows:
        try:
            dt = datetime.fromisoformat(ts.replace("Z",""))
            new_ts = dt.strftime("%Y-%m-%d %H:%M:%S")
            c.execute(
                f"UPDATE {table} SET timestamp=? WHERE id=?",
                (new_ts, row_id)
            )
        except Exception:
            pass

    conn.commit()
    conn.close()

normalize("ssh_attacks")
normalize("web_attacks")

print("[+] Timestamp normalization completed")
