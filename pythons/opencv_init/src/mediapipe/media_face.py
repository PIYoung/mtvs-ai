import cv2
import numpy as np
import mediapipe as mp

cap = cv2.VideoCapture(0)

mp_draw = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh()

while True:
    success, frame = cap.read()

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(img_rgb)

    if result.multi_face_landmarks:
        for face_lms in result.multi_face_landmarks:
            xy_point = []

            for c, lm in enumerate(face_lms.landmark):
                ih, iw, ic = frame.shape
                xy_point.append([lm.x, lm.y])
                
                # 얼굴 맨 위, 맨 아래 점 찍기
                # if c == 10 or c == 152:
                #     cv2.circle(frame, (int(lm.x * iw), int(lm.y * ih)), 3, (255, 0, 0), 3)


            # 얼굴 모자이크
            top_left = np.min(xy_point, axis=0)
            bottom_right = np.max(xy_point, axis=0)
            mean_xy = np.mean(xy_point, axis=0)

            face_width = int(bottom_right[0] * iw) - int(top_left[0] * iw)
            face_height = int(bottom_right[1] * ih) - int(top_left[1] * ih)

            fh = int(top_left[1] * ih)
            fw = int(top_left[0] * iw)

            roi = frame[fh : fh + face_height, fw : fw + face_width]
            roi = cv2.resize(roi, (int(face_width / 14), int(face_height / 14)))
            roi = cv2.resize(
                roi, (face_width, face_height), interpolation=cv2.INTER_AREA
            )

            try:
                frame[fh : fh + face_height, fw : fw + face_width] = roi
            except Exception as e:
                print(e)


    cv2.imshow("face", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
