class ESLoader:
    """Класс загрузки данных в Elasticsearch"""

    def __init__(self, connection, index_name):
        self.connection = connection
        self.index_name = index_name

    def load_data_to_elasticsearch(self, movies_from_postgres):
        """Метод загрузки данных в Elasticsearch"""
        for movie in movies_from_postgres:
            self.connection.index(index=self.index_name, doc_type="_doc", body=movie, id=movie.get("id"))
