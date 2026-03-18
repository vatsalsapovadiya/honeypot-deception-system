import sqlite3
from datetime import datetime

db = "../database/attacks.db"
conn = sqlite3.connect(db)
c = conn.cursor()

c.execute("""
INSERT INTO ssh_attacks
(timestamp, src_ip, username, password, command)
VALUES (?, ?, ?, ?, ?)
""", (
    datetime.now().isoformat(),
    "192.168.1.100",
    "root",
    "toor",
    "uname -a"
))

conn.commit()
conn.close()

print("[+] Test insert successful")
