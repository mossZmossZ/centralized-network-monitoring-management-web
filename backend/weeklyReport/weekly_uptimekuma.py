import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

# Assuming your .env is in the project root
dotenv_path = Path(__file__).resolve().parents[1] / '.env'
load_dotenv(dotenv_path)

BASE_URL = os.getenv("OPENSEARCH_URL", "http://localhost:9200")
INDEX_NAME = os.getenv("OPENSEARCH_INDEX", "uptime_kuma_alerts-*")
USER = os.getenv("OPENSEARCH_USER")
PASSWORD = os.getenv("OPENSEARCH_PASS")

ALLOWED_MONITORS = {"ENG KMUTNB", "ECE ENG", "KMUTNB"}

TIME_SLOTS = [
    "Monday",    # Slot 0
    "Tuesday",   # Slot 1
    "Wednesday", # Slot 2
    "Thursday",  # Slot 3
    "Friday",    # Slot 4
    "Saturday",  # Slot 5
    "Sunday"     # Slot 6
]

def get_monitor_down_week():
    query = {
        "query": {
            "bool": {
                "must": [
                    {"range": {"@timestamp": {"gte": "now-7d", "lte": "now"}}},  # Past 7 day
                    {"match_phrase": {"message": "Down"}}
                ]
            }
        }
    }
    auth = (USER, PASSWORD) if USER and PASSWORD else None

    try:
        response = requests.get(
            f"{BASE_URL}/{INDEX_NAME}/_search",
            headers={"Content-Type": "application/json"},
            auth=auth,
            data=json.dumps(query),
            verify=False  # Ignore SSL issues if necessary
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return json.dumps({"error": f"Error connecting to OpenSearch: {str(e)}"}, indent=4)

    data = response.json()
    hits = data.get("hits", {}).get("hits", [])

    web_issues = []
    for hit in hits:
        source = hit["_source"]
        timestamp = source.get("@timestamp", "")
        monitor_name = source.get("monitor_name", "Unknown")

        if monitor_name not in ALLOWED_MONITORS:
            continue  # Skip this entry

        message = source.get("message", "")
        status = "Down" if "Down" in message else "Unknown"

        if "PING" in message and "packet loss" in message:
            issue_description = "PING Down"
        else:
            issue_description = message.split("]")[-1].strip()

        formatted_time = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")

        web_issues.append([formatted_time, monitor_name, status, issue_description])

    return json.dumps({"web_issues": web_issues}, indent=4)


def get_graph_down_week():
    query = {
        "query": {
            "bool": {
                "must": [
                    {"range": {"@timestamp": {"gte": "now-7d/d", "lte": "now"}}},  # Today from 00:00 to now
                    {"match_phrase": {"message": "Down"}}
                ]
            }
        }
    }

    auth = (USER, PASSWORD) if USER and PASSWORD else None

    try:
        response = requests.get(
            f"{BASE_URL}/{INDEX_NAME}/_search",
            headers={"Content-Type": "application/json"},
            auth=auth,
            data=json.dumps(query),
            verify=False  # Ignore SSL verification issues if necessary
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return json.dumps({"error": f"Error connecting to OpenSearch: {str(e)}"}, indent=4)

    data = response.json()
    hits = data.get("hits", {}).get("hits", [])

    # Initialize web_downtime with zero counts for all time slots
    web_downtime = {monitor: [0] * 7 for monitor in ALLOWED_MONITORS}

    for hit in hits:
        source = hit["_source"]
        timestamp = source.get("@timestamp", "")
        monitor_name = source.get("monitor_name", "Unknown")

        if monitor_name not in ALLOWED_MONITORS:
            continue

        dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
        day_index = dt.weekday()  # แปลง timestamp เป็น index ของวัน (Monday = 0, ..., Sunday = 6)

        web_downtime[monitor_name][day_index] += 1  # เพิ่มจำนวนครั้งที่ Down ในวันนั้น

    return json.dumps({"web_downtime": web_downtime}, indent=4)

def get_down_count_week():
    monitor_down_data = json.loads(get_monitor_down_week())
    down_count = len(monitor_down_data.get("web_issues", []))
    return json.dumps({"Web Application": down_count}, indent=4)

# if __name__ == "__main__":
#     #print(get_monitor_down_week())
#     print(get_graph_down_week())
#     #print(get_down_count_week())