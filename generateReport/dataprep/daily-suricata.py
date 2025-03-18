import os
import requests
import json
from datetime import datetime, timedelta, timezone
from dateutil import parser
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenSearch configuration
OPENSEARCH_URL = os.getenv("OPENSEARCH_URL")
OPENSEARCH_SURICATA_INDEX = os.getenv("OPENSEARCH_SURICATA_INDEX")

TIME_SLOTS = ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"]

def fetch_suricata_alerts():
    """Fetch Suricata alerts from OpenSearch in the last 24 hours."""
    
    url = f"{OPENSEARCH_URL}/{OPENSEARCH_SURICATA_INDEX}/_search"
    
    now = datetime.now(timezone.utc)
    past_24_hours = (now - timedelta(days=1)).isoformat()

    query = {
        "size": 10000,
        "query": {
            "bool": {
                "must": [
                    {"range": {"@timestamp": {"gte": past_24_hours}}},
                    {"match": {"event_type": "alert"}}
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
    """Extract the main keywords from the signature."""
    keywords = ["Port Scan", "DROP Listed", "SSH Scan", "Compromised", "Malware", "Dshield"]
    for word in keywords:
        if word in signature:
            return word
    return signature.split()[0]  # Default: use the first word if no match

def get_threat_summary():
    """Aggregate threats, count occurrences, and store the last hit timestamp."""
    
    alerts = fetch_suricata_alerts()
    threat_data = {}

    for timestamp, signature, sig_id in alerts:
        key = (signature, sig_id)
        converted_time = parser.isoparse(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        if key in threat_data:
            threat_data[key]["count"] += 1
            if timestamp > threat_data[key]["last_hit"]:
                threat_data[key]["last_hit"] = converted_time
        else:
            threat_data[key] = {"count": 1, "last_hit": converted_time}

    sorted_threats = sorted(threat_data.items(), key=lambda x: x[1]["count"], reverse=True)
    
    top_10_threats = [
        [data["last_hit"], signature, str(data["count"])]
        for (signature, _), data in sorted_threats[:10]
    ]

    return {"threats_detected": top_10_threats}

def get_graph_threats():
    """Generate threat history grouped into 6 time slots, using top 3 threats."""

    alerts = fetch_suricata_alerts()
    threat_counts = {sig: [0] * len(TIME_SLOTS) for sig in []}  # Ensures correct structure

    for timestamp, signature, sig_id in alerts:
        short_signature = extract_short_signature(signature)
        parsed_time = parser.isoparse(timestamp)
        time_hour = parsed_time.strftime("%H:%M")

        # Determine the closest time slot
        closest_slot_index = min(
            range(len(TIME_SLOTS)),
            key=lambda i: abs(int(TIME_SLOTS[i].split(":")[0]) - int(time_hour.split(":")[0]))
        )

        if short_signature not in threat_counts:
            threat_counts[short_signature] = [0] * len(TIME_SLOTS)

        threat_counts[short_signature][closest_slot_index] += 1

    # Get total counts for ranking
    total_counts = {sig: sum(counts) for sig, counts in threat_counts.items()}

    # Sort and get top 3 threats
    top_3_threats = sorted(total_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    top_3_signatures = {sig for sig, _ in top_3_threats}

    # Filter only top 3 threats
    final_threats = {sig: threat_counts[sig] for sig in top_3_signatures}

    return {"threats_history": final_threats}  

# Run the functions and print the results
if __name__ == "__main__":
    print(get_threat_summary())
    print(get_graph_threats())  





