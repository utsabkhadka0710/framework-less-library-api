import psycopg

def get_connection():
    return psycopg.connect(
        dbname = "library_db",
        user = "postgres",
        password = "rocketman",
        host = "localhost",
        port = "5432"
    )