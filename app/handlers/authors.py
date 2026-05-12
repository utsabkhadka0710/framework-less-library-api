import db.queries as queries
import re

def is_valid_email(email):
    return (re.match(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9.]+\.[a-zA-Z0-9]+$",email))



def format_authors(rows):
    return [
        {"id": r[0],"name": r[1], "email": r[2]} for r in rows
    ]


def authors_handler(query, params=None):

    if params:
        id = params.get("id")
        row = queries.get_authors(id=id)
        print(row)
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
    order = query.get("order",["desc"])[0]
    email = query.get("email",[None])[0]

    rows = queries.get_authors(name,email,sort,order)
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

        author = {
            "id": row[0],
            "name": row[1],
            "email": row[2]
        }

        return 201, {
            "status": "success",
            "data": author
            }
    
    except Exception as e:
        print("Unexpected Error:", e)
        return 400, {
            "status": "error",
            "message": "Email already exists"
        }
    