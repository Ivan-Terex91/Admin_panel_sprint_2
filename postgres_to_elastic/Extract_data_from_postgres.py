from settings import dsn_pg
import psycopg2


class PostgresLoader:
    """Класс загрузки фильмов из postgresql."""

    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.all_movie_list = []
        self.transform_movie_list = []

    def load_movies(self) -> list:
        """Метод загрузки всех фильмов."""

        self.cursor.execute("""
        SELECT movie.id, movie.title, movie.description, movie.creation_date, 
        movie.age_limit, movie.rating, movie.imdb_rating, movie.movie_type
        FROM content.movies_movie AS movie """)

        for row in self.cursor.fetchall():
            self.all_movie_list.append(row)

        for _movie in self.all_movie_list:
            movie = Movie(self.cursor, *_movie)
            movie.transform_data()
            self.transform_movie_list.append(movie.__dict__)

        return self.transform_movie_list


class Movie:
    """Фильмы"""

    def __init__(self, cursor, idx, title, description, creation_date, age_limit, imdb_rating, rating, movie_type):
        self.cursor = cursor
        self.id = idx
        self.title = title
        self.description = description
        self.creation_date = creation_date
        self.age_limit = age_limit
        self.imdb_rating = imdb_rating
        self.rating = rating
        self.movie_type = movie_type
        self.genres = []
        self.actors = []
        self.directors = []
        self.writers = []

    def genres_list(self):
        """Запрашиваем все жанры связаные с фильмом"""

        self.cursor.execute("""
        SELECT genre.name 
        FROM content.movies_genre AS genre INNER JOIN 
        content.movies_movie_genres AS movie_genres
        ON movie_genres.genre_id = genre.id
        AND movie_genres.movie_id = %s""", (self.id,))

        for genre in self.cursor.fetchall():
            self.genres.append(*genre)

    def persons(self):
        """Запрашиваем всех людей связанных с фильмом"""
        self.cursor.execute("""
        SELECT person.firstname, person.lastname, movieperson.role
        FROM content.movies_person AS person INNER JOIN content.movies_movieperson AS movieperson
        ON person.id = movieperson.person_id
        AND movieperson.movie_id = %s""", (self.id,))

        for person in self.cursor.fetchall():
            if person[-1] == 'actor':
                self.actors.append(" ".join((person[0], person[1])))
            if person[-1] == 'writer':
                self.writers.append(" ".join((person[0], person[1])))
            if person[-1] == 'director':
                self.directors.append(" ".join((person[0], person[1])))

    def transform_data(self):
        """Метод нормализации данных."""
        self.genres_list()
        self.persons()
        del self.cursor


if __name__ == '__main__':
    with psycopg2.connect(**dsn_pg) as postgres_conn:
        pg = PostgresLoader(postgres_conn)
        pg.load_movies()
