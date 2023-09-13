import psycopg2


def create_db():
    connection = psycopg2.connect(
        database='postgres',
        user='postgres',
        password='6802425'
    )
    connection.autocommit = True

    with connection.cursor() as cur:
        cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'netology_db';")
        exists = cur.fetchone()
        if not exists:
            cur.execute('CREATE DATABASE netology_db;')
            print("Database has been created successfully")
        else:
            print("Database exists")
    connection.close()