import csv
import os
import time
import requests
import mimetypes

# Config
POSTER_BASE_URL = 'https://image.tmdb.org/t/p/w500'
INPUT_CSV = 'popular_movies.csv'
POSTER_DIR = 'posters'

os.makedirs(POSTER_DIR, exist_ok=True)

def get_extension_from_content_type(content_type):
    ext = mimetypes.guess_extension(content_type)
    if ext == '.jpe':
        return '.jpg'
    return ext or '.jpg'

def download_poster(movie_id, poster_path):
    if not poster_path:
        print(f"Skipping ID {movie_id} (no poster_path)")
        return

    url = POSTER_BASE_URL + poster_path
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        content_type = response.headers.get('Content-Type', 'image/jpeg')
        extension = get_extension_from_content_type(content_type)
        filename = f"{movie_id}{extension}"
        filepath = os.path.join(POSTER_DIR, filename)

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"✔ Downloaded {filename}")
    except Exception as e:
        print(f"✖ Failed to download poster for ID {movie_id}: {e}")

def main():
    with open(INPUT_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            movie_id = row['id']
            poster_path = row['poster_path']
            download_poster(movie_id, poster_path)
            time.sleep(0.2)

if __name__ == '__main__':
    main()
