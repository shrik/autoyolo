import cv2

WIDTH = 1920
HEIGHT = 1080

video_path = "../data/basketball/basketball.avi"
cap = cv2.VideoCapture(video_path)

i = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    left_frame = frame[:HEIGHT, :WIDTH, :]
    right_frame = frame[:HEIGHT, WIDTH:, :]
    cv2.imwrite(f"../data/basketball/left/{i:06d}.jpg", left_frame)
    cv2.imwrite(f"../data/basketball/right/{i:06d}.jpg", right_frame)
    i += 1
    
