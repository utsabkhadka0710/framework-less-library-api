from .connection import get_cursor


def get_authors(name=None, sort=None, order="asc",id=None):

    base_query = "SELECT id, name, email FROM authors"

    if id:
        base_query += " WHERE id = %s"
        with get_cursor() as cur:
            cur.execute(base_query, (id,))
            row = cur.fetchone()
            return row

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

    with get_cursor() as cur:
        cur.execute(base_query,params)
        rows = cur.fetchall()
        return rows



def create_author(name, email):

    with get_cursor() as cur:
        cur.execute(
            "INSERT INTO authors(name, email) VALUES (%s, %s) RETURNING id, name, email;",
            (name, email)
            )
        new_author = cur.fetchone()
        return new_author


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
        
    params = (name, email, author_id)
    query = """
            UPDATE authors
            SET
                name = %s,
                email = %s
            WHERE id = %s
            RETURNING id, name, email
            """
    with get_cursor() as cur:
        cur.execute(query,params)
        row = cur.fetchone()
        message = "Updated"
        return [row], message



def delete_author(id=None):

    with get_cursor() as cur:
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

        return author_row,books_rows if author_row else ()