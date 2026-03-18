import os
import shutil
import pandas as pd
from sklearn.model_selection import train_test_split

# =========================
# Paths
# =========================
METADATA_PATH = "data/HAM10000_metadata.csv"
IMAGE_DIR_1 = "data/HAM10000_images_part_1"
IMAGE_DIR_2 = "data/HAM10000_images_part_2"
OUTPUT_BASE = "data/datasets/skin"

# =========================
# Settings
# =========================
TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15
RANDOM_STATE = 42

# =========================
# Read metadata
# =========================
df = pd.read_csv(METADATA_PATH)

# Keep only needed columns
df = df[["image_id", "dx"]].copy()

# Create full image path
def find_image_path(image_id):
    path1 = os.path.join(IMAGE_DIR_1, f"{image_id}.jpg")
    path2 = os.path.join(IMAGE_DIR_2, f"{image_id}.jpg")

    if os.path.exists(path1):
        return path1
    elif os.path.exists(path2):
        return path2
    else:
        return None

df["image_path"] = df["image_id"].apply(find_image_path)

# Remove missing images if any
df = df[df["image_path"].notnull()].reset_index(drop=True)

print(f"Total valid images found: {len(df)}")
print("\nClass distribution before split:")
print(df["dx"].value_counts())

# =========================
# Split per class
# =========================
train_data = []
val_data = []
test_data = []

classes = sorted(df["dx"].unique())

for class_name in classes:
    class_df = df[df["dx"] == class_name]

    train_df, temp_df = train_test_split(
        class_df,
        test_size=(1 - TRAIN_RATIO),
        random_state=RANDOM_STATE,
        shuffle=True
    )

    val_df, test_df = train_test_split(
        temp_df,
        test_size=(TEST_RATIO / (VAL_RATIO + TEST_RATIO)),
        random_state=RANDOM_STATE,
        shuffle=True
    )

    train_data.append(train_df)
    val_data.append(val_df)
    test_data.append(test_df)

train_df = pd.concat(train_data).reset_index(drop=True)
val_df = pd.concat(val_data).reset_index(drop=True)
test_df = pd.concat(test_data).reset_index(drop=True)

print("\nSplit sizes:")
print(f"Train: {len(train_df)}")
print(f"Val:   {len(val_df)}")
print(f"Test:  {len(test_df)}")

# =========================
# Create folders
# =========================
for split_name in ["train", "val", "test"]:
    for class_name in classes:
        os.makedirs(os.path.join(OUTPUT_BASE, split_name, class_name), exist_ok=True)

# =========================
# Copy images
# =========================
def copy_images(split_df, split_name):
    for _, row in split_df.iterrows():
        src = row["image_path"]
        class_name = row["dx"]
        image_name = os.path.basename(src)

        dst = os.path.join(OUTPUT_BASE, split_name, class_name, image_name)
        shutil.copy2(src, dst)

copy_images(train_df, "train")
copy_images(val_df, "val")
copy_images(test_df, "test")

print("\nDataset prepared successfully.")
print(f"Saved to: {OUTPUT_BASE}")

print("\nFinal class distribution:")
for split_name, split_df in [("train", train_df), ("val", val_df), ("test", test_df)]:
    print(f"\n{split_name.upper()}:")
    print(split_df["dx"].value_counts())