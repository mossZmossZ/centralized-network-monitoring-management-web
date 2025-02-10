from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter(prefix="/api/files", tags=["files"])

GENERATED_REPORTS_DIR = "generated_reports"
os.makedirs(GENERATED_REPORTS_DIR, exist_ok=True)


@router.get("/")
async def list_files():
    return os.listdir(GENERATED_REPORTS_DIR)


@router.get("/download/{filename}")
async def download_file(filename: str):
    filepath = os.path.join(GENERATED_REPORTS_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(filepath, filename=filename)


@router.get("/view/{filename}")
async def view_file(filename: str):
    filepath = os.path.join(GENERATED_REPORTS_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(filepath, media_type="application/pdf")