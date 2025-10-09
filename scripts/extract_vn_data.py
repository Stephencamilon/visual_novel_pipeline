import requests
import json
import os

def extract_vn_data():
    # Ensures output folder exists
    os.makedirs("data/raw", exist_ok=True)

    # VNDB API endpoint
    url = "https://api.vndb.org/kana/vn"

    # Request body - asking for the first 100 released visual novels
    payload = {
        # "filters": ["released", "=", True],
        "fields": ("id, title, aliases, released, rating, developers{id,name}, length, platforms, image{id, url}, languages, description"),
        "results": 100,
        "page": 1
    }

    print("Fetching data from VNDB API...")
    response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})

    # response status
    if response.status_code == 200:
        data = response.json()
        os.makedirs("data/raw", exist_ok=True)

        with open("data/raw/vn_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"Saved {len(data.get('results', []))} visual novels to data/raw/vn_data.json")
   
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        print(response.text)
   
    print("Response JSON", response.json())

if __name__ == "__main__":
    extract_vn_data()