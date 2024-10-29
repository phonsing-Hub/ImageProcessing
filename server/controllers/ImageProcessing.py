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
        for index, image in enumerate(images):
            extension = Path(image.filename).suffix
            new_filename = f"img{index}{extension}"
            image_path = self.user_dir / new_filename

            content = await image.read()
            with open(image_path, "wb") as f:
                f.write(content)

            self.saved_files.append(new_filename)
            