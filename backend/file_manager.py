import os
from fastapi import APIRouter
from fastapi.responses import FileResponse
from fastapi import FastAPI, HTTPException

router = APIRouter(tags=["File_manager-Custom"])

# Define the directories for daily, weekly, and monthly reports
REPORTS_BASE_PATH = "generated_reports/custom_report"
REPORTS_BASE_PATH_SCHEDULE = "generated_reports/schedule_report"
def list_files_in_directory(directory):
    """Utility function to list files in a given directory."""
    files = []
    if os.path.exists(directory):
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return files

@router.get("/custom/files")
async def get_files():
    """Endpoint to return the files categorized by daily, weekly, and monthly."""
    daily_files = list_files_in_directory(os.path.join(REPORTS_BASE_PATH, "daily"))
    weekly_files = list_files_in_directory(os.path.join(REPORTS_BASE_PATH, "weekly"))
    monthly_files = list_files_in_directory(os.path.join(REPORTS_BASE_PATH, "monthly"))

    return {
        "daily": daily_files,
        "weekly": weekly_files,
        "monthly": monthly_files
    }

@router.get("/schedule/files")
async def get_files_schedule():
    """Endpoint to return the files categorized by daily, weekly, and monthly."""
    daily_files = list_files_in_directory(os.path.join(REPORTS_BASE_PATH_SCHEDULE, "daily"))
    weekly_files = list_files_in_directory(os.path.join(REPORTS_BASE_PATH_SCHEDULE, "weekly"))
    monthly_files = list_files_in_directory(os.path.join(REPORTS_BASE_PATH_SCHEDULE, "monthly"))

    return {
        "daily": daily_files,
        "weekly": weekly_files,
        "monthly": monthly_files
    }

@router.get("/custom/files/{file_type}/{file_name}/preview")
async def preview_file(file_type: str, file_name: str):
    file_path = os.path.join(REPORTS_BASE_PATH, file_type, file_name)
    print(file_path)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Send the PDF file as a response with appropriate content type
    return FileResponse(file_path, media_type="application/pdf")

@router.get("/schedule/files/{file_type}/{file_name}/preview")
async def preview_file_schedule(file_type: str, file_name: str):
    file_path = os.path.join(REPORTS_BASE_PATH_SCHEDULE, file_type, file_name)
    print(file_path)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Send the PDF file as a response with appropriate content type
    return FileResponse(file_path, media_type="application/pdf")

@router.get("/custom/files/{file_type}/{file_name}/download")
async def download_file(file_type: str, file_name: str):
    file_path = os.path.join(REPORTS_BASE_PATH, file_type, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Send the file as a response with the Content-Disposition header to prompt download
    return FileResponse(file_path, media_type="application/pdf", headers={
        "Content-Disposition": f"attachment; filename={file_name}"
    })

@router.get("/schedule/files/{file_type}/{file_name}/download")
async def download_file_schedule(file_type: str, file_name: str):
    file_path = os.path.join(REPORTS_BASE_PATH_SCHEDULE, file_type, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Send the file as a response with the Content-Disposition header to prompt download
    return FileResponse(file_path, media_type="application/pdf", headers={
        "Content-Disposition": f"attachment; filename={file_name}"
    })

@router.delete("/custom/files/{file_type}/{file_name}")
async def delete_file(file_type: str, file_name: str):
    file_path = os.path.join(REPORTS_BASE_PATH, file_type, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Attempt to delete the file
    try:
        os.remove(file_path)
        return {"message": f"File '{file_name}' has been deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")
    
@router.delete("/schedule/files/{file_type}/{file_name}")
async def delete_file(file_type: str, file_name: str):
    file_path = os.path.join(REPORTS_BASE_PATH_SCHEDULE, file_type, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Attempt to delete the file
    try:
        os.remove(file_path)
        return {"message": f"File '{file_name}' has been deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")