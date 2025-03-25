from fastapi import APIRouter, HTTPException
import httpx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

router = APIRouter(tags=["Alert"])

# Get Google Chat webhook URL from .env
GOOGLE_CHAT_WEBHOOK_URL = os.getenv("GOOGLE_CHAT_WEBHOOK_URL")

if not GOOGLE_CHAT_WEBHOOK_URL:
    raise ValueError("GOOGLE_CHAT_WEBHOOK_URL is not set in the .env file")

@router.post("/send_alert")
async def send_alert(alert_data: dict):
    """
    Endpoint to send alerts to Google Chat
    """
    message = {
        "text": f"🚨 *ALERT*: {alert_data.get('message', 'No details provided.')}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GOOGLE_CHAT_WEBHOOK_URL, json=message)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to send alert to Google Chat")

    return {"status": "Alert sent successfully"}
