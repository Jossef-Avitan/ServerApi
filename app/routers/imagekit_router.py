from fastapi import APIRouter, UploadFile, File, Query
from app.services.imagekit_service import ImageKitService

router = APIRouter(prefix="/api/imagekit", tags=["imagekit"])
imagekit_service = ImageKitService()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    file_id: str = Query(..., description="מזהה ייחודי לקובץ - ישמש ככתובת הגישה"),
    file_name: str = Query(..., description="שם הקובץ שיישמר במערכת")
):
    """
    העלאת קובץ לשרת ImageKit
    - מקבל קובץ, מזהה ייחודי ושם קובץ
    - מחזיר את פרטי הקובץ כולל כתובת URL לגישה
    """
    result = await imagekit_service.upload_file(
        file=file.file,
        file_name=file_name,
        custom_id=file_id
    )
    
    return {
        "status": "success",
        "file_id": file_id,
        "file_name": file_name,
        "access_url": f"{result['url']}",
        "direct_url": f"{result['thumbnail_url']}"
    }

@router.get("/files/{file_id}")
async def get_file(file_id: str):
    """נקודת קצה לקבלת קובץ לפי ID"""
    file = await imagekit_service.get_file_by_id(file_id)
    return {"status": "success", "data": file}

@router.get("/files")
async def get_files():
    """נקודת קצה לקבלת רשימת קבצים"""
    files = await imagekit_service.get_file_list()
    return {"status": "success", "data": files} 