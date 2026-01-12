import argparse
from ultralytics import YOLO

parser = argparse.ArgumentParser()
parser.add_argument("--data_yaml", required=True)
parser.add_argument("--epochs", type=int, default=10)
parser.add_argument("--device", default="cpu")

args = parser.parse_args()

model = YOLO("yolov8n.pt")

model.train(
    data=args.data_yaml,
    epochs=args.epochs,
    device=args.device,
    imgsz=640,
    batch=8,
    project="runs",
    name="detect/train",
    exist_ok=True
)
