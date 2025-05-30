import cv2
import numpy as np
from keras.models import load_model
from keras.utils import img_to_array

class EmotionDetector:
    def __init__(self, model_path="modelo_emociones.h5"):
        self.model = load_model(model_path)
        self.labels = ['happy', 'sad']
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.img_size = 100
        self.cap = cv2.VideoCapture(0)
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def preprocess_face(self, face_image):
        face_image = cv2.resize(face_image, (self.img_size, self.img_size))
        face_image = face_image.astype("float") / 255.0
        face_image = img_to_array(face_image)
        return np.expand_dims(face_image, axis=0)

    def predict_emotion(self, face_roi):
        prediction = self.model.predict(face_roi)[0]
        label = self.labels[np.argmax(prediction)]
        confidence = np.max(prediction)
        return label, confidence

    def draw_result(self, frame, x, y, w, h, label, confidence):
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(frame, f"{label} ({confidence:.2f})", 
                   (x, y-10), self.font, 0.8, (255, 255, 255), 2)

    def run(self):
        while True:
            frame = self.cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.3, minNeighbors=5
            )

            for (x, y, w, h) in faces:
                face_roi = gray[y:y+h, x:x+w]
                processed_face = self.preprocess_face(face_roi)
                label, confidence = self.predict_emotion(processed_face)
                self.draw_result(frame, x, y, w, h, label, confidence)

if __name__ == "__main__":
    detector = EmotionDetector()
    detector.run()