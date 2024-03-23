import cv2
import face_recognition
from flask import Flask, Response


app = Flask(__name__)

def load_cascade():
    return cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_faces(image, face_cascade):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return image, faces

def check_face(frame, reference_encoding):
    frame_encodings = face_recognition.face_encodings(frame)
    for encoding in frame_encodings:
        results = face_recognition.compare_faces([reference_encoding], encoding)
        if True in results:
            return True
    return False

def main():
    face_cascade = load_cascade()

    reference_img = face_recognition.load_image_file("obama.jpg")
    reference_img = face_recognition.load_image_file("123.jpg")


    reference_encoding = face_recognition.face_encodings(reference_img)[0]

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 650)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        ret, frame = cap.read()
        if ret:
            frame, faces = detect_faces(frame, face_cascade)
            if len(faces) > 0:  # Check if the faces array is not empty
                face_match = check_face(frame, reference_encoding)
                if face_match:
                    cv2.putText(frame, "Match", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
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
    
