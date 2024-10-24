from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import BackgroundTasks
from fastapi.responses import StreamingResponse
from pahoMqtt import PahoMQTT
from face import Facerec
import cv2

paho = PahoMQTT()
paho.connect_mqtt()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sfr = Facerec()
sfr.load_encoding_images("images/")

def generate_video_stream():
    cap = cv2.VideoCapture(0)

    target_width = 1280
    target_height = 720
    led1_status = -1 
    led2_status = -1 

    while True:
        ret, frame = cap.read()
        if not ret:
            break
       
        frame = cv2.resize(frame, (target_width, target_height))

        face_locations, face_names = sfr.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

            if name == "Who are you?":
                color = (0, 0, 200) 
                new_led1_status = 0
                new_led2_status = 1
            else:
                color = (200, 0, 0)
                new_led1_status = 1
                new_led2_status = 0
                
            if new_led1_status != led1_status or new_led2_status != led2_status:
                paho.publish({"LED1": new_led1_status, "LED2": new_led2_status})
                led1_status = new_led1_status
                led2_status = new_led2_status

            cv2.putText(
                frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, color, 2
            )
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 4)

        _, buffer = cv2.imencode(".jpg", frame)
        frame_bytes = buffer.tobytes()

        yield (
            b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
        )

    cap.release()
    cv2.destroyAllWindows()

# Define a route for video streaming
@app.get("/video")
def video_feed():
    return StreamingResponse(
        generate_video_stream(), media_type="multipart/x-mixed-replace; boundary=frame"
    )

# @app.get("/mqtt")
# def send_mqtt(background_tasks: BackgroundTasks):
#     background_tasks.add_task(paho.publish(), paho.connect_mqtt())
#     return "send_mqtt success"
