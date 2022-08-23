import cv2
import numpy as np
import matplotlib.pyplot as plt

src = cv2.imread("images/gerbera jamesonii.jpg")
src = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
src = cv2.resize(src, (200, 200))

dst = cv2.GaussianBlur(src, (0, 0), 4)
# plt.imshow(dst)
# plt.show()

src = cv2.imread("images/gerbera jamesonii.jpg")
src_ycrcb = cv2.cvtColor(src, cv2.COLOR_BGR2YCrCb)
src_f = src_ycrcb[:, :, 0].astype(np.float32)
blr = cv2.GaussianBlur(src_f, (0, 0), 6.0)
src_ycrcb[:, :, 0] = np.clip(2.0 * src_f - blr, 0, 255).astype(np.uint8)
dst = cv2.cvtColor(src_ycrcb, cv2.COLOR_YCrCb2RGB)
# plt.imshow(dst)
# plt.show()

src = cv2.imread("images/woman_640.jpg")
src = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
dst = cv2.bilateralFilter(src, -1, 100, 5)

plt.imshow(dst)
plt.show()
