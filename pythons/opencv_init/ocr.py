import pytesseract
import cv2
import matplotlib.pyplot as plt

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

src = cv2.imread("images/hangul.png")
src = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)

# plt.imshow(src)
# plt.show()

# type below on bash
# export TESSDATA_PREFIX="C:/Program Files/Tesseract-OCR/tessdata/"
print(pytesseract.image_to_string(src, lang="ko"))

# print(pytesseract.image_to_data(src, lang="ko"))

# result = pytesseract.image_to_osd(src, lang="ko")
# for box, text, conf in result:
#     print(box, text, conf)
