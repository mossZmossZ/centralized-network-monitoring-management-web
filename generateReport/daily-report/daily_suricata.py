import os
import requests
import json
from datetime import datetime, timedelta, timezone
timestamp = datetime.now(timezone.utc)

from dateutil import parser
from dotenv import load_dotenv
load_dotenv()

OPENSEARCH_URL = os.getenv("OPENSEARCH_URL")
OPENSEARCH_SURICATA_INDEX = os.getenv("OPENSEARCH_SURICATA_INDEX")

TIME_SLOTS = ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"]
TIME_SLOTS_GRAPH = [
    ("00:00", "04:00"),
    ("04:00", "08:00"),
    ("08:00", "12:00"),
    ("12:00", "16:00"),
    ("16:00", "20:00"),
    ("20:00", "00:00")
]

def fetch_suricata_alerts():
    url = f"{OPENSEARCH_URL}/{OPENSEARCH_SURICATA_INDEX}/_search"
    
    now = datetime.now(timezone.utc)
    past_24_hours = (now - timedelta(days=1)).isoformat()

    query = {
        "size": 10000,
        "query": {
            "bool": {
                "must": [
                    {"range": {"@timestamp": {"gte": past_24_hours}}},
                    {"match": {"event_type": "alert"}},
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
        
        alerts.append((timestamp, signature, signature_id))

    return alerts

def extract_short_signature(signature):
    keywords = ["Port Scan", "DROP Listed", "SSH Scan", "Compromised", "Malware", "Dshield"]
    for word in keywords:
        if word in signature:
            return word
    return signature.split()[0]  # Default: use the first word if no match

def get_threat_summary():
    alerts = fetch_suricata_alerts()  # Assuming this returns a list of [timestamp, signature, sig_id]
    threat_data = {}

    for timestamp, signature, sig_id, severity in alerts:
        short_signature = extract_short_signature(signature)  # Use extracted signature category
        key = (short_signature, sig_id, severity)

        converted_time = parser.isoparse(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        if key in threat_data:
            threat_data[key]["count"] += 1
            if timestamp > threat_data[key]["last_hit"]:
                threat_data[key]["last_hit"] = converted_time
        else:
            threat_data[key] = {"count": 1, "last_hit": converted_time}

    sorted_threats = sorted(threat_data.items(), key=lambda x: x[1]["count"], reverse=True)
    
    top_10_threats = [
        [data["last_hit"], short_signature, str(data["count"])]
        for (short_signature, _), data in sorted_threats[:10]
    ]

    return {"threats_detected": top_10_threats}

def get_graph_threats():
    alerts = fetch_suricata_alerts()  # Expected to return a list of [timestamp, signature, sig_id]
    threat_counts = {}

    # Use local time (no timezone adjustments)
    now = datetime.now()  
    today_str = now.strftime("%Y-%m-%d")
    current_hour = now.hour

    # Determine the current valid time slot index
    current_slot_index = None
    for i, (start, end) in enumerate(TIME_SLOTS_GRAPH):
        start_hour = int(start.split(":")[0])
        end_hour = int(end.split(":")[0]) if end != "00:00" else 24
        if start_hour <= current_hour < end_hour:
            current_slot_index = i
            break
    if current_slot_index is None:
        return {"threats_history": {}}

    for timestamp, signature, sig_id in alerts:
        short_signature = extract_short_signature(signature)
        parsed_time = parser.isoparse(timestamp)  # Assuming the timestamp is in local time
        parsed_date = parsed_time.strftime("%Y-%m-%d")
        parsed_hour = parsed_time.hour

        # Only process alerts from today
        if parsed_date != today_str:
            continue

        # Only iterate up to the current slot index
        for i in range(current_slot_index + 1):
            start_hour = int(TIME_SLOTS_GRAPH[i][0].split(":")[0])
            end_hour = int(TIME_SLOTS_GRAPH[i][1].split(":")[0]) if TIME_SLOTS_GRAPH[i][1] != "00:00" else 24

            if start_hour <= parsed_hour < end_hour:
                if short_signature not in threat_counts:
                    threat_counts[short_signature] = [0] * len(TIME_SLOTS_GRAPH)
                threat_counts[short_signature][i] += 1
                break

    # Set future slots explicitly to 0 for all threats
    for sig in threat_counts:
        for i in range(current_slot_index + 1, len(TIME_SLOTS_GRAPH)):
            threat_counts[sig][i] = 0

    total_counts = {sig: sum(counts) for sig, counts in threat_counts.items()}
    top_3_threats = sorted(total_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    top_3_signatures = {sig for sig, _ in top_3_threats}
    final_threats = {sig: threat_counts[sig] for sig in top_3_signatures}

    return {"threats_history": final_threats}

if __name__ == "__main__":
    #print(fetch_suricata_alerts())
    print(get_threat_summary())
    #print(get_graph_threats())  





