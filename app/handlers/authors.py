import re
import app.db.author_queries as queries
from app.utils.logger import create_logger
from app.utils.validator import is_valid_email
from app.utils.formatter import format_authors


logger = create_logger(name=__name__)

print()

def authors_handler(query, params=None):

    if params:
        id = params.get("id")
        row = queries.get_authors(id=id)

        if row:
            data = format_authors([row])
            return 200, {
                "status": "success",
                "data": data
            }
        return 404, {
            "error": "Not found",
        }


    name = query.get("name",[None])[0]
    sort = query.get("sort",[None])[0]
    order = query.get("order",["asc"])[0]

    rows = queries.get_authors(name,sort,order)
    data = format_authors(rows)
    return 200, {
        "status":"success",
        "data":data
        }

def create_author_handler(data):
    name = data.get("name")
    email = data.get("email")

    if not name or len(name)<2:
        return 400, {
            "status":"error",
            "message": "name must be atleast 2 characters"
        }
    
    if not email or not is_valid_email(email):     
        return 400,{
            "status": "error",
            "message": "enter a valid Email"
        }


    try:
        row = queries.create_author(name,email)

        author = format_authors([row])

        return 201, {
            "status": "success",
            "data": author
            }
    
    except Exception as e:
        logger.error(f"Unexpected Error: {e}")
        return 400, {
            "status": "error",
            "message": "Email already exists"
        }

def delete_author_handler(params):
    id = params.get("id")
    author_row, books_rows = queries.delete_author(id)

    if not author_row:
        return 404, {
            "error": f"author with id:{id} not found"
        }
    
    author_data = format_authors([author_row])


    deleted_book_data = [
        {
            "id": r[0],
            "title": r[1],
            "isbn": r[2],
            "published_year": r[3]
        } for r in books_rows
    ]

    data = [
        {"deleted_author":author_data},
        {"deleted_books_by_author": deleted_book_data}
         ]
    
    return 200, {
        "status": "success",
        "data": data
    }


def put_author_handler(data, params):
    id = params.get("id", None)
    name = data.get("name", None)
    email = data.get("email", None)

    
    if not name or len(name)<2:
        return 400, {
            "status":"error",
            "message": "name must be atleast 2 characters"
        }
    
    if not email or not is_valid_email(email):     
        return 400,{
            "status": "error",
            "message": "enter a valid Email"
        }
    
    try:
        row, message = queries.put_author(id, name, email)
        if row:
            updated_data = format_authors(row)
            return 200, {
                "status": "success",
                "data": updated_data,
                "message": message
            }

    except Exception as e:
        logger.info(f"Error: {e}")

    return 400, {
        "status": "error",
        "message": "coundn't update book"
    }
