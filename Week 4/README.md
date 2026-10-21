# Week 4 - Relational Data, ORM & Transactions

A small library database built with SQLite and SQLAlchemy. It has related tables
(authors, books, members, loans), a data layer for creating, reading, updating and
deleting records, a transaction for borrowing books, tests, and a seed script.

## Project structure

```
week 4/
├── main.py                  # short demo of the data layer
├── seed.py                  # creates the tables and adds sample data
├── src/
│   ├── models.py             # the schema: Author, Book, Member, Loan
│   ├── db.py                 # engine, create_tables, session_scope (transactions)
│   ├── repository.py         # persistence only: add / get / update / delete
│   └── services.py           # business rules: borrow_book, return_book
├── tests/
│   ├── conftest.py           # fresh test database for every test
│   ├── test_repository.py    # CRUD and relationships
│   ├── test_services.py      # borrowing and returning rules
│   └── test_transactions.py  # rollback and commit behaviour, seed script
├── requirements.txt
└── README.md
```

## How to run

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python seed.py       # create library.db with sample data
python main.py       # run the demo (starts a fresh library.db each time)
pytest               # 21 tests
black --check .      # formatting
ruff check .         # linting
```

## How the code is separated

| Layer | File | Job |
|---|---|---|
| Models | `models.py` | What the tables look like |
| Repository | `repository.py` | Reads and writes the database. It has no rules in it |
| Services | `services.py` | Decides what is allowed (for example, you cannot borrow a book with no copies) and uses the repository |
| Transaction | `db.py` | `session_scope` wraps a piece of work |

Keeping the layers apart means a rule can change without touching the database
code, and the database could change without touching the rules.

## What the tests cover

- **Create, read, update, delete** for authors and books
- **Relationships** (author to books and back, active loans per member)
- **Rules** (borrow, return, out of stock, unknown ids, returning twice)
- **Transactions** (commit saves, any error rolls back, a failure halfway undoes the first step)
- **Constraints** (duplicate author name and member email are rejected)
- **Seed script** (adds data once, does nothing the second time)
