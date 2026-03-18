import os
import shutil
import random
from pathlib import Path

SOURCE_DIR = "Dataset_BUSI_with_GT"
DEST_DIR = "data/datasets/breast"

TRAIN_RATIO = 0.7
VAL_RATIO = 0.15
TEST_RATIO = 0.15

classes = ["normal", "benign", "malignant"]

for cls in classes:
    images = os.listdir(os.path.join(SOURCE_DIR, cls))
    random.shuffle(images)

    train_split = int(len(images) * TRAIN_RATIO)
    val_split = int(len(images) * (TRAIN_RATIO + VAL_RATIO))

    train_imgs = images[:train_split]
    val_imgs = images[train_split:val_split]
    test_imgs = images[val_split:]

    for split, split_imgs in zip(
        ["train", "val", "test"],
        [train_imgs, val_imgs, test_imgs]
    ):

        os.makedirs(os.path.join(DEST_DIR, split, cls), exist_ok=True)

        for img in split_imgs:
            src = os.path.join(SOURCE_DIR, cls, img)
            dst = os.path.join(DEST_DIR, split, cls, img)
            shutil.copy(src, dst)

print("Breast dataset prepared successfully.")