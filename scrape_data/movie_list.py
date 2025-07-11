import os
import requests
import csv
import time

API_KEY = os.getenv('API_KEY')
BASE_URL = 'https://api.themoviedb.org/3'
OUTPUT_CSV = 'popular_movies.csv'
PAGES = 50

def fetch_popular_movies(page):
    url = f"{BASE_URL}/movie/popular"
    params = {
        'api_key': API_KEY,
        'language': 'en-US',
        'page': page
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get('results', [])

def write_movies_to_csv(movies, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'title', 'release_date', 'poster_path', 'popularity', 'overview']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for movie in movies:
            writer.writerow({
                'id': movie.get('id'),
                'title': movie.get('title'),
                'release_date': movie.get('release_date'),
                'poster_path': movie.get('poster_path'),
                'popularity': movie.get('popularity'),
                'overview': movie.get('overview')
            })

def main():
    all_movies = []
    for page in range(1, PAGES + 1):
        print(f"Fetching page {page}...")
        movies = fetch_popular_movies(page)
        all_movies.extend(movies)
        time.sleep(0.25)

    print(f"Fetched {len(all_movies)} movies. Writing to CSV...")
    write_movies_to_csv(all_movies, OUTPUT_CSV)
    print(f"Done. Data saved to '{OUTPUT_CSV}'.")

if __name__ == '__main__':
    main()
