import cv2
import numpy as np
import pandas as pd
import mediapipe as mp

gesture = {
    0: "zero",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "siz",
    7: "rock",
    8: "spiderman",
    9: "yeah",
    10: "ok",
}

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5
)

df = pd.read_csv("../../data/gesture_train.csv", header=None)
angle = df.iloc[:, :-1]
label = df.iloc[:, -1]

angle = angle.to_numpy().astype(np.float32)
label = label.to_numpy().astype(np.float32)

knn = cv2.ml.KNearest_create()
knn.train(angle, cv2.ml.ROW_SAMPLE, label)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, img = cap.read()

    if not ret:
        break

    img = cv2.flip(img, 1)
    result = hands.process(img)

    if result.multi_hand_landmarks is not None:
        for res in result.multi_hand_landmarks:
            joint = np.zeros((21, 3))

            for j, lm in enumerate(res.landmark):
                joint[j] = [lm.x, lm.y, lm.z]

            # Get direction vector of bone from parent to child
            v1 = joint[
                [0, 1, 2, 3, 0, 5, 6, 7, 0, 9, 10, 11, 0, 13, 14, 15, 0, 17, 18, 19], :
            ]  # Parent joint
            v2 = joint[
                [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                :,
            ]  # Child joint
            v = v2 - v1  # [20,3]
            # Normalize v
            v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

            # Get angle using arccos of dot product
            angle = np.arccos(
                np.einsum(
                    "nt,nt->n",
                    v[[0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16, 17, 18], :],
                    v[[1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19], :],
                )
            )  # [15,]

            angle = np.degrees(angle)

            data = np.array([angle], dtype=np.float32)
            ret, results, neighbors, dist = knn.findNearest(data, 5)

            idx = int(results[0][0])

            if idx in gesture.keys():
                cv2.putText(
                    img,
                    text=gesture[idx].upper(),
                    org=(
                        int(res.landmark[0].x * img.shape[1]),
                        int(res.landmark[0].y * img.shape[0]),
                    ),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1,
                    color=(255, 255, 255),
                    thickness=2,
                )

            mp_drawing.draw_landmarks(img, res, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Hand gesture", img)
    if cv2.waitKey(1) == 27:
        break

cap.release()
