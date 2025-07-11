import csv
import os
import sqlite3


def load_movies_csv_to_sqlite():
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    db_path = os.path.join(data_dir, "movies.db")
    csv_path = "movies/popular_movies.csv"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # fmt: off
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            release_date TEXT,
            poster_path TEXT,
            popularity REAL,
            overview TEXT
        )
    ''')
    # fmt: on

    cursor.execute("DELETE FROM movies")

    with open(csv_path, "r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            # fmt: off
            cursor.execute("""
                INSERT OR IGNORE INTO movies (
                    id,
                    title,
                    release_date,
                    poster_path,
                    popularity,
                    overview
                ) VALUES (
                    ?, ?, ?, ?, ?, ?
                );
            """, (
                int(row['id']),
                row['title'],
                row['release_date'],
                row['poster_path'],
                float(row['popularity']),
                row['overview']
            ))
            # fmt: on

    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM movies")
    count = cursor.fetchone()[0]
    print(f"Loaded {count} movies into the database")

    conn.close()


if __name__ == "__main__":
    load_movies_csv_to_sqlite()
