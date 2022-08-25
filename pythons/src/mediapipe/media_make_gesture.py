import cv2
import numpy as np
import pandas as pd
import mediapipe as mp

mp_hands = mp.solutions.mediapipe.python.solutions.hands
mp_drawing = mp.solutions.mediapipe.python.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5
)

total_result = []


def on_click(event, x, y, flags, param):
    global data, file

    if event == cv2.EVENT_LBUTTONDOWN:
        total_result.append(data)


cap = cv2.VideoCapture(0)
cv2.namedWindow("Dataset")
cv2.setMouseCallback("Dataset", on_click)

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
            data = np.append(data, 0)

            mp_drawing.draw_landmarks(img, res, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Dataset", img)
    if cv2.waitKey(1) == 27:
        break

total_result = np.array(total_result, dtype=np.float32)
df = pd.DataFrame(total_result)
df.to_csv("../../data/gesture_new.csv", mode="a", index=False, header=False)
cap.release()
