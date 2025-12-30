from fastapi import UploadFile
from PIL import Image
import os
import uuid
from app.config import settings
from io import BytesIO

async def save_and_compress_image(file: UploadFile, report_id: int) -> str:
    """Save and compress uploaded image"""
    
    # Create uploads directory if not exists
    upload_dir = os.path.join(settings.UPLOAD_DIR, "reports", str(report_id))
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    file_ext = os.path.splitext(file.filename)[1].lower()
    unique_filename = f"{uuid.uuid4()}.webp"  # Always save as WebP
    file_path = os.path.join(upload_dir, unique_filename)
    
    # Read image
    contents = await file.read()
    image = Image.open(BytesIO(contents))
    
    # Convert to RGB if necessary
    if image.mode in ('RGBA', 'LA', 'P'):
        image = image.convert('RGB')
    
    # Resize if too large
    max_size = (1200, 1200)
    image.thumbnail(max_size, Image.Resampling.LANCZOS)
    
    # Save as WebP with compression
    image.save(file_path, 'WEBP', quality=75, optimize=True)
    
    # Return relative path
    relative_path = os.path.join("reports", str(report_id), unique_filename)
    return relative_path

def delete_image(image_path: str):
    """Delete image file"""
    full_path = os.path.join(settings.UPLOAD_DIR, image_path)
    if os.path.exists(full_path):
        os.remove(full_path)
