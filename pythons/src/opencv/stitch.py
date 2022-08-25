import sys
import cv2

img_names = [
    "../../images/pano1.jpg",
    "../../images/pano2.jpg",
    "../../images/pano3.jpg",
]
imgs = []

for name in img_names:
    img = cv2.imread(name)

    if img is None:
        sys.exit()

    imgs.append(img)

stitcher = cv2.Stitcher_create()
status, dst = stitcher.stitch(imgs)

if status != cv2.STITCHER_OK:
    sys.exit()

cv2.imwrite("../../images/output.jpg", dst)
cv2.imshow("dst", dst)
cv2.waitKey()
cv2.destroyAllWindows()
