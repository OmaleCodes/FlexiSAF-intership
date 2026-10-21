"""A short demo of the data layer. Run it with:  python main.py
It starts a fresh library.db every time, so it always gives the same result.
"""

from pathlib import Path

from sqlalchemy import select

from seed import seed
from src.db import get_engine, session_scope
from src.models import Author
from src.repository import LibraryRepository
from src.services import OutOfStockError, borrow_book, return_book


def show_catalogue(repo: LibraryRepository) -> None:
    for author in repo.session.scalars(select(Author).order_by(Author.name)):
        print(f"  {author.name}")
        for book in author.books:
            print(f"    - {book.title}: {book.copies_available} available")


def main() -> None:
    Path("library.db").unlink(missing_ok=True)
    engine = get_engine()
    seed(engine)

    with session_scope(engine) as session:
        repo = LibraryRepository(session)
        print("Catalogue:")
        show_catalogue(repo)

        book = repo.find_book("Arrow of God")
        assert book is not None
        loan = borrow_book(repo, member_id=1, book_id=book.id)
        print(f"\nAmaka borrowed {book.title!r}. Copies left: {book.copies_available}")

        try:
            borrow_book(repo, member_id=2, book_id=book.id)
        except OutOfStockError as error:
            print(f"Tunde could not borrow it: {error}")

        member = repo.get_member(1)
        assert member is not None
        titles = [active.book.title for active in repo.list_active_loans(1)]
        print(f"{member.name}'s active loans: {titles}")

        return_book(repo, loan.id)
        print(f"Amaka returned it. Copies left: {book.copies_available}")


if __name__ == "__main__":
    main()