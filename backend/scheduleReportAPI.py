from fastapi import APIRouter, BackgroundTasks, HTTPException
import datetime
import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from dateutil.relativedelta import relativedelta
from monthlyReport.monthly_report_generate import build_report
from weeklyReport.weekly_report_generate import build_report
from dailyReport.daily_report_generate import build_report
from websocket_router import ws_manager
import threading

# Define the full absolute path to save the generated reports
REPORTS_FOLDER_MONTHLY = os.path.join('generated_reports', 'schedule_report', 'monthly')
REPORTS_FOLDER_WEEKLY = os.path.join('generated_reports', 'schedule_report', 'weekly')
REPORTS_FOLDER_DAILY = os.path.join('generated_reports', 'schedule_report', 'daily')

# FastAPI Router for Schedule Reports (No need for manual triggering)
router = APIRouter(prefix="/api/report", tags=["report-schedule"])

# Ensure the reports folder exists (create if it doesn't)
for folder in [REPORTS_FOLDER_MONTHLY, REPORTS_FOLDER_WEEKLY, REPORTS_FOLDER_DAILY]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Helper function to generate unique report filename
def get_unique_filename(base_path: str):
    version = 1
    file_path = base_path
    while os.path.exists(file_path):
        version += 1
        file_path = f"{base_path.rsplit('.', 1)[0]}-{version}.pdf"
    return file_path

# Schedule Reports (Triggered by APScheduler)
def generate_daily_report():
    today = str(datetime.date.today())
    schedule_report_name = f"schedule-{today}-Monitoring_Report.pdf"
    report_path = os.path.join(REPORTS_FOLDER_DAILY, schedule_report_name)
    unique_report_path = get_unique_filename(report_path)
    print(f"Saving daily report to: {unique_report_path}")
    build_report(unique_report_path)
    # Notify WebSocket clients
    ws_manager.send_notification(f"Daily Report generated successfully")

def generate_weekly_report():
    today = str(datetime.date.today())
    schedule_report_name = f"schedule-{today}-Weekly-Monitoring_Report.pdf"
    report_path = os.path.join(REPORTS_FOLDER_WEEKLY, schedule_report_name)
    unique_report_path = get_unique_filename(report_path)
    print(f"Saving weekly report to: {unique_report_path}")
    build_report(unique_report_path)
    # Notify WebSocket clients
    ws_manager.send_notification(f"Weekly Report generated successfully")

def generate_monthly_report():
    today = str(datetime.date.today())
    schedule_report_name = f"schedule-{today}-monthly-Monitoring_Report.pdf"
    report_path = os.path.join(REPORTS_FOLDER_MONTHLY, schedule_report_name)
    unique_report_path = get_unique_filename(report_path)
    print(f"Saving monthly report to: {unique_report_path}")
    build_report(unique_report_path)
    # Notify WebSocket clients
    ws_manager.send_notification(f"Monthly Report generated successfully")

# Set up scheduler to run daily, weekly, and monthly tasks using Cron triggers
def start_scheduler():
    scheduler = BackgroundScheduler()
    
    # Cron trigger for daily report at midnight
    scheduler.add_job(generate_daily_report, 'cron', hour=0, minute=0)  # Every day at midnight
    
    # Cron trigger for weekly report every Sunday at midnight
    scheduler.add_job(generate_weekly_report, 'cron', day_of_week='sun', hour=0, minute=0)  # Every Sunday at midnight
    
    # Cron trigger for monthly report on the 1st of the month at midnight
    scheduler.add_job(generate_monthly_report, 'cron', day=1, hour=0, minute=0)  # Every 1st of the month at midnight
    
    scheduler.start()
    
    print("Scheduler started")

# Endpoint to manually start the scheduler
@router.post("/start-scheduler")
async def start_scheduler_endpoint():
    try:
        # Run the scheduler in a separate thread to avoid blocking FastAPI startup
        threading.Thread(target=start_scheduler, daemon=True).start()
        return {"message": "Scheduler started in the background"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start scheduler: {str(e)}")

# Function to get the next Sunday for the weekly report
def get_next_weekly_report_time(today: datetime.datetime):
    days_until_next_sunday = (6 - today.weekday()) % 7  # 6 = Sunday
    if days_until_next_sunday == 0:  # If today is Sunday, schedule next Sunday
        days_until_next_sunday = 7
    
    next_sunday = today + datetime.timedelta(days=days_until_next_sunday)
    next_sunday = next_sunday.replace(hour=0, minute=0, second=0, microsecond=0)  # Set to midnight
    return next_sunday

# Endpoint to get the next report times (daily, weekly, monthly)
@router.get("/next-schedule")
async def get_next_schedule():
    now = datetime.datetime.now()

    # Next daily report time is the next midnight
    next_daily_report_time = datetime.datetime(now.year, now.month, now.day, 0, 0) + datetime.timedelta(days=1)
    
    # Next weekly report time is the next Sunday at midnight
    next_weekly_report_time = get_next_weekly_report_time(now)
    
    # Next monthly report time is the first day of next month at midnight
    next_monthly_report_time = datetime.datetime(now.year, now.month, 1, 0, 0) + relativedelta(months=1)

    return {
        "next_daily_report": next_daily_report_time,
        "next_weekly_report": next_weekly_report_time,
        "next_monthly_report": next_monthly_report_time,
    }

# Schedule Reports (Triggered by APScheduler)
@router.get("/generate_daily_report_API")
async def generate_daily_report_API():
    today = str(datetime.date.today())
    schedule_report_name = f"schedule-{today}-Monitoring_Report.pdf"
    report_path = os.path.join(REPORTS_FOLDER_DAILY, schedule_report_name)
    unique_report_path = get_unique_filename(report_path)
    print(f"Saving daily report to: {unique_report_path}")
    build_report(unique_report_path)
    # Notify WebSocket clients
    await ws_manager.send_notification(f"Daily Report generated successfully")
    return(f"Daily Report generated successfully: {unique_report_path}")

@router.get("/generate_weekly_report_API")
async def generate_weekly_report_API():
    today = str(datetime.date.today())
    schedule_report_name = f"schedule-{today}-Weekly-Monitoring_Report.pdf"
    report_path = os.path.join(REPORTS_FOLDER_WEEKLY, schedule_report_name)
    unique_report_path = get_unique_filename(report_path)
    print(f"Saving weekly report to: {unique_report_path}")
    build_report(unique_report_path)
    # Notify WebSocket clients
    await ws_manager.send_notification(f"Weekly Report generated successfully")
    return(f"Weekly Report generated successfully: {unique_report_path}")

@router.get("/generate_monthly_report_API")
async def generate_monthly_report_API():
    today = str(datetime.date.today())
    schedule_report_name = f"schedule-{today}-monthly-Monitoring_Report.pdf"
    report_path = os.path.join(REPORTS_FOLDER_MONTHLY, schedule_report_name)
    unique_report_path = get_unique_filename(report_path)
    print(f"Saving monthly report to: {unique_report_path}")
    build_report(unique_report_path)
    # Notify WebSocket clients
    await ws_manager.send_notification(f"Monthly Report generated successfully")
    return(f"Monthly Report generated successfully: {unique_report_path}")