import torch
from ultralytics import YOLO

from ultralytics.engine.model import Model

image_dir = "/home/zrgy/workspace/sports/WASB-SBDT/src/tennis/game4/Clip3"

# Load a pre-trained YOLOv10n model
# model = YOLO("runs/detect/train13/weights/best.pt")
model = YOLO("models/yolov8n_tennis_1280.pt")


model.export(format="onnx", opset=12)

# TODO BUG INT8
