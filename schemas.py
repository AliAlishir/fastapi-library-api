
from pydantic import BaseModel, ConfigDict


class BookCreate(BaseModel):
    title: str
    author: str
    published_year: int | None = None


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    published_year: int | None = None


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    published_year: int | None

    model_config = ConfigDict(from_attributes=True)
