from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv


from websocket_router import websocket_router  # Import your websocket router
# Import routers
from file_manager import router as file_manager_router
from alert_gateway import router as alert_router
from customReportAPI import router as custom_report_router
from scheduleReportAPI import router as schedule_report_router
from database_manager_API import router as db_router
from user_authen import router as auth_router
from maintenance_router import router as maintenance_router
from init_db import init_db
# Load environment variables
load_dotenv()

# Set up environment variables for TeX (if needed)
os.environ["PATH"] = "/Library/TeX/texbin:" + os.environ.get("PATH", "")

# Initialize FastAPI app
app = FastAPI(root_path="/api")

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
init_db()

@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI with WebSocket"}

# Include all routers including the new custom report router
app.include_router(file_manager_router)
app.include_router(alert_router)
app.include_router(custom_report_router)
app.include_router(schedule_report_router)
app.include_router(websocket_router)  # Include the websocket router
app.include_router(db_router)
app.include_router(auth_router)
app.include_router(maintenance_router)