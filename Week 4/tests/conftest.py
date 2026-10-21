import pytest
from sqlalchemy import Engine, func, select

from src.db import create_tables, get_engine, session_scope
from src.repository import LibraryRepository


@pytest.fixture
def engine(tmp_path):
    """A fresh, empty test database for every test."""
    engine = get_engine(f"sqlite:///{tmp_path / 'test.db'}")
    create_tables(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def ids(engine: Engine) -> dict[str, int]:
    """One author, two books (1 copy each) and one member. Returns their ids."""
    with session_scope(engine) as session:
        repo = LibraryRepository(session)
        author = repo.add_author("Test Author")
        book_a = repo.add_book("Book A", author.id, copies=1)
        book_b = repo.add_book("Book B", author.id, copies=1)
        member = repo.add_member("Test Member", "test@example.com")
        return {
            "author": author.id,
            "book_a": book_a.id,
            "book_b": book_b.id,
            "member": member.id,
        }


def count_rows(engine: Engine, model: type) -> int:
    with session_scope(engine) as session:
        return session.scalar(select(func.count()).select_from(model)) or 0