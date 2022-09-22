import cv2
import numpy as np
import mediapipe as mp

mp_drawing = mp.solutions.mediapipe.python.solutions.drawing_utils  # 관절 드로잉
mp_pose = mp.solutions.mediapipe.python.solutions.pose  # 미디어파이프 솔루션 포즈

cap = cv2.VideoCapture(0)


def calculate_angle(a, b, c):
    a = np.array(a)  # first point
    b = np.array(b)  # middle point
    c = np.array(c)  # end point

    ang1 = np.arctan2(c[1] - b[1], c[0] - b[0])
    ang2 = np.arctan2(a[1] - b[1], a[0] - b[0])
    radians = ang1 - ang2
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle


with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2),
        )

        landmarks = results.pose_landmarks.landmark

        pos_r_shoulder = [
            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y,
        ]
        pos_r_elbow = [
            landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
            landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y,
        ]
        pos_r_wrist = [
            landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
            landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y,
        ]

        angle = calculate_angle(pos_r_shoulder, pos_r_elbow, pos_r_wrist)

        cv2.putText(
            image,
            str(angle),
            tuple(np.multiply(pos_r_shoulder, [640, 480]).astype(int)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

        cv2.imshow("Pose Estimation", image)

        if cv2.waitKey(10) & 0xFF == ord("q"):
            break
