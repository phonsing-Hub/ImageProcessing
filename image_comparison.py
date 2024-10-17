import cv2
import face_recognition

img = cv2.imread("Messi1.webp")
rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_encoding = face_recognition.face_encodings(rgb_img)[0]

img2 = cv2.imread("images/me.jpg")
rgb_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
img_encoding2 = face_recognition.face_encodings(rgb_img2)[0]

result = face_recognition.compare_faces([img_encoding], img_encoding2)
# print("Result: ", result)
print(f"Image Encoding:{img_encoding}")
while True:
    cv2.imshow("Img", img)
    # cv2.imshow("Img 2", img2)
    cv2.imshow("Img rgb", rgb_img)
    # cv2.imshow("Img 2 rgb", rgb_img2)
    key = cv2.waitKey(1)
    if key == ord('q'):
            break
    
cv2.destroyAllWindows()