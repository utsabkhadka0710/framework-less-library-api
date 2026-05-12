from .connection import get_connection


def author_exists(author_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM authors WHERE id = %s", (author_id,))

    row = cur.fetchone()

    cur.close()
    conn.close()

    return row is not None



def get_authors(name=None, email=None, sort=None, order="desc",id=None):
    conn = get_connection()
    cur = conn.cursor()

    base_query = "SELECT id, name, email FROM authors"

    if id:
        base_query += " WHERE id = %s"

        cur.execute(base_query, (id,))

        row = cur.fetchone()

        cur.close()
        conn.close()

        return row
    
    params= []

    if name:
        base_query += " WHERE name ILIKE %s "
        params.append(f"%{name}%")

    if email:
        base_query += " AND email = %s" if name else " WHERE email = %s"
        params.append(f"{email}")

    #SORTING (safe)
    allowed_sort_fields = {
        "name": "name",
        "created_at": "created_at",
        "id": "id"
    }

    sort_field = allowed_sort_fields.get(sort,"id")

    order = order.lower()
    if not order in ["asc","desc"]:
        order = "desc"

    base_query += f" ORDER BY {sort_field} {order}"

    cur.execute(base_query,params)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows



def create_author(name, email):
    conn = get_connection()

    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO authors(name, email) VALUES (%s, %s) RETURNING id, name, email;",
            (name, email)
            )
        
        new_author = cur.fetchone()

        conn.commit()
    
    except:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()

    return new_author



def get_books(title=None, author=None, year=None, sort=None, order="desc",id=None):
    conn = get_connection()
    cur = conn.cursor()

    base_query = """
            SELECT
                books.id,
                books.title,
                books.isbn,
                books.published_year,
                books.author_id,
                authors.name,
                authors.email
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
        order = "desc"

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

    except:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()
        
    return new_book

