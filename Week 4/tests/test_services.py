from datetime import date

import pytest

from src.db import session_scope
from src.models import Loan
from src.repository import LibraryRepository
from src.services import (
    AlreadyReturnedError,
    NotFoundError,
    OutOfStockError,
    borrow_book,
    return_book,
)
from tests.conftest import count_rows


def test_borrow_book_takes_a_copy_and_creates_a_loan(engine, ids):
    with session_scope(engine) as session:
        repo = LibraryRepository(session)
        loan = borrow_book(repo, ids["member"], ids["book_a"])
        assert loan.returned_on is None
        assert repo.get_book(ids["book_a"]).copies_available == 0
    assert count_rows(engine, Loan) == 1


def test_borrow_when_no_copies_left_is_refused(engine, ids):
    with session_scope(engine) as session:
        borrow_book(LibraryRepository(session), ids["member"], ids["book_a"])
    with pytest.raises(OutOfStockError), session_scope(engine) as session:
        borrow_book(LibraryRepository(session), ids["member"], ids["book_a"])
    assert count_rows(engine, Loan) == 1


def test_borrow_unknown_member_or_book(engine, ids):
    with session_scope(engine) as session:
        repo = LibraryRepository(session)
        with pytest.raises(NotFoundError, match="Member"):
            borrow_book(repo, 999, ids["book_a"])
        with pytest.raises(NotFoundError, match="Book"):
            borrow_book(repo, ids["member"], 999)


def test_return_book_puts_the_copy_back(engine, ids):
    with session_scope(engine) as session:
        repo = LibraryRepository(session)
        loan = borrow_book(repo, ids["member"], ids["book_a"])
        returned = return_book(repo, loan.id)
        assert returned.returned_on == date.today()
        assert repo.get_book(ids["book_a"]).copies_available == 1


def test_return_twice_is_refused(engine, ids):
    with session_scope(engine) as session:
        repo = LibraryRepository(session)
        loan = borrow_book(repo, ids["member"], ids["book_a"])
        return_book(repo, loan.id)
        with pytest.raises(AlreadyReturnedError):
            return_book(repo, loan.id)


def test_return_unknown_loan(engine):
    with session_scope(engine) as session, pytest.raises(NotFoundError):
        return_book(LibraryRepository(session), 999)


def test_active_loans_only_lists_unreturned_books(engine, ids):
    with session_scope(engine) as session:
        repo = LibraryRepository(session)
        first = borrow_book(repo, ids["member"], ids["book_a"])
        borrow_book(repo, ids["member"], ids["book_b"])
        return_book(repo, first.id)
        active = repo.list_active_loans(ids["member"])
        assert [loan.book.title for loan in active] == ["Book B"]