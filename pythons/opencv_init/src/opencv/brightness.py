import cv2
import numpy as np
import matplotlib.pyplot as plt

src = cv2.imread("../images/starry_night.jpg", cv2.IMREAD_GRAYSCALE)

# 255 이상을 넘어가는 값은 255로 고정
dst1 = cv2.add(src, 100)
# plt.imshow(dst1, cmap="gray")
# plt.show()

# numpy에서 255(dtype=uint8)를 넘어가면 자동으로 overflow 처리해줌
dst2 = src + 100
# plt.imshow(dst2, cmap="gray")
# plt.show()

src = cv2.imread("../images/starry_night.jpg")

dst1 = cv2.add(src, (100, 100, 100, 0))
dst1 = cv2.cvtColor(dst1, cv2.COLOR_BGR2RGB)
# plt.imshow(dst1)
# plt.show()

dst2 = np.clip(src + 100.0, 0, 255).astype(np.uint8)
dst2 = cv2.cvtColor(dst2, cv2.COLOR_BGR2RGB)
# plt.imshow(dst2)
# plt.show()

src = cv2.imread("../images/starry_night.jpg")

b_plane, g_plane, r_plane = cv2.split(src)
# plt.subplot(1, 3, 1)
# plt.imshow(b_plane, cmap="gray")
# plt.subplot(1, 3, 2)
# plt.imshow(g_plane, cmap="gray")
# plt.subplot(1, 3, 3)
# plt.imshow(r_plane, cmap="gray")
# plt.show()

src = cv2.imread("../images/MnM.jpg")
src = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)

h_plane, s_plane, v_plane = cv2.split(src)
# plt.subplot(1, 3, 1)
# plt.imshow(h_plane, cmap="gray")
# plt.subplot(1, 3, 2)
# plt.imshow(s_plane, cmap="gray")
# plt.subplot(1, 3, 3)
# plt.imshow(v_plane, cmap="gray")
# plt.show()

src = cv2.imread("../images/MnM.jpg")
src = cv2.cvtColor(src, cv2.COLOR_BGR2YCrCb)

y_plane, cr_plane, cb_plane = cv2.split(src)
# plt.subplot(1, 3, 1)
# plt.imshow(y_plane, cmap="gray")
# plt.subplot(1, 3, 2)
# plt.imshow(cr_plane, cmap="gray")
# plt.subplot(1, 3, 3)
# plt.imshow(cb_plane, cmap="gray")
# plt.show()

# 색상 값 히스토그램으로 확인
src = cv2.imread("../images/starry_night.jpg", cv2.IMREAD_GRAYSCALE)
hist = cv2.calcHist([src], [0], None, [256], [0, 256])
# plt.subplot(1, 2, 1)
# plt.imshow(src, cmap="gray")
# plt.subplot(1, 2, 2)
# plt.plot(hist)
# plt.show()

# 색상 분포 히스토그램으로 확인
src = cv2.imread("../images/starry_night.jpg")
colors = ["b", "g", "r"]
bgr_planes = cv2.split(src)
plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(src, cv2.COLOR_BGR2RGB))
plt.subplot(1, 2, 2)
for p, c in zip(bgr_planes, colors):
    hist = cv2.calcHist([p], [0], None, [256], [0, 256])
    plt.plot(hist, color=c)
    plt.xlim([0, 256])

plt.show()
