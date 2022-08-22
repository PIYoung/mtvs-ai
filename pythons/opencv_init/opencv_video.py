import cv2

v_cap = cv2.VideoCapture(0)

while True:
    ret, frame = v_cap.read()
    # 좌우반전
    frame = cv2.flip(frame, 1)

    cv2.imshow("frame", frame)

    # press esc exit
    if cv2.waitKey(1) == 27:
        v_cap.release()
        cv2.destroyAllWindows()
        break
