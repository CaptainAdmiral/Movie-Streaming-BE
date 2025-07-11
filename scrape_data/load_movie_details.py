import json
import os
import shelve
from typing import Any


def load_movie_details_to_db():
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    db_path = os.path.join(data_dir, "movie_details.db")
    json_path = "movies/movie_details.json"

    with open(json_path, "r", encoding="utf-8") as file:
        movie_data: dict[str, Any] = json.load(file)

    count = 0
    with shelve.open(db_path) as db:
        for movie_id, movie_details in movie_data.items():
            db[movie_id] = movie_details

        count = len(db)
    print(f"Loaded {count} movie details into db")

    db.close()


if __name__ == "__main__":
    load_movie_details_to_db()
