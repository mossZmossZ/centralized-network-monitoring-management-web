import os
import httpx
import asyncio
import docker
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from urllib.parse import urlparse
from fastapi.responses import StreamingResponse

# Load environment variables
load_dotenv()

# ✅ Initialize FastAPI
app = FastAPI()

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Connect to Docker
client = docker.from_env()


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


@app.get("/ping")
async def get_service_status():
    """Returns cached service statuses instantly."""
    return ping_results


@app.on_event("startup")
async def startup_event():
    """Starts the background ping updater when the server starts."""
    asyncio.create_task(update_ping_status())


# =======================
# ✅ Docker Management APIs
# =======================

@app.get("/containers")
def list_containers():
    """List all containers (running and stopped)"""
    try:
        containers = client.containers.list(all=True)
        return [{"id": c.id, "name": c.name, "status": c.status} for c in containers]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/containers/run")
def run_container(image: str, name: str = None, command: str = None):
    """Run a new Docker container"""
    try:
        container = client.containers.run(image, name=name, command=command, detach=True)
        return {"message": f"Container {container.id} started", "id": container.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/containers/stop/{container_id}")
def stop_container(container_id: str):
    """Stop a running container"""
    try:
        container = client.containers.get(container_id)
        container.stop()
        return {"message": f"Container {container_id} stopped"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/containers/restart/{container_id}")
def restart_container(container_id: str):
    """Restart a container"""
    try:
        container = client.containers.get(container_id)
        container.restart()
        return {"message": f"Container {container_id} restarted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/containers/logs/{container_id}")
def get_logs(container_id: str):
    """Fetch logs of a container"""
    try:
        container = client.containers.get(container_id)
        logs = container.logs(tail=100).decode("utf-8")
        return {"logs": logs}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/containers/logs/stream/{container_id}")
async def stream_logs(container_id: str):
    """Stream container logs in real-time"""
    try:
        container = client.containers.get(container_id)

        async def event_generator():
            for line in container.logs(stream=True, follow=True):
                yield line.decode("utf-8")

        return StreamingResponse(event_generator(), media_type="text/plain")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/containers/status/{container_id}")
def container_status(container_id: str):
    """Check if a container is running"""
    try:
        container = client.containers.get(container_id)
        return {"id": container.id, "name": container.name, "status": container.status}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))