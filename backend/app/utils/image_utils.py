from pathlib import Path
from fastapi import UploadFile
import shutil
import base64

async def save_temp_image(file: UploadFile, temp_dir: Path) -> Path:
    temp_dir.mkdir(parents=True, exist_ok=True)
    file_path = temp_dir / file.filename
    
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return file_path

def image_to_base64(image_path: Path) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")