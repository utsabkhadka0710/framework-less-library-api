# 📚 Framework-less Library API

A RESTful CRUD API for managing a library system — built entirely in **pure Python**, with no external backend frameworks like Django or FastAPI. Uses Python's built-in `http.server` module and connects to a **PostgreSQL** database hosted on NeonDB.

🚀 **Live API:** https://framework-less-library-api-utsab.onrender.com

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)
- [Running Tests](#running-tests)
- [Deployment](#deployment)
- [Known Limitations](#known-limitations)
- [Roadmap](#roadmap)

---

## Overview

This project demonstrates how to build a production REST API from scratch in Python without relying on any third-party backend frameworks. It implements a library management system with full CRUD operations on books and authors.

The goal is to understand how HTTP servers, request routing, and database connections work under the hood — the same things frameworks like Django and FastAPI abstract away.

---

## Features

- ✅ Full **CRUD** support — GET, POST, PUT, DELETE
- ✅ **PostgreSQL** integration via `psycopg`
- ✅ **Zero backend framework dependencies** — only Python's standard library for the HTTP server layer
- ✅ **Database migrations** for schema management
- ✅ **Seed scripts** for populating data (500+ real books included)
- ✅ **Test suite** included
- ✅ **Deployed on Render** with **NeonDB** as the managed PostgreSQL host

---

## Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Language   | Python 3.x                        |
| HTTP Server| `http.server` (Python stdlib)     |
| Database   | PostgreSQL (NeonDB)               |
| DB Driver  | `psycopg` (psycopg3)              |
| Hosting    | Render                            |
| Config     | `python-dotenv`                   |

---

## Project Structure

```
framework-less-library-api/
├── app/                       # Core application code
│   ├── server.py              # HTTP server entry point
│   ├── router.py              # Request routing logic
│   ├── handlers/              # Route handlers (GET, POST, PUT, DELETE)
│   ├── utils/                 # Reusable and repeated logic
│   └── db/                    # Database connection and query helpers
├── migrations/                # SQL migration files
├── seeds/                     # Seed data scripts
├── test/                      # Test cases
├── .env.example               # Environment variable template
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Database Schema

```sql
CREATE TABLE authors (
    id           SERIAL PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    email        VARCHAR(100) UNIQUE NOT NULL,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE books (
    id             SERIAL PRIMARY KEY,
    title          VARCHAR(200) NOT NULL,
    isbn           VARCHAR(10) UNIQUE NOT NULL,
    published_year INT,
    author_id      INT REFERENCES authors(id) ON DELETE CASCADE,
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Getting Started

**1. Clone the repository**

```bash
git clone https://github.com/utsabkhadka0710/framework-less-library-api.git
cd framework-less-library-api
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Set up environment variables**

```bash
cp .env.example .env
```

Edit `.env` with your PostgreSQL credentials.

**4. Run migrations**

```bash
python migrations/migrate.py
```

**5. (Optional) Seed the database**

```bash
python seeds/seed.py
```

**6. Start the server**

```bash
python -m app.server
```

The server will start at `http://localhost:8000`.

---

## Environment Variables

| Variable   | Description                   | Example                              |
|------------|-------------------------------|--------------------------------------|
| `DB_NAME`  | PostgreSQL database name      | `library`                            |
| `USER`     | Database username             | `postgres`                           |
| `PASSWORD` | Database user password        | `yourpassword`                       |
| `HOST`     | Database host                 | `ep-xxx.us-east-2.aws.neon.tech`    |
| `PORT`     | Database port                 | `5432`                               |

---

## Running the Server

```bash
python -m app.server
```

The server binds to `0.0.0.0` and reads the port from the `PORT` environment variable (defaults to `8000` locally). This is required for Render deployment.

---

## API Endpoints

Base URL (local): `http://localhost:8000`  
Base URL (production): `https://framework-less-library-api-utsab.onrender.com`

### Authors

| Method   | Endpoint           | Description            |
|----------|--------------------|------------------------|
| `GET`    | `/authors`         | Fetch all authors      |
| `GET`    | `/authors/{id}`    | Fetch a single author  |
| `POST`   | `/authors`         | Add a new author       |
| `PUT`    | `/authors/{id}`    | Update an author       |
| `DELETE` | `/authors/{id}`    | Delete an author       |

### Books

| Method   | Endpoint        | Description             |
|----------|-----------------|-------------------------|
| `GET`    | `/books`        | Fetch all books         |
| `GET`    | `/books/{id}`   | Fetch a single book     |
| `POST`   | `/books`        | Add a new book          |
| `PUT`    | `/books/{id}`   | Update an existing book |
| `DELETE` | `/books/{id}`   | Delete a book           |

### Example Requests

**Get all books**
```bash
curl https://framework-less-library-api-utsab.onrender.com/books
```

**Add a new author**
```bash
curl -X POST https://framework-less-library-api-utsab.onrender.com/authors \
  -H "Content-Type: application/json" \
  -d '{"name": "George Orwell", "email": "george.orwell@example.com"}'
```

**Add a new book**
```bash
curl -X POST https://framework-less-library-api-utsab.onrender.com/books \
  -H "Content-Type: application/json" \
  -d '{"title": "1984", "isbn": "0451524934", "published_year": 1949, "author_id": 1}'
```

**Update a book**
```bash
curl -X PUT https://framework-less-library-api-utsab.onrender.com/books/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Nineteen Eighty-Four"}'
```

**Delete a book**
```bash
curl -X DELETE https://framework-less-library-api-utsab.onrender.com/books/1
```

---

## Running Tests

```bash
locust -f test/locust_get_test.py
```

---

## Deployment

This API is deployed on **Render** with **NeonDB** as the managed PostgreSQL database.

### Render Setup

| Field            | Value                             |
|------------------|-----------------------------------|
| Runtime          | Python 3                          |
| Build Command    | `pip install -r requirements.txt` |
| Start Command    | `python -m app.server`            |
| Instance Type    | Free                              |

### NeonDB

NeonDB provides a free serverless PostgreSQL database. The connection requires `sslmode=require`.

> **Note:** Render's free tier spins down after 15 minutes of inactivity. The first request after idle may take ~30 seconds to respond.

---

## Known Limitations

- The server becomes unstable under **35–40 concurrent requests**. Thread pooling or async I/O improvements are planned.
- No authentication or authorization layer yet.
- Input validation and error responses are minimal at this stage.

---

## Roadmap

- [ ] Fix concurrency/scaling (thread pool or async server)
- [ ] Add proper input validation and error responses
- [ ] Improve code structure and readability
- [ ] Add authentication (API keys or JWT)
- [ ] Write comprehensive API docs (OpenAPI/Swagger)
- [ ] Add more endpoints (members, loans/checkouts)
- [ ] Containerize with Docker

---

## Contributing

This is a personal learning project, but contributions and suggestions are welcome. Feel free to open an issue or submit a pull request.

---

## License

This project is open source. No license has been specified yet.