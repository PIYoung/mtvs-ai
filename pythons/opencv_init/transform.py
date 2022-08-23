import cv2
import numpy as np
import matplotlib.pyplot as plt

src = cv2.imread("images/business-card_640.jpg")
src = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)

w, h = 720, 480

src_quad = np.array([[160, 207], [395, 112], [487, 221], [239, 327]], np.float32)
dst_quea = np.array(
    [
        [
            0,
            0,
        ],
        [w - 1, 0],
        [w - 1, h - 1],
        [0, h - 1],
    ],
    np.float32,
)

pers = cv2.getPerspectiveTransform(src_quad, dst_quea)
dst = cv2.warpPerspective(src, pers, (w, h))

plt.imshow(dst)
plt.show()
