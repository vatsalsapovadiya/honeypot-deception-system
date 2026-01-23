# 🛡️ Honeypot-Based Cyber Deception System

A **SOC-style Honeypot and Cyber Deception System** built for academic research and hands-on cybersecurity learning. This project captures **real attacker behavior** using SSH and Web honeypots, normalizes attack telemetry, and provides a **near real-time monitoring dashboard** similar to Security Operations Centers (SOCs).

---

## 📌 Project Highlights

- 🐝 **SSH Honeypot (Cowrie)** - Captures brute-force and SSH interaction attempts
- 🌐 **Custom Web Honeypot (Flask)** - Credential harvesting simulation
- 🍯 **Cyber Deception Layer**
  - Honeytoken credentials
  - Fake admin, IoT, and backup endpoints
- 📊 **Live SOC-Style Dashboard**
  - SSH & Web attack counters
  - Latest attack feed
  - Real-time brute-force alerting
- 🔁 **Automated Log Ingestion Pipeline**
- 🔒 **Fully isolated, ethical, and safe environment**

---

## 🧱 System Architecture

```
Attacker
    ↓
[ SSH Honeypot (Cowrie) ]  [ Web Honeypot (Flask) ]
    ↓                           ↓
         Raw Attack Logs
                ↓
         SQLite Database
                ↓
    Normalization & Analytics
                ↓
       SOC-Style Dashboard
```

---

## 🛠️ Technologies Used

| Component | Technology |
|-----------|-----------|
| Operating System | Kali Linux |
| SSH Honeypot | Cowrie |
| Web Honeypot | Flask (Python) |
| Database | SQLite |
| Dashboard | Flask + HTML/CSS/JavaScript |
| Visualization | Chart.js |
| Automation | Python |
| Virtualization | VirtualBox |

---

## ⚙️ Prerequisites

- Kali Linux (recommended in VirtualBox)
- Python 3.9 or above
- Internet access (for initial setup)
- Minimum 4 GB RAM

---

## 🚀 Installation & Setup Guide

### 🔹 Step 1: Clone the Repository

```bash
git clone https://github.com/<your-username>/honeypot-based-cyber-deception-system.git
cd honeypot-based-cyber-deception-system
```

### 🔹 Step 2: Install and Configure Cowrie (SSH Honeypot)

```bash
# Create a dedicated user for Cowrie
sudo adduser cowrie
su - cowrie

# Clone Cowrie repository
git clone https://github.com/cowrie/cowrie.git
cd cowrie

# Setup virtual environment
python3 -m venv cowrie-env
source cowrie-env/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

**Configure Cowrie:**

```bash
cp etc/cowrie.cfg.dist etc/cowrie.cfg
nano etc/cowrie.cfg
```

Ensure the following configuration:

```ini
[ssh]
enabled = true
listen_port = 2222
```

**Start Cowrie:**

```bash
cowrie start
```

### 🔹 Step 3: Setup the Database

```bash
# Create SQLite database
sqlite3 database/attacks.db
```

**Tables used:**
- `ssh_attacks`
- `web_attacks`
- `attack_events`

### 🔹 Step 4: Setup Web Honeypot

```bash
cd web_honeypot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start web honeypot
python3 app.py
```

**Access the web honeypot at:**
- `http://127.0.0.1:8080`
- `http://127.0.0.1:8080/admin`
- `http://127.0.0.1:8080/iot`

### 🔹 Step 5: Setup Dashboard

```bash
cd dashboard

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start dashboard
python3 app.py
```

**Access the dashboard at:**
- `http://127.0.0.1:5000`

### 🔹 Step 6: Start Automated Ingestion Pipeline

```bash
cd scripts
python3 auto_pipeline.py
```

This enables:
- Automatic log ingestion
- Continuous analytics updates
- Near real-time dashboard refresh

---

## 🧪 Attack Simulation & Testing

### SSH Brute-Force Simulation

```bash
ssh root@127.0.0.1 -p 2222
```

### Simulate Multiple Attacker IPs

```bash
ssh root@127.0.0.1 -p 2222 -b 127.0.0.2
ssh root@127.0.0.1 -p 2222 -b 127.0.0.3
```

### Nmap Reconnaissance

```bash
nmap -p 2222 127.0.0.1
```

---

## 📊 Dashboard Features

- ✅ Live SSH and Web attack counters
- ✅ Latest attack table (real-time)
- ✅ SSH brute-force alert banner
- ✅ Attack-rate spike visualization
- ✅ Per-IP attack tracking

---

## 📸 Screenshots

Screenshots demonstrating the system are available in the `/screenshots` directory:

- Live Dashboard View
- SSH Brute-Force Detection
- Cowrie Log Capture
- Attack Rate Spike Graph

---

## ⚖️ Ethics & Legal Disclaimer

⚠️ **IMPORTANT:** This project is designed for **educational and research purposes only**.

- ✅ Fully isolated virtual environment
- ✅ No real systems targeted
- ✅ No real credentials used
- ✅ Attacks generated only on own setup

**DO NOT** use this system to target unauthorized networks or systems. Unauthorized access to computer systems is illegal.

---

## 🎓 Academic Relevance

This project demonstrates:

- Cyber deception techniques
- Honeypot deployment and monitoring
- SOC-style data pipelines
- Real-time attack analysis

**Suitable for:**
- Final-year cybersecurity projects
- SOC / Blue-Team training
- Academic research demonstrations

---

## 🚀 Future Enhancements

- [ ] Geo-IP attack mapping
- [ ] Threat scoring & severity levels
- [ ] SIEM integration
- [ ] Cloud-based deployment
- [ ] IDS correlation

---

## 👤 Author

**Vatsal Sapovadiya**  
Cybersecurity Enthusiast | Blue-Team & SOC Focus

---

## 📜 License

MIT License  
For educational and academic use only.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!  
Feel free to check the [issues page](https://github.com/<your-username>/honeypot-based-cyber-deception-system/issues).

---

## ⭐ Show Your Support

Give a ⭐ if this project helped you learn about honeypots and cyber deception!

---

## 📧 Contact

For questions or collaboration:
- GitHub: [@your-username](https://github.com/your-username)
- Email: your.email@example.com
