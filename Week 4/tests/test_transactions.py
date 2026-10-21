import pytest

from seed import seed
from src.db import session_scope
from src.models import Author, Book, Loan
from src.repository import LibraryRepository
from src.services import OutOfStockError, borrow_book
from tests.conftest import count_rows


def test_committed_data_is_visible_in_a_new_session(engine, ids):
    with session_scope(engine) as session:
        assert LibraryRepository(session).get_book(ids["book_a"]) is not None


def test_error_in_the_middle_undoes_everything(engine, ids):
    """Borrow Book A, then Book A again (no copies) - the first borrow is undone too."""
    with pytest.raises(OutOfStockError), session_scope(engine) as session:
        repo = LibraryRepository(session)
        borrow_book(repo, ids["member"], ids["book_a"])
        borrow_book(repo, ids["member"], ids["book_a"])

    assert count_rows(engine, Loan) == 0
    with session_scope(engine) as session:
        assert LibraryRepository(session).get_book(ids["book_a"]).copies_available == 1


def test_any_error_rolls_back_earlier_changes(engine):
    with pytest.raises(RuntimeError), session_scope(engine) as session:
        LibraryRepository(session).add_author("Will Not Be Saved")
        raise RuntimeError("something went wrong")
    assert count_rows(engine, Author) == 0


def test_successful_transaction_saves_all_steps(engine, ids):
    with session_scope(engine) as session:
        repo = LibraryRepository(session)
        borrow_book(repo, ids["member"], ids["book_a"])
        borrow_book(repo, ids["member"], ids["book_b"])
    assert count_rows(engine, Loan) == 2


def test_seed_adds_data_once(engine):
    assert seed(engine) is True
    assert (count_rows(engine, Author), count_rows(engine, Book)) == (3, 5)
    assert seed(engine) is False
    assert count_rows(engine, Book) == 5