import sys
import cv2
import numpy as np


def cartoon_filter(img: np.ndarray):
    h, w = img.shape[:2]
    img2 = cv2.resize(img, (w // 2, h // 2))

    blr = cv2.bilateralFilter(img2, -1, 20, 7)
    edge = 255 - cv2.Canny(img2, 80, 120)
    edge = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)

    dst = cv2.bitwise_and(blr, edge)
    dst = cv2.resize(dst, (w, h), interpolation=cv2.INTER_NEAREST)

    return dst


def pencil_sketch(img: np.ndarray):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blr = cv2.GaussianBlur(gray, (0, 0), 3)
    dst = cv2.divide(gray, blr, scale=256)

    return dst


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error opening video stream or file")
    sys.exit()

cam_mode1, cam_mode2 = False, False

while True:
    ret, frame = cap.read()

    if not ret:
        break

    if cam_mode1:
        frame = cartoon_filter(frame)
    elif cam_mode2:
        frame = pencil_sketch(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

    cv2.imshow("frame", frame)

    key = cv2.waitKey(1)

    if key == 27:
        break
    elif key == 49:
        cam_mode1 = True
        cam_mode2 = False
    elif key == 50:
        cam_mode1 = False
        cam_mode2 = True


cap.release()
cv2.destroyAllWindows()