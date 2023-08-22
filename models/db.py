import psycopg2
from elasticsearch import Elasticsearch

#postgreSQL

class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            host='localhost',
            dbname='Property',
            user='myuser',
            password='mypassword'
        )
        self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()
        self.connection.close()

db = Database()

#elasticsearch

def elasticsearch_connection():
    ELASTICSEARCH_HOST = 'localhost'
    ELASTICSEARCH_PORT = 9201  
    ELASTICSEARCH_SCHEME = 'http' 
    es = Elasticsearch([{'host': ELASTICSEARCH_HOST, 'port': ELASTICSEARCH_PORT, 'scheme': ELASTICSEARCH_SCHEME}])
    return es

