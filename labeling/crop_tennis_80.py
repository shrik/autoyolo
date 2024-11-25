from ultralytics import YOLO
import os
import glob
import cv2
import random


model = YOLO("../models/yolov8n_tennis_640_taishan.pt")
results = model.predict("../games/images/taishan6k/000080.jpg")
print(results)

def aug_crop_image(image, bbox, size_w, size_h):
    WIDTH = image.shape[1]
    HEIGHT = image.shape[0]
    x, y, w, h = bbox
    MIN_MARGIN = 10
    x = x * WIDTH
    y = y * HEIGHT
    w = w * WIDTH
    h = h * HEIGHT
    left_margin = random.randint(MIN_MARGIN, size_w - 2*MIN_MARGIN)
    top_margin = random.randint(MIN_MARGIN, size_h - 2*MIN_MARGIN)
    x1 = max(int(x - w/2 - left_margin), 0)
    y1 = max(int(y - h/2 - top_margin), 0)
    x2 = min(int(x1 + size_w), WIDTH)
    y2 = min(int(y1 + size_h), HEIGHT)
    crop_img = image[y1:y2, x1:x2]
    crop_img = cv2.resize(crop_img, (size_w, size_h))
    return crop_img

def outputs(result, image, imagename, output_dir, name):
    image_dir = os.path.join(output_dir, "images", name)
    label_dir = os.path.join(output_dir, "labels", name)
    os.makedirs(image_dir, exist_ok=True)
    os.makedirs(label_dir, exist_ok=True)
    filepath = os.path.join(label_dir, imagename.replace(".jpg", ".txt"))
    for item in result[0].boxes:
        if item.cls == 0: # tennis ball
            cropped_img = aug_crop_image(image, item.xywhn.cpu().numpy().tolist()[0], 80, 80)
            cv2.imwrite(os.path.join(image_dir, imagename), cropped_img)

imagefiles = glob.glob("../games/images/taishan6k/*.jpg")
for imagepath in imagefiles:
    imagename = os.path.basename(imagepath)
    results = model.predict(imagepath)
    image = cv2.imread(imagepath)
    outputs(results, image, imagename, "../games/zoom", name="taishan6k")


