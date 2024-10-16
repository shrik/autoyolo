import os
import time

import cv2

from ultralytics import YOLO

image_dir = "/home/zrgy/workspace/sports/WASB-SBDT/src/tennis/game4/Clip3"

# Load a pre-trained YOLOv10n model
model = YOLO("runs/detect/train13/weights/best.pt")
# model = YOLO("yolov8n.pt")
# model.val()
# Assuming 'result' is a tuple containing the coordinates of the rectangle
# (x, y, width, height)
imagefiles = os.listdir(image_dir)
imagefiles.sort()
imagefiles = imagefiles
s = time.time()
for imagefile in imagefiles:
    image_path = os.path.join(image_dir, imagefile)
    image = cv2.imread(image_path)
    results = model.predict(source=image_path,save = True)
    for result in results:
        print("result", result.probs)
        newimage = cv2.imread(image_path)
        # if result.boxes.xyxyn.shape[0] == 0:
        #     plt.imshow(newimage)
        #     cv2.imshow("hi", newimage)
        #     cv2.waitKey(0)
        #     continue
        #
        # x1,y1,x2,y2 = list(result.boxes.xyxyn.cpu().numpy()[0])
        # img_w, img_h = newimage.shape[1], newimage.shape[0]
        # newimage = cv2.rectangle(newimage, (int(x1 * img_w), int(y1 * img_h)), (int(x2 * img_w), int(y2 * img_h)), (255,0,0), 1)
        # cv2.imshow("hi", newimage)
        # cv2.waitKey(0)
print((time.time() - s) * 1000/len(imagefiles))