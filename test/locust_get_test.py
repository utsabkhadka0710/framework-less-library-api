from locust import HttpUser, task, between
from random import randint

class MyApiUser(HttpUser):
    host = "http://localhost:8000"
    wait_time = between(0.1,3)

    @task
    def get_books(self):
        self.client.get("/books")

    @task
    def get_books_by_id(self):
        self.client.get(f"/books/{randint(1,500)}")

    def get_authors(self):
        self.client.get("/authors")

    @task
    def get_authors_by_id(self):
        self.client.get(f"/authors/{randint(1,5)}")
