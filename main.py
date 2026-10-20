from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="FastAPI Library API",
    description="A simple in-memory library API built with FastAPI.",
    version="1.0.0",
)


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=120)
    published_year: Optional[int] = Field(default=None, ge=0, le=2100)


class BookUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    author: Optional[str] = Field(default=None, min_length=1, max_length=120)
    published_year: Optional[int] = Field(default=None, ge=0, le=2100)


class Book(BookCreate):
    id: int



books: dict[int, dict] = {
    1: {"id": 1, "title": "The Little Prince", "author": "Antoine de Saint-Exupéry", "published_year": 1943},
    2: {"id": 2, "title": "1984", "author": "George Orwell", "published_year": 1949},
}
next_book_id = 3


@app.get("/books", response_model=list[Book], summary="List all books")
def list_books():
    return list(books.values())


@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED, summary="Add a book")
def create_book(book: BookCreate):
    global next_book_id
    new_book = {"id": next_book_id, **book.model_dump()}
    books[next_book_id] = new_book
    next_book_id += 1
    return new_book


@app.get("/books/{book_id}", response_model=Book, summary="Get a book")
def get_book(book_id: int):
    book = books.get(book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@app.patch("/books/{book_id}", response_model=Book, summary="Update a book")
def update_book(book_id: int, changes: BookUpdate):
    book = books.get(book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    updates = changes.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide at least one field to update",
        )

    book.update(updates)
    return book


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a book")
def delete_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    del books[book_id]
    return None
