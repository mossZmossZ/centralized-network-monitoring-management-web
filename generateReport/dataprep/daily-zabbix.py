import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
from collections import defaultdict
import json
# Load environment variables
load_dotenv()

# Read Zabbix credentials
ZABBIX_SERVER = os.getenv("ZABBIX_SERVER")
ZABBIX_API_TOKEN = os.getenv("ZABBIX_API_TOKEN")

# Zabbix API URL
ZABBIX_API_URL = f"{ZABBIX_SERVER}/api_jsonrpc.php"

# Define time slots (converted to integer hours for correct comparison)
time_slots = [0, 4, 8, 12, 16, 20]
time_slots_cpu = ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"]

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

def get_Zabbix_servers_group_id():
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
            "filter": {"name": ["Zabbix servers"]}
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


def get_today_server_problem():
    """Fetch server-related problems from Zabbix for 'Zabbix Servers' only for today."""
    group_id = get_Zabbix_servers_group_id()
    if not group_id:
        print("Could not find 'Zabbix servers' group.")
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
            "groupids": [group_id],  # Filter events by Zabbix Servers group
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
    server_issues = []
    for issue in data.get("result", []):
        # Convert timestamp to formatted datetime
        timestamp = datetime.fromtimestamp(int(issue["clock"]))
        formatted_time = timestamp.strftime("%Y-%m-%d %I:%M:%S %p")  # Example: "2025-03-15 12:47:49 PM"

        # Get Host (default to 'Unknown' if missing)
        host = issue["hosts"][0]["host"] if "hosts" in issue and issue["hosts"] else "Unknown"

        # Get Full Problem Description
        full_problem_description = issue.get("name", "Unknown Issue")

        # Extract problem type (Keep only "Link Down", "CPU High", etc.)
        problem_type = extract_problem_type(full_problem_description)

        # Calculate Duration
        duration_seconds = int(now.timestamp()) - int(issue["clock"])
        days, remainder = divmod(duration_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes = remainder // 60
        duration_str = f"{days}d {hours}h {minutes}m"

        # Append to results
        server_issues.append([formatted_time, host, problem_type, duration_str])

    return {"os_issues": server_issues}  # Return formatted list


def extract_problem_type(description):
    """
    Extract only the core problem type from the full problem description.
    Example: 
      "Interface Gi1/0/24(vlan 50 for cctv): Link down" → "Link Down"
      "CPU utilization is high" → "CPU High"
    """

    # Common problem patterns
    problem_keywords = [
        "link down", "speed change", "disk full", "high memory usage",
        "cpu high", "icmp unreachable", "no snmp data collection",
        "power supply warning", "temperature warning"
    ]

    # Check if any known problem type is in the description
    for keyword in problem_keywords:
        if keyword in description.lower():
            return keyword.title()  # Convert to title case (e.g., "Link Down")

    # If no match, return "Other Issue"
    return "Other Issue"


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
        # Convert timestamp to formatted datetime
        timestamp = datetime.fromtimestamp(int(issue["clock"]))
        formatted_time = timestamp.strftime("%Y-%m-%d %I:%M:%S %p")  # Example: "2025-03-15 12:47:49 PM"

        # Get Host (default to 'Unknown' if missing)
        host = issue["hosts"][0]["host"] if "hosts" in issue and issue["hosts"] else "Unknown"

        # Get Problem Description
        full_problem_description = issue.get("name", "Unknown Issue")

        # Extract problem type using category_map
        problem_type = "Other Issue"
        for category, keywords in category_map.items():
            if any(keyword in full_problem_description.lower() for keyword in keywords):
                problem_type = category
                break

        # Calculate Duration
        duration_seconds = int(now.timestamp()) - int(issue["clock"])
        days, remainder = divmod(duration_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes = remainder // 60
        duration_str = f"{days}d {hours}h {minutes}m"

        # Append to results
        network_issues.append([formatted_time, host, problem_type, duration_str])

    return {"network_issues": network_issues}  # Return formatted list




def get_problem_graph():
    """Generate structured problem history graph data from Zabbix problems for today."""
    raw_issues_data = get_today_zabbix_problem()  # Fetch today's problem data
    raw_issues = raw_issues_data["network_issues"]  # Extract network issues list

    # Initialize problem history with empty counts for each time slot
    problem_history = defaultdict(lambda: [0] * len(time_slots))

    for issue in raw_issues:
        formatted_time, host, problem_type, duration = issue  # Extract issue details

        # Extract the hour from the formatted timestamp (e.g., "2025-03-17 12:14:54 AM")
        event_hour = datetime.strptime(formatted_time, "%Y-%m-%d %I:%M:%S %p").hour

        # Assign to correct time slot
        for i in range(len(time_slots)):
            if i == len(time_slots) - 1:  # Last slot (20:00 - 00:00)
                if event_hour >= time_slots[i] or event_hour < time_slots[0]:
                    problem_history[problem_type][i] += 1
                    break
            elif time_slots[i] <= event_hour < time_slots[i + 1]:  # Any other slot
                problem_history[problem_type][i] += 1
                break

    return {"problem_history": dict(problem_history)}  # Convert defaultdict to dict

def count_today_problems():
    """Count the total number of problems reported today from Zabbix."""
    raw_issues_data = get_today_zabbix_problem()  # Fetch today's problem data
    raw_issues = raw_issues_data["network_issues"]  # Extract network issues list

    # Count the number of issues
    total_problems = len(raw_issues)

    return total_problems

def count_today_server_problems():
    """Count the total number of problems reported today from Zabbix."""
    raw_issues_data = get_today_server_problem()  # Fetch today's problem data
    raw_issues = raw_issues_data["os_issues"]  # Extract network issues list

    # Count the number of issues
    total_server_problems = len(raw_issues)

    return total_server_problems

def get_today_cpu_usage():
    """Fetch and structure CPU usage data for each host."""
    
    group_id = get_Zabbix_servers_group_id()
    if not group_id:
        print("❌ Could not find 'Zabbix Servers' group.")
        return {}

    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ZABBIX_API_TOKEN}"
    }

    # Step 1: Get all hosts in the Zabbix Servers group
    payload_hosts = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": ["hostid", "name"],
            "groupids": [group_id]
        },
        "id": 1
    }

    response_hosts = requests.post(ZABBIX_API_URL, json=payload_hosts, headers=HEADERS)
    data_hosts = response_hosts.json()

    if "error" in data_hosts:
        print("❌ Error fetching hosts:", data_hosts["error"])
        return {}

    hosts = {host["hostid"]: host["name"] for host in data_hosts.get("result", [])}

    # Step 2: Fetch CPU usage metrics for each host
    cpu_usage = defaultdict(lambda: [0] * len(time_slots_cpu))

    now = datetime.now()
    timestamps = [(now.replace(hour=int(ts.split(":")[0]), minute=0, second=0) - timedelta(days=1)).timestamp() for ts in time_slots_cpu]

    for host_id, host_name in hosts.items():
        item_id = get_cpu_itemid(host_id)
        if not item_id:
            print(f"⚠️ No valid CPU item found for {host_name} (Host ID: {host_id})")
            continue

        cpu_data = fetch_cpu_data(host_id, item_id)
        if not cpu_data:
            print(f"⚠️ Warning: No CPU data found for {host_name}.")
            continue

        # Convert timestamps to HH:MM format and map values
        cpu_values = {
            datetime.fromtimestamp(int(entry["clock"])).strftime("%H:%M"): round(float(entry["value"]), 2)  # Remove * 100
            for entry in cpu_data
        }

        # Align CPU values to predefined time slots
        aligned_values = []
        for ts in time_slots_cpu:
            closest_time = min(cpu_values.keys(), key=lambda t: abs(datetime.strptime(t, "%H:%M") - datetime.strptime(ts, "%H:%M"))) if cpu_values else None
            aligned_values.append(cpu_values.get(closest_time, 0))

        cpu_usage[host_name] = aligned_values

    return {"cpu_usage": dict(cpu_usage)}


def fetch_cpu_data(host_id, item_id):
    """Fetch the last 24 hours of CPU history for the given item ID."""

    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ZABBIX_API_TOKEN}"
    }

    time_from = int((datetime.now() - timedelta(days=1)).timestamp())

    payload_cpu = {
        "jsonrpc": "2.0",
        "method": "history.get",
        "params": {
            "output": "extend",
            "history": 0,  # Use history type 0 (integer)
            "itemids": item_id,
            "sortfield": "clock",
            "sortorder": "ASC",
            "time_from": time_from,
            "limit": 1000
        },
        "id": 1
    }

    response_cpu = requests.post(ZABBIX_API_URL, json=payload_cpu, headers=HEADERS)
    data_cpu = response_cpu.json()

    if "error" in data_cpu:
        print(f"❌ Error fetching CPU data for {host_id}:", data_cpu["error"])
        return []

    return data_cpu.get("result", [])


def get_cpu_itemid(host_id):
    """Fetch the item ID for CPU utilization for a given host ID."""
    
    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ZABBIX_API_TOKEN}"
    }

    payload = {
        "jsonrpc": "2.0",
        "method": "item.get",
        "params": {
            "output": ["itemid", "key_"],
            "hostids": host_id,
            "search": {"key_": "system.cpu.util"},
            "sortfield": "name"
        },
        "id": 1
    }

    response = requests.post(ZABBIX_API_URL, json=payload, headers=HEADERS)
    data = response.json()

    if "error" in data:
        print("❌ Error fetching CPU item:", data["error"])
        return None

    for item in data.get("result", []):
        if item.get("key_") == "system.cpu.util":
            return item["itemid"]

    return None


# Example Usage
if __name__ == "__main__":
    #problem_data = get_problem_graph()  # Fetch problem history for today
    #print(problem_data)  # Print final structured data
    #print(get_today_zabbix_problem())
    #print(count_today_problems())
    #print(get_today_server_problem())
    #print(count_today_server_problems())
    # Example usage:
    print(get_today_cpu_usage())
    #print(get_all_cpu_items(10084))