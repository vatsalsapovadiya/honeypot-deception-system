from flask import Flask, jsonify, render_template, request, redirect, session, Response, send_file
import sqlite3
import os

app = Flask(__name__)

# 🔐 Secret key
app.secret_key = "supersecretkey"

# ✅ Absolute DB path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, "../database/attacks.db")

# 🔐 Login credentials
USERNAME = "maverick"
PASSWORD = "Vatsal"


# -----------------------------
# Helper DB function
# -----------------------------
def query_db(sql):
    try:
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        data = c.execute(sql).fetchall()
        conn.close()
        return data
    except Exception as e:
        print("DB Error:", e)
        return []


# -----------------------------
# Auth helpers
# -----------------------------
def is_logged_in():
    return session.get("logged_in")

def protect_api():
    return jsonify({"error": "Unauthorized"}), 401


# -----------------------------
# Login system
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username")
        pwd = request.form.get("password")

        if user == USERNAME and pwd == PASSWORD:
            session["logged_in"] = True
            return redirect("/")
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/")
def index():
    if not is_logged_in():
        return redirect("/login")
    return render_template("dashboard.html")


# -----------------------------
# APIs
# -----------------------------
@app.route("/api/attack_counts")
def attack_counts():
    if not is_logged_in(): return protect_api()

    data = query_db("""
        SELECT attack_vector, COUNT(*)
        FROM attack_events
        GROUP BY attack_vector
    """)

    result = {"SSH": 0, "WEB": 0}
    for row in data:
        result[row[0]] = row[1]

    return jsonify(result)


@app.route("/api/top_ips")
def top_ips():
    if not is_logged_in(): return protect_api()

    data = query_db("""
        SELECT src_ip, COUNT(*)
        FROM attack_events
        GROUP BY src_ip
        ORDER BY COUNT(*) DESC
        LIMIT 5
    """)

    return jsonify([{"ip": row[0], "count": row[1]} for row in data])


@app.route("/api/timeline")
def timeline():
    if not is_logged_in(): return protect_api()

    data = query_db("""
        SELECT substr(timestamp, 1, 10), COUNT(*)
        FROM attack_events
        GROUP BY 1
        ORDER BY 1
    """)

    return jsonify([{"date": row[0], "count": row[1]} for row in data])


@app.route("/api/latest_attacks")
def latest_attacks():
    if not is_logged_in(): return protect_api()

    data = query_db("""
        SELECT timestamp, src_ip, attack_vector, username, endpoint, severity
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
            "endpoint": row[4],
            "severity": row[5] if len(row) > 5 else 1
        } for row in data
    ])


@app.route("/api/alerts")
def alerts():
    if not is_logged_in(): return protect_api()

    data = query_db("""
        SELECT src_ip, COUNT(*), MAX(severity)
        FROM attack_events
        GROUP BY src_ip
        HAVING COUNT(*) >= 3 OR MAX(severity) >= 5
    """)

    return jsonify([
        {"ip": row[0], "count": row[1], "severity": row[2]}
        for row in data
    ])


@app.route("/api/stats")
def stats():
    if not is_logged_in(): return protect_api()

    data = query_db("SELECT COUNT(*) FROM attack_events")
    total = data[0][0] if data else 0

    return jsonify({"total_attacks": total})


# -----------------------------
# 🌍 GEOLOCATION
# -----------------------------
@app.route("/api/geo")
def geo():
    if not is_logged_in(): return protect_api()

    data = query_db("""
        SELECT src_ip, COUNT(*)
        FROM attack_events
        GROUP BY src_ip
    """)

    results = []

    for row in data:
        ip = row[0]
        count = row[1]

        if ip.startswith("127.") or ip == "0.0.0.0":
            continue

        try:
            import requests
            res = requests.get(f"http://ip-api.com/json/{ip}", timeout=2).json()

            if res.get("status") == "success":
                results.append({
                    "ip": ip,
                    "count": count,
                    "lat": res.get("lat"),
                    "lon": res.get("lon"),
                    "country": res.get("country")
                })
        except:
            continue

    return jsonify(results)


# -----------------------------
# 📄 EXPORT CSV
# -----------------------------
@app.route("/api/export/csv")
def export_csv():
    if not is_logged_in(): return protect_api()

    data = query_db("""
        SELECT timestamp, src_ip, attack_vector, username, endpoint, severity
        FROM attack_events
        ORDER BY timestamp DESC
    """)

    def generate():
        yield "Timestamp,IP,Type,Username,Endpoint,Severity\n"
        for row in data:
            yield f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]}\n"

    return Response(generate(),
                    mimetype="text/csv",
                    headers={"Content-Disposition": "attachment;filename=attack_report.csv"})


# -----------------------------
# 📄 EXPORT PDF
# -----------------------------
@app.route("/api/export/pdf")
def export_pdf():
    if not is_logged_in(): return protect_api()

    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
    from reportlab.lib import colors

    file_path = "attack_report.pdf"

    data = query_db("""
        SELECT timestamp, src_ip, attack_vector, username, endpoint, severity
        FROM attack_events
        ORDER BY timestamp DESC
    """)

    pdf = SimpleDocTemplate(file_path)

    table_data = [["Time", "IP", "Type", "User", "Endpoint", "Severity"]]

    for row in data:
        table_data.append(list(map(str, row)))

    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('GRID',(0,0),(-1,-1),1,colors.black)
    ]))

    pdf.build([table])

    return send_file(file_path, as_attachment=True)


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    print("🔐 Login: http://127.0.0.1:5000/login")
    app.run(host="0.0.0.0", port=5000, debug=True)
