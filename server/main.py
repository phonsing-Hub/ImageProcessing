from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi import HTTPException
from controllers.ImageProcessing import Img
from controllers.streaming import OpenStreaming
# from lib.face import Facerec
from typing import List

# face = Facerec()

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

# @app.post("/api/v1/upload")
# async def upload_images(name: str = Form(...), images: List[UploadFile] = File(...)):
#     if not images:
#         raise HTTPException(status_code=400, detail="No files provided")
#     Img_handler = Img(name)
#     await Img_handler.save(images)
#     result = await face.load_encoding_images(str(Img_handler.user_dir), name)
#     if result is None:
#         raise HTTPException(status_code=500, detail="Database error")
#     return {
#         "message": "Images uploaded successfully",
#         "directory": str(Img_handler.user_dir),
#         "saved_files": Img_handler.saved_files,
#     }


# Define a route for video streaming
@app.get("/video")
def video_feed():
    stm = OpenStreaming()
    return StreamingResponse(
        stm.generate_video_stream(), media_type="multipart/x-mixed-replace; boundary=frame"
    )

