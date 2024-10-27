from pathlib import Path
from typing import List
from fastapi import UploadFile
from datetime import datetime

class Img:
    def __init__(self, name: str):
        self.base_dir = Path("public")
        self.user_dir = self.base_dir / name
        self.user_dir.mkdir(parents=True, exist_ok=True)
        self.saved_files = []
        self.timestamp = ""

    async def save(self, images: List[UploadFile]):
        for image in images:
            # Generate a timestamped filename
            self.timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S:%f")
            extension = Path(image.filename).suffix
            new_filename = f"{self.timestamp}{extension}"
            image_path = self.user_dir / new_filename
            
            # Save the file
            with open(image_path, "wb") as f:
                content = await image.read()
                f.write(content)
            
            self.saved_files.append(new_filename)
