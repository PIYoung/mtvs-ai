import cv2
import sys
import random
import numpy as np
import matplotlib.pyplot as plt

src = cv2.imread("../images/OpenCV_logo.png", cv2.IMREAD_GRAYSCALE)

if src is None:
    print("Image load failed!")
    sys.exit()

_, src_bin = cv2.threshold(src, 0, 255, cv2.THRESH_OTSU)
contours, _ = cv2.findContours(src_bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
h, w = src.shape[:2]
dst = np.zeros((h, w, 3), dtype=np.uint8)

for i in range(len(contours)):
    c = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    cv2.drawContours(dst, contours, i, c, 1, cv2.LINE_AA)

cv2.imshow("src", src)
cv2.imshow("src_bin", src_bin)
cv2.imshow("dst", dst)
cv2.waitKey()
cv2.destroyAllWindows()
