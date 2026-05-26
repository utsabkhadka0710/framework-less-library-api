from .connection import get_cursor


def get_books(title=None,isbn=None, author=None, year=None, sort=None, order="asc",id=None):

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
        with get_cursor() as cur:
            cur.execute(base_query, (id,))
            row = cur.fetchone()
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
    
    with get_cursor() as cur:
        cur.execute(base_query,params)
        rows = cur.fetchall()
        return rows



def create_book(title, isbn, published_year, author_id):
    with get_cursor() as cur:
        print("create book called")
        cur.execute(
            """INSERT INTO books (title, isbn, published_year, author_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id, title, isbn, published_year, author_id""",
            (title, isbn, published_year, author_id)
        )
        new_book = cur.fetchone()
        print(new_book)
        return new_book



def put_book(book_id, title, isbn, published_year, author_id):

    if not get_books(id=book_id):
        print("put book entered line 132")
        try:
            print(create_book(title=title,isbn=isbn,published_year=published_year,author_id=author_id))
            row = get_books(isbn=isbn)
            print("inside put book try line 136: ",row)
            message = "Created"
            return row, message
        except Exception as e:
            return None, e
          

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
    
    with get_cursor() as cur:
        cur.execute(query,params)
        row = cur.fetchone()
        message = "Updated"
        return [row], message



def delete_book(id=None): 

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
    with get_cursor() as cur:
        cur.execute(select_query,(id,))
        row = cur.fetchone()
        query = "DELETE FROM books WHERE id = %s "
        cur.execute(query,(id,))
        return row