from turtle import delay
import cv2

v_cap = cv2.VideoCapture("images/flower.mp4")
fps = round(v_cap.get(cv2.CAP_PROP_FPS))
delay = round(1000 / fps)

while True:
    ret, frame = v_cap.read()

    if not ret:
        break

    cv2.imshow("mp4", frame)

    if cv2.waitKey(delay) == 27:
        break


v_cap.release()
cv2.destroyAllWindows()
