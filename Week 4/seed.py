"""Fills the database with sample data.
Run it with:  python seed.py
"""

from sqlalchemy import Engine, func, select

from src.db import create_tables, get_engine, session_scope
from src.models import Author
from src.repository import LibraryRepository

SAMPLE_BOOKS = {
    "Chinua Achebe": [("Things Fall Apart", 3), ("Arrow of God", 1)],
    "Chimamanda Ngozi Adichie": [("Half of a Yellow Sun", 2), ("Purple Hibiscus", 2)],
    "Wole Soyinka": [("The Lion and the Jewel", 1)],
}
SAMPLE_MEMBERS = [
    ("Amaka Obi", "amaka@example.com"),
    ("Tunde Bello", "tunde@example.com"),
]


def seed(engine: Engine) -> bool:
    """Create the tables and add sample data. Returns False if already seeded."""
    create_tables(engine)
    with session_scope(engine) as session:
        if session.scalar(select(func.count()).select_from(Author)):
            return False
        repo = LibraryRepository(session)
        for author_name, books in SAMPLE_BOOKS.items():
            author = repo.add_author(author_name)
            for title, copies in books:
                repo.add_book(title, author.id, copies)
        for name, email in SAMPLE_MEMBERS:
            repo.add_member(name, email)
    return True


if __name__ == "__main__":
    if seed(get_engine()):
        print("Database seeded: 3 authors, 5 books, 2 members.")
    else:
        print("Database already has data - nothing added.")