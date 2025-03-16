import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
from collections import defaultdict

# Load environment variables
load_dotenv()

# Read Zabbix credentials
ZABBIX_SERVER = os.getenv("ZABBIX_SERVER")
ZABBIX_API_TOKEN = os.getenv("ZABBIX_API_TOKEN")

# Zabbix API URL
ZABBIX_API_URL = f"{ZABBIX_SERVER}/api_jsonrpc.php"

# Define time slots (converted to integer hours for correct comparison)
time_slots = [0, 4, 8, 12, 16, 20]

# Define problem categories
category_map = {
    "Link Down": ["link down"],
    "Speed Change": ["ethernet has changed to lower speed", "speed change"],
    "Port Failure": ["port failure", "interface failure", "port issue"]
}


def get_discovered_hosts_group_id():
    """Fetch the Host Group ID for 'Discovered Hosts' from Zabbix."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ZABBIX_API_TOKEN}"
    }
    
    payload = {
        "jsonrpc": "2.0",
        "method": "hostgroup.get",
        "params": {
            "output": ["groupid"],
            "filter": {"name": ["Discovered hosts"]}
        },
        "auth": None,
        "id": 1
    }

    response = requests.post(ZABBIX_API_URL, json=payload, headers=headers)
    data = response.json()

    if "error" in data:
        print("Error fetching host group:", data["error"])
        return None

    groups = data.get("result", [])
    if groups:
        return groups[0]["groupid"]  # Return the first matching group ID
    return None


def get_today_zabbix_problem():
    """Fetch network-related problems from Zabbix for 'Discovered Hosts' only for today."""
    group_id = get_discovered_hosts_group_id()
    if not group_id:
        print("Could not find 'Discovered Hosts' group.")
        return []

    # Define time range: Start of today to now
    now = datetime.now()
    start_of_today = datetime(now.year, now.month, now.day, 0, 0)  # Midnight today
    time_from = int(start_of_today.timestamp())  # Start of today
    time_to = int(now.timestamp())  # Current time

    # Request headers for API authentication
    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ZABBIX_API_TOKEN}"  # Use API Token
    }

    # API request payload
    payload = {
        "jsonrpc": "2.0",
        "method": "event.get",
        "params": {
            "output": ["clock", "name", "objectid"],
            "selectHosts": ["host"],
            "selectAlerts": ["message"],
            "groupids": [group_id],  # Filter events by Discovered Hosts group
            "source": 0,  # Triggers
            "value": 1,   # Problem state (Active Issues)
            "time_from": time_from,
            "time_till": time_to,
            "sortfield": ["clock"],
            "sortorder": "DESC",
            "limit": 500  # Fetch more events for accurate categorization
        },
        "auth": None,
        "id": 1
    }

    # Send API request
    response = requests.post(ZABBIX_API_URL, json=payload, headers=HEADERS)
    data = response.json()

    # Check for errors
    if "error" in data:
        print("Error:", data["error"])
        return []

    # Process results
    network_issues = []
    for issue in data.get("result", []):
        timestamp = datetime.fromtimestamp(int(issue["clock"]))
        time_str = timestamp.strftime("%H:%M")  # Get time in HH:MM format
        problem_type = issue.get("name", "Unknown Issue")  # Problem description

        network_issues.append({"time": time_str, "problem_type": problem_type})

    return network_issues  # Return the cleaned issues list


def get_problem_graph():
    """Generate structured problem history graph data from Zabbix problems for today."""
    raw_issues = get_today_zabbix_problem()  # Fetch today's problem data

    problem_history = defaultdict(lambda: [0] * len(time_slots))  # Default 0 counts

    for issue in raw_issues:
        problem_type = issue["problem_type"].lower()  # Convert to lowercase for case-insensitive matching
        event_hour = int(issue["time"].split(":")[0])  # Convert event time (HH:MM) to integer hour

        # Assign problem type to a category
        assigned = False
        for category, keywords in category_map.items():
            if any(keyword in problem_type for keyword in keywords):
                assigned = True
                for i in range(len(time_slots)):
                    if i == len(time_slots) - 1:  # Last slot (20:00 - 00:00)
                        if event_hour >= time_slots[i] or event_hour < time_slots[0]:
                            problem_history[category][i] += 1
                            break
                    elif time_slots[i] <= event_hour < time_slots[i + 1]:  # Any other slot
                        problem_history[category][i] += 1
                        break
                break
        
        # If no category matched, put it in "Other Issues"
        if not assigned:
            for i in range(len(time_slots)):
                if i == len(time_slots) - 1:  # Last slot (20:00 - 00:00)
                    if event_hour >= time_slots[i] or event_hour < time_slots[0]:
                        problem_history["Other Issues"][i] += 1
                        break
                elif time_slots[i] <= event_hour < time_slots[i + 1]:  # Any other slot
                    problem_history["Other Issues"][i] += 1
                    break

    return {"problem_history": dict(problem_history)}  # Convert defaultdict to dict


# Example Usage
if __name__ == "__main__":
    problem_data = get_problem_graph()  # Fetch problem history for today
    print(problem_data)  # Print final structured data
    #print(get_today_zabbix_problem())