# 허프변환
import cv2
import numpy as np
import matplotlib.pyplot as plt

src = cv2.imread("../images/building.jpg")
edges = cv2.Canny(src, 50, 150)
lines = cv2.HoughLinesP(edges, 1.0, np.pi / 180.0, 160, minLineLength=50, maxLineGap=5)
dst = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

if lines is not None:
    for i in range(lines.shape[0]):
        # start point
        pt1 = (lines[i][0][0], lines[i][0][1])
        # end point
        pt2 = (lines[i][0][2], lines[i][0][3])
        cv2.line(dst, pt1, pt2, (0, 0, 255), 2, cv2.LINE_AA)

# plt.imshow(dst)
# plt.show()

road_img = cv2.imread("../images/road1.jpg")
road_img = cv2.cvtColor(road_img, cv2.COLOR_BGR2RGB)
# plt.imshow(road_img)
# plt.show()

road_gray = cv2.cvtColor(road_img, cv2.COLOR_RGB2GRAY)
# plt.imshow(road_gray, cmap="gray")
# plt.show()

road_blur = cv2.GaussianBlur(road_gray, (5, 5), 0)
# plt.imshow(road_blur, cmap="gray")
# plt.show()

road_edge = cv2.Canny(road_blur, 100, 250)
# plt.imshow(road_edge, cmap="gray")
# plt.show()

mask = np.zeros([1098, 1400], dtype=np.uint8)
# plt.imshow(mask, cmap="gray")
# plt.show()

mask_color = 255
vertices = np.array([[(50, 1098), (600, 700), (900, 700), (1400, 1098)]])
cv2.fillPoly(mask, vertices, mask_color)
# plt.imshow(mask, cmap="gray")
# plt.show()

result_img = cv2.bitwise_and(road_edge, mask)

line_img = np.zeros((1098, 1400, 3), dtype=np.uint8)

road_line = cv2.HoughLinesP(
    result_img, 2, np.pi / 180, 90, minLineLength=120, maxLineGap=10
)
for line in road_line:
    for x1, y1, x2, y2 in line:
        cv2.line(line_img, (x1, y1), (x2, y2), (255, 0, 0), 2)

plt.imshow(line_img)
plt.show()
