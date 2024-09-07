# YOLOv8 Face Detection and Recognition

This project demonstrates how to use **YOLOv8** for real-time face detection and **Face Recognition** to identify known faces. The system captures video from a webcam, detects faces using YOLOv8, and recognizes them using a pre-trained Face Recognition model.

## Requirements

To run this project, you'll need to install the following dependencies:

- `ultralytics` (for YOLOv8)
- `face-recognition` (for face recognition)
- `opencv-python` (for handling video capture)

### Installation

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv yolov8-face-recognition-env
   source yolov8-face-recognition-env/bin/activate  # On macOS/Linux
   # On Windows:
   # yolov8-face-recognition-env\Scripts\activate

2. Install the required libraries:

   ```bash
   pip install ultralytics face-recognition opencv-python
   ```

## Running the Project

 - Download the YOLOv8 weights file yolov8n.pt or the version you want from the [ Ultralytics repository.](https://awesomeopensource.com/project/elangosundar/awesome-README-templates)
 - Place a reference image named your.jpg (or modify the script to use your own image) in the same directory
 - Run the Python script

  ```bash
  python yolov8_face_recognition.py
  ```


## How It Works
- YOLOv8 detects faces in the video feed in real-time.
- The detected face is extracted and passed to the Face Recognition model to identify if it matches a known face.
- The bounding box and name of the recognized face (if matched) will be displayed on the video feed.

## Customizing for Your Own Faces
To recognize different faces, replace the image `your.jpg` with your own image, and adjust the `known_names` list accordingly. Make sure the image file name matches the one in the script or update the script to load the correct image.

## Exit the Program
Press `q` to exit the program and release the camera.

## Troubleshooting
- Ensure your webcam is working properly and accessible by OpenCV.
- Make sure the known face image has clear and recognizable facial features for accurate recognition.
- For faster performance, you can use the `yolov8n.pt` (nano) model for YOLOv8, which is optimized for speed.

## License




[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

