from app.db.connection import get_connection

def main():
        
    conn = get_connection()
    cur = conn.cursor()
        
    query = """CREATE TABLE authors(
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE books(
                id SERIAL PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                isbn VARCHAR(10) UNIQUE not NULL,
                published_year INT,
                author_id INT REFERENCES authors(id) ON DELETE CASCADE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );"""
    try:  
        cur.execute(query=query)
    except:
        raise conn.rollback
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    from app.utils.logger import create_logger
    logger = create_logger(__name__)
    try:
        logger.info("Migrating tables...")
        main()
        logger.info("Tables migrated sucessfully!")
    except Exception as e:
        logger.error(f"Error occured during migration: {e}")
