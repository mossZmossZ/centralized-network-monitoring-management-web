import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

BASE_URL = os.getenv("OPENSEARCH_URL", "http://localhost:9200")
INDEX_NAME = os.getenv("OPENSEARCH_INDEX", "uptime_kuma_alerts-*")
USER = os.getenv("OPENSEARCH_USER")
PASSWORD = os.getenv("OPENSEARCH_PASS")

ALLOWED_MONITORS = {"ENG KMUTNB", "ECE ENG", "KMUTNB"}

TIME_SLOTS = TIME_SLOTS = {
    "01-05": range(1, 6),
    "06-10": range(6, 11),
    "11-15": range(11, 16),
    "16-20": range(16, 21),
    "21-25": range(21, 26),
    "26-31": range(26, 32),
}

def get_monitor_down_month():
    query = {
        "query": {
            "bool": {
                "must": [
                    {"range": {"@timestamp": {"gte": "now-30d", "lte": "now"}}},  # Past 7 day
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


def get_graph_down_month():
    query = {
        "query": {
            "bool": {
                "must": [
                    {"range": {"@timestamp": {"gte": "now-30d/d", "lte": "now"}}},  
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
            verify=False
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return json.dumps({"error": f"Error connecting to OpenSearch: {str(e)}"}, indent=4)

    data = response.json()
    hits = data.get("hits", {}).get("hits", [])

    # กำหนดให้แต่ละช่วงเริ่มต้นที่ 0
    web_downtime = {monitor: {slot: 0 for slot in TIME_SLOTS} for monitor in ALLOWED_MONITORS}

    for hit in hits:
        source = hit["_source"]
        timestamp = source.get("@timestamp", "")
        monitor_name = source.get("monitor_name", "Unknown")

        if monitor_name not in ALLOWED_MONITORS:
            continue

        dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
        day = dt.day  # ดึงวันที่ของเดือน (1-31)

        # หาช่วงที่วันที่อยู่ในนั้น
        for slot, days in TIME_SLOTS.items():
            if day in days:
                web_downtime[monitor_name][slot] += 1  # เพิ่มจำนวน down ในช่วงนั้น
                break

    return json.dumps({"web_downtime": web_downtime}, indent=4)

def get_down_count_month():
    monitor_down_data = json.loads(get_monitor_down_month())
    down_count = len(monitor_down_data.get("web_issues", []))
    return json.dumps({"Web Application": down_count}, indent=4)

if __name__ == "__main__":
    print(get_monitor_down_month())
    print(get_graph_down_month())
    print(get_down_count_month())