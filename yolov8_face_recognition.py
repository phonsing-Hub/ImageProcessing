import cv2
from ultralytics import YOLO
import face_recognition

# โหลด YOLOv8 model
model = YOLO('yolov8n.pt')  # ใช้เวอร์ชัน 'nano' สำหรับความเร็ว

# เปิดกล้อง
cap = cv2.VideoCapture(0)

# โหลดภาพฐานข้อมูลใบหน้าที่รู้จัก
known_image = face_recognition.load_image_file("name.jpg")
known_encoding = face_recognition.face_encodings(known_image)[0]

# ระบุชื่อบุคคล
known_faces = [known_encoding]
known_names = ["name"]

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # ใช้ YOLO ในการตรวจจับใบหน้า
    results = model(frame)

    for r in results:
        for box in r.boxes.xyxy:
            x1, y1, x2, y2 = map(int, box)
            face_img = frame[y1:y2, x1:x2]

            # แปลงภาพใบหน้าที่ตรวจจับได้เพื่อใช้กับ face_recognition
            rgb_face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
            face_encodings = face_recognition.face_encodings(rgb_face_img)

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_faces, face_encoding)
                name = "Unknown"

                if True in matches:
                    match_index = matches.index(True)
                    name = known_names[match_index]

                # วาดกรอบและแสดงชื่อ
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    # แสดงผล
    cv2.imshow("YOLOv8 Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
