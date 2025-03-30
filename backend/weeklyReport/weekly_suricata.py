import os
import requests
import json
from datetime import datetime, timedelta, timezone
timestamp = datetime.now(timezone.utc)

from dateutil import parser
from dotenv import load_dotenv
from pathlib import Path

# Assuming your .env is in the project root
dotenv_path = Path(__file__).resolve().parents[1] / '.env'
load_dotenv(dotenv_path)
OPENSEARCH_URL = os.getenv("OPENSEARCH_URL")
OPENSEARCH_SURICATA_INDEX = os.getenv("OPENSEARCH_SURICATA_INDEX")

TIME_SLOTS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def fetch_suricata_alerts():
    url = f"{OPENSEARCH_URL}/{OPENSEARCH_SURICATA_INDEX}/_search"
    
    now = datetime.now(timezone.utc)
    past_week = (now - timedelta(days=7)).isoformat()

    query = {
        "size": 10000,
        "query": {
            "bool": {
                "must": [
                    {"range": {"@timestamp": {"gte": past_week}}},
                    {"match": {"event_type": "alert"}},
                    {"terms": {"alert.severity": [2, 3]}}  # ดึงเฉพาะ severity 2 และ 3
                ]
            }
        },
        "sort": [{"@timestamp": {"order": "desc"}}]
    }

    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers, data=json.dumps(query))

    if response.status_code != 200:
        print("Error fetching data:", response.text)
        return []

    data = response.json()

    alerts = []
    for hit in data.get("hits", {}).get("hits", []):
        source = hit.get("_source", {})
        timestamp = source.get("@timestamp", "")
        alert_info = source.get("alert", {})

        if not alert_info:
            continue

        signature = alert_info.get("signature", "Unknown Threat")
        signature_id = str(alert_info.get("signature_id", "0"))
        severity = alert_info.get("severity", "N/A")  # เพิ่มระดับ severity ลงไป
        
        alerts.append((timestamp, signature, signature_id, severity))

    return alerts

def extract_short_signature(signature):
    keywords = ["Port Scan", "DROP Listed", "SSH Scan", "Compromised", "Malware", "Dshield"]
    for word in keywords:
        if word in signature:
            return word
    return signature.split()[0]  # Default: use the first word if no match

def get_threat_summary():
    alerts = fetch_suricata_alerts()  # Fetch Suricata alerts for the last 7 days
    threat_data = {}

    for timestamp, signature, sig_id, severity in alerts:
        # ✅ Extract and categorize the signature
        short_signature = extract_short_signature(signature)

        # ✅ Truncate signature to 30 characters with "..." if necessary
        if len(signature) > 30:
            signature = signature[:30] + "..."

        # ✅ Use a combination of short signature, sig_id, and severity as key
        key = (signature, sig_id, severity)

        # ✅ Convert timestamp to readable format
        converted_time = parser.isoparse(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        # ✅ Aggregate threat data
        if key in threat_data:
            threat_data[key]["count"] += 1
            if timestamp > threat_data[key]["last_hit"]:
                threat_data[key]["last_hit"] = converted_time
        else:
            threat_data[key] = {"count": 1, "last_hit": converted_time}

    # ✅ Sort threats by count (descending order)
    sorted_threats = sorted(threat_data.items(), key=lambda x: x[1]["count"], reverse=True)

    # ✅ Format the top 10 threats with truncated names
    top_10_threats = [
        [
            data["last_hit"],   # Date and time of last occurrence
            signature,          # Truncated signature (30 chars max)
            str(data["count"])  # Count of occurrences
        ]
        for (signature, _, _), data in sorted_threats[:10]
    ]

    return {"threats_detected": top_10_threats}


def get_graph_threats():
    alerts = fetch_suricata_alerts()  # Expected to return a list of [timestamp, signature, sig_id]
    threat_counts = {sig: [0] * len(TIME_SLOTS) for sig in ["DROP Listed", "Port Scan", "Dshield"]}

    for timestamp, signature, sig_id, severity in alerts:
        short_signature = extract_short_signature(signature)
        parsed_time = parser.isoparse(timestamp)
        day_of_week = parsed_time.strftime('%A')  # 'Monday', 'Tuesday', etc.

        if short_signature not in threat_counts:
            threat_counts[short_signature] = [0] * len(TIME_SLOTS)
        
        day_index = TIME_SLOTS.index(day_of_week)  # Get index of the day in the list
        threat_counts[short_signature][day_index] += 1

    return {"threats_history": threat_counts}

if __name__ == "__main__":
    #print(fetch_suricata_alerts())
    print(get_threat_summary())
    #print(get_graph_threats())  





