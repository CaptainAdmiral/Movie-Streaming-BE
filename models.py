from pydantic import BaseModel
from typing import Optional

class MovieSchema(BaseModel):
    id: int
    title: str
    release_date: Optional[str] = None
    poster_path: Optional[str] = None
    popularity: Optional[float] = None
    overview: Optional[str] = None

class Genre(BaseModel):
    id: int
    name: str

class ProductionCompany(BaseModel):
    id: int
    logo_path: Optional[str] = None
    name: str
    origin_country: str

class BelongsToCollection(BaseModel):
    id: int
    name: str
    poster_path: Optional[str] = None
    backdrop_path: Optional[str] = None

class MovieDetails(BaseModel):
    adult: bool
    backdrop_path: Optional[str] = None
    belongs_to_collection: Optional[BelongsToCollection] = None
    budget: int
    genres: list[Genre]
    homepage: Optional[str] = None
    id: int
    imdb_id: Optional[str] = None
    origin_country: list[str]
    original_language: str
    original_title: str
    overview: str
    popularity: float
    poster_path: Optional[str] = None
    production_companies: list[ProductionCompany]
    release_date: str
    revenue: int
    runtime: Optional[int] = None
    status: str
    tagline: Optional[str] = None
    title: str
    video: bool
    vote_average: float
    vote_count: int

class MovieListResponse(BaseModel):
    movies: list[MovieSchema]
    total: int
    limit: Optional[int] = None
    offset: Optional[int] = None

