
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from database import Base, engine, get_db
from schemas import BookCreate, BookResponse, BookUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library API")

DbSession = Annotated[Session, Depends(get_db)]


@app.get("/books", response_model=list[BookResponse])
def get_books(db: DbSession):
    return db.scalars(select(models.Book)).all()


@app.post(
    "/books",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_book(book: BookCreate, db: DbSession):
    new_book = models.Book(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: DbSession):
    book = db.get(models.Book, book_id)

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    return book


@app.patch("/books/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    updates: BookUpdate,
    db: DbSession,
):
    book = db.get(models.Book, book_id)

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    update_data = updates.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)
    return book


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: DbSession):
    book = db.get(models.Book, book_id)

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    db.delete(book)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
