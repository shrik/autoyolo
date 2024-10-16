import os
import time

import cv2

from ultralytics import YOLO

image_dir = "games/images/val"

# Load a pre-trained YOLOv10n model
model = YOLO("../../rknn_ultralytics/runs/detect/train37/weights/best.pt")

# model = YOLO("models/yolov8n_tennis.pt")

def parse_label(label_path):
    label_box = open(label_path, "r").readlines()[0].strip().split(" ")
    label_box = [float(x) for x in label_box]
    return label_box[1:]


def iou(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    
    # Calculate coordinates of intersection rectangle
    x_left = max(x1, x2)
    y_top = max(y1, y2)
    x_right = min(x1 + w1, x2 + w2)
    y_bottom = min(y1 + h1, y2 + h2)
    
    # Check if there is an intersection
    if x_right < x_left or y_bottom < y_top:
        return 0.0
    
    # Calculate intersection area
    intersection = (x_right - x_left) * (y_bottom - y_top)
    
    # Calculate union area
    box1_area = w1 * h1
    box2_area = w2 * h2
    union_area = box1_area + box2_area - intersection
    
    # Calculate IoU
    iou = intersection / union_area
    
    return iou


imagefiles = os.listdir(image_dir)
imagefiles.sort()
imagefiles = imagefiles
s = time.time()
tp, tn, fp, fn = 0, 0, 0, 0

total_count = len(imagefiles)
for imagefile in imagefiles:
    image_path = os.path.join(image_dir, imagefile)
    label_path = os.path.join(image_path.replace("images", "labels").replace(".jpg", ".txt"))
    label_box = parse_label(label_path)
    image = cv2.imread(image_path)
    results = model.predict(source=image_path)
    tp_setted = False
    for result in results:
        # import pdb;pdb.set_trace()

        if result.boxes is None:
            continue
        for box in result.boxes:
            if box.conf.cpu().numpy().tolist()[0] < 0.5:
                continue
            pbox = tuple(box.xywhn.cpu().numpy().tolist()[0])
            if iou(label_box, pbox) > 0:
                if not tp_setted:
                    tp += 1
                    tp_setted = True
            else:
                fp += 1
    
precision = tp / (tp + fp)
recall = tp / total_count
f1 = 2 * (precision * recall) / (precision + recall)
accuracy = (tp + tn) / (tp + tn + fp + fn)

print(f"Precision: {precision}, Recall: {recall}, F1: {f1}, Accuracy: {accuracy}")



 # TP   | TN   | FP   | FN   | Prec       | Recall       | F1       | Accuracy       | RMSE | AP  |
