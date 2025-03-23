# customReport/daily/customDailyreportAPI.py
from fastapi import APIRouter
from pydantic import BaseModel
import datetime
import os

# Absolute import from the daily-report folder
from dailyReport.daily_report_generate import build_report

# Define the request model for the POST API
class DateRequest(BaseModel):
    date: str  # The date in the format YYYY-MM-DD

# Create a new router
router = APIRouter()

# Define the full absolute path to save the generated reports (custom_report/daily inside the generated_reports folder)
REPORTS_FOLDER = os.path.join('generated_reports', 'custom_report', 'daily')

# Ensure the reports folder exists (create if it doesn't)
if not os.path.exists(REPORTS_FOLDER):
    print(f"Creating directory: {REPORTS_FOLDER}")  # Debugging print statement
    os.makedirs(REPORTS_FOLDER)

def get_unique_filename(base_path: str):
    """Generate a unique filename by appending a version number if needed."""
    version = 1
    file_path = base_path
    while os.path.exists(file_path):  # Check if the file already exists
        version += 1  # Increment version number
        file_path = f"{base_path.rsplit('.', 1)[0]}-{version}.pdf"  # Append version number to filename
    return file_path

@router.post("/custom-daily-report")
async def custom_daily_report(data: DateRequest):
    # Validate and format the date from the request
    try:
        # Try to parse the date in case it's incorrect
        date_object = datetime.datetime.strptime(data.date, "%Y-%m-%d")
    except ValueError:
        return {"error": "Invalid date format, expected YYYY-MM-DD."}
    
    # Generate the custom report name
    custom_report_name = f"Custom-{data.date}-Monitoring_Report.pdf"
    
    # Define the full path to save the report in the 'daily' folder
    report_path = os.path.join(REPORTS_FOLDER, custom_report_name)
    
    # Ensure the filename is unique (handle versioning if the file already exists)
    unique_report_path = get_unique_filename(report_path)
    
    # Debugging: Print the path to ensure it's correct
    print(f"Saving report to: {unique_report_path}")  # This will show the exact location of where the file is being saved

    # Call the build_report function with the full path for saving the report
    build_report(unique_report_path)
    
    return {"message": f"Custom daily report generated: {unique_report_path}"}
