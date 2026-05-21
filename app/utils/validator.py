import re
from datetime import datetime

def is_valid_email(email):
    return (re.match(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9.]+\.[a-zA-Z0-9]+$",email))

def is_valid_isbn(isbn):
    return re.match(r"^\d{10}$",isbn)

def is_valid_year(year):
    current_year = datetime.now().year
    try:
        return 1000 <= int(year) <= current_year
    except Exception:
        return False

