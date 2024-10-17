import cv2
from face import Facerec
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

# Initialize FastAPI app
app = FastAPI()

# Encode faces from a folder
sfr = Facerec()
sfr.load_encoding_images("images/")

# Define a generator function for video streaming
def generate_video_stream():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detect Faces
        face_locations, face_names = sfr.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

            cv2.putText(
                frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2
            )
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

        # Encode frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Yield the frame in multipart format
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
        )

    cap.release()
    cv2.destroyAllWindows()

# Define a route for video streaming
@app.get("/video")
def video_feed():
    return StreamingResponse(generate_video_stream(), media_type="multipart/x-mixed-replace; boundary=frame")
