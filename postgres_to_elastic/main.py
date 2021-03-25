from elasticsearch import Elasticsearch
import psycopg2
from psycopg2.extensions import connection as _connection
from Load_data_to_elastic_search import ESLoader
from Extract_data_from_postgres import PostgresLoader
from settings import dsn_pg, dsn_es


def load_data_from_postgres_to_elasticsearch(pg_conn: _connection, es: Elasticsearch, es_index_name: str):
    """Основной метод загрузки данных из Postgres в Elasticsearch"""
    postgres_loader = PostgresLoader(pg_conn)
    elasticsearch_loader = ESLoader(es, es_index_name)

    data = postgres_loader.load_movies()
    elasticsearch_loader.load_data_to_elasticsearch(data)


if __name__ == "__main__":
    with psycopg2.connect(**dsn_pg) as postgres_conn, Elasticsearch(
            [{"host": dsn_es.get("host"), "port": dsn_es.get("port")}]) as es_conn:
        load_data_from_postgres_to_elasticsearch(postgres_conn, es_conn, dsn_es.get("index_name"))
