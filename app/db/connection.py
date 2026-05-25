import os
import psycopg
from psycopg_pool import ConnectionPool
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()
db_config = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("USER"),
    "password": os.getenv("PASSWORD"),
    "host": os.getenv("HOST"),
    "port": os.getenv("PORT")
}

def get_connection():
    return psycopg.connect(
        **db_config
    )

db_pool = ConnectionPool(
    conninfo="",
    kwargs= db_config,
    min_size=1,
    max_size=50,
    open=True
)

@contextmanager
def get_cursor():
    conn = db_pool.getconn()
    cur = conn.cursor()

    try:
        yield cur
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise
    finally:
        cur.close()
        db_pool.putconn(conn)
