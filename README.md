# 🛡️ Honeypot-Based Cyber Deception System

A **SOC-style Honeypot and Cyber Deception System** designed for academic, research, and blue-team learning purposes.  
This project captures **real attacker behavior** using SSH and Web honeypots, applies **deception techniques**, and visualizes attacks through a **near real-time security dashboard**.

---

## 📌 Abstract

This project presents a GUI-based **Honeypot-Based Cyber Deception System** designed for academic and final-year use.  
The system integrates an SSH honeypot (Cowrie) and a custom Python-Flask web honeypot to capture, analyze, and visualize attacker behavior in a controlled environment.  

A real-time dashboard provides insights such as attack counts, latest attack activity, and brute-force detection alerts.  
The project emphasizes **ethical isolation**, **ease of deployment**, and **originality** through deception techniques such as honeytokens and simulated web/IoT interfaces.  

All tools used are **free and open-source**, making the system cost-effective, reproducible, and suitable for cybersecurity education and research. :contentReference[oaicite:1]{index=1}

---

## 🎯 Problem Statement

Traditional security systems often fail to detect **early-stage attacks** and provide limited visibility into **attacker behavior**.  
There is a need for a **low-cost, practical system** that can safely attract attackers, log their activities, and help students understand real-world cyber threats without exposing real infrastructure. :contentReference[oaicite:2]{index=2}

---

## 🎯 Objectives

- Design an easy-to-deploy honeypot-based deception system  
- Capture SSH and Web-based attacker interactions securely  
- Provide a GUI-based dashboard for attack visualization  
- Implement deception techniques using fake services and credentials  
- Ensure ethical and legal compliance  
- Use only free and open-source technologies  

:contentReference[oaicite:3]{index=3}

---

## 🧱 System Architecture

Attacker
↓
SSH / Web Honeypots
↓
Honeypot Logs (Cowrie + Flask)
↓
SQLite Database
↓
Normalization & Analytics Layer
↓
SOC-style Dashboard (Real-Time)


---

## 🛠️ Tools & Technologies

| Category | Tools |
|------|------|
| Operating System | Kali Linux |
| SSH Honeypot | Cowrie |
| Web Honeypot | Flask (Python) |
| Database | SQLite |
| Dashboard | Flask, HTML, CSS, JavaScript |
| Visualization | Chart.js |
| Automation | Python |
| Virtualization | VirtualBox |

:contentReference[oaicite:4]{index=4}

---

## 📂 Project Structure

honeypot-based-cyber-deception-system/
│
├── database/
│ └── attacks.db
│
├── scripts/
│ ├── cowrie_ingest.py
│ ├── build_attack_events.py
│ ├── auto_pipeline.py
│ └── ssh_bruteforce_sim.py
│
├── web_honeypot/
│ ├── app.py
│ ├── requirements.txt
│ └── templates/
│ ├── login.html
│ ├── admin.html
│ └── iot.html
│
├── dashboard/
│ ├── app.py
│ ├── requirements.txt
│ └── templates/
│ └── dashboard.html
│
├── screenshots/
│ ├── dashboard_live.png
│ ├── ssh_bruteforce.png
│ └── cowrie_logs.png
│
└── README.md


---

## ⚙️ Installation & Setup (Step-by-Step)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/honeypot-based-cyber-deception-system.git
cd honeypot-based-cyber-deception-system
2️⃣ Install and Configure Cowrie (SSH Honeypot)
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
3️⃣ Setup Web Honeypot
cd web_honeypot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
Access:

http://127.0.0.1:8080
http://127.0.0.1:8080/admin
http://127.0.0.1:8080/iot
4️⃣ Setup Dashboard
cd dashboard
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
Access:

http://127.0.0.1:5000
5️⃣ Start Automated Ingestion Pipeline
cd scripts
python3 auto_pipeline.py
This automatically:

Ingests Cowrie logs

Normalizes attack data

Updates the dashboard in near real-time

🧪 Attack Simulation
SSH Brute-Force
ssh root@127.0.0.1 -p 2222
Simulate Multiple Source IPs
ssh root@127.0.0.1 -p 2222 -b 127.0.0.2
Nmap Reconnaissance
nmap -p 2222 127.0.0.1
📊 Dashboard Features
Live SSH and Web attack counts

Latest attack feed (real-time)

SSH brute-force alert banner

Attack rate visualization

Per-IP attacker tracking

📸 Screenshots
Screenshots demonstrating system functionality are available in the screenshots/ directory:

Live Dashboard View

SSH Brute-Force Detection

Cowrie Logs

Attack Rate Spike

⚖️ Ethical & Legal Considerations
Fully isolated virtual environment

No public exposure

No real credentials used

Attacks performed only on owned infrastructure

This project is intended strictly for educational and research purposes. 
Honeypot_Project_Final_Def


🎓 Academic & Practical Relevance
This project demonstrates:

Honeypot deployment

Cyber deception techniques

SOC-style telemetry pipelines

Real-time attack monitoring

Blue-team security analysis

Suitable for:

Final-year cybersecurity projects

SOC analyst training

Defensive security research

🚀 Future Enhancements
Geo-IP attack mapping

Threat severity scoring

SIEM integration

Cloud-based deployment

IDS correlation

👤 Author
Vatsal Sapovadiya
Cybersecurity | SOC & Blue-Team Enthusiast

📜 License
MIT License — Educational Use
