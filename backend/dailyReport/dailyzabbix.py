import os
import requests
from dotenv import load_dotenv

from datetime import datetime, timedelta
from collections import defaultdict
# Assuming your .env is in the project root
from pathlib import Path
dotenv_path = Path(__file__).resolve().parents[1] / '.env'
load_dotenv(dotenv_path)

ZABBIX_SERVER = os.getenv("ZABBIX_SERVER")
ZABBIX_API_TOKEN = os.getenv("ZABBIX_API_TOKEN")
ZABBIX_API_URL = f"{ZABBIX_SERVER}/api_jsonrpc.php"


time_slots = [0, 4, 8, 12, 16, 20]
time_slots_cpu = ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"]

def get_discovered_hosts_group_id():
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
    print(data)
    if "error" in data:
        print("Error fetching host group:", data["error"])
        return None
    groups = data.get("result", [])
    if groups:
        return groups[0]["groupid"]  
    return None

def get_Zabbix_servers_group_id():
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
        return groups[0]["groupid"] 
    return None


def get_today_server_problem():
    """Fetch server issues from the past 24 hours and return a shortened list."""

    group_id = get_Zabbix_servers_group_id()
    if not group_id:
        print("Could not find 'Zabbix servers' group.")
        return []

    now = datetime.now()
    past_24h = now - timedelta(hours=24)

    time_from = int(past_24h.timestamp())
    time_to = int(now.timestamp())

    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ZABBIX_API_TOKEN}"
    }

    payload = {
        "jsonrpc": "2.0",
        "method": "event.get",
        "params": {
            "output": ["clock", "name", "objectid"],
            "selectHosts": ["host"],
            "selectAlerts": ["message"],
            "groupids": [group_id],
            "source": 0,  # Triggers only
            "value": 1,  # Problems only
            "time_from": time_from,
            "time_till": time_to,
            "sortfield": ["clock"],
            "sortorder": "DESC",
            "limit": 500
        },
        "auth": None,
        "id": 1
    }

    response = requests.post(ZABBIX_API_URL, json=payload, headers=HEADERS)
    data = response.json()

    if "error" in data:
        print("Error:", data["error"])
        return []

    server_issues = []

    for issue in data.get("result", []):
        timestamp = datetime.fromtimestamp(int(issue["clock"]))
        formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")

        host = issue["hosts"][0]["host"] if "hosts" in issue and issue["hosts"] else "Unknown"
        full_problem_description = issue.get("name", "Unknown Issue")

        # Cut problem description to 30 characters if too long
        shortened_description = (
            full_problem_description[:30] + "..." if len(full_problem_description) > 30 else full_problem_description
        )

        # Calculate duration since the problem started
        duration_seconds = int(now.timestamp()) - int(issue["clock"])
        days, remainder = divmod(duration_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes = remainder // 60
        duration_str = f"{days}d {hours}h {minutes}m"

        server_issues.append([formatted_time, host, shortened_description, duration_str])

    return {"os_issues": server_issues}

def get_today_zabbix_problem():
    """Fetch Zabbix problems from the past 24 hours and return a shortened list."""

    group_id = get_discovered_hosts_group_id()
    if not group_id:
        print("Could not find 'Discovered Hosts' group.")
        return []

    now = datetime.now()
    past_24h = now - timedelta(days=1)

    time_from = int(past_24h.timestamp())
    time_to = int(now.timestamp())

    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ZABBIX_API_TOKEN}"
    }

    payload = {
        "jsonrpc": "2.0",
        "method": "event.get",
        "params": {
            "output": ["clock", "name", "objectid"],
            "selectHosts": ["host"],
            "selectAlerts": ["message"],
            "groupids": [group_id],
            "source": 0,  # Triggers only
            "value": 1,  # Problems only
            "time_from": time_from,
            "time_till": time_to,
            "sortfield": ["clock"],
            "sortorder": "DESC",
            "limit": 500
        },
        "auth": None,
        "id": 1
    }

    response = requests.post(ZABBIX_API_URL, json=payload, headers=HEADERS)
    data = response.json()

    if "error" in data:
        print("Error:", data["error"])
        return []

    issue_counts = defaultdict(lambda: {"time": None, "count": 0, "timestamp": 0, "full_issue": ""})

    for issue in data.get("result", []):
        timestamp = int(issue["clock"])
        formatted_time = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

        host = issue["hosts"][0]["host"] if "hosts" in issue and issue["hosts"] else "Unknown"
        full_problem_description = issue.get("name", "Unknown Issue")

        # Remove device name before colon (e.g., FortiGate: -> just the description)
        if ":" in full_problem_description:
            description = full_problem_description.split(":", 1)[-1].strip()
        else:
            description = full_problem_description

        # Shorten the problem description to 25 characters max
        shortened_description = (
            description[:25] + "..." if len(description) > 25 else description
        )

        key = (host, full_problem_description)

        if key not in issue_counts:
            issue_counts[key]["time"] = formatted_time
            issue_counts[key]["timestamp"] = timestamp
            issue_counts[key]["full_issue"] = shortened_description

        issue_counts[key]["count"] += 1

    formatted_issues = sorted(
        [
            [info["time"], host, info["full_issue"], info["count"]]
            for (host, problem), info in issue_counts.items()
        ],
        key=lambda x: (-x[3], -datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S").timestamp())
    )

    return {"network_issues": formatted_issues}


def get_problem_graph():
    raw_issues_data = get_today_zabbix_problem()  # Fetch issues
    raw_issues = raw_issues_data.get("network_issues", [])  

    now = datetime.now()
    start_of_today = datetime(now.year, now.month, now.day, 0, 0)  # Today 00:00

    problem_history = defaultdict(lambda: [0] * len(time_slots))
    has_valid_data = False  # Track if at least one issue is counted

    for issue in raw_issues:
        formatted_time, host, problem_type, duration = issue  
        event_dt = datetime.strptime(formatted_time, "%Y-%m-%d %H:%M:%S")

        # Skip issues before 00:00 today
        if event_dt < start_of_today:
            continue  

        event_hour = event_dt.hour  # Extract hour from event

        # Assign the issue to the correct time slot
        for i in range(len(time_slots)):
            next_slot = time_slots[i + 1] if i + 1 < len(time_slots) else 24  # End of day
            
            if time_slots[i] <= event_hour < next_slot:
                problem_history[problem_type][i] += duration
                has_valid_data = True  # At least one valid issue exists
                break

    # If no valid issues were found for today, return "No Data"
    if not has_valid_data:
        return {"problem_history": {"No Data": [0, 0, 0, 0, 0, 0]}}
    
    return {"problem_history": dict(problem_history)}


def count_today_problems():
    raw_issues_data = get_today_zabbix_problem()
    raw_issues = raw_issues_data.get("network_issues", [])

    total_problems = sum(issue[3] for issue in raw_issues)  # Summing the count column

    return total_problems

def count_today_server_problems():
   
    raw_issues_data = get_today_server_problem()  # Fetch today's problem data
    raw_issues = raw_issues_data["os_issues"]  

    total_server_problems = len(raw_issues)

    return total_server_problems

def get_today_cpu_usage():
    group_id = get_Zabbix_servers_group_id()
    if not group_id:
        print("❌ Could not find 'Zabbix Servers' group.")
        return {}

    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ZABBIX_API_TOKEN}"
    }

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

    now = datetime.now()
    today_midnight = now.replace(hour=0, minute=0, second=0)  # Start of today

    # Generate time slots from 00:00 to now (hourly)
    time_slots_cpu = [today_midnight + timedelta(hours=i) for i in range(now.hour + 1)]
    time_slots_str = [ts.strftime("%H:%M") for ts in time_slots_cpu]  # Format time slot labels

    cpu_usage = defaultdict(lambda: [0] * len(time_slots_str))  # Default all slots to 0

    for host_id, host_name in hosts.items():
        item_id = get_cpu_itemid(host_id)
        if not item_id:
            print(f"⚠️ No valid CPU item found for {host_name} (Host ID: {host_id})")
            continue

        cpu_data = fetch_cpu_data(host_id, item_id)
        if not cpu_data:
            print(f"⚠️ Warning: No CPU data found for {host_name}.")
            continue

        cpu_values = {
            datetime.fromtimestamp(int(entry["clock"])).strftime("%H:%M"): round(float(entry["value"]), 2)
            for entry in cpu_data
        }

        aligned_values = []
        for ts in time_slots_str:
            closest_time = min(cpu_values.keys(), key=lambda t: abs(datetime.strptime(t, "%H:%M") - datetime.strptime(ts, "%H:%M"))) if cpu_values else None
            aligned_values.append(int(cpu_values.get(closest_time, 0)))  # Default to 0 if missing

        cpu_usage[host_name] = aligned_values

    return {"cpu_usage": dict(cpu_usage)}



def fetch_cpu_data(host_id, item_id):
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

#if __name__ == "__main__":
    #problem_data = get_problem_graph()  # Fetch problem history for today
    #print(problem_data)  # Print final structured data
    #print(get_today_zabbix_problem())
    # print(count_today_problems())
    #print(get_today_server_problem())
    #print(count_today_server_problems())
    #print(get_today_cpu_usage())
    #print(get_all_cpu_items(10084))