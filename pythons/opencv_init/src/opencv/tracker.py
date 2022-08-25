import sys
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    sys.exit()

tracker = cv2.TrackerCSRT_create()
ret, frame = cap.read()

if not ret:
    sys.exit()

rc = cv2.selectROI("frame", frame)
tracker.init(frame, rc)

while True:
    ret, frame = cap.read()

    if not ret:
        sys.exit()

    ret, rc = tracker.update(frame)
    rc = tuple(int(_) for _ in rc)

    cv2.rectangle(frame, rc, (255, 0, 0), 2)
    cv2.imshow("frame", frame)

    if cv2.waitKey(20) == 27:
        break

cap.release()
cv2.destroyAllWindows()
