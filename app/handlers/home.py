def home_handler(query=None,params=None):
    return 200, {
        "status": "success",
        "mesage": "A RESTful CRUD API for managing a library system — built entirely in **pure Python**, with no external backend frameworks like Django or FastAPI. Uses Python's built-in `http.server` module and connects to a **PostgreSQL** database hosted on NeonDB.",
        "live API on 🚀": "🚀 https://framework-less-library-api-utsab.onrender.com"
        }