import os
import requests
from datetime import datetime, timedelta
from collections import defaultdict
from dotenv import load_dotenv
from pathlib import Path

# Assuming your .env is in the project root
dotenv_path = Path(__file__).resolve().parents[1] / '.env'
load_dotenv(dotenv_path)


ZABBIX_SERVER = os.getenv("ZABBIX_SERVER")
ZABBIX_API_TOKEN = os.getenv("ZABBIX_API_TOKEN")
ZABBIX_API_URL = f"{ZABBIX_SERVER}/api_jsonrpc.php"


time_slots = {
    "01-05": range(1, 6),
    "06-10": range(6, 11),
    "11-15": range(11, 16),
    "16-20": range(16, 21),
    "21-25": range(21, 26),
    "26-31": range(26, 32),
}
time_slots_cpu = ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"]


category_map = {
    "Link Down": ["link down"],
    "Speed Change": ["ethernet has changed to lower speed", "speed change"],
    "Port Failure": ["port failure", "interface failure", "port issue"]
}

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


def get_month_server_problem():
    group_id = get_Zabbix_servers_group_id()
    if not group_id:
        print("Could not find 'Zabbix servers' group.")
        return []
    
    now = datetime.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0)
    
    time_from = int(start_of_month.timestamp())  
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

    response = requests.post(ZABBIX_API_URL, json=payload, headers=HEADERS)
    data = response.json()

    if "error" in data:
        print("Error:", data["error"])
        return []

    server_issues = []
    
    for issue in data.get("result", []):
        timestamp = datetime.fromtimestamp(int(issue["clock"]))
        formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")  # ✅ 24-hour format
        
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

def get_month_zabbix_problem():
    """Fetch Zabbix problems from the past 24 hours with a 24-hour format."""
    
    group_id = get_discovered_hosts_group_id()
    if not group_id:
        print("Could not find 'Discovered Hosts' group.")
        return []

    now = datetime.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0)  
    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)

    time_from = int(start_of_month.timestamp())  
    time_to = int(end_of_month.timestamp())  

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

    response = requests.post(ZABBIX_API_URL, json=payload, headers=HEADERS)
    data = response.json()

    if "error" in data:
        print("Error:", data["error"])
        return []

    issue_counts = defaultdict(lambda: {"time": None, "count": 0, "timestamp": 0})

    for issue in data.get("result", []):
        timestamp = int(issue["clock"])
        formatted_time = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")  # 24-hour format

        host = issue["hosts"][0]["host"] if "hosts" in issue and issue["hosts"] else "Unknown"
        full_problem_description = issue.get("name", "Unknown Issue")

        problem_type = "Other Issue"
        for category, keywords in category_map.items():
            if any(keyword in full_problem_description.lower() for keyword in keywords):
                problem_type = category
                break

        key = (host, problem_type)

        if problem_type == "Link Down":
            issue_counts[key]["time"] = formatted_time
            issue_counts[key]["timestamp"] = timestamp
            issue_counts[key]["count"] += 1
        else:
            if issue_counts[key]["time"] is None:
                issue_counts[key]["time"] = formatted_time
                issue_counts[key]["timestamp"] = timestamp
            issue_counts[key]["count"] += 1

    formatted_issues = sorted(
        [[info["time"], host, problem, info["count"]] for (host, problem), info in issue_counts.items()],
        key=lambda x: (-x[3], -datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S").timestamp())  
    )

    return {"network_issues": formatted_issues} 


def get_problem_graph():
    raw_issues_data = get_month_zabbix_problem()  # Fetch issues
    raw_issues = raw_issues_data.get("network_issues", [])  

    now = datetime.now()
    start_of_today = datetime(now.year, now.month, 1, 0, 0)  # เริ่มต้นเดือน

    problem_history = defaultdict(lambda: {slot: 0 for slot in time_slots.keys()})
    has_valid_data = False  

    for issue in raw_issues:
        formatted_time, host, problem_type, duration = issue  
        event_dt = datetime.strptime(formatted_time, "%Y-%m-%d %H:%M:%S")

        if event_dt < start_of_today:
            continue  

        event_day = event_dt.day  

        for slot, day_range in time_slots.items():
            if event_day in day_range:
                problem_history[problem_type][slot] += duration
                has_valid_data = True
                break

    if not has_valid_data:
        return {"problem_history": {"No Data": {slot: 0 for slot in time_slots.keys()}}}

    return {"problem_history": dict(problem_history)}


def count_today_problems():
    raw_issues_data = get_month_zabbix_problem()
    raw_issues = raw_issues_data.get("network_issues", [])

    total_problems = sum(issue[3] for issue in raw_issues)  # Summing the count column

    return total_problems

def count_today_server_problems():
   
    raw_issues_data = get_month_server_problem()  # Fetch today's problem data
    raw_issues = raw_issues_data["os_issues"]  

    total_server_problems = len(raw_issues)

    return total_server_problems

def get_month_cpu_usage():
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

    # สร้าง time slots จาก 00:00 ถึงตอนนี้ (เป็น datetime objects)
    time_slots_cpu = [today_midnight + timedelta(hours=i) for i in range(now.hour + 1)]
    time_slots_str = [ts.strftime("%H:%M") for ts in time_slots_cpu]  # ฟอร์แมตเป็น string ช่วงเวลา

    cpu_usage = defaultdict(lambda: [0] * len(time_slots_str))  # กำหนดค่าเริ่มต้นทั้งหมดเป็น 0

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
    #print(count_today_problems())
    #print(get_today_server_problem())
    #print(count_today_server_problems())
    #print(get_today_cpu_usage())
    #print(get_all_cpu_items(10084))