from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from controllers.ImageProcessing import Img
from controllers.streaming import OpenStreaming
from lib.face import Facerec
from typing import List
from db.db import execute_query  # นำเข้าฟังก์ชัน execute_query จาก db.py
import json

face = Facerec()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/public", StaticFiles(directory="public"), name="public")


@app.get("/")
def Hello():
    return {"message": "Hello Word"}


@app.post("/api/v1/upload")
async def upload_images(name: str = Form(...),note: str = Form(...), images: List[UploadFile] = File(...)):
    if not images:
        raise HTTPException(status_code=400, detail="No files provided")
    Img_handler = Img(name)
    await Img_handler.save(images)
    result = await face.load_encoding_images(name, str(Img_handler.user_dir),note)
    if result is None:
        raise HTTPException(status_code=500, detail="Database error")
    raise HTTPException(status_code=201, detail={
        "message": "Images uploaded successfully"
    })

@app.get("/api/v1/users")
async def get_users():
    select_query = "SELECT id, name, note, image_name FROM CPE422.users"
    result = execute_query(select_query)
    if result is None:
        raise HTTPException(status_code=500, detail="Database query failed.")
    elif not result:
        raise HTTPException(status_code=404, detail="No users found.")
    response_data = []
    for data in result:
        if "image_name" in data and data["image_name"]:
            data["image_name"] = json.loads(data["image_name"])  # Parse image_name
        response_data.append({
            "key": data["id"],
            "name": data["name"],
            "note": data["note"],
            "image_name": data["image_name"]
        })
    
    return JSONResponse(status_code=200, content=response_data)

@app.get("/api/v1/video")
def video_feed():
    stm = OpenStreaming()
    return StreamingResponse(
        stm.generate_video_stream(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )
 