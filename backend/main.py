from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import os
import subprocess
from dotenv import load_dotenv

# Import routers
from ping_service import router as ping_router, update_ping_status
from docker_service import router as docker_router
from report_api import router as report_router
from file_manager import router as file_manager_router
from alert_gateway import router as alert_router  # Import the new alert router
from zabbix_daily_data_api import router as zabbix_router
# Load environment variables
load_dotenv()

os.environ["PATH"] = "/Library/TeX/texbin:" + os.environ.get("PATH", "")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/debug/path")
async def debug_path():
    return {"PATH": os.environ.get("PATH")}


# Include routers
app.include_router(docker_router)
app.include_router(report_router)
app.include_router(file_manager_router)
app.include_router(alert_router)  # Include alert gateway router
app.include_router(zabbix_router, prefix="/zabbix", tags=["Zabbix"])
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
