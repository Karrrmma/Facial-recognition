import cv2
import face_recognition
from flask import Flask, Response
import os
from pymongo import MongoClient
import numpy as np
import base64
app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client.recog
face = db.face

def load_cascade():
                            #uses a path below              #classfier that is pretrained
    return cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def detect_faces(image, face_cascade):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #min neighbor means five rectangle in the frame then it decides if its a face
    #min size checks the size of the face min it can detect
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return image, faces


def check_face(frame, reference_encodings):
    frame_encodings = face_recognition.face_encodings(frame)
    for encoding in frame_encodings:
        results = face_recognition.compare_faces([ref['image_data'] for ref in reference_encodings], encoding)
        if True in results:
            return reference_encodings[results.index(True)]['name']
    return None

def load_reference_images(folder_path):
    reference_encodings = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.jpg') or filename.endswith('.jpeg'):
            name = filename.split('.')[0]  # Assuming the name is the first part of the filename
            img_path = os.path.join(folder_path, filename)
            img = face_recognition.load_image_file(img_path)
            encoding = face_recognition.face_encodings(img)
            if encoding:
                reference_encodings.append({'name': name, 'image_data': encoding[0]})
    return reference_encodings



def main():
    face_cascade = load_cascade()
    reference_encodings = load_reference_images('folder')

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 650)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    while True:
        ret, frame = cap.read()
        if ret:
            frame, faces = detect_faces(frame, face_cascade)
            if len(faces) > 0:  # Check if the faces array is not empty
                recognized_name = check_face(frame, reference_encodings)
                #recognized_name = check_face(frame)

                if recognized_name:
                    cv2.putText(frame, recognized_name, (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
                else:
                    cv2.putText(frame, "Not Match", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
            #cv2.imshow("Video", frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(main(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
