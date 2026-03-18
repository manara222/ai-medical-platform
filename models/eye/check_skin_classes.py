import pandas as pd

METADATA_PATH = r"C:\Users\YOUR_NAME\Downloads\Compressed\archive\HAM10000_metadata.csv"

df = pd.read_csv(METADATA_PATH)

print("Columns:")
print(df.columns.tolist())

print("\nUnique values in dx:")
print(sorted(df["dx"].dropna().unique().tolist()))

print("\nClass counts:")
print(df["dx"].value_counts())