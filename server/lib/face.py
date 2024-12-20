import face_recognition
import cv2
import os
import glob
import numpy as np
from db.db import execute_query  # นำเข้าฟังก์ชัน execute_query จาก db.py
import json


class Facerec:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []

        # Resize frame for a faster speed
        self.frame_resizing = 0.25


    async def load_encoding_images(self, person_name, images_path, note):
        image_files = glob.glob(os.path.join(images_path, "*.*"))
        print(f"{len(image_files)} encoding images found for {person_name}.")

        encodings = []
        imagename = []
        # Process each image file
        for img_path in image_files:
            img = cv2.imread(img_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            print(f"{img_path} encoding images found for {person_name}.")
            # Get encoding
            imagename.append(img_path)
            img_encoding = face_recognition.face_encodings(rgb_img)
            if img_encoding:
                encodings.append(
                    img_encoding[0]
                )  # Append the encoding if a face is found
            else:
                print(f"No face found in {img_path}")

        if encodings:
            avg_encoding = np.mean(encodings, axis=0)
            print(f"Encodings loaded and averaged for {person_name}")
            encoding_json = json.dumps(avg_encoding.tolist())
            image_json = json.dumps(imagename)
            insert_query = (
                "INSERT INTO CPE422.users (name, note, image_encoding, image_name) VALUES (%s,%s,%s,%s)"
            )
            result = execute_query(insert_query, (person_name, note, encoding_json, image_json))
            return result
        else:
            print(f"No valid encodings found in {images_path}")
            return None
    

    def detect_known_faces(self, frame):
        small_frame = cv2.resize(
            frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing
        )
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations
        )

        face_names = []
        for face_encoding in face_encodings:
            # Check if there are any known face encodings to compare with
            if not self.known_face_encodings:
                face_names.append("Who are you?")
                continue

            # Compare the face with known faces
            matches = face_recognition.compare_faces(
                self.known_face_encodings, face_encoding, tolerance=0.45
            )
            name = "Who are you?"

            # Use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(
                self.known_face_encodings, face_encoding
            )

            # Only proceed if face_distances has elements
            if face_distances.size > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
                    match_percentage = (
                        1 - face_distances[best_match_index]
                    ) * 100  # Calculate the match percentage
                    name = f"{name} ({match_percentage:.2f}%)"

            face_names.append(name)

        # Convert to numpy array to adjust coordinates with frame resizing quickly
        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing
        return face_locations.astype(int), face_names


#    def load_encoding_images(self, images_path):
#         """
#         Load encoding images from path
#         :param images_path: path to the folder containing subfolders of persons
#         :return:
#         """
#         # List all subfolders in the images_path (each subfolder corresponds to one person)
#         persons_folders = [
#             f for f in os.listdir(images_path)
#             if os.path.isdir(os.path.join(images_path, f))
#         ]

#         for person_folder in persons_folders:
#             person_path = os.path.join(images_path, person_folder)

#             # Load all image files from the person's folder
#             image_files = glob.glob(os.path.join(person_path, "*.*"))

#             print(f"{len(image_files)} encoding images found for {person_folder}.")

#             encodings = []  # To store all encodings for this person

#             # Store image encodings and names for each person
#             for img_path in image_files:
#                 img = cv2.imread(img_path)
#                 rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#                 # Get encoding
#                 img_encoding = face_recognition.face_encodings(rgb_img)
#                 if len(img_encoding) > 0:  # Check if there's a face found in the image
#                     # print(f"{img_path} images encoding:")
#                     # print(f"[{img_encoding}]")
#                     encodings.append(img_encoding[0])  # Append the encoding for averaging
#                 else:
#                     print(f"No face found in {img_path}")

#             if len(encodings) > 0:
#                 # Calculate the average encoding for this person
#                 avg_encoding = np.mean(encodings, axis=0)  # Average across all encodings
#                 print(f"images encoding Average: {avg_encoding} ")
#                 self.known_face_encodings.append(avg_encoding)
#                 self.known_face_names.append(person_folder)  # Use the folder name as the person's name
#             else:
#                 print(f"No valid encodings found for {person_folder}")

#         print("Encoding images loaded")
