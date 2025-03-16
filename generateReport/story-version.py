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

# Define time slots
time_slots = ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"]

# Define problem categories
category_map = {
    "Link Down": ["link down"],
    "Speed Change": ["ethernet has changed to lower speed"],
    "No SNMP Data Collection": ["no snmp data"],
    "Power Supply Warning": ["power supply is in warning state"],
    "High Temperature": ["temperature is above warning threshold"],
    "ICMP Unreachable": ["unavailable by icmp ping"]
}


def get_zabbix_problem(days: int):
    """Fetch network-related problems from Zabbix for 'Discovered Hosts' within the last 'days' days."""
    
    # Define time range
    time_to = int(datetime.now().timestamp())  # Current time
    time_from = int((datetime.now() - timedelta(days=days)).timestamp())  # Time range based on user input

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
            "source": 0,  # Triggers
            "value": 1,   # Problem state (Active Issues)
            "time_from": time_from,
            "time_till": time_to,
            "sortfield": ["clock"],
            "sortorder": "DESC",
            "limit": 100  # Get more events for better aggregation
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
        host = issue["hosts"][0]["host"] if issue["hosts"] else "Unknown"  # Extract Host

        # Only include issues related to "Discovered Hosts"
        if "Discovered" in host:
            network_issues.append({"time": time_str, "problem_type": problem_type})

    return network_issues  # Return the cleaned issues list


def get_problem_graph(days: int):
    """Generate structured problem history graph data from Zabbix problems."""
    raw_issues = get_zabbix_problem(days)  # Fetch problem data

    problem_history = defaultdict(lambda: [0] * len(time_slots))  # Default 0 counts

    for issue in raw_issues:
        problem_type = issue["problem_type"]
        time = issue["time"]

        # Assign problem type to a category
        assigned = False
        for category, keywords in category_map.items():
            if any(keyword in problem_type.lower() for keyword in keywords):
                assigned = True
                problem_history[category] = [x + y for x, y in zip(problem_history[category], [1] * len(time_slots))]
                break
        
        # If no category matched, put it in "Other Issues"
        if not assigned:
            problem_history["Other Issues"] = [x + y for x, y in zip(problem_history["Other Issues"], [1] * len(time_slots))]

    return {"problem_history": dict(problem_history)}  # Convert defaultdict to dict


# Example Usage
if __name__ == "__main__":
    problem_data = get_problem_graph(7)  # Fetch problem history for the last 7 days
    print(problem_data)  # Print final structured data
