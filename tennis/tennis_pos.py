import os
import time

import cv2

from ultralytics import YOLO
import torch
from torchvision.ops import nms
import json

CONF_THRESH = 0.5
NMS_THRESH = 0.2

def my_nms(boxes, iou_threshold):
    if len(boxes) == 0:
        return []

    boxes_tensor = torch.tensor([box.xywhn.cpu().numpy().tolist()[0] for box in boxes])
    scores = torch.tensor([box.conf.cpu().numpy().tolist()[0] for box in boxes])
    nms_indices = nms(boxes_tensor, scores, iou_threshold=iou_threshold)
    nms_boxes = [boxes[i] for i in nms_indices]
    return nms_boxes


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


import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description='Auto-label images using YOLO model')
parser.add_argument('--image_dir', type=str, default="../../taishanimgs", help='Directory containing images to label')
parser.add_argument('--model_path', type=str, default="models/yolov8n_tennis.pt", help='Path to the YOLO model')
args = parser.parse_args()

# Use parsed arguments
image_dir = args.image_dir

# Load the YOLO model
model = YOLO(args.model_path)


import os
imagefiles = []
for root, dirs, files in os.walk(image_dir):
    for file in files:
        if file.endswith('.jpg'):
            imagefiles.append(os.path.join(root, file))
imagefiles.sort()

def output_pos(image_path, nms_boxes):
    result = []
    for box in nms_boxes:
        result.append({
            "class": box.cls.cpu().numpy().tolist()[0],
            "box": box.xywhn.cpu().numpy().tolist()[0],
            "conf": box.conf.cpu().numpy().tolist()[0],
        })
    return {
        "image_path": image_path,
        "pos": result,
        "index": int(image_path.split("/")[-1].split(".")[0]),
    }
        
output_file = open("tennis_pos.json", "w")

valid_image_files = []
for imagefile in imagefiles:
    image_path = imagefile
    image = cv2.imread(image_path)
    results = model.predict(source=image_path)
    if len(results) > 1:
        raise Exception("More than one result")
    result = results[0]
    boxes = []
    if result.boxes is None:
        continue
    for box in result.boxes:
        if box.conf.cpu().numpy().tolist()[0] < CONF_THRESH:
            continue
        boxes.append(box)
    nms_boxes = my_nms(boxes, NMS_THRESH)
    if len(nms_boxes) == 0:
        continue
    valid_image_files.append(image_path)
    
    result = output_pos(image_path, nms_boxes)
    output_file.write(json.dumps(result) + "\n")
output_file.close()

#python auto_label.py --image_dir data/taishanimgs/ --model_path models/yolov10n_tennis_1280_v2.pt 