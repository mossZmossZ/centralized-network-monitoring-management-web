import os
import asyncio
import httpx
from dotenv import load_dotenv
from urllib.parse import urlparse
from fastapi import APIRouter

# Load environment variables
load_dotenv()

router = APIRouter()

# ✅ Service list (Only Ping URLs)
SERVICES = {
    "Services": [
        {"name": "Docker Server", "pingUrl": os.getenv("VITE_DOCKER_SERVER_PING")},
        {"name": "Zabbix", "pingUrl": os.getenv("VITE_ZABBIX_PING")},
        {"name": "Prometheus", "pingUrl": os.getenv("VITE_PROMETHEUS_PING")},
    ],
    "Logging": [
        {"name": "Fluentd", "pingUrl": os.getenv("VITE_FLUENTD_PING")},
        {"name": "OpenSearch", "pingUrl": os.getenv("VITE_OPENSEARCH_PING")},
    ],
    "Dashboard": [
        {"name": "Grafana", "pingUrl": os.getenv("VITE_GRAFANA_PING")},
        {"name": "Uptime Kuma", "pingUrl": os.getenv("VITE_UPTIMEKUMA_PING")},
    ],
}

# ✅ Global storage for results
ping_results = {}


def format_url(url: str) -> str:
    """Ensure URL starts with http:// or https://"""
    if not urlparse(url).scheme:
        return "https://" + url
    return url


async def update_ping_status():
    """Periodically checks service status and updates the cache."""
    global ping_results

    while True:
        results = {}
        async with httpx.AsyncClient() as client:
            for category, services in SERVICES.items():
                results[category] = []
                for service in services:
                    if not service["pingUrl"]:
                        print(f"⚠️ {service['name']}: URL Not Set")
                        results[category].append({"name": service["name"], "status": "❌ Down"})
                        continue

                    try:
                        url = format_url(service["pingUrl"])
                        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

                        # ✅ Fix for Uptime Kuma
                        if "uptime kuma" in service["name"].lower():
                            url = f"{url}/api/status"  # ✅ Correct API endpoint

                        response = await client.get(url, headers=headers, timeout=3.0)

                        if response.status_code == 200:
                            status = "✅ Up"
                        else:
                            status = "❌ Down"
                            print(f"❌ {service['name']} is DOWN ({response.status_code})")

                    except httpx.RequestError as e:
                        status = "❌ Down"
                        print(f"❌ {service['name']} Request Error: {e}")

                    results[category].append({"name": service["name"], "status": status})

        # ✅ Store latest results
        ping_results = results
        print("✅ Updated service status")

        await asyncio.sleep(10)  # ✅ Set interval (every 10 seconds)


@router.get("/ping")
async def get_service_status():
    """Returns cached service statuses instantly."""
    return ping_results
