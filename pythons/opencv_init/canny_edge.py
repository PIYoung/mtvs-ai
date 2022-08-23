import cv2
import matplotlib.pyplot as plt

src = cv2.imread("images/galaxy-soho.jpg")

dst = cv2.Canny(src, 50, 200)

plt.imshow(dst, cmap="gray")
plt.show()
