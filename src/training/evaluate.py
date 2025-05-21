# Custom Evaluation on the test set (by creating a data.yaml)
from ultralytics import YOLO
from pathlib import Path
import json
project_root = Path(__file__).resolve().parent.parent.parent
project_path = "../results/figures"
data_path = project_root / "data" / "splits" / "data.yaml"
# get current model version
model_dir = project_root / "results" / "models"
model_version_config = model_dir / "model_config.json"
with open(model_version_config, "r") as f:
    model_config = json.load(f)
    # get the current version
    current_version = model_config["current_version"]

# Replace with the current version of your model
current_model_path = model_dir / f"yolov8_model_{current_version}.pt"
model = YOLO(current_model_path)
metrics = model.val(data=data_path, split="test", conf=0.25, save=True,
                     project=project_path, name="test_metrics")
