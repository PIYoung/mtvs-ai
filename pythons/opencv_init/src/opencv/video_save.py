import cv2

# 0번 카메라 == 내장 카메라 연결
v_cap = cv2.VideoCapture(0)

w = round(v_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = round(v_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# video 압축 형식
fourcc = cv2.VideoWriter_fourcc(*"DIVX")
fps = v_cap.get(cv2.CAP_PROP_FPS)

out = cv2.VideoWriter("output.avi", fourcc, fps, (w, h))

while True:
    ret, frame = v_cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)
    out.write(frame)

    if cv2.waitKey(1) == 27:
        break


out.release()
v_cap.release()
cv2.destroyAllWindows()
