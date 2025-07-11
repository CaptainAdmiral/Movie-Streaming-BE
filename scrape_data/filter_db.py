import os
import shelve
import sqlite3

DATA_PATH = "data"
conn = sqlite3.connect(os.path.join(DATA_PATH, "movies.db"))
porn = []
with shelve.open(os.path.join(DATA_PATH, "movie_details.db")) as db:
    for id, item in db.items():
        if any(tag["id"] == 10749 for tag in item["genres"]):
            porn.append(id)

cursor = conn.cursor()

ids_to_delete = []
placeholders = ", ".join(["?"] * len(ids_to_delete))
query = f"DELETE FROM movies WHERE id IN ({placeholders})"

cursor.execute(query, ids_to_delete)
conn.commit()

print(f"{cursor.rowcount} records deleted.")

cursor.close()
conn.close()
