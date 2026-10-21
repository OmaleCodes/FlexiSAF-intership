"""The database tables (the schema), written as Python classes."""

from datetime import date

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    # One author -> many books. Deleting an author also deletes their books.
    books: Mapped[list["Book"]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    copies_available: Mapped[int] = mapped_column(default=1)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))

    author: Mapped[Author] = relationship(back_populates="books")
    loans: Mapped[list["Loan"]] = relationship(back_populates="book")


class Member(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)

    loans: Mapped[list["Loan"]] = relationship(back_populates="member")


class Loan(Base):
    """A member borrowing a book. This links Member and Book (many-to-many)."""

    __tablename__ = "loans"

    id: Mapped[int] = mapped_column(primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    borrowed_on: Mapped[date] = mapped_column(default=date.today)
    returned_on: Mapped[date | None] = mapped_column(default=None)

    member: Mapped[Member] = relationship(back_populates="loans")
    book: Mapped[Book] = relationship(back_populates="loans")