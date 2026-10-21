"""reading and writing the database"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models import Author, Book, Loan, Member


class LibraryRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    #Authors
    def add_author(self, name: str) -> Author:
        author = Author(name=name)
        self.session.add(author)
        self.session.flush()  # sends the INSERT so the new id is available
        return author

    def get_author(self, author_id: int) -> Author | None:
        return self.session.get(Author, author_id)

    def delete_author(self, author_id: int) -> bool:
        author = self.get_author(author_id)
        if author is None:
            return False
        self.session.delete(author)
        self.session.flush()
        return True

    #Books
    def add_book(self, title: str, author_id: int, copies: int = 1) -> Book:
        book = Book(title=title, author_id=author_id, copies_available=copies)
        self.session.add(book)
        self.session.flush()
        return book

    def get_book(self, book_id: int) -> Book | None:
        return self.session.get(Book, book_id)

    def find_book(self, title: str) -> Book | None:
        return self.session.scalars(select(Book).where(Book.title == title)).first()

    def list_books_by_author(self, author_id: int) -> list[Book]:
        query = select(Book).where(Book.author_id == author_id).order_by(Book.title)
        return list(self.session.scalars(query))

    def update_book_title(self, book_id: int, new_title: str) -> Book | None:
        book = self.get_book(book_id)
        if book is not None:
            book.title = new_title
        return book

    def delete_book(self, book_id: int) -> bool:
        book = self.get_book(book_id)
        if book is None:
            return False
        self.session.delete(book)
        self.session.flush()
        return True

    #Members
    def add_member(self, name: str, email: str) -> Member:
        member = Member(name=name, email=email)
        self.session.add(member)
        self.session.flush()
        return member

    def get_member(self, member_id: int) -> Member | None:
        return self.session.get(Member, member_id)

    #Loans
    def add_loan(self, member_id: int, book_id: int) -> Loan:
        loan = Loan(member_id=member_id, book_id=book_id)
        self.session.add(loan)
        self.session.flush()
        return loan

    def get_loan(self, loan_id: int) -> Loan | None:
        return self.session.get(Loan, loan_id)

    def list_active_loans(self, member_id: int) -> list[Loan]:
        query = select(Loan).where(
            Loan.member_id == member_id, Loan.returned_on.is_(None)
        )
        return list(self.session.scalars(query))