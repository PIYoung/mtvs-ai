import cv2
import matplotlib.pyplot as plt

plt.axis("off")

# opencv에서는 이미지를 BGR순서로 불러옴
img = cv2.imread("../../images/starry_night.jpg")

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# plt.imshow(img)
# plt.show()

# Gray이미지는 채널이 1개
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# plt.imshow(imgGray, cmap="gray")
# plt.show()

src = cv2.imread("../../images/starry_night.jpg", cv2.IMREAD_COLOR)
mask = cv2.imread("../../images/starry_night_mask.jpg", cv2.IMREAD_GRAYSCALE)
dst = cv2.imread("../../images/starry_night_BGR.jpg", cv2.IMREAD_COLOR)

result = cv2.copyTo(src, mask, dst)
result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
# plt.imshow(result)
# plt.show()

img = cv2.imread("../../images/starry_night.jpg", cv2.IMREAD_COLOR)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# plt.imshow(img)
# plt.show()

print(img.shape)  # (640, 1024, 3)

cv2.line(img, (0, 0), (300, 300), (255, 0, 0), 20)
cv2.line(img, (30, 30), (250, 300), (255, 0, 0), 20)
# plt.imshow(img)
# plt.show()

img = cv2.imread("../../images/starry_night.jpg", cv2.IMREAD_COLOR)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
cv2.rectangle(img, (10, 10), (100, 100), (255, 0, 0), 10)
# plt.imshow(img)
# plt.show()

# x, y, w, h로 그리기
img = cv2.imread("../../images/starry_night.jpg", cv2.IMREAD_COLOR)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
cv2.rectangle(img, (100, 100, 30, 50), (0, 255, 0), 10)
# plt.imshow(img)
# plt.show()

img = cv2.imread("../../images/starry_night.jpg", cv2.IMREAD_COLOR)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
cv2.circle(img, (300, 300), 50, (255, 0, 0), 5)
plt.imshow(img)
plt.show()
