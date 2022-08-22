import cv2
import numpy as np

old_x = old_y = -1

def on_mouse(event, x, y, flags, user_data):
    global old_x, old_y

    if event == cv2.EVENT_LBUTTONDOWN:
        old_x, old_y = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if flags & cv2.EVENT_FLAG_LBUTTON:
            cv2.line(img, (old_x, old_y), (x, y), (0, 0, 255), 5, cv2.LINE_AA)
            cv2.imshow("image", img)
            old_x, old_y = x, y


img = np.ones((480, 640, 3), dtype=np.uint8) * 255
cv2.imshow("image", img)
cv2.setMouseCallback("image", on_mouse, img)
cv2.waitKey()
