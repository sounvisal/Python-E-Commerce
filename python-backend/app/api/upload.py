import os
import re
import uuid
import shutil
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, HTTPException, status

router = APIRouter(prefix="/upload", tags=["File Uploads"])

# Target storage directories (Storefront and Admin public folders)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
FRONTEND_UPLOADS_DIR = os.path.join(PROJECT_ROOT, "frontend", "public", "images", "uploads")
ADMIN_UPLOADS_DIR = os.path.join(PROJECT_ROOT, "admin", "public", "images", "uploads")

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".svg", ".gif", ".avif"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

def ensure_directories():
    os.makedirs(FRONTEND_UPLOADS_DIR, exist_ok=True)
    os.makedirs(ADMIN_UPLOADS_DIR, exist_ok=True)

def sanitize_filename(filename: str) -> str:
    # Extract extension and base
    base, ext = os.path.splitext(filename)
    ext = ext.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format '{ext}'. Allowed formats: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
        )
    # Clean base name
    clean_base = re.sub(r'[^a-zA-Z0-9_\-]', '_', base).strip('_')[:30] or "asset"
    timestamp = datetime.now().strftime("%y%m%d%H%M%S")
    unique_suffix = uuid.uuid4().hex[:6]
    return f"{clean_base}_{timestamp}_{unique_suffix}{ext}"

@router.post("", status_code=status.HTTP_201_CREATED)
async def upload_single_file(file: UploadFile = File(...)):
    """
    Upload a single image or asset.
    Saves binary file to both Storefront and Admin public/images/uploads directories.
    Returns the public web URL (/images/uploads/filename.ext).
    """
    ensure_directories()
    
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided in upload payload."
        )

    safe_name = sanitize_filename(file.filename)
    frontend_path = os.path.join(FRONTEND_UPLOADS_DIR, safe_name)
    admin_path = os.path.join(ADMIN_UPLOADS_DIR, safe_name)

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File exceeds maximum allowed size of 10MB ({len(content)} bytes)."
        )

    # Write to frontend
    with open(frontend_path, "wb") as f:
        f.write(content)

    # Mirror copy to admin
    try:
        shutil.copyfile(frontend_path, admin_path)
    except Exception as e:
        print(f"[Upload] Warning: Could not mirror to admin: {e}")

    public_url = f"/images/uploads/{safe_name}"

    return {
        "status": "success",
        "message": "File uploaded and synchronized successfully",
        "data": {
            "filename": safe_name,
            "original_filename": file.filename,
            "url": public_url,
            "size": len(content),
            "content_type": file.content_type
        }
    }

@router.post("/multiple", status_code=status.HTTP_201_CREATED)
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    """
    Upload multiple images simultaneously for product galleries or review photo sets.
    """
    ensure_directories()
    uploaded = []

    for file in files:
        if not file.filename:
            continue
        safe_name = sanitize_filename(file.filename)
        frontend_path = os.path.join(FRONTEND_UPLOADS_DIR, safe_name)
        admin_path = os.path.join(ADMIN_UPLOADS_DIR, safe_name)

        content = await file.read()
        if len(content) > MAX_FILE_SIZE:
            continue

        with open(frontend_path, "wb") as f:
            f.write(content)

        try:
            shutil.copyfile(frontend_path, admin_path)
        except Exception:
            pass

        uploaded.append({
            "filename": safe_name,
            "original_filename": file.filename,
            "url": f"/images/uploads/{safe_name}",
            "size": len(content),
            "content_type": file.content_type
        })

    return {
        "status": "success",
        "message": f"Successfully uploaded {len(uploaded)} files",
        "data": uploaded
    }
