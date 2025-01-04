from imagekitio import ImageKit
from app.config import settings

class ImageKitService:
    def __init__(self):
        self.imagekit = ImageKit(
            private_key=settings.IMAGEKIT_PRIVATE_KEY,
            public_key=settings.IMAGEKIT_PUBLIC_KEY,
            url_endpoint=settings.IMAGEKIT_URL_ENDPOINT
        )

    async def upload_file(self, file, file_name, custom_id=None):
        """העלאת קובץ ל-ImageKit עם ID מותאם אישית"""
        try:
            upload = self.imagekit.upload_file(
                file=file,
                file_name=file_name,
                options={
                    "responseFields": ["tags", "customCoordinates", "url"],
                    "useUniqueFileName": False,  # משתמש בשם המקורי
                    "fileName": custom_id if custom_id else file_name  # משתמש ב-ID מותאם אם סופק
                }
            )
            return {
                "id": upload.get("fileId"),
                "name": upload.get("name"),
                "url": upload.get("url"),
                "thumbnail_url": f"{settings.IMAGEKIT_URL_ENDPOINT}/{custom_id if custom_id else upload.get('name')}"
            }
        except Exception as e:
            raise Exception(f"שגיאה בהעלאת הקובץ: {str(e)}")

    async def get_file_by_id(self, file_id):
        """קבלת קובץ לפי ID"""
        try:
            file_url = f"{settings.IMAGEKIT_URL_ENDPOINT}/{file_id}"
            return {"url": file_url}
        except Exception as e:
            raise Exception(f"שגיאה בקבלת הקובץ: {str(e)}")

    async def get_file_list(self):
        """קבלת רשימת הקבצים מ-ImageKit"""
        try:
            files = self.imagekit.list_files()
            return files
        except Exception as e:
            raise Exception(f"שגיאה בקבלת רשימת הקבצים: {str(e)}") 