import os
import shelve
import sqlite3
from sqlite3 import Connection as SQLiteConnection
from typing import Optional

import uvicorn
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import MovieDetails, MovieListResponse, MovieSchema

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

movies_router = APIRouter(prefix="/movies", tags=["movies"])

DATA_PATH = "data"
assert os.path.exists(DATA_PATH)


# Stand-in for a relational database like postgres
def get_sqlite():
    conn = sqlite3.connect(os.path.join(DATA_PATH, "movies.db"))
    try:
        yield conn
    finally:
        conn.close()


# Stand-in for a key value store or documentdb like dynamodb
def get_kv_store():
    with shelve.open(os.path.join(DATA_PATH, "movie_details.db")) as db:
        yield db


@app.get("/")
def root():
    return {"status": "ok"}


@movies_router.get("/", response_model=MovieListResponse)
def list_movies(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    search: Optional[str] = None,
    db: SQLiteConnection = Depends(get_sqlite),
):
    cursor = db.cursor()

    count_query = "SELECT COUNT(*) FROM movies"
    count_params = []

    if search is not None:
        count_query += " WHERE title LIKE ?"
        count_params.append(f"%{search}%")

    cursor.execute(count_query, count_params)
    count = cursor.fetchone()[0]

    # fmt: off
    query = """
        SELECT 
            id,
            title,
            release_date,
            poster_path,
            popularity,
            overview
        FROM 
            movies
    """
    # fmt: on

    params = []

    if search is not None:
        query += " WHERE title like ?"
        params.append(f"%{search}%")

    query += " ORDER BY popularity DESC"

    if limit is not None:
        query += " LIMIT ?"
        params.append(limit)

    if offset is not None:
        query += " OFFSET ?"
        params.append(offset)

    cursor.execute(query, params)
    rows = cursor.fetchall()

    movies = []
    for row in rows:
        movie = MovieSchema(
            id=row[0],
            title=row[1],
            release_date=row[2],
            poster_path=row[3],
            popularity=row[4],
            overview=row[5],
        )
        movies.append(movie)

    return MovieListResponse(movies=movies, total=count, limit=limit, offset=offset)


@movies_router.get("/{movie_id}", response_model=MovieDetails)
def get_movie_details(movie_id: int, db: shelve.Shelf = Depends(get_kv_store)):
    movie_data = db.get(str(movie_id))

    if not movie_data:
        raise HTTPException(status_code=404, detail="Movie not found")

    return MovieDetails(**movie_data)


app.include_router(movies_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
