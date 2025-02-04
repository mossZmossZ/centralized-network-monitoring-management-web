import docker
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

router = APIRouter()

# ✅ Connect to Docker
try:
    client = docker.from_env()
    client.ping()
    print("✅ Docker is running")
except Exception as e:
    client = None
    print(f"❌ Docker is NOT running: {e}")


@router.get("/docker/status")
def check_docker_status():
    """Check if Docker is running"""
    return {"docker_running": client is not None}


@router.get("/containers")
def list_containers():
    """List all containers (running and stopped)"""
    if client is None:
        raise HTTPException(status_code=503, detail="Docker is not running")

    try:
        containers = client.containers.list(all=True)
        return [{"id": c.id, "name": c.name, "status": c.status} for c in containers]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/containers/run")
def run_container(image: str, name: str = None, command: str = None):
    """Run a new Docker container"""
    if client is None:
        raise HTTPException(status_code=503, detail="Docker is not running")

    try:
        container = client.containers.run(image, name=name, command=command, detach=True)
        return {"message": f"Container {container.id} started", "id": container.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/containers/stop/{container_id}")
def stop_container(container_id: str):
    """Stop a running container"""
    if client is None:
        raise HTTPException(status_code=503, detail="Docker is not running")

    try:
        container = client.containers.get(container_id)
        container.stop()
        return {"message": f"Container {container_id} stopped"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/containers/restart/{container_id}")
def restart_container(container_id: str):
    """Restart a container"""
    if client is None:
        raise HTTPException(status_code=503, detail="Docker is not running")

    try:
        container = client.containers.get(container_id)
        container.restart()
        return {"message": f"Container {container_id} restarted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/containers/logs/{container_id}")
def get_logs(container_id: str):
    """Fetch logs of a container"""
    if client is None:
        raise HTTPException(status_code=503, detail="Docker is not running")

    try:
        container = client.containers.get(container_id)
        logs = container.logs(tail=100).decode("utf-8")
        return {"logs": logs}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/containers/logs/stream/{container_id}")
async def stream_logs(container_id: str):
    """Stream container logs in real-time"""
    if client is None:
        raise HTTPException(status_code=503, detail="Docker is not running")

    try:
        container = client.containers.get(container_id)

        async def event_generator():
            for line in container.logs(stream=True, follow=True):
                yield line.decode("utf-8")

        return StreamingResponse(event_generator(), media_type="text/plain")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/containers/status/{container_id}")
def container_status(container_id: str):
    """Check if a container is running"""
    if client is None:
        raise HTTPException(status_code=503, detail="Docker is not running")

    try:
        container = client.containers.get(container_id)
        return {"id": container.id, "name": container.name, "status": container.status}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
