import cv2

cap = cv2.VideoCapture("tennis.h264")

i = 0
while True:
    ret, frame = cap.read()
    if ret == -1:
        break
    cv2.imwrite("data/images/" + "%06i" % i + ".jpg", frame)
    i+=1
    print(f".", end="")



