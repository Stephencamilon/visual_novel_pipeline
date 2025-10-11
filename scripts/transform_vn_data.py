import json
import pandas as pd
import os

def transform_vn_data():
    # 1️⃣ Load raw JSON
    raw_path = "data/raw/vn_data.json"
    clean_path = "data/clean/visual_novels_clean.csv"

    if not os.path.exists(raw_path):
        print(f"❌ File not found: {raw_path}. Run extract_vn_data.py first.")
        return

    with open(raw_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    vn_list = data.get("results", [])
    if not vn_list:
        print("❌ No visual novel data found in the file.")
        return

    # 2️⃣ Flatten nested 'developers' field
    for vn in vn_list:
        devs = vn.get("developers", [])
        vn["developers"] = ", ".join([d.get("name", "") for d in devs]) if devs else None

    # 3️⃣ Create DataFrame
    df = pd.DataFrame(vn_list)
    
    # Reorder columns: id, title, description first
    first_cols = ["id", "title", "description"]
    other_cols = [col for col in df.columns if col not in first_cols]
    df = df[first_cols + other_cols]

    # 4️⃣ Clean data
    # Replace empty strings with NaN
    df.replace("", pd.NA, inplace=True)
    # Remove duplicates by title
    df.drop_duplicates(subset=["title"], inplace=True)
    # Sort alphabetically by title
    df.sort_values(by="title", inplace=True)

    # 5️⃣ Save to CSV
    os.makedirs("data/clean", exist_ok=True)
    df.to_csv(clean_path, index=False, encoding="utf-8")

    print(f"✅ Clean data saved to {clean_path}")
    print(f"📊 {len(df)} rows | {len(df.columns)} columns")

if __name__ == "__main__":
    transform_vn_data()
