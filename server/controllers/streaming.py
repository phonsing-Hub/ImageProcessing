import cv2
from lib.face import Facerec

from lib.pahoMqtt import PahoMQTT
face = Facerec()
paho = PahoMQTT()


class OpenStreaming:
    def __init__(self):
        self.target_width = 1280
        self.target_height = 720
        self.led1_status = -1
        self.led2_status = -1
        paho.connect_mqtt()
        # face.load_encoding_images("images")

    def generate_video_stream(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise RuntimeError("Could not start video capture.")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (self.target_width, self.target_height))
            face_locations, face_names = face.detect_known_faces(frame)
            for face_loc, name in zip(face_locations, face_names):
                y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
                color = (0, 0, 200) if name == "Who are you?" else (200, 0, 0)
                new_led1_status, new_led2_status = (
                    (0, 1) if name == "Who are you?" else (1, 0)
                )

                if (
                    new_led1_status != self.led1_status
                    or new_led2_status != self.led2_status
                ):
                    # paho.publish({"LED1": new_led1_status, "LED2": new_led2_status})
                    self.led1_status, self.led2_status = (
                        new_led1_status,
                        new_led2_status,
                    )

                cv2.putText(
                    frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, color, 2
                )
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 4)

            _, buffer = cv2.imencode(".jpg", frame)
            frame_bytes = buffer.tobytes()
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
            )

        cap.release()
