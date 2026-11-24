from app.api.deps import get_current_user, get_optional_user
from app.core.config import settings
import os
import re
import uuid
import shutil
from datetime import datetime
from typing import List
from fastapi import Depends, APIRouter, UploadFile, File, HTTPException, status

def is_env_truthy(key: str, default: bool = False) -> bool:
    val = os.getenv(key)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")

def is_storage_enabled() -> bool:
    if is_env_truthy("DISABLE_UPLOADS", False):
        return False
    return True

def get_storage_type() -> str:
    if not is_storage_enabled():
        return "disabled"
    persistent = (os.getenv("PERSISTENT_STORAGE_DIR") or "").strip()
    if persistent:
        return "persistent"
    if not settings.PRODUCTION:
        return "local"
    return "ephemeral"

def require_local_uploads():
    if not is_storage_enabled():
        raise HTTPException(
            status_code=403,
            detail="Hosted file storage is disabled or read-only on this deployment. Configure persistent storage."
        )


router = APIRouter(prefix="/upload", tags=["File Uploads"])

# Target storage directories (Storefront, Admin, and Persistent Storage folders)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
PERSISTENT_DIR = (os.getenv("PERSISTENT_STORAGE_DIR") or "").strip()

if PERSISTENT_DIR:
    UPLOADS_DIR = os.path.join(PERSISTENT_DIR, "images", "uploads")
    VIDEOS_DIR = os.path.join(PERSISTENT_DIR, "videos")
else:
    UPLOADS_DIR = os.path.join(PROJECT_ROOT, "frontend", "public", "images", "uploads")
    VIDEOS_DIR = os.path.join(PROJECT_ROOT, "frontend", "public", "videos")

FRONTEND_UPLOADS_DIR = UPLOADS_DIR
ADMIN_UPLOADS_DIR = os.path.join(PROJECT_ROOT, "admin", "public", "images", "uploads")
FRONTEND_VIDEOS_DIR = VIDEOS_DIR
ADMIN_VIDEOS_DIR = os.path.join(PROJECT_ROOT, "admin", "public", "videos")
DIST_UPLOADS_DIR = os.path.join(PROJECT_ROOT, "frontend", "dist", "images", "uploads")
DIST_VIDEOS_DIR = os.path.join(PROJECT_ROOT, "frontend", "dist", "videos")

# Safe raster formats only (SVG excluded to prevent same-origin Stored XSS)
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}
ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".webm", ".mov", ".m4v", ".ogg"}
MAX_FILE_SIZE = 10 * 1024 * 1024       # 10 MB for images
MAX_VIDEO_SIZE = 50 * 1024 * 1024      # 50 MB for UGC video clips
CHUNK_SIZE = 64 * 1024                 # 64 KB streaming chunks

async def read_bounded_content(file: UploadFile, max_size: int) -> bytes:
    """Reads file content in bounded chunks to protect against memory exhaustion."""
    chunks = []
    total = 0
    while chunk := await file.read(CHUNK_SIZE):
        total += len(chunk)
        if total > max_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File exceeds maximum allowed size of {max_size // (1024 * 1024)}MB."
            )
        chunks.append(chunk)
    if total == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty files cannot be uploaded.")
    return b"".join(chunks)

@router.get("/status", dependencies=[Depends(get_current_user)])
def get_upload_status():
    """Check storage availability and readiness. Requires authenticated user."""
    enabled = is_storage_enabled()
    storage_type = get_storage_type()
    return {
        "status": "success",
        "data": {
            "enabled": enabled,
            "storage_type": storage_type,
            "max_image_mb": MAX_FILE_SIZE // (1024 * 1024),
            "max_video_mb": MAX_VIDEO_SIZE // (1024 * 1024),
            "allowed_formats": sorted(list(ALLOWED_EXTENSIONS))
        }
    }

def ensure_directories():
    os.makedirs(UPLOADS_DIR, exist_ok=True)
    os.makedirs(VIDEOS_DIR, exist_ok=True)
    os.makedirs(ADMIN_UPLOADS_DIR, exist_ok=True)
    os.makedirs(ADMIN_VIDEOS_DIR, exist_ok=True)
    if os.path.exists(os.path.dirname(DIST_UPLOADS_DIR)):
        os.makedirs(DIST_UPLOADS_DIR, exist_ok=True)
    if os.path.exists(os.path.dirname(DIST_VIDEOS_DIR)):
        os.makedirs(DIST_VIDEOS_DIR, exist_ok=True)

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

@router.post("", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user), Depends(require_local_uploads)])
async def upload_single_file(file: UploadFile = File(...)):
    """
    Upload a single image or asset.
    Saves binary file to both Storefront and Admin public/images/uploads directories.
    Returns the public web URL (/images/uploads/filename.ext).
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided in upload payload."
        )

    safe_name = sanitize_filename(file.filename)
    ensure_directories()
    primary_path = os.path.join(UPLOADS_DIR, safe_name)

    content = await read_bounded_content(file, MAX_FILE_SIZE)

    # Write to primary storage
    with open(primary_path, "wb") as f:
        f.write(content)

    # Mirror copy to admin and dist uploads if present
    for extra_dir in (ADMIN_UPLOADS_DIR, DIST_UPLOADS_DIR):
        if os.path.isdir(os.path.dirname(extra_dir)):
            try:
                os.makedirs(extra_dir, exist_ok=True)
                shutil.copyfile(primary_path, os.path.join(extra_dir, safe_name))
            except Exception:
                pass

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

@router.post("/multiple", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user), Depends(require_local_uploads)])
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    """
    Upload multiple images simultaneously for product galleries or review photo sets.
    """
    ensure_directories()
    uploaded = []

    for file in files:
        if not file.filename:
            continue
        try:
            safe_name = sanitize_filename(file.filename)
        except HTTPException:
            continue
        primary_path = os.path.join(UPLOADS_DIR, safe_name)

        try:
            content = await read_bounded_content(file, MAX_FILE_SIZE)
        except HTTPException:
            continue

        with open(primary_path, "wb") as f:
            f.write(content)

        for extra_dir in (ADMIN_UPLOADS_DIR, DIST_UPLOADS_DIR):
            if os.path.isdir(os.path.dirname(extra_dir)):
                try:
                    os.makedirs(extra_dir, exist_ok=True)
                    shutil.copyfile(primary_path, os.path.join(extra_dir, safe_name))
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

def sanitize_video_filename(filename: str) -> str:
    base, ext = os.path.splitext(filename)
    ext = ext.lower()
    if ext not in ALLOWED_VIDEO_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported video format '{ext}'. Allowed formats: {', '.join(sorted(ALLOWED_VIDEO_EXTENSIONS))}"
        )
    clean_base = re.sub(r'[^a-zA-Z0-9_\-]', '_', base).strip('_')[:30] or "video_review"
    timestamp = datetime.now().strftime("%y%m%d%H%M%S")
    unique_suffix = uuid.uuid4().hex[:6]
    return f"{clean_base}_{timestamp}_{unique_suffix}{ext}"

@router.post("/video", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user), Depends(require_local_uploads)])
async def upload_video_file(file: UploadFile = File(...)):
    """
    Upload a short-form video review or product texture masterclass clip.
    Saves binary stream to Storefront and Admin public/videos directories.
    Returns the public web URL (/videos/filename.mp4).
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided in video upload payload."
        )

    safe_name = sanitize_video_filename(file.filename)
    ensure_directories()
    primary_path = os.path.join(VIDEOS_DIR, safe_name)

    content = await read_bounded_content(file, MAX_VIDEO_SIZE)

    # Write to primary videos storage
    with open(primary_path, "wb") as f:
        f.write(content)

    # Mirror copy to admin and dist videos if present
    for extra_dir in (ADMIN_VIDEOS_DIR, DIST_VIDEOS_DIR):
        if os.path.isdir(os.path.dirname(extra_dir)):
            try:
                os.makedirs(extra_dir, exist_ok=True)
                shutil.copyfile(primary_path, os.path.join(extra_dir, safe_name))
            except Exception:
                pass

    public_url = f"/videos/{safe_name}"

    return {
        "status": "success",
        "message": "Video uploaded and synchronized successfully",
        "data": {
            "filename": safe_name,
            "original_filename": file.filename,
            "url": public_url,
            "size": len(content),
            "content_type": file.content_type
        }
    }

