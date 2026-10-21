"""Database connection and the transaction helper."""

from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from src.models import Base

DEFAULT_URL = "sqlite:///library.db"


def get_engine(url: str = DEFAULT_URL) -> Engine:
    return create_engine(url)


def create_tables(engine: Engine) -> None:
    Base.metadata.create_all(engine)


@contextmanager
def session_scope(engine: Engine) -> Iterator[Session]:
    """One transaction: save everything if the block works, undo everything if not."""
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()