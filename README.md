🛡️ Honeypot-Based Cyber Deception System

A SOC-style honeypot and cyber deception system designed for academic research and hands-on cybersecurity learning.
This project captures real attacker behavior using SSH and Web honeypots, normalizes attack telemetry, and provides a near real-time attack monitoring dashboard.

📌 Key Features

🐝 SSH Honeypot (Cowrie) for brute-force & command capture

🌐 Custom Web Honeypot (Flask) for credential harvesting

🧠 Cyber Deception Layer

Honeytoken credentials

Fake admin & IoT panels

📊 SOC-style Dashboard

Live attack counts

Latest attacks table

Real-time brute-force alerting

🔁 Automated Log Ingestion Pipeline

🔒 Fully isolated & ethical environment

🧱 Architecture Overview
Attacker
   ↓
[ SSH / Web Honeypots ]
   ↓
Cowrie Logs + Web Logs
   ↓
SQLite Database
   ↓
Normalization & Analytics
   ↓
Live SOC Dashboard

🛠️ Technologies Used
Component	Technology
OS	Kali Linux
SSH Honeypot	Cowrie
Web Honeypot	Flask (Python)
Database	SQLite
Dashboard	Flask + HTML/CSS/JS
Visualization	Chart.js
Automation	Python
Virtualization	VirtualBox
⚙️ System Requirements

Kali Linux (VM recommended)

Python 3.9+

VirtualBox

4 GB RAM minimum

🚀 Installation & Setup (STEP-BY-STEP)
🔹 Step 1: Clone Repository
git clone https://github.com/<your-username>/honeypot-based-cyber-deception-system.git
cd honeypot-based-cyber-deception-system

🔹 Step 2: Install Cowrie (SSH Honeypot)
sudo adduser cowrie
su - cowrie
git clone https://github.com/cowrie/cowrie.git
cd cowrie
python3 -m venv cowrie-env
source cowrie-env/bin/activate
pip install -r requirements.txt
pip install -e .


Configure Cowrie:

cp etc/cowrie.cfg.dist etc/cowrie.cfg
nano etc/cowrie.cfg


Set:

[ssh]
enabled = true
listen_port = 2222


Start Cowrie:

cowrie start

🔹 Step 3: Setup Database
sqlite3 database/attacks.db < schema.sql   # (or run manually)


Tables:

ssh_attacks

web_attacks

attack_events

🔹 Step 4: Web Honeypot Setup
cd web_honeypot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py


Access:

http://127.0.0.1:8080
http://127.0.0.1:8080/admin
http://127.0.0.1:8080/iot

🔹 Step 5: Dashboard Setup
cd dashboard
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py


Access:

http://127.0.0.1:5000

🔹 Step 6: Automated Ingestion Pipeline
cd scripts
python3 auto_pipeline.py


This automatically:

Ingests Cowrie logs

Builds analytics

Updates dashboard in near real-time

🧪 Attack Simulation
SSH Brute-Force
ssh root@127.0.0.1 -p 2222

Multiple IP Simulation
ssh root@127.0.0.1 -p 2222 -b 127.0.0.2

Nmap Recon
nmap -p 2222 127.0.0.1

📊 Dashboard Capabilities

Live SSH & Web attack counts

Latest attack feed

Brute-force alert banner

Attack rate visualization

Per-IP attack tracking

📸 Screenshots

Screenshots are available in the /screenshots directory:

Live Dashboard

SSH Brute-Force Simulation

Cowrie Logs

Attack Rate Spike

⚖️ Ethics & Legal Compliance

Fully isolated VM environment

No public exposure

No real credentials

Attacks generated on own system only

This project is strictly for educational and research purposes.

🎓 Academic Relevance

This project demonstrates:

Cyber deception techniques

SOC data pipelines

Real-time security monitoring

Attack behavior analysis

Suitable for:

Final-year cybersecurity projects

SOC analyst learning

Blue-team research

📌 Future Enhancements

Geo-IP mapping

Threat scoring

SIEM integration

Cloud deployment

IDS correlation

🧑‍💻 Author

Vatsal Sapovadiya
Cybersecurity Enthusiast | SOC & Blue-Team Focus
