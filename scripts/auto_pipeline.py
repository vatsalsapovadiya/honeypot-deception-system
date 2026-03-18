import json
import sqlite3
import time

LOG_FILE = "/home/cowrie/cowrie/var/log/cowrie/cowrie.json"
DB = "../database/attacks.db"

# Track last read position
last_position = 0

def insert_attack(data):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    try:
        c.execute("""
            INSERT INTO attack_events 
            (timestamp, src_ip, attack_vector, username, password, command, endpoint, severity)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, data)
        conn.commit()
    except Exception as e:
        print("DB Error:", e)

    conn.close()


def process_log(line):
    try:
        log = json.loads(line)

        # SSH Login Attempt
        if log.get("eventid") == "cowrie.login.failed":
            return (
                log.get("timestamp"),
                log.get("src_ip"),
                "SSH",
                log.get("username"),
                log.get("password"),
                "login attempt",
                "ssh-login",
                5
            )

        # SSH Command Execution
        elif log.get("eventid") == "cowrie.command.input":
            return (
                log.get("timestamp"),
                log.get("src_ip"),
                "SSH",
                "",
                "",
                log.get("input"),
                "ssh-command",
                3
            )

    except:
        return None


def monitor_logs():
    global last_position

    print("🚀 Auto Pipeline Started...")

    while True:
        with open(LOG_FILE, "r") as f:
            f.seek(last_position)
            lines = f.readlines()
            last_position = f.tell()

        for line in lines:
            data = process_log(line)
            if data:
                insert_attack(data)
                print("✅ Inserted:", data)

        time.sleep(2)


if __name__ == "__main__":
    monitor_logs()
