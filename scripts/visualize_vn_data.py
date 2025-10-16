import pandas as pd
import matplotlib.pyplot as plt
import os
import ast

def visualize_vn_data():
    data_path = "data/clean/visual_novels_clean.csv"
    if not os.path.exists(data_path):
        print(f"❌ Missing file: {data_path}. Run transform_vn_data.py first.")
        return

    df = pd.read_csv(data_path)
    print("✅ Data loaded successfully.")
    print(f"Rows: {len(df)}, Columns: {len(df.columns)}")

    # --- Rating Distribution ---
    plt.figure(figsize=(8, 5))
    df["rating"].dropna().hist(bins=20, edgecolor="black")
    plt.title("Distribution of VN Ratings")
    plt.xlabel("Rating")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()

    # --- Most Common Platforms ---
    plt.figure(figsize=(8, 5))
    df["platforms"].value_counts().head(10).plot(kind="bar", color="skyblue")
    plt.title("Most Common Platforms")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # --- Average Rating by Length ---
    plt.figure(figsize=(7, 4))
    df.groupby("length")["rating"].mean().sort_values(ascending=False).plot(kind="bar", color="orange")
    plt.title("Average Rating by VN Length")
    plt.ylabel("Average Rating")
    plt.tight_layout()
    plt.show()

    # --- Top 10 Developers by Avg Rating ---
    dev_df = df.dropna(subset=["developers"]).copy()
    dev_df["developers"] = dev_df["developers"].str.split(", ")
    dev_df = dev_df.explode("developers")
    top_devs = dev_df.groupby("developers")["rating"].mean().sort_values(ascending=False).head(10)

    plt.figure(figsize=(9, 5))
    top_devs.plot(kind="bar", color="green")
    plt.title("Top 10 Developers by Average Rating")
    plt.ylabel("Average Rating")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
   # --- Top Visual Novel by Rating Per Year (2010-2020) ---
    df["released"] = pd.to_datetime(df["released"], errors="coerce")
    df["year"] = df["released"].dt.year
    yearly = df[(df["year"] >= 2010) & (df["year"] <= 2020)].copy()
    top_per_year = yearly.sort_values(['year', 'rating'], ascending=[True, False]).groupby('year').first().reset_index()

    # Create labels like "2011: VN Title"
    top_per_year["label"] = top_per_year["year"].astype(str) + ": " + top_per_year["title"]

    plt.figure(figsize=(12, 7))
    plt.barh(top_per_year["label"], top_per_year["rating"], color="teal")
    plt.xlabel("Rating")
    plt.title("Top Visual Novel by Rating Per Year (2010-2020)")
    plt.tight_layout()
    plt.show()
    
    # --- Top 10 Genres by Tag Name ---
    def extract_tag_names(tag_str):
        try:
            tags = ast.literal_eval(tag_str)
            return [tag.get("name") for tag in tags if isinstance(tag, dict)]
        except Exception:
            return []

    df["tag_names"] = df["tags"].dropna().apply(extract_tag_names)
    all_tag_names = df["tag_names"].explode()
    top_genres = all_tag_names.value_counts().head(10)

    plt.figure(figsize=(9, 5))
    top_genres.plot(kind="bar", color="slateblue")
    plt.title("Top 10 Genres (Tag Names) in Visual Novel Database")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    

if __name__ == "__main__":
    visualize_vn_data()
