from ultralytics import YOLOv10
# Load a pretrained YOLO model (recommended for training)
model = YOLOv10.from_pretrained('jameslahm/yolov10n')

# Train the model using the 'coco8.yaml' dataset for 3 epochs
results = model.train(data="tennis.yaml", epochs=1000, imgsz=640)

# Evaluate the model's performance on the validation set
results = model.val()

# Perform object detection on an image using the model
results = model("games/images/val/0009.jpg")

# Export the model to ONNX format
success = model.export(format="onnx")