from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from ping_service import router as ping_router, update_ping_status
from docker_service import router as docker_router
from report_api import router as report_router
from file_manager import router as file_manager_router

import os
import subprocess
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

@app.get("/debug/pdflatex")
async def debug_pdflatex():
    try:
        output = subprocess.check_output(["pdflatex", "--version"])
        return {"pdflatex_version": output.decode("utf-8")}
    except FileNotFoundError:
        return {"error": "pdflatex not found"}

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(update_ping_status())

app.include_router(ping_router)
app.include_router(docker_router)
app.include_router(report_router)
app.include_router(file_manager_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)