from fastapi import APIRouter, HTTPException
import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
from collections import defaultdict

load_dotenv()

router = APIRouter()

ZABBIX_SERVER = os.getenv("ZABBIX_SERVER")
ZABBIX_API_TOKEN = os.getenv("ZABBIX_API_TOKEN")
ZABBIX_API_URL = f"{ZABBIX_SERVER}/api_jsonrpc.php"

time_slots = [0, 4, 8, 12, 16, 20]
time_slots_cpu = ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"]

category_map = {
    "Link Down": ["link down"],
    "Speed Change": ["ethernet has changed to lower speed", "speed change"],
    "Port Failure": ["port failure", "interface failure", "port issue"]
}

def extract_problem_type(description):
    problem_keywords = [
        "link down", "speed change", "disk full", "high memory usage",
        "cpu high", "icmp unreachable", "no snmp data collection",
        "power supply warning", "temperature warning"
    ]

    for keyword in problem_keywords:
        if keyword in description.lower():
            return keyword.title()

    return "Other Issue"

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
        return None
    groups = data.get("result", [])
    if groups:
        return groups[0]["groupid"]
    return None

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
    if "error" in data:
        return None
    groups = data.get("result", [])
    if groups:
        return groups[0]["groupid"]
    return None

@router.get("/today_server_problem")
def get_today_server_problem():
    group_id = get_Zabbix_servers_group_id()
    if not group_id:
        raise HTTPException(status_code=404, detail="Could not find 'Zabbix servers' group.")
    
    now = datetime.now()
    start_of_today = datetime(now.year, now.month, now.day, 0, 0)
    time_from = int(start_of_today.timestamp())
    time_to = int(now.timestamp())

    headers = {
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
            "source": 0,
            "value": 1,
            "time_from": time_from,
            "time_till": time_to,
            "sortfield": ["clock"],
            "sortorder": "DESC",
            "limit": 500
        },
        "auth": None,
        "id": 1
    }

    response = requests.post(ZABBIX_API_URL, json=payload, headers=headers)
    data = response.json()
    if "error" in data:
        raise HTTPException(status_code=500, detail=data["error"])

    server_issues = []
    for issue in data.get("result", []):
        timestamp = datetime.fromtimestamp(int(issue["clock"]))
        formatted_time = timestamp.strftime("%Y-%m-%d %I:%M:%S %p")
        host = issue["hosts"][0]["host"] if "hosts" in issue and issue["hosts"] else "Unknown"
        full_problem_description = issue.get("name", "Unknown Issue")
        problem_type = extract_problem_type(full_problem_description)

        duration_seconds = int(now.timestamp()) - int(issue["clock"])
        days, remainder = divmod(duration_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes = remainder // 60
        duration_str = f"{days}d {hours}h {minutes}m"

        server_issues.append([formatted_time, host, problem_type, duration_str])

    return {"os_issues": server_issues}

@router.get("/today_zabbix_problem")
def get_today_zabbix_problem():
    group_id = get_discovered_hosts_group_id()
    if not group_id:
        raise HTTPException(status_code=404, detail="Could not find 'Discovered Hosts' group.")

    now = datetime.now()
    start_of_today = datetime(now.year, now.month, now.day, 0, 0)
    time_from = int(start_of_today.timestamp())
    time_to = int(now.timestamp())

    headers = {
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
            "source": 0,
            "value": 1,
            "time_from": time_from,
            "time_till": time_to,
            "sortfield": ["clock"],
            "sortorder": "DESC",
            "limit": 500
        },
        "auth": None,
        "id": 1
    }

    response = requests.post(ZABBIX_API_URL, json=payload, headers=headers)
    data = response.json()

    if "error" in data:
        raise HTTPException(status_code=500, detail=data["error"])

    network_issues = []
    for issue in data.get("result", []):
        timestamp = datetime.fromtimestamp(int(issue["clock"]))
        formatted_time = timestamp.strftime("%Y-%m-%d %I:%M:%S %p")

        host = issue["hosts"][0]["host"] if "hosts" in issue and issue["hosts"] else "Unknown"
        full_problem_description = issue.get("name", "Unknown Issue")

        problem_type = "Other Issue"
        for category, keywords in category_map.items():
            if any(keyword in full_problem_description.lower() for keyword in keywords):
                problem_type = category
                break

        duration_seconds = int(now.timestamp()) - int(issue["clock"])
        days, remainder = divmod(duration_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes = remainder // 60
        duration_str = f"{days}d {hours}h {minutes}m"

        network_issues.append([formatted_time, host, problem_type, duration_str])

    return {"network_issues": network_issues}

@router.get("/today_problem_graph")
def get_problem_graph():
    raw_issues_data = get_today_zabbix_problem()  
    raw_issues = raw_issues_data["network_issues"]  

    problem_history = defaultdict(lambda: [0] * len(time_slots))

    for issue in raw_issues:
        formatted_time, host, problem_type, duration = issue  
        event_hour = datetime.strptime(formatted_time, "%Y-%m-%d %I:%M:%S %p").hour

        for i in range(len(time_slots)):
            if i == len(time_slots) - 1: 
                if event_hour >= time_slots[i] or event_hour < time_slots[0]:
                    problem_history[problem_type][i] += 1
                    break
            elif time_slots[i] <= event_hour < time_slots[i + 1]:  
                problem_history[problem_type][i] += 1
                break
    return {"problem_history": dict(problem_history)}  

@router.get("/count_today_server_problems")
def count_today_problems():
    
    raw_issues_data = get_today_zabbix_problem() 
    raw_issues = raw_issues_data["network_issues"]  

    total_problems = len(raw_issues)

    return total_problems

@router.get("/count_today_server_problems")
def count_today_server_problems():
   
    raw_issues_data = get_today_server_problem()  # Fetch today's problem data
    raw_issues = raw_issues_data["os_issues"]  

    total_server_problems = len(raw_issues)

    return total_server_problems

@router.get("/today_cpu_usage")
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

        cpu_values = {
            datetime.fromtimestamp(int(entry["clock"])).strftime("%H:%M"): round(float(entry["value"]), 2)  # Remove * 100
            for entry in cpu_data
        }

        aligned_values = []
        for ts in time_slots_cpu:
            closest_time = min(cpu_values.keys(), key=lambda t: abs(datetime.strptime(t, "%H:%M") - datetime.strptime(ts, "%H:%M"))) if cpu_values else None
            aligned_values.append(cpu_values.get(closest_time, 0))

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