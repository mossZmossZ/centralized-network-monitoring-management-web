# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Import routers
from report_api import router as report_router
from file_manager import router as file_manager_router
from alert_gateway import router as alert_router
from customDailyreportAPI import router as custom_report_router  # Import from the same level

# Load environment variables
load_dotenv()

# Set up environment variables for TeX (if needed)
os.environ["PATH"] = "/Library/TeX/texbin:" + os.environ.get("PATH", "")

# Initialize FastAPI app
app = FastAPI()

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    #allow_origins=["http://localhost:5173"],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/debug/path")
async def debug_path():
    return {"PATH": os.environ.get("PATH")}

# Include all routers including the new custom report router

app.include_router(report_router)
app.include_router(file_manager_router)
app.include_router(alert_router)
app.include_router(custom_report_router)  # Include the custom report router

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
