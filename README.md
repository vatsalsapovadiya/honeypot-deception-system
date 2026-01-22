# 🛡️ Honeypot-Based Cyber Deception System

A **SOC-style Honeypot and Cyber Deception System** designed for academic research and hands-on cybersecurity learning.  
This project captures **real attacker behavior** using SSH and Web honeypots, normalizes attack telemetry, and provides **near real-time attack visibility** through a live dashboard.

The system is fully **isolated, ethical, and reproducible**, making it suitable for final-year projects, SOC learning, and blue-team research.

---

## 📌 Key Features

- 🐝 **SSH Honeypot (Cowrie)**
  - Captures brute-force attempts
  - Logs credentials, commands, and attacker IPs

- 🌐 **Custom Web Honeypot (Flask)**
  - Fake login pages (`/`, `/admin`, `/iot`)
  - Credential harvesting without real authentication

- 🎭 **Cyber Deception Layer**
  - Honeytoken credentials
  - Fake administrative and IoT interfaces
  - Behavioral analysis of attacker intent

- 📊 **SOC-Style Dashboard**
  - Live SSH & Web attack counts
  - Latest attack feed (real-time)
  - Brute-force detection alerts
  - Attack-rate spike visualization

- 🔁 **Automated Ingestion Pipeline**
  - Near real-time log ingestion
  - Analytics normalization
  - No manual intervention required

- 🔒 **Ethical & Isolated Design**
  - Localhost / VM-only deployment
  - No public exposure
  - No real credentials or assets

---

## 🧱 System Architecture

