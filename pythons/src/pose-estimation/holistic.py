import cv2
import csv
import numpy as np
import mediapipe as mp
from os import path

import joblib
import pandas as pd

model = joblib.load("face.pkl")

mp_drawing = mp.solutions.mediapipe.python.solutions.drawing_utils  # 관절 드로잉
mp_holistic = mp.solutions.mediapipe.python.solutions.holistic  # 미디어파이프 솔루션 헬리스틱

cap = cv2.VideoCapture(0)

with mp_holistic.Holistic(
    min_detection_confidence=0.5, min_tracking_confidence=0.5
) as holistic:
    while cap.isOpened():
        _, frame = cap.read()

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        results = holistic.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        mp_drawing.draw_landmarks(
            image,
            results.face_landmarks,
            mp_holistic.FACEMESH_CONTOURS,
            mp_drawing.DrawingSpec(color=(80, 110, 10), thickness=1, circle_radius=1),
            mp_drawing.DrawingSpec(color=(80, 256, 120), thickness=1, circle_radius=1),
        )

        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_holistic.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=3, circle_radius=3),
            mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=3, circle_radius=3),
        )

        try:
            # face landmarks 값 가져오기
            face = results.face_landmarks.landmark
            face_list = []
            for temp in face:
                face_list.append([temp.x, temp.y, temp.z])

            face_row = list(np.array(face_list).flatten())

            X = pd.DataFrame([face_row])
            print(model.predict([face_row])[0])

            if not path.isfile("coords.csv"):
                landmarks = ["label"]
                for temp in range(1, len(face_list) + 1):
                    landmarks += [
                        "x{}".format(temp),
                        "y{}".format(temp),
                        "z{}".format(temp),
                        "v{}".format(temp),
                    ]

                with open("coords.csv", mode="w", newline="") as f:
                    csv_writer = csv.writer(
                        f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
                    )
                    csv_writer.writerow(landmarks)
                    f.close()

            if cv2.waitKey(10) & 0xFF == ord("s"):
                with open("coords.csv", mode="a", newline="") as f:
                    face_row.insert(0, "sad")
                    csv_writer = csv.writer(
                        f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
                    )
                    csv_writer.writerow(face_row)
                    f.close()
        except Exception as e:
            print(e)
            pass

        cv2.imshow("Holistic Estimation", image)

        if cv2.waitKey(10) & 0xFF == ord("q"):
            break
