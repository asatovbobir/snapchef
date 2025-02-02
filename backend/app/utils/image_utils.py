from pathlib import Path
from fastapi import UploadFile
import shutil
import base64
import logging

logging.basicConfig(level=logging.INFO)

async def save_temp_image(file: UploadFile, temp_dir: Path) -> Path:
    """Saves an uploaded image temporarily and returns its path."""
    temp_dir.mkdir(parents=True, exist_ok=True)
    file_path = temp_dir / file.filename

    logging.info(f"Saving image to: {file_path}")

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        logging.error(f"Error saving image: {e}")
        raise e

    if not file_path.exists():
        logging.error(f"Image file not found after saving: {file_path}")
        raise FileNotFoundError("Failed to save image.")

    logging.info(f"Image saved successfully: {file_path}")
    return file_path


def image_to_base64(image_path: Path) -> str:
    """Converts an image to base64 encoding."""
    if not image_path.exists():
        logging.error(f"Image file does not exist: {image_path}")
        raise FileNotFoundError(f"File not found: {image_path}")

    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        logging.error(f"Error encoding image to base64: {e}")
        raise e
