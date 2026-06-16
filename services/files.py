import os
import shutil

from fastapi import UploadFile


async def add_file(file: UploadFile | None):
    if file:
        name_dir = "image" if file.content_type.startswith("image/") else "other_file"
        os.makedirs(f"upload_files/{name_dir}", exist_ok=True)
        file_location = f"upload_files/{name_dir}/{name_dir}_{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return file_location
    return None
