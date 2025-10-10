import requests
import json
import os

def extract_vn_data():
    # Ensures output folder exists
    os.makedirs("data/raw", exist_ok=True)

    url = "https://api.vndb.org/kana/vn"
    all_results = []
    page = 1
    while True:
        payload = {
            # "filters": ["released", "=", True],
            "fields": ("id, title, aliases, released, rating, developers{id,name}, length, platforms, image{id, url}, languages, description"),
            "results": 100,
            "page": page
        }
        print(f"Fetching page {page} from VNDB API...")
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            if not results:
                print("No more results found.")
                break
            all_results.extend(results)
            print(f"Fetched {len(results)} visual novels from page {page}.")
            if len(results) < 100:
                print("Last page reached.")
                break
            page += 1
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            print(response.text)
            break
    with open("data/raw/vn_data.json", "w", encoding="utf-8") as f:
        json.dump({"results": all_results}, f, indent=4, ensure_ascii=False)
    print(f"Saved {len(all_results)} visual novels to data/raw/vn_data.json")
    print("Response JSON", data)
   
   

if __name__ == "__main__":
    extract_vn_data()