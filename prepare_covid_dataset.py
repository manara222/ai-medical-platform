import os
import shutil
import random

SOURCE_DIR = "data/datasets/covid/train"
DEST_VAL = "data/datasets/covid/val"

VAL_RATIO = 0.15

classes = os.listdir(SOURCE_DIR)

for cls in classes:
    
    src_folder = os.path.join(SOURCE_DIR, cls)
    images = os.listdir(src_folder)
    
    random.shuffle(images)
    
    val_count = int(len(images) * VAL_RATIO)
    
    val_images = images[:val_count]
    
    dest_folder = os.path.join(DEST_VAL, cls)
    os.makedirs(dest_folder, exist_ok=True)
    
    for img in val_images:
        src = os.path.join(src_folder, img)
        dst = os.path.join(dest_folder, img)
        
        shutil.move(src, dst)

print("Validation set created successfully.")