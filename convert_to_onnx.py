import torch
from ultralytics import YOLO

from ultralytics.engine.model import Model

model = YOLO("models/basketball_sz.pt")


model.export(format="onnx", opset=12)

# TODO BUG INT8


# cp models/yolov10n_tennis_1280_v2.onnx ~/xanylabeling_data/models/tennis_yolov10/yolov10n.onnx