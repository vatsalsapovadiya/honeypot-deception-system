import sqlite3

DB = "../database/attacks.db"
conn = sqlite3.connect(DB)
c = conn.cursor()

# SSH attacks
for row in c.execute("""
    SELECT timestamp, src_ip, username, password, command
    FROM ssh_attacks
"""):
    c.execute("""
        INSERT INTO attack_events
        (timestamp, src_ip, attack_vector, username, password, command, endpoint, severity)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row[0], row[1], "SSH",
        row[2], row[3], row[4],
        None, 3
    ))

# Web attacks
for row in c.execute("""
    SELECT timestamp, src_ip, username, password, endpoint
    FROM web_attacks
"""):
    c.execute("""
        INSERT INTO attack_events
        (timestamp, src_ip, attack_vector, username, password, command, endpoint, severity)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row[0], row[1], "WEB",
        row[2], row[3], None,
        row[4], 2
    ))

conn.commit()
conn.close()

print("[+] Unified attack_events table built")
