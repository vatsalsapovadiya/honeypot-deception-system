from flask import Flask, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Database path (relative to dashboard folder)
DB = "../database/attacks.db"


# -----------------------------
# Helper function (read-only)
# -----------------------------
def query_db(sql):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    data = c.execute(sql).fetchall()
    conn.close()
    return data


# -----------------------------
# Main Dashboard Page
# -----------------------------
@app.route("/")
def index():
    return render_template("dashboard.html")


# -----------------------------
# API: Attack Counts (SSH vs WEB)
# -----------------------------
@app.route("/api/attack_counts")
def attack_counts():
    data = query_db("""
        SELECT attack_vector, COUNT(*)
        FROM attack_events
        GROUP BY attack_vector
    """)
    return jsonify({row[0]: row[1] for row in data})

# -----------------------------
# API: Top Attacker IPs
# -----------------------------
@app.route("/api/top_ips")
def top_ips():
    data = query_db("""
        SELECT src_ip, COUNT(*)
        FROM attack_events
        GROUP BY src_ip
        ORDER BY COUNT(*) DESC
        LIMIT 5
    """)
    return jsonify([{"ip": row[0], "count": row[1]} for row in data])

# -----------------------------
# API: Attack Timeline (per day)
# -----------------------------
@app.route("/api/timeline")
def timeline():
    data = query_db("""
        SELECT substr(timestamp, 1, 10), COUNT(*)
        FROM attack_events
        GROUP BY 1
        ORDER BY 1
    """)
    return jsonify([{"date": row[0], "count": row[1]} for row in data])

# -----------------------------
# API: Latest Attacks (LIVE)
# -----------------------------
@app.route("/api/latest_attacks")
def latest_attacks():
    data = query_db("""
        SELECT timestamp, src_ip, attack_vector, username, endpoint
        FROM attack_events
        ORDER BY id DESC
        LIMIT 5
    """)
    return jsonify([
        {
            "time": row[0],
            "ip": row[1],
            "type": row[2],
            "user": row[3],
            "endpoint": row[4]
        } for row in data
    ])


# -----------------------------
# API: Alerts (SSH brute-force)
# -----------------------------
@app.route("/api/alerts")
def alerts():
    data = query_db("""
        SELECT src_ip, COUNT(*)
        FROM attack_events
        WHERE attack_vector = 'SSH'
        GROUP BY src_ip
        HAVING COUNT(*) >= 3
    """)
    return jsonify([{"ip": row[0], "count": row[1]} for row in data])

# -----------------------------
# Run the Dashboard
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


