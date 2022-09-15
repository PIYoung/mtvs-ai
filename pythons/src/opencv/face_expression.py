import cv2
import numpy as np
import tensorflow as tf

font = cv2.FONT_HERSHEY_SIMPLEX
EMOTIONS_LIST = ["Angry", "Disgust", "Fear", "Happy", "Neutral", "Sad", "Surprise"]
model = tf.keras.models.load_model("../../models/face_expression_model.h5")
cap = cv2.VideoCapture(0)
face_classifier = cv2.CascadeClassifier(
    "../../xmls/haarcascade_frontalface_default.xml"
)

while True:
    _, frame = cap.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_frame, 1.3, 5)

    for (x, y, w, h) in faces:
        face = gray_frame[y : y + h, x : x + w]
        roi = cv2.resize(face, (48, 48))
        pred = model.predict(roi[np.newaxis, :, :, np.newaxis])
        label = EMOTIONS_LIST[np.argmax(pred)]

        cv2.putText(frame, label, (x, y), font, 1, (255, 255, 0), 2)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow("Facial Expression Recognition", frame)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
