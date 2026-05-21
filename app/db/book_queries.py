from .connection import get_connection


def get_books(title=None,isbn=None, author=None, year=None, sort=None, order="asc",id=None):
    conn = get_connection()
    cur = conn.cursor()

    base_query = """
            SELECT
                books.id,
                books.title,
                books.isbn,
                books.published_year,
                books.author_id,
                authors.name
            FROM books
            JOIN authors ON books.author_id=authors.id
    """

    if id:
        base_query = base_query + " WHERE books.id = %s"
        cur.execute(base_query, (id,))

        row = cur.fetchone()

        cur.close()
        conn.close()

        return row


    conditions = []
    params = []

    if title:
        conditions.append("books.title ILIKE %s")
        params.append(f"%{title}%")

    if isbn:
        conditions.append("books.isbn ILIKE %s")
        params.append(isbn)

    if author:
        conditions.append("authors.name ILIKE %s")
        params.append(f"%{author}%")

    if year:
        conditions.append("books.published_year = %s")
        params.append(year)


    if conditions:
        base_query += " WHERE " + " AND " .join(conditions)


    allowed_sorted_fields = {
        "title": "books.title",
        "published_year": "books.published_year",
        "created_year": "books.created_at"
    }

    sort_field = allowed_sorted_fields.get(sort,"books.id")

    order = order.lower()
    if order not in ["asc","desc"]:
        order = "asc"

    base_query += f" ORDER BY {sort_field} {order}"
    

    cur.execute(base_query,params)
    
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows




def create_book(title, isbn, published_year, author_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """INSERT INTO books (title, isbn, published_year, author_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id, title, isbn, published_year, author_id""",
            (title, isbn, published_year, author_id)
        )

        new_book = cur.fetchone()
        conn.commit()

        return new_book
    except:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()




def put_book(book_id, title, isbn, published_year, author_id):
    
    conn = get_connection()
    cur = conn.cursor()

    if not get_books(id=book_id):
        try:
            create_book(title=title,isbn=isbn,published_year=published_year,author_id=author_id)
            row = get_books(isbn=isbn)
            message = "Created"

            return row, message

        except Exception as e:
            print("Error: ",e)
            return None
        
        finally:
            cur.close()
            conn.close()
    
          
    query = """WITH updated_book AS (
                    UPDATE books
                    SET
                        title = %s,
                        isbn =%s,
                        published_year = %s,
                        author_id = %s
                    WHERE id = %s
                    RETURNING id, title, isbn, published_year, author_id
                )
                SELECT
                    ub.id, ub.title, ub.isbn, ub.published_year, authors.id, authors.name
                    FROM updated_book as ub
                    JOIN authors ON ub.author_id = authors.id
                """
    
    
    params = (title,isbn,published_year,author_id,book_id)
    try:
        cur.execute(query,params)

        row = cur.fetchone()
        message = "Updated"
        conn.commit()

        return [row], message

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()




def delete_book(id=None): 
    conn = get_connection()
    cur = conn.cursor()

    try:

        select_query = """
                        SELECT
                            books.id,
                            books.title,
                            books.isbn,
                            books.published_year,
                            books.author_id,
                            authors.name
                        FROM books
                        JOIN authors ON books.author_id = authors.id
                        where books.id = %s
                        """
        cur.execute(select_query,(id,))
        row = cur.fetchone()

        if row:
            query = "DELETE FROM books WHERE id = %s "
            cur.execute(query,(id,))
            conn.commit()

        cur.close()
        conn.close()

        return row

        
    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()
        