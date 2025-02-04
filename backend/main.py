from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from ping_service import router as ping_router, update_ping_status
from docker_service import router as docker_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(update_ping_status())

app.include_router(ping_router)
app.include_router(docker_router)
