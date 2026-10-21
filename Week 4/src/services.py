"""use the repository to read and write data."""

from datetime import date

from src.models import Loan
from src.repository import LibraryRepository


class NotFoundError(Exception):
    """The member, book or loan does not exist."""


class OutOfStockError(Exception):
    """No copies of the book are left to borrow."""


class AlreadyReturnedError(Exception):
    """The loan was already returned."""


def borrow_book(repo: LibraryRepository, member_id: int, book_id: int) -> Loan:
    """Borrow a book: one copy less on the shelf, and a new loan record."""
    if repo.get_member(member_id) is None:
        raise NotFoundError(f"Member {member_id} not found")
    book = repo.get_book(book_id)
    if book is None:
        raise NotFoundError(f"Book {book_id} not found")
    if book.copies_available < 1:
        raise OutOfStockError(f"No copies left of {book.title!r}")

    book.copies_available -= 1
    return repo.add_loan(member_id, book_id)


def return_book(repo: LibraryRepository, loan_id: int) -> Loan:
    """Return a book: mark the loan as returned and put the copy back."""
    loan = repo.get_loan(loan_id)
    if loan is None:
        raise NotFoundError(f"Loan {loan_id} not found")
    if loan.returned_on is not None:
        raise AlreadyReturnedError(f"Loan {loan_id} was already returned")

    loan.returned_on = date.today()
    loan.book.copies_available += 1
    return loan