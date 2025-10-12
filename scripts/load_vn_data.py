import sqlite3
import pandas as pd
import os

def load_vn_data():
    clean_path = "data/clean/visual_novels_clean.csv"
    db_path = "data/visual_novel_db.sqlite"

    if not os.path.exists(clean_path):
        print(f"❌ Clean CSV not found: {clean_path}. Run transform_vn_data.py first.")
        return

    print("📂 Loading cleaned data into SQLite database...")

    # 1️⃣ Load the cleaned CSV
    df = pd.read_csv(clean_path)

    # 2️⃣ Create (or connect to) the SQLite DB
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 3️⃣ Create the table (replace if exists)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visual_novels (
            id TEXT,
            title TEXT,
            released TEXT,
            rating REAL,
            length TEXT,
            platforms TEXT,
            developers TEXT
        )
    """)

    # 4️⃣ Insert data (replace old data)
    df.to_sql("visual_novels", conn, if_exists="replace", index=False)

    # 5️⃣ Quick test query
    sample = pd.read_sql("SELECT title, rating FROM visual_novels ORDER BY rating DESC LIMIT 5", conn)
    print("🔥 Top 5 Rated Visual Novels:")
    print(sample)

    conn.close()
    print(f"✅ Data successfully loaded into {db_path}")

if __name__ == "__main__":
    load_vn_data()
