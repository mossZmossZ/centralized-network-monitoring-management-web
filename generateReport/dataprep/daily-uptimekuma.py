import os
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# API URL and Token from environment variables
uptime_kuma_api_url = os.getenv('UPTIME_KUMA_API_URL')  # Base API URL, e.g., http://localhost:3001
uptime_kuma_api_token = os.getenv('UPTIME_KUMA_API_TOKEN')

# Example endpoint to fetch all monitors
monitors_url = f"{uptime_kuma_api_url}/api/monitors"

# Example request header with the API token
headers = {
    "Authorization": f"Bearer {uptime_kuma_api_token}",  # Authorization using Bearer token
    "Content-Type": "application/json"
}

# Send a GET request to fetch all monitors
response = requests.get(monitors_url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    monitors_data = response.json()  # Assuming the response is JSON
    print("Monitors List: ", monitors_data)  # Print the full list of monitors to find the monitor_id

    # Optionally: Format the output to show only relevant details like monitor name and ID
    for monitor in monitors_data:
        print(f"Monitor ID: {monitor['id']}, Name: {monitor['name']}")
else:
    print("Error fetching monitors:", response.status_code)
