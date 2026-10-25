# 🛡️ AEGIS AI — AI-Powered Cyber Threat Detection & Incident Response Platform

> **A Next-Generation Autonomous SOC Assistant & Cyber Threat Telemetry Correlator**  
> Built with **Python** & **Streamlit** | Modern Dark Navy-Blue Cyber Aesthetic | 100% Safe Synthetic Telemetry

---

## 🌟 Hackathon Project Overview

In modern Security Operations Centers (SOCs), cybersecurity analysts face severe **alert fatigue**:
- **Massive Alert Volume**: Thousands of low-fidelity logs flood SIEM consoles every hour.
- **Disconnected Signals**: Traditional rule engines flag isolated log lines without correlating full multi-stage kill chains.
- **Lack of Explainability**: Black-box systems output cryptic anomaly numbers without telling analysts *why* something was flagged.
- **Delayed Incident Response**: Analysts must manually look up containment commands while adversaries move laterally.

**AEGIS AI** solves this problem by combining deterministic heuristic rule detection with graph incident correlation, asset-criticality weighting, explainable AI (XAI) rationale, and prescriptive human-in-the-loop containment playbooks.

---

## 🚀 Key Features

| Feature | Description |
| :--- | :--- |
| **📊 SOC Command Center** | Real-time KPI metric cards (Total Events, Suspicious Events, High-Risk Alerts, Critical Incidents), interactive threat timeline, and severity distribution. |
| **🧪 100% Safe Synthetic Telemetry** | Generates realistic enterprise telemetry including brute force, port scans, web injection, data exfiltration, and normal background traffic. |
| **⚡ Heuristic Detection Engine** | Evaluates failed login velocity, stealth port scans, SQL injection signatures, directory traversal, sensitive port exposure, and impossible travel. |
| **🎯 Dynamic Risk Scoring (0–100)** | Assigns risk scores and severity classifications (**Low**, **Medium**, **High**, **Critical**) with asset tier bonuses (Crown Jewels like Domain Controllers). |
| **🧩 Incident Correlator** | Groups individual related alerts across time, IP addresses, and assets into multi-stage attack campaigns (e.g., Reconnaissance ➔ Brute Force ➔ Lateral Movement). |
| **🤖 Explainable AI (XAI)** | Plain-English explanations breaking down the exact trigger conditions, behavioral anomalies, and MITRE ATT&CK tactics for each alert. |
| **🛡️ Prescriptive Playbooks** | Generates ready-to-use defensive commands (Linux `iptables`, Windows Defender Firewall `netsh`, Azure AD MFA enforcement, EDR host isolation). |
| **🔍 Search & Deep Dive** | Searchable and filterable alerts table with a detailed event inspector modal and raw packet viewer. |
| **🧪 Live Attack Injection Lab** | Interactive sandbox allowing judges to fire custom attack vectors on demand and observe real-time detection. |
| **📄 One-Click Incident Report** | Export complete incident response briefs in Markdown format for audit and SOC leadership. |

---

## 📁 Project Structure

```text
AEGIS_AI/
├── app.py              # Main Streamlit application with UI, rules engine, correlation & XAI
├── requirements.txt    # Project dependencies (streamlit, pandas, plotly)
└── README.md           # Setup instructions, architecture, and hackathon presentation guide
```

---

## 💻 Quickstart Guide (Windows)

Follow these simple steps to install and run AEGIS AI on your Windows machine.

### Prerequisites
Make sure you have **Python 3.10 or newer** installed on your Windows computer.

---

### Step 1: Open Terminal in the Project Folder
Open **PowerShell** or **Command Prompt** and navigate to your project directory:

```powershell
cd C:\Users\chandini\Desktop\AEGIS_AI
```

---

### Step 2: Install Dependencies
Run the following command to install `streamlit`, `pandas`, and `plotly`:

```powershell
python -m pip install -r requirements.txt
```

> 💡 **Tip for Beginners**: Using `python -m pip` ensures that packages are installed directly into your active Python environment.

---

### Step 3: Run AEGIS AI
Launch the application using Streamlit:

```powershell
python -m streamlit run app.py
```

> 💡 **Tip for Beginners**: Using `python -m streamlit run app.py` prevents any `'streamlit' is not recognized` errors on Windows if the Python Scripts directory is not on your PATH.

---

### Step 4: Open in Your Browser
Streamlit will automatically open your default browser. If it doesn't, navigate to:
```text
http://localhost:8501
```

---

## 🛠️ Beginner Troubleshooting & Windows Tips

### 1. Error: `'streamlit' is not recognized as an internal or external command`
- **Solution**: Instead of typing `streamlit run app.py`, always run:
  ```powershell
  python -m streamlit run app.py
  ```

### 2. Error: `Program 'python.exe' failed to run` or opens the Microsoft Store
- If Windows tries to open the Microsoft Store when typing `python`:
  1. Open Windows **Settings** (Win + I).
  2. Search for **"Manage app execution aliases"**.
  3. Turn **OFF** the toggles for `App Installer (python.exe)` and `App Installer (python3.exe)`.
  4. Try running with `py -m streamlit run app.py` instead.

### 3. Error: `Port 8501 is already in use`
- Run the app on a different port:
  ```powershell
  python -m streamlit run app.py --server.port 8502
  ```

### 4. PowerShell Execution Policy Restriction
- If PowerShell prevents running scripts, run:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
  Or simply open standard **Command Prompt (`cmd.exe`)** and run the commands there.

---

## 🏗️ System Architecture & Detection Pipeline

```text
 +-----------------------------------------------------------------------------------+
 |                             AEGIS AI SOC PIPELINE                                 |
 +-----------------------------------------------------------------------------------+
 
   [ 1. Ingestion Layer ]        -->  Safe, Structured Telemetry (Auth, Net, Web, DNS)
             │
             ▼
   [ 2. Heuristic Rule Engine ]   -->  Deterministic Signature & Velocity Evaluation
             │                        (R101 Brute Force, R102 Port Scan, R103 SQLi, etc.)
             ▼
   [ 3. Asset & Context Matrix ] -->  Crown Jewel & Criticality Scoring Boost
             │                        (Domain Controllers & Payment DBs weighted)
             ▼
   [ 4. AI Explainability (XAI) ] -->  Generates Human-Readable "Why Flagged" Breakdown
             │                        + MITRE ATT&CK Tactic & Technique Mapping
             ▼
   [ 5. Incident Correlator ]    -->  Graph Clustering across Attacker IP & Asset Chains
             │                        (Reduces 50 alerts into 1 cohesive incident)
             ▼
   [ 6. Containment Playbooks ]   -->  Prescriptive Human-in-the-Loop Mitigation Commands
                                      (Perimeter Drop, EDR Host Isolation, MFA Reset)
```

---

## 🎯 3-Minute Hackathon Demo Script (For Judges)

When presenting to judges or instructors, follow this high-impact 3-minute sequence:

### **Minute 1: The Problem & Dashboard Overview**
- Open the dashboard at `http://localhost:8501`.
- Point out the dark navy-blue SOC aesthetic and live status banner.
- Highlight the **KPI Metric Cards**: Total Ingested Events, Suspicious Events, High-Risk Alerts, and Correlated Incidents.
- Show the **Threat Volume Timeline** and **Alert Severity Distribution** donut chart.

### **Minute 2: Explainable AI (XAI) & Deep Dive**
- Switch to the **"🚨 Threat Detection & Alerts Table"** tab.
- Filter by `Severity: Critical` or search for `185.220.101.5`.
- Select an event in the **Deep Dive Event Inspector**.
- Show the judges **"Why was this flagged?"**:
  - Explain how AEGIS AI reveals the velocity anomaly, payload signature, and asset criticality instead of giving a mystery score.
  - Show the mapped **MITRE ATT&CK tactic**.

### **Minute 3: Multi-Stage Incident Correlation & Live Attack Injection**
- Switch to the **"🧩 Incident Correlation & War Room"** tab.
  - Explain how AEGIS AI groups disparate alerts (port scan + brute force) into an overarching incident (`INC-2026-101`), eliminating alert fatigue.
  - Click **"Execute Complete Containment"** to demonstrate automated human-approved mitigation.
- Switch to the **"🧪 Live Attack Injection Lab"** tab:
  - Ask a judge to pick an attack scenario (e.g. *Web Application SQL Injection*).
  - Click **"Fire Threat Vector into AEGIS AI"**.
  - Show the live engine intercepting, scoring, and generating firewall rules in real time!

---

## 🔒 Safety & Ethical Notice

AEGIS AI operates strictly as a **defensive cybersecurity analytical prototype**.
- All telemetry, IP addresses, log formats, and payloads generated are **100% synthetic**.
- The application does **not** perform network scanning, penetration testing, packet sniffing, or attacks on real systems.
- Completely safe to run on local laptops, campus networks, and hackathon presentation environments.

---

## 📄 License

Developed for hackathon demonstration. Open source under the MIT License.
