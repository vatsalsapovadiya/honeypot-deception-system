
import json
import sqlite3
from datetime import datetime

DB_PATH = "../database/attacks.db"
LOG_PATH = "/home/cowrie/cowrie/var/log/cowrie/cowrie.json"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

processed = 0

with open(LOG_PATH, "r") as logfile:
    for line in logfile:
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue

        event_id = event.get("eventid")
        timestamp = event.get("timestamp")
        src_ip = event.get("src_ip")

        if event_id == "cowrie.login.failed":
            cursor.execute("""
                INSERT INTO ssh_attacks
                (timestamp, src_ip, username, password, command)
                VALUES (?, ?, ?, ?, ?)
            """, (
                timestamp,
                src_ip,
                event.get("username"),
                event.get("password"),
                None
            ))
            processed += 1

        elif event_id == "cowrie.login.success":
            cursor.execute("""
                INSERT INTO ssh_attacks
                (timestamp, src_ip, username, password, command)
                VALUES (?, ?, ?, ?, ?)
            """, (
                timestamp,
                src_ip,
                event.get("username"),
                event.get("password"),
                "LOGIN_SUCCESS"
            ))
            processed += 1

        elif event_id == "cowrie.command.input":
            cursor.execute("""
                INSERT INTO ssh_attacks
                (timestamp, src_ip, username, password, command)
                VALUES (?, ?, ?, ?, ?)
            """, (
                timestamp,
                src_ip,
                event.get("username"),
                None,
                event.get("input")
            ))
            processed += 1

conn.commit()
conn.close()

print(f"[+] Ingested {processed} Cowrie SSH events")
               
