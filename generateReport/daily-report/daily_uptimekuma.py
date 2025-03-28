import os
import requests
import json
import re
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()


BASE_URL = os.getenv("OPENSEARCH_URL")
INDEX_NAME = os.getenv("OPENSEARCH_INDEX")
USER = os.getenv("OPENSEARCH_USER")
PASSWORD = os.getenv("OPENSEARCH_PASS")

# Allowed Monitor Names (Filter only these monitors)
ALLOWED_MONITORS = {"ENG KMUTNB", "ECE ENG", "KMUTNB"}

# Time Slots for Classifying Results (Optional)
TIME_SLOTS = [
    (0, 6),    # 00:00 - 06:00  -> Slot 0
    (6, 12),   # 06:00 - 12:00  -> Slot 1
    (12, 18),  # 12:00 - 18:00  -> Slot 2
    (18, 24)   # 18:00 - 00:00  -> Slot 3
]
def clean_message(message):
    """Remove emojis, special characters, and line breaks from the message."""
    # Remove emojis and special symbols
    clean_msg = re.sub(r"[\U00010000-\U0010ffff]", "", message)
    # Remove line breaks and extra spaces
    clean_msg = clean_msg.replace("\n", " ").strip()
    return clean_msg


def get_monitor_down_day():
    """Fetch 'Down' monitors from uptime_kuma_alerts-* over the last 24 hours."""
    
    # Elasticsearch query to get "Down" events within the last 24 hours
    query = {
        "query": {
            "bool": {
                "must": [
                    {"range": {"@timestamp": {"gte": "now-24h", "lte": "now"}}},  # Last 24 hours
                    {"match": {"message": "Down"}}  # Match Down in message
                ]
            }
        },
        "size": 1000,  # Increase size if needed
        "sort": [
            {"@timestamp": {"order": "desc"}}  # Sort by most recent
        ]
    }

    # 🛑 Authentication (Optional)
    auth = (USER, PASSWORD) if USER and PASSWORD else None

    try:
        # ✅ Make a POST request to Elasticsearch with the query
        response = requests.post(
            f"{BASE_URL}/{INDEX_NAME}/_search",
            headers={"Content-Type": "application/json"},
            auth=auth,
            data=json.dumps(query),
            verify=False  # Ignore SSL verification if necessary
        )

        # 🚨 Check for valid response
        if response.status_code != 200:
            print(f"Error! Status code: {response.status_code}, Reason: {response.reason}")
            return json.dumps({"error": f"Failed to retrieve data. Status: {response.status_code}"}, indent=4)

        # 🎯 Get the response data in JSON format
        data = response.json()

        # Check if hits exist and process results
        hits = data.get("hits", {}).get("hits", [])
        if not hits:
            return json.dumps({"web_issues": []}, indent=4)

        web_issues = []
        for hit in hits:
            source = hit["_source"]
            timestamp = source.get("@timestamp", "")
            monitor_name = source.get("monitor_name", "Unknown")

            # Skip monitors not in ALLOWED_MONITORS
            if monitor_name not in ALLOWED_MONITORS:
                continue

            message = source.get("message", "")
            status = "Down" if "Down" in message else "Unknown"

            # Extract issue description (after "]")
            if "]" in message:
                issue_description = message.split("]")[-1].strip()
            else:
                issue_description = message

            # Clean unwanted characters and emojis
            issue_description = clean_message(issue_description)

            # Cut issue description to 50 characters max
            issue_description = (
                issue_description[:50] + "..." if len(issue_description) > 50 else issue_description
            )

            # Format timestamp to readable format
            try:
                event_time = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
                formatted_time = event_time.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                formatted_time = timestamp  # Fallback if parsing fails

            # Add cleaned data without time slot
            web_issues.append([formatted_time, monitor_name, status, issue_description])

        # 🎉 Return results as JSON
        return json.dumps({"web_issues": web_issues}, indent=4)

    except requests.exceptions.RequestException as e:
        return json.dumps({"error": f"Error connecting to OpenSearch: {str(e)}"}, indent=4)


def get_graph_down_day():
    query = {
        "query": {
            "bool": {
                "must": [
                    {"range": {"@timestamp": {"gte": "now/d", "lte": "now"}}},  # Today from 00:00 to now
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
    web_downtime = {monitor: [0, 0, 0, 0] for monitor in ALLOWED_MONITORS}

    for hit in hits:
        source = hit["_source"]
        timestamp = source.get("@timestamp", "")
        monitor_name = source.get("monitor_name", "Unknown")

        if monitor_name not in ALLOWED_MONITORS:
            continue

        dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
        hour = dt.hour

        for i, (start, end) in enumerate(TIME_SLOTS):
            if start <= hour < end:
                web_downtime[monitor_name][i] += 1
                break

    return json.dumps({"web_downtime": web_downtime}, indent=4)

def get_down_count_day():
    monitor_down_data = json.loads(get_monitor_down_day())
    down_count = len(monitor_down_data.get("web_issues", []))
    return json.dumps({"Web Application": down_count}, indent=4)

if __name__ == "__main__":
    print(get_monitor_down_day())
    #print(get_graph_down_day())
    #print(get_down_count_day())
    #print(get_all_monitor_status())