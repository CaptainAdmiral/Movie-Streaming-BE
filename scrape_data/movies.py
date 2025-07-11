import csv
import json
import os
import requests
import time

API_KEY = os.getenv('API_KEY')
BASE_URL = 'https://api.themoviedb.org/3'
INPUT_CSV = 'popular_movies.csv'
OUTPUT_JSON = 'movie_details.json'

def read_movie_ids_from_csv(filename):
    ids = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ids.append(row['id'])
    return ids

def fetch_movie_detail(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {
        'api_key': API_KEY,
        'language': 'en-US'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch movie ID {movie_id}: {response.status_code}")
        return None

def main():
    movie_ids = read_movie_ids_from_csv(INPUT_CSV)
    results = {}

    for idx, movie_id in enumerate(movie_ids, 1):
        if movie_id in results:
            continue

        print(f"[{idx}/{len(movie_ids)}] Fetching details for ID {movie_id}...")
        data = fetch_movie_detail(movie_id)
        if data:
            results[movie_id] = data
        time.sleep(0.25)

    print(f"Saving {len(results)} movie details to {OUTPUT_JSON}...")
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as jsonfile:
        json.dump(results, jsonfile, indent=2)

    print("Done.")

if __name__ == '__main__':
    main()
