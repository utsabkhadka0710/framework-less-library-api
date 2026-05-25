from .connection import db_pool


def get_authors(name=None, sort=None, order="asc",id=None):
    conn = db_pool.getconn()
    cur = conn.cursor()

    base_query = "SELECT id, name, email FROM authors"

    if id:
        base_query += " WHERE id = %s"
        try:
            cur.execute(base_query, (id,))
            row = cur.fetchone()
            return row
        except Exception as e:
            conn.rollback()
            raise
        finally:
            cur.close()
            db_pool.putconn(conn)

    
    params= []

    if name:
        base_query += " WHERE name ILIKE %s "
        params.append(f"%{name}%")

    allowed_sort_fields = {
        "name": "name",
        "created_at": "created_at",
        "id": "id"
    }

    sort_field = allowed_sort_fields.get(sort,"id")

    order = order.lower()
    if not order in ["asc","desc"]:
        order = "asc"

    base_query += f" ORDER BY {sort_field} {order}"

    try:
        cur.execute(base_query,params)
        rows = cur.fetchall()
        return rows
    except Exception as e:
        conn.rollback()
        raise
    finally:
        cur.close()
        db_pool.putconn(conn)



def create_author(name, email):
    conn = db_pool.getconn()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO authors(name, email) VALUES (%s, %s) RETURNING id, name, email;",
            (name, email)
            )
        
        new_author = cur.fetchone()

        conn.commit()

        return new_author
    except Exception as e:
        conn.rollback()
        raise
    finally:
        cur.close()
        db_pool.putconn(conn)



def put_author(author_id, name, email):

    if not get_authors(id=author_id):
        try:
            new_row = create_author(name,email)
            new_author_id = new_row[0]
            row = get_authors(id=new_author_id)
            message = "Created"
            return [row], message
        except Exception as e:
            return (),e

        
    

    conn = db_pool.getconn()
    cur = conn.cursor()
    params = (name, email, author_id)
    query = """
            UPDATE authors
            SET
                name = %s,
                email = %s
            WHERE id = %s
            RETURNING id, name, email
            """
    try:
        cur.execute(query,params)
        row = cur.fetchone()
        message = "Updated"
        conn.commit()
        return [row], message
    except Exception as e:
        return None,e
        conn.rollback()
        raise
    finally:
        cur.close()
        db_pool.putconn(conn)



def delete_author(id=None):
    conn = db_pool.getconn()
    cur = conn.cursor()

    try:
        cur.execute("SELECT id,name,email FROM authors WHERE id = %s",(id,))
        author_row = cur.fetchone()

        if author_row:
            select_books_query = """
                            SELECT
                                id as book_id,
                                title,
                                isbn,
                                published_year
                            FROM books
                            WHERE author_id = %s
                            """
            cur.execute(select_books_query,(id,))
            books_rows = cur.fetchall()

            query = "DELETE FROM authors WHERE id = %s"
            cur.execute(query,(id,))
            conn.commit()

        return author_row,books_rows if author_row else ()
    except Exception as e:
        conn.rollback()
        raise
    finally:
        cur.close()
        db_pool.putconn(conn)
        