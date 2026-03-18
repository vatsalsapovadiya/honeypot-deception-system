# 🛡️ Honeypot-Based Cyber Deception System

## 📌 Overview

The **Honeypot-Based Cyber Deception System** is a cybersecurity project designed to simulate vulnerable environments and capture real-world attack behavior. It integrates SSH and web-based honeypots with a real-time monitoring dashboard to analyze attacker activities.

This system is built for **educational, research, and demonstration purposes**, showcasing how modern **Security Operations Centers (SOC)** monitor, detect, and analyze cyber threats.

---

## 🚀 Key Features

### 🔍 Honeypot Integration
- SSH honeypot using Cowrie
- Custom web honeypot for login attack simulation
- Captures attacker credentials, commands, and behavior

### 🔄 Automated Data Pipeline
- Real-time log monitoring
- Automatic parsing of Cowrie & web logs
- Continuous insertion into SQLite database

### 📊 Interactive Dashboard
- Real-time attack visualization via WebSockets
- Attack type distribution (SSH vs Web)
- Top attacker IP tracking
- Attack timeline analytics

### 🌍 Geo-Location Tracking
- Maps attacker IPs globally
- Displays attack origins using live geolocation API

### 🚨 Smart Alert System
- Detects brute-force attempts
- Severity-based alert triggering
- Highlights suspicious IP behavior

### 🎯 Threat Severity Classification
- Low, Medium, High threat levels
- Color-coded visualization in dashboard
- Severity-based filtering and alerts

### 🔐 Authentication System
- Secure login for dashboard access
- Session-based authentication
- Protected API endpoints

### 📄 Report Export
- Export attack data as CSV
- Useful for analysis and presentations

---

## 🏗️ System Architecture

```
[ Attacker ]
     ↓
[ SSH Honeypot (Cowrie, port 2222) ]   [ Web Honeypot (Flask, port 8080) ]
     ↓                                        ↓
                  [ Raw Log Files ]
                         ↓
             [ Auto Pipeline Script ]
                         ↓
               [ SQLite Database ]
                         ↓
              [ Flask Backend API ]
                         ↓
       [ Dashboard UI (Charts + Map + Alerts) ]
```

---

## 🛠️ Tech Stack

| Layer         | Technology                |
|---------------|---------------------------|
| OS            | Kali Linux / Ubuntu 20.04+|
| Backend       | Python 3.9+, Flask        |
| Database      | SQLite                    |
| SSH Honeypot  | Cowrie                    |
| Frontend      | HTML, CSS, JavaScript     |
| Visualization | Chart.js                  |
| Real-time     | Flask-SocketIO, Eventlet  |
| Geolocation   | IP Geolocation API        |

---

## 📂 Project Structure

```
honeypot-deception-system/
│
├── cowrie/
│   └── database/            # Cowrie SQLite log database
│
├── dashboard/
│   ├── app.py               # Flask dashboard backend
│   └── templates/
│       ├── dashboard.html
│       └── login.html
│
├── scripts/
│   └── auto_pipeline.py     # Log ingestion & DB pipeline
│
├── requirements.txt         # Python dependencies
├── setup.sh                 # Automated setup script
└── README.md
```

---

## ⚙️ Prerequisites

Before you begin, ensure you have the following:

- **OS:** Kali Linux or Ubuntu 20.04+ (recommended inside VirtualBox)
- **Python:** 3.9 or above
- **RAM:** Minimum 4 GB
- **Internet:** Required for initial setup and geolocation API
- **Git:** Installed (`sudo apt install git`)

---

## 🚀 Complete Installation & Setup Guide

Follow these steps **in order** on a fresh Kali Linux / Ubuntu system.

---

### 🔹 Step 1: Update System & Install System Dependencies

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git python3 python3-pip python3-venv sqlite3 \
    libssl-dev libffi-dev build-essential python3-dev
```

---

### 🔹 Step 2: Clone the Repository

```bash
git clone https://github.com/vatsalsapovadiya/honeypot-deception-system.git
cd honeypot-deception-system
```

> ⚠️ **Note:** All subsequent paths are relative to this project root directory.

---

### 🔹 Step 3: Install & Configure Cowrie (SSH Honeypot)

Cowrie must be run as a **dedicated non-root user** for security.

#### 3a — Create a Cowrie system user

```bash
sudo adduser --disabled-password --gecos "" cowrie
```

#### 3b — Switch to the cowrie user and install Cowrie

```bash
sudo su - cowrie

# Clone Cowrie into the cowrie user's home directory
git clone https://github.com/cowrie/cowrie.git
cd cowrie

# Create and activate a Python virtual environment
python3 -m venv cowrie-env
source cowrie-env/bin/activate

# Install Cowrie's dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install Cowrie itself in editable mode
pip install -e .
```

#### 3c — Configure Cowrie

```bash
# Copy the example config
cp etc/cowrie.cfg.dist etc/cowrie.cfg

# Edit the config
nano etc/cowrie.cfg
```

Find and confirm (or add) the following settings in `etc/cowrie.cfg`:

```ini
[ssh]
enabled = true
listen_port = 2222

[output_jsonlog]
enabled = true
```

Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).

#### 3d — (Optional but recommended) Redirect port 22 → 2222 using iptables

While still as root (exit the cowrie user first: `exit`):

```bash
sudo iptables -t nat -A PREROUTING -p tcp --dport 22 -j REDIRECT --to-port 2222
```

To make this persistent across reboots:

```bash
sudo apt install -y iptables-persistent
sudo netfilter-persistent save
```

#### 3e — Start Cowrie

```bash
# Switch back to the cowrie user
sudo su - cowrie
cd ~/cowrie
source cowrie-env/bin/activate
bin/cowrie start
```

Verify it is running:

```bash
bin/cowrie status
```

You should see: `cowrie is running (PID XXXXX)`.

Cowrie logs are written to:
- `~/cowrie/var/log/cowrie/cowrie.json` (JSON structured log — used by the pipeline)
- `~/cowrie/var/log/cowrie/cowrie.log` (plain text log)

Exit back to your main user when done:

```bash
exit
```

---

### 🔹 Step 4: Set Up the SQLite Database

Navigate back to the project root:

```bash
cd ~/honeypot-deception-system
```

Create the database directory and initialize the database:

```bash
mkdir -p cowrie/database

sqlite3 cowrie/database/attacks.db <<EOF
CREATE TABLE IF NOT EXISTS ssh_attacks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    src_ip TEXT,
    username TEXT,
    password TEXT,
    success INTEGER DEFAULT 0,
    severity TEXT DEFAULT 'Low'
);

CREATE TABLE IF NOT EXISTS web_attacks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    src_ip TEXT,
    method TEXT,
    path TEXT,
    username TEXT,
    password TEXT,
    user_agent TEXT,
    severity TEXT DEFAULT 'Low'
);

CREATE TABLE IF NOT EXISTS attack_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    attack_type TEXT,
    src_ip TEXT,
    details TEXT,
    severity TEXT DEFAULT 'Low'
);
EOF
```

Confirm the database was created:

```bash
sqlite3 cowrie/database/attacks.db ".tables"
# Expected output: attack_events  ssh_attacks  web_attacks
```

---

### 🔹 Step 5: Set Up the Dashboard

#### 5a — Create a virtual environment for the dashboard

```bash
cd dashboard
python3 -m venv venv
source venv/bin/activate
```

#### 5b — Install Python dependencies

```bash
pip install --upgrade pip
pip install -r ../requirements.txt
```

The `requirements.txt` installs:
- `Flask==3.0.0`
- `flask-socketio==5.3.5`
- `python-socketio==5.10.0`
- `eventlet==0.33.3`
- `requests==2.31.0`

#### 5c — Verify the database path in `app.py`

Open `app.py` and confirm the database path matches your setup:

```bash
nano app.py
```

Look for a line like:

```python
DB = '../cowrie/database/attacks.db'
```

If it differs (e.g., `'../database/attacks.db'`), update it to point to where you created the DB in Step 4.

#### 5d — Run the dashboard

```bash
python3 app.py
```

You should see:

```
 * Running on http://127.0.0.1:5000
 * WebSocket support: eventlet
```

---

### 🔹 Step 6: Run the Auto Pipeline Script

Open a **new terminal tab/window**, navigate to the project root, and run:

```bash
cd ~/honeypot-deception-system/scripts
python3 auto_pipeline.py
```

This script continuously:
- Reads Cowrie's JSON logs from `~/cowrie/var/log/cowrie/cowrie.json`
- Parses and inserts SSH attack events into the SQLite database
- Feeds data to the dashboard in near real-time

> ⚠️ Keep this running in the background while the dashboard is active.

---

### 🔹 Step 7: (Alternative) Use the Setup Script

If you prefer, you can run the included `setup.sh` from the project root to automate dependency installation and directory structure setup:

```bash
chmod +x setup.sh
bash setup.sh
```

> Note: `setup.sh` handles pip installation and directory scaffolding. You still need to complete Steps 3 (Cowrie) and 4 (DB initialization) manually.

---

## 🌐 Access the Dashboard

Once the dashboard is running, open your browser and go to:

```
http://127.0.0.1:5000/login
```

### 🔑 Default Login Credentials

| Field    | Value      |
|----------|------------|
| Username | `admin`    |
| Password | `admin123` |

> ⚠️ Change these credentials before deploying in any shared environment.

---

## 🧪 Testing & Attack Simulation

### SSH Brute-Force Simulation

From a terminal (or another machine on the same network):

```bash
ssh root@127.0.0.1 -p 2222
```

Try multiple failed login attempts to trigger brute-force detection.

### Simulate Multiple Attacker IPs

```bash
ssh root@127.0.0.1 -p 2222 -b 127.0.0.2
ssh root@127.0.0.1 -p 2222 -b 127.0.0.3
```

### Nmap Port Scan

```bash
nmap -p 2222 127.0.0.1
```

### Insert Test Data Directly into DB

```bash
sqlite3 cowrie/database/attacks.db \
  "INSERT INTO ssh_attacks (timestamp, src_ip, username, password, severity) \
   VALUES (datetime('now'), '192.168.1.99', 'root', 'password123', 'High');"
```

---

## 📊 Dashboard Features

| Feature                  | Description                                  |
|--------------------------|----------------------------------------------|
| 📈 Real-time charts       | Live SSH and Web attack counters             |
| 🌍 Global attack map      | Geo-mapped attacker IPs                      |
| 🚨 Alert banner           | SSH brute-force detection alerts             |
| 📋 Attack logs table      | Live log of all captured events              |
| 📁 Export CSV             | Download attack data as CSV                  |

---

## ▶️ Running Order Summary

Use this as a quick-reference checklist every time you start the system:

```
Terminal 1 — Start Cowrie:
    sudo su - cowrie
    cd ~/cowrie && source cowrie-env/bin/activate
    bin/cowrie start

Terminal 2 — Start Auto Pipeline:
    cd ~/honeypot-deception-system/scripts
    python3 auto_pipeline.py

Terminal 3 — Start Dashboard:
    cd ~/honeypot-deception-system/dashboard
    source venv/bin/activate
    python3 app.py

Browser — Open Dashboard:
    http://127.0.0.1:5000/login
```

---

## 🛑 Stopping the System

```bash
# Stop Cowrie
sudo su - cowrie -c "cd ~/cowrie && source cowrie-env/bin/activate && bin/cowrie stop"

# Stop auto_pipeline.py and app.py
# Press Ctrl+C in their respective terminals
```

---

## 🔧 Troubleshooting

| Issue | Fix |
|---|---|
| `Address already in use` on port 5000 | Run `fuser -k 5000/tcp` then restart |
| Cowrie won't start | Check `~/cowrie/var/log/cowrie/cowrie.log` for errors |
| Dashboard shows no data | Ensure `auto_pipeline.py` is running and DB path in `app.py` is correct |
| `ModuleNotFoundError` | Activate the correct `venv` before running any script |
| Permission denied on port 22 | Cowrie uses port 2222; use iptables redirect (Step 3d) |
| DB not found error | Confirm DB was created in Step 4 and path matches `app.py` |

---

## 🎓 Use Cases

- Cybersecurity education & lab demonstrations
- Ethical hacking and SOC workflow simulation
- Threat intelligence research

---

## ⚠️ Disclaimer

This project is intended for **educational and research purposes only**.

- ✅ Use only in an isolated virtual environment
- ✅ Do not connect to public or production networks
- ❌ Do not target systems you do not own or have explicit permission to test

Unauthorized access to computer systems is **illegal**.

---

## 👤 Author

**Vatsal Sapovadiya**  
Cybersecurity Enthusiast | Blue-Team & SOC Focus | SOC Practitioner

- GitHub: [@vatsalsapovadiya](https://github.com/vatsalsapovadiya)
- Email: [vatsalsapovadiya22@gmail.com](mailto:vatsalsapovadiya22@gmail.com)
- LinkedIn: [Vatsal Sapovadiya](https://www.linkedin.com/in/vatsalsapovadiya)

---

## ⭐ Future Enhancements

- Machine Learning-based anomaly detection
- Email/SMS alert integration
- Role-based authentication
- Cloud deployment (AWS/Azure)
- SIEM integration
- Advanced analytics dashboard

---

## 📜 License

MIT License — For educational and academic use only.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!  
Feel free to check the [issues page](https://github.com/vatsalsapovadiya/honeypot-deception-system/issues).

---

## ⭐ Show Your Support

Give a ⭐ if this project helped you learn about honeypots and cyber deception!
