def format_authors(author_row):
    return [
        {
            "id": r[0],
            "name": r[1],
            "email": r[2]
        } for r in author_row
    ]

def format_books(rows):
    return [
        {
            "id": r[0],
            "title": r[1],
            "isbn": r[2],
            "published_year":r[3],
            "author":{
                "author_id": r[4],
                "author_name": r[5]
            }
         } for r in rows
    ]