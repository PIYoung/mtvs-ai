import cv2
import numpy as np
import mediapipe as mp

cap = cv2.VideoCapture(0)
p_time = 0

mp_draw = mp.solutions.mediapipe.python.solutions.drawing_utils
mp_face_mesh = mp.solutions.mediapipe.python.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()
face_img = cv2.imread("../../images/face1.png", cv2.IMREAD_UNCHANGED)


def overlay_transparent(
    background_img, img_to_overlay_t, x, y, overlay_size=None, angle=0
):
    try:
        bg_img = background_img.copy()
        # convert 3 channels to 4 channels
        if bg_img.shape[2] == 3:
            bg_img = cv2.cvtColor(bg_img, cv2.COLOR_BGR2BGRA)

        if overlay_size is not None:
            img_to_overlay_t = cv2.resize(img_to_overlay_t, overlay_size)

        b, g, r, a = cv2.split(img_to_overlay_t)
        mask = cv2.medianBlur(a, 5)

        # 얼굴 중심점 설정
        h, w, _ = img_to_overlay_t.shape
        roi = bg_img[int(y - h / 2) : int(y + h / 2), int(x - w / 2) : int(x + w / 2)]
        img1_bg = cv2.bitwise_and(roi.copy(), roi.copy(), mask=cv2.bitwise_not(mask))
        img2_fg = cv2.bitwise_and(img_to_overlay_t, img_to_overlay_t, mask=mask)

        bg_img[
            int(y - h / 2) : int(y + h / 2), int(x - w / 2) : int(x + w / 2)
        ] = cv2.add(img1_bg, img2_fg)
        bg_img = cv2.cvtColor(bg_img, cv2.COLOR_BGRA2BGR)

        return bg_img
    except Exception as e:
        print(e)
        return background_img


def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)

    return result


while True:
    success, frame = cap.read()

    frame = cv2.flip(frame, 1)
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(img_rgb)
    ih, iw, ic = frame.shape
    face_2d = []
    face_3d = []

    if result.multi_face_landmarks:
        for face_lms in result.multi_face_landmarks:
            xy_point = []

            for c, lm in enumerate(face_lms.landmark):
                x = int(lm.x * iw)
                y = int(lm.y * ih)

                xy_point.append([lm.x, lm.y])
                face_2d.append([x, y])
                face_3d.append([x, y, lm.z])
                cv2.circle(frame, (x, y), 3, (255, 0, 0), 3)

            face_2d = np.array(face_2d, dtype=np.float64)
            face_3d = np.array(face_3d, dtype=np.float64)
            focal_length = 1 * iw
            cam_matrix = np.array(
                [[focal_length, 0, ih / 2], [0, focal_length, iw / 2], [0, 0, 1]]
            )
            dist_matrix = np.zeros((4, 1), dtype=np.float64)

            success, rot_vec, trans_vec = cv2.solvePnP(
                face_3d, face_2d, cam_matrix, dist_matrix
            )

            r_mat, jac = cv2.Rodrigues(rot_vec)
            angles, mtx_r, mtx_q, qx, qy, qz = cv2.RQDecomp3x3(r_mat)

            x = -(angles[0] * 360)
            y = -(angles[1] * 360)
            z = -(angles[2] * 360)

            cv2.putText(
                frame,
                f"X: {np.round(x, 2)}",
                (10, 50),
                cv2.FONT_HERSHEY_PLAIN,
                2,
                (255, 0, 0),
                2,
            )
            cv2.putText(
                frame,
                f"Y: {np.round(y, 2)}",
                (10, 100),
                cv2.FONT_HERSHEY_PLAIN,
                2,
                (255, 0, 0),
                2,
            )
            cv2.putText(
                frame,
                f"Z: {np.round(z, 2)}",
                (10, 150),
                cv2.FONT_HERSHEY_PLAIN,
                2,
                (255, 0, 0),
                2,
            )

            top_left = np.min(xy_point, axis=0)
            bottom_right = np.max(xy_point, axis=0)
            mean_xy = np.mean(xy_point, axis=0)

            face_width = int(bottom_right[0] * iw) - int(top_left[0] * iw)
            face_height = int(bottom_right[1] * ih) - int(top_left[1] * ih)

            if face_width > 0 and face_height > 0:
                try:
                    result_img = overlay_transparent(
                        frame,
                        rotate_image(face_img, y * 180 / np.pi),
                        int(mean_xy[0] * iw),
                        int(mean_xy[1] * ih),
                        overlay_size=(face_width + 50, face_height + 50),
                    )
                    frame = result_img
                except Exception as e:
                    print(e)

    cv2.imshow("face", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
