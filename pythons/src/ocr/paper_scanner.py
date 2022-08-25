import sys
import cv2
import numpy as np


def drawROI(img, corners):
    cpy = img.copy()

    c1 = (192, 192, 255)
    c2 = (128, 128, 255)

    for pt in corners:
        cv2.circle(cpy, tuple(pt.astype(int)), 25, c1, -1, cv2.LINE_AA)

    for i in range(4):
        cv2.line(
            cpy,
            tuple(corners[i].astype(int)),
            tuple(corners[i + 1 if i != 3 else 0].astype(int)),
            c2,
            2,
            cv2.LINE_AA,
        )

    disp = cv2.addWeighted(img, 0.3, cpy, 0.7, 0)

    return disp


def on_mouse(event, x, y, flags, param):
    global src_quad, drag_src, pt_old, src

    if event == cv2.EVENT_LBUTTONDOWN:
        for i in range(4):
            if cv2.norm(src_quad[i] - (x, y)) < 25:
                drag_src[i] = True
                pt_old = (x, y)
                break

    if event == cv2.EVENT_LBUTTONUP:
        for i in range(4):
            drag_src[i] = False

    if event == cv2.EVENT_MOUSEMOVE:
        for i in range(4):
            if drag_src[i]:
                dx = x - pt_old[0]
                dy = y - pt_old[1]

                src_quad[i] += (dx, dy)

                cpy = drawROI(src, src_quad)
                cv2.imshow("img", cpy)
                pt_old = (x, y)
                break


src = cv2.imread("../../images/docsimg2.jpg")

if src is None:
    print("Image load failed!")
    sys.exit()


h, w = src.shape[:2]

dw = 500
dh = round(dw * 297 / 210)

src_quad = np.array(
    [[30, 30], [30, h - 30], [w - 30, h - 30], [w - 30, 30]], np.float32
)
dst_quad = np.array([[0, 0], [0, dh - 1], [dw - 1, dh - 1], [dw - 1, 0]], np.float32)

drag_src = [False] * 4

disp = drawROI(src, src_quad)

cv2.imshow("img", disp)
cv2.setMouseCallback("img", on_mouse)

while True:
    key = cv2.waitKey()

    if key == 13:
        break
    elif key == 27:
        cv2.destroyWindow("img")
        sys.exit()


pers = cv2.getPerspectiveTransform(src_quad, dst_quad)
dst = cv2.warpPerspective(src, pers, (dw, dh))

cv2.imshow("dst", dst)
cv2.waitKey()
cv2.destroyAllWindows()
