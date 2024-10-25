from ultralytics import YOLO
# params = {"model": "yolov10x.pt", "epochs": 1000, "imgsz": 640, "batch": 16}
# params = {"model": "yolov10n.pt", "epochs": 1000, "imgsz": 1280, "batch": 16}
# params = {"model": "yolov10x", "epochs": 1000, "imgsz": 640, "batch": 16}

# params = {"model": "yolov8n.pt", "epochs": 1000, "imgsz": 640, "batch": 64}
params = {"model": "models/yolov10n_tennis_1280_v2.pt", "epochs": 1000, "imgsz": 1280, "batch": 16}


# Load a pretrained YOLO model (recommended for training)
# model = YOLO("models/yolov10n_tennis_1280.pt")
model = YOLO(params["model"])

# Train the model using the 'coco8.yaml' dataset for 3 epochs
results = model.train(data="tennis.yaml", epochs=params["epochs"], imgsz=params["imgsz"],
                      batch=params["batch"], scale=0.8)

# Evaluate the model's performance on the validation set
results = model.val()

# Perform object detection on an image using the model
results = model("games/images/val/0009.jpg")

# Export the model to ONNX format
success = model.export(format="onnx")
# /home/zrgy/workspace/sports/rknn_ultralytics/runs/detect/train31/weights/last.pt
# / home / zrgy / workspace / sports / rknn_ultralytics / runs / detect / train30 /
# yolov10x  17 epoch
# 0.723       0.58       0.65      0.289

# yolov10n
#  0.719      0.636      0.733      0.353