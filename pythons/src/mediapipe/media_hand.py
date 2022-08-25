import cv2
import math
import socket
import numpy as np
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_port = ("127.0.0.1", 5053)

cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5
) as hands:
    while True:
        success, frame = cap.read()

        if not success:
            continue

        img_rgb = cv2.flip(frame, 1)
        results = hands.process(img_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                p1 = hand_landmarks.landmark[4]
                p2 = hand_landmarks.landmark[8]

                f1 = np.array([p1.x, p1.y, p1.z])
                f2 = np.array([p2.x, p2.y, p2.z])

                temp = np.linalg.norm(f1 - f2)
                volume = abs(int(temp * 100))

                # send_port의 주소로 접속한 유저들에게 데이터 전송
                # socket.sendto(str(volume).encode(), send_port)

                cv2.putText(
                    img_rgb,
                    text="Volume: %d" % volume,
                    org=(10, 30),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1,
                    color=(255, 0, 0),
                    thickness=2,
                )

                mp_drawing.draw_landmarks(
                    img_rgb, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )

        cv2.imshow("face", img_rgb)

        if cv2.waitKey(1) == 27:
            break

cap.release()
cv2.destroyAllWindows()
