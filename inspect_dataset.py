from pathlib import Path
import pandas as pd

file_path = Path("data/mock_call_records_10000.xlsx")

df = pd.read_excel(file_path)

print("Rows:", len(df))
print("Columns:", df.columns.tolist())
print("\nData types:")
print(df.dtypes)
print("\nMissing values:")
print(df.isna().sum())
print("\nDuplicate rows:", df.duplicated().sum())
print("\nID column present:", "id" in df.columns)

if "id" in df.columns:
    print("Unique IDs:", df["id"].nunique())
    print("Duplicate IDs:", df["id"].duplicated().sum())

for column in ["callStartTime", "callEndTime"]:
    if column in df.columns:
        print(f"\n{column}:")
        print("Python types:", df[column].map(type).value_counts())
        print("Minimum:", df[column].min())
        print("Maximum:", df[column].max())