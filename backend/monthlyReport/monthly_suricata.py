import os
import requests
import json
from datetime import datetime, timedelta, timezone
from dateutil import parser
from dotenv import load_dotenv
from pathlib import Path

# Assuming your .env is in the project root
dotenv_path = Path(__file__).resolve().parents[1] / '.env'
load_dotenv(dotenv_path)


OPENSEARCH_URL = os.getenv("OPENSEARCH_URL")
OPENSEARCH_SURICATA_INDEX = os.getenv("OPENSEARCH_SURICATA_INDEX")

# เปลี่ยนจากวันในสัปดาห์เป็นวันที่ของเดือน (1-31)
TIME_SLOTS = {
    "01-05": range(1, 6),
    "06-10": range(6, 11),
    "11-15": range(11, 16),
    "16-20": range(16, 21),
    "21-25": range(21, 26),
    "26-31": range(26, 32),
}

def fetch_suricata_alerts():
    url = f"{OPENSEARCH_URL}/{OPENSEARCH_SURICATA_INDEX}/_search?scroll=1m"
    
    now = datetime.now(timezone.utc)
    past_month = (now - timedelta(days=30)).isoformat()

    query = {
        "size": 5000,  # ดึงทีละ 5000 records
        "query": {
            "bool": {
                "must": [
                    {"range": {"@timestamp": {"gte": past_month}}},
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
    scroll_id = data.get("_scroll_id", None)
    alerts = []

    while scroll_id and len(data.get("hits", {}).get("hits", [])) > 0:
        for hit in data["hits"]["hits"]:
            source = hit.get("_source", {})
            timestamp = source.get("@timestamp", "")
            alert_info = source.get("alert", {})

            if not alert_info:
                continue

            signature = alert_info.get("signature", "Unknown Threat")
            signature_id = str(alert_info.get("signature_id", "0"))

            alerts.append((timestamp, signature, signature_id))

        # ดึงข้อมูลหน้าถัดไป
        scroll_url = f"{OPENSEARCH_URL}/_search/scroll"
        scroll_query = {"scroll": "1m", "scroll_id": scroll_id}
        response = requests.get(scroll_url, headers=headers, data=json.dumps(scroll_query))

        if response.status_code != 200:
            break

        data = response.json()
        scroll_id = data.get("_scroll_id", None)

    return alerts

def extract_short_signature(signature):
    keywords = ["Port Scan", "DROP Listed", "SSH Scan", "Compromised", "Malware", "Dshield"]
    for word in keywords:
        if word in signature:
            return word
    return signature.split()[0]

def get_threat_summary():
    alerts = fetch_suricata_alerts()
    threat_data = {}

    for timestamp, signature, sig_id in alerts:
        short_signature = extract_short_signature(signature)
        key = (short_signature, sig_id)

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
    alerts = fetch_suricata_alerts()
    
    # ใช้ dictionary ที่ key เป็นช่วงวันที่แทน
    threat_counts = {sig: {slot: 0 for slot in TIME_SLOTS.keys()} for sig in ["DROP Listed", "Port Scan", "Dshield"]}

    for timestamp, signature, sig_id in alerts:
        short_signature = extract_short_signature(signature)
        parsed_time = parser.isoparse(timestamp)
        day_of_month = int(parsed_time.strftime('%d'))  # แปลงวันที่เป็น int

        # หา key ที่มี range ครอบคลุมวันที่นี้
        slot_key = next((key for key, days in TIME_SLOTS.items() if day_of_month in days), None)

        if slot_key:
            if short_signature not in threat_counts:
                threat_counts[short_signature] = {slot: 0 for slot in TIME_SLOTS.keys()}
            
            threat_counts[short_signature][slot_key] += 1

    return {"threats_history": threat_counts}

if __name__ == "__main__":
    print(get_threat_summary())
    print(get_graph_threats())
