# FastAPI Library API

A RESTful API for managing a library's book collection, built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.

## Features

- Retrieve all books
- Add a new book
- Retrieve a book by ID
- Update book details
- Delete a book
- Persist data in PostgreSQL
- Validate request and response data with Pydantic
- Automatically generate interactive API documentation

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Psycopg
- Pydantic
- Uvicorn

## Project Structure

```text
fastapi-library-api/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Requirements

- Python 3.10+
- PostgreSQL

## Installation

Clone the repository:

```bash
git clone https://github.com/AliAlishir/fastapi-library-api.git
cd fastapi-library-api
```

Create and activate a virtual environment.

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Database Configuration

Create a PostgreSQL database named `library_db`.

Create a `.env` file in the project root and configure the database connection:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/library_db
```

Replace `YOUR_PASSWORD` with the password for your PostgreSQL user.

The application uses SQLAlchemy to connect to PostgreSQL and create the database table if it does not already exist.

### Books Table

The `books` table contains the following fields:

| Column | Type | Description |
|---|---|---|
| `id` | Integer | Primary key, auto-incrementing |
| `title` | VARCHAR(255) | Book title |
| `author` | VARCHAR(255) | Author name |
| `published_year` | Integer | Publication year; nullable |

## Running the Application

Start the development server:

```bash
python -m uvicorn main:app --reload
```

The API will be available at:

http://127.0.0.1:8000

## API Documentation

FastAPI provides interactive API documentation at:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/books` | Retrieve all books |
| POST | `/books` | Create a new book |
| GET | `/books/{book_id}` | Retrieve a book by ID |
| PATCH | `/books/{book_id}` | Update an existing book |
| DELETE | `/books/{book_id}` | Delete a book by ID |

### Example: Create a Book

**Request**

```http
POST /books
Content-Type: application/json
```

```json
{
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "published_year": 1925
}
```

**Response**

```json
{
  "id": 1,
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "published_year": 1925
}
```

## Error Handling

The API returns an HTTP `404 Not Found` response when a requested book does not exist.

## Security

Database credentials are stored in environment variables rather than hardcoded in the application. The `.env` file should not be committed to version control.

## License

No license has been specified for this project.
