# Week 3 - Project 1: Typed Data Processing Toolkit

A command-line tool that reads the Netflix titles dataset (`netflix_titles.csv`,
8,807 rows), checks every row against simple rules, and saves two files:
the **clean** rows, and the **invalid** rows with the reason each one was rejected.

Result on the dataset: **8,800 clean rows and 7 invalid rows**
(3 rows where the duration was typed into the rating column, 4 rows with no rating).

## Project structure

```
week 3/
├── main.py                 # Command-line interface (argparse)
├── src/
│   ├── models.py            # Record dataclass, InvalidRecordError, allowed values
│   ├── processor.py         # read_rows (generator), check_row, process_file, writers
│   └── decorators.py        # @timed decorator, reused from Week 2
├── tests/
│   └── test_processor.py
├── data/
│   └── netflix_titles.csv   # input dataset
├── output/
│   ├── clean_titles.csv     # rows that passed
│   ├── invalid_titles.csv   # rows that failed, with the reason
│   └── report.txt           # summary of the run
├── requirements.txt
└── README.md
```

## How to run

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python main.py data/netflix_titles.csv                  # results go to output/
python main.py data/netflix_titles.csv --output-dir results
python main.py --help
```

Example output:

```
process_file took 0.13 seconds
Netflix Titles Toolkit - Report
Input file   : netflix_titles.csv
Rows read    : 8807
Clean rows   : 8800
Invalid rows : 7
Why rows were rejected:
  Invalid rating: 3
  Missing required field: 4
```

If the file does not exist, the tool prints `Error: file not found` instead of crashing.

## Run the tests and checks

```bash
pytest              # 21 tests
black --check .     # formatting
ruff check .        # linting
```

## Validation rules

| Field | Rule |
|---|---|
| `show_id` | Required, and must not repeat |
| `title` | Required |
| `release_year` | Required, must be a whole number |
| `type` | Required, must be "Movie" or "TV Show" |
| `rating` | Required, must be a known rating such as TV-MA, PG-13 or R |
| `duration` | Required. Movies end in `min` (e.g. `90 min`); TV shows contain `Season` (e.g. `2 Seasons`) |
| `director`, `country`, `date_added` | Optional. Many rows leave them empty, so rejecting those rows would throw away good data |

Rows with a problem are saved in `invalid_titles.csv` with a `reason` column.

## How it works

1. `read_rows` is a **generator**: it gives the CSV back one row at a time.
2. `check_row` checks one row. It returns a `Record` (a dataclass), or raises
   `InvalidRecordError` with a message saying which rule failed.
3. `process_file` loops over the rows, sends good ones to a clean list and bad ones
   to an invalid list, then writes both files. A `set` of seen IDs catches duplicates.
4. `main.py` reads the command-line options and prints the report.

The rating is checked before the duration on purpose. Three rows
(s5542, s5795, s5814) have the duration in the rating column, so they are
reported as `Invalid rating: '74 min'`, which explains the problem best.

## What I used from Weeks 1 and 2

| Skill | Where |
|---|---|
| Type hints | Every function in `src/` and `main.py` |
| Dataclass | `Record` in `models.py` |
| Meaningful errors | `InvalidRecordError` with a clear message |
| Project structure, tests, linting | `src/`, `tests/`, pytest, black, ruff |
| Generators | `read_rows` |
| Decorator | `@timed` on `process_file` (same file as Week 2) |
| Context manager | `with open(...)` closes the files safely |
