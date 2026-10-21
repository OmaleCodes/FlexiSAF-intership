import pytest
from sqlalchemy.exc import IntegrityError

from src.db import session_scope
from src.models import Book
from src.repository import LibraryRepository
from tests.conftest import count_rows


def test_add_and_get_author(engine):
    with session_scope(engine) as session:
        repo = LibraryRepository(session)
        author = repo.add_author("Chinua Achebe")
        assert repo.get_author(author.id).name == "Chinua Achebe"


def test_get_missing_author_returns_none(engine):
    with session_scope(engine) as session:
        assert LibraryRepository(session).get_author(999) is None


def test_author_and_book_are_linked(engine, ids):
    with session_scope(engine) as session:
        repo = LibraryRepository(session)
        author = repo.get_author(ids["author"])
        assert [book.title for book in author.books] == ["Book A", "Book B"]
        assert repo.get_book(ids["book_a"]).author.name == "Test Author"


def test_list_books_by_author_is_sorted(engine, ids):
    with session_scope(engine) as session:
        repo = LibraryRepository(session)
        repo.add_book("Aardvark", ids["author"])
        titles = [book.title for book in repo.list_books_by_author(ids["author"])]
        assert titles == ["Aardvark", "Book A", "Book B"]


def test_update_book_title(engine, ids):
    with session_scope(engine) as session:
        LibraryRepository(session).update_book_title(ids["book_a"], "New Title")
    with session_scope(engine) as session:
        assert LibraryRepository(session).get_book(ids["book_a"]).title == "New Title"


def test_delete_book(engine, ids):
    with session_scope(engine) as session:
        repo = LibraryRepository(session)
        assert repo.delete_book(ids["book_a"]) is True
        assert repo.delete_book(ids["book_a"]) is False
    assert count_rows(engine, Book) == 1


def test_deleting_author_deletes_their_books(engine, ids):
    with session_scope(engine) as session:
        LibraryRepository(session).delete_author(ids["author"])
    assert count_rows(engine, Book) == 0


def test_duplicate_author_name_is_rejected(engine, ids):
    with pytest.raises(IntegrityError), session_scope(engine) as session:
        LibraryRepository(session).add_author("Test Author")


def test_duplicate_member_email_is_rejected(engine, ids):
    with pytest.raises(IntegrityError), session_scope(engine) as session:
        LibraryRepository(session).add_member("Someone Else", "test@example.com")