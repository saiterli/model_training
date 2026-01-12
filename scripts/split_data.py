import os
import shutil
import random
from pathlib import Path

RAW_DIR = Path("data/raw")
TRAIN_IMG = Path("data/train/images")
TRAIN_LBL = Path("data/train/labels")
VAL_IMG = Path("data/val/images")
VAL_LBL = Path("data/val/labels")

SPLIT_RATIO = 0.8

images = list(RAW_DIR.glob("*.jpg"))
random.shuffle(images)

split_index = int(len(images) * SPLIT_RATIO)
train_images = images[:split_index]
val_images = images[split_index:]

def copy_pair(img_list, img_dst, lbl_dst):
    for img in img_list:
        label = img.with_suffix(".txt")
        shutil.copy(img, img_dst / img.name)
        if label.exists():
            shutil.copy(label, lbl_dst / label.name)

copy_pair(train_images, TRAIN_IMG, TRAIN_LBL)
copy_pair(val_images, VAL_IMG, VAL_LBL)

print("Train images:", len(train_images))
print("Val images:", len(val_images))
