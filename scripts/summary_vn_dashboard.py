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

    # Prepare data for subplots
    rating_data = df["rating"].dropna()
    platforms_data = df["platforms"].value_counts().head(10)
    length_data = df.groupby("length")["rating"].mean().sort_values(ascending=False)
    dev_df = df.dropna(subset=["developers"]).copy()
    dev_df["developers"] = dev_df["developers"].str.split(", ")
    dev_df = dev_df.explode("developers")
    top_devs = dev_df.groupby("developers")["rating"].mean().sort_values(ascending=False).head(10)
    df["released"] = pd.to_datetime(df["released"], errors="coerce")
    df["year"] = df["released"].dt.year
    yearly = df[(df["year"] >= 2010) & (df["year"] <= 2020)].copy()
    top_per_year = yearly.sort_values(['year', 'rating'], ascending=[True, False]).groupby('year').first().reset_index()
    top_per_year["label"] = top_per_year["year"].astype(str) + ": " + top_per_year["title"]
    def extract_tag_names(tag_str):
        try:
            tags = ast.literal_eval(tag_str)
            return [tag.get("name") for tag in tags if isinstance(tag, dict)]
        except Exception:
            return []
    df["tag_names"] = df["tags"].dropna().apply(extract_tag_names)
    all_tag_names = df["tag_names"].explode()
    top_genres = all_tag_names.value_counts().head(10)

    # Create summary dashboard
    fig, axs = plt.subplots(3, 2, figsize=(16, 15))
    fig.suptitle("Visual Novel Database Summary", fontsize=22, x=0.5)  # Center the title

    # Rating Distribution
    axs[0, 0].hist(rating_data, bins=20, edgecolor="black")
    axs[0, 0].set_title("Distribution of VN Ratings")
    axs[0, 0].set_xlabel("Rating")
    axs[0, 0].set_ylabel("Count")

    # Most Common Platforms
    platforms_data.plot(kind="bar", color="skyblue", ax=axs[0, 1])
    axs[0, 1].set_title("Most Common Platforms")
    axs[0, 1].set_ylabel("Count")
    axs[0, 1].tick_params(axis='x', rotation=45)

    # Average Rating by Length
    length_data.plot(kind="bar", color="orange", ax=axs[1, 0])
    axs[1, 0].set_title("Average Rating by VN Length")
    axs[1, 0].set_ylabel("Average Rating")
    axs[1, 0].tick_params(axis='x', rotation=45)

    # Top 10 Developers by Avg Rating
    top_devs.plot(kind="bar", color="green", ax=axs[1, 1])
    axs[1, 1].set_title("Top 10 Developers by Average Rating")
    axs[1, 1].set_ylabel("Average Rating")
    axs[1, 1].tick_params(axis='x', rotation=45)

    # Top Visual Novel by Rating Per Year (2010-2020)
    axs[2, 0].barh(top_per_year["label"], top_per_year["rating"], color="teal")
    axs[2, 0].set_xlabel("Rating")
    axs[2, 0].set_title("Top VN by Rating Per Year (2010-2020)")

    # Top 10 Genres by Tag Name
    top_genres.plot(kind="bar", color="slateblue", ax=axs[2, 1])
    axs[2, 1].set_title("Top 10 Genres (Tag Names)")
    axs[2, 1].set_ylabel("Count")
    axs[2, 1].tick_params(axis='x', rotation=45)

    plt.tight_layout(rect=[0, 0.05, 1, 0.98])  # Add more space for the title
    plt.show()

if __name__ == "__main__":
    visualize_vn_data()