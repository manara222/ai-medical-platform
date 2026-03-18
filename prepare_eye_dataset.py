import os
import pandas as pd
import shutil
from sklearn.model_selection import train_test_split

DATA_PATH = "data/datasets/eye/ODIR-5K"
TRAIN_IMAGES = os.path.join(DATA_PATH, "Training Images")
TEST_IMAGES = os.path.join(DATA_PATH, "Testing Images")
LABEL_FILE = os.path.join(DATA_PATH, "data.xlsx")

OUTPUT_BASE = "data/datasets/eye"

CLASSES = [
    "Cataract",
    "Normal",
    "Diabetic Retinopathy",
    "Glaucoma"
]

print("Loading labels...")
df = pd.read_excel(LABEL_FILE)

print("Columns:", df.columns)

# استخراج الصور التي تحتوي على أحد الأمراض الأربعة
records = []

for _, row in df.iterrows():
    image_name = str(row["Left-Fundus"])  # اسم الصورة
    labels = str(row["Left-Diagnostic Keywords"])

    for disease in CLASSES:
        if disease.lower() in labels.lower():
            records.append({
                "image": image_name,
                "label": disease
            })
            break

data_df = pd.DataFrame(records)

print("Total usable images:", len(data_df))
print(data_df["label"].value_counts())

# تقسيم البيانات
train_df, temp_df = train_test_split(
    data_df,
    test_size=0.3,
    stratify=data_df["label"],
    random_state=42
)

val_df, test_df = train_test_split(
    temp_df,
    test_size=0.5,
    stratify=temp_df["label"],
    random_state=42
)

print("Train:", len(train_df))
print("Val:", len(val_df))
print("Test:", len(test_df))


def create_structure():
    for split in ["train", "val", "test"]:
        for cls in CLASSES:
            path = os.path.join(OUTPUT_BASE, split, cls.replace(" ", "_"))
            os.makedirs(path, exist_ok=True)


def copy_images(df, split):
    for _, row in df.iterrows():
        img = row["image"]
        label = row["label"].replace(" ", "_")

        src = os.path.join(TRAIN_IMAGES, img)

        if not os.path.exists(src):
            src = os.path.join(TEST_IMAGES, img)

        if not os.path.exists(src):
            continue

        dst = os.path.join(OUTPUT_BASE, split, label, img)

        shutil.copy2(src, dst)


create_structure()

copy_images(train_df, "train")
copy_images(val_df, "val")
copy_images(test_df, "test")

print("Eye dataset prepared successfully.")