import pandas as pd

# مسار ملف metadata
METADATA_PATH = "data/HAM10000_metadata.csv"

# قراءة الملف
df = pd.read_csv(METADATA_PATH)

print("\nColumns in dataset:")
print(df.columns.tolist())

print("\nUnique classes in dx column:")
print(sorted(df["dx"].unique()))

print("\nClass distribution:")
print(df["dx"].value_counts())