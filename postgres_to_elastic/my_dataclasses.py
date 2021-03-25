from dataclasses import dataclass, field
import uuid


@dataclass
class Movie:
    """Фильмы"""
    title: str
    description: str
    creation_date: str
    age_limit: int
    imdb_rating: float
    rating: float
    movie_type: str
    genres: list = field(default_factory=list)
    actors: list = field(default_factory=list)
    directors: list = field(default_factory=list)
    writers: list = field(default_factory=list)
    id: uuid.UUID = field(default_factory=uuid.uuid4)
