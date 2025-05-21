## PyTorch pretrained *.pt models as well as configuration *.yaml files can be passed to the YOLO() class to create a model instance in python:
from ultralytics import YOLO
from pathlib import Path

# Load a pretrained YOLOv8n model
# Display model information (optional)
model = YOLO("yolov8n.pt")
model.info()
project_root = Path(__file__).resolve().parent.parent.parent
data_path = project_root / "data" / "splits" / "data.yaml"

# Train the model on the dataset for 100 epochs
results = model.train(data=data_path, epochs=100, imgsz=640)
