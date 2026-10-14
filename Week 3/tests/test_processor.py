import csv
import sys
from pathlib import Path

import pytest

from main import main
from src.models import InvalidRecordError
from src.processor import check_row, process_file, read_rows

COLUMNS = [
    "show_id", "type", "title", "director", "cast", "country", "date_added",
    "release_year", "rating", "duration", "listed_in", "description",
]  # fmt: skip


def make_row(**changes: str) -> dict[str, str]:
    """A valid movie row. Each test changes only the field it cares about."""
    row = {
        "show_id": "s1", "type": "Movie", "title": "Test Movie",
        "director": "Jane Doe", "cast": "A, B", "country": "Nigeria",
        "date_added": "May 1, 2020", "release_year": "2019", "rating": "PG",
        "duration": "90 min", "listed_in": "Dramas", "description": "A test.",
    }  # fmt: skip
    row.update(changes)
    return row


def write_csv(path: Path, rows: list[dict[str, str]], columns=COLUMNS) -> Path:
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    return path


def read_csv(path: Path) -> list[dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


# ---- check_row: one row at a time ----


def test_valid_movie_row():
    record = check_row(make_row())
    assert record.title == "Test Movie"
    assert record.release_year == 2019
    assert record.director == "Jane Doe"


def test_valid_tv_show_row():
    record = check_row(make_row(type="TV Show", duration="2 Seasons"))
    assert record.content_type == "TV Show"


def test_optional_fields_can_be_empty():
    record = check_row(make_row(director="", country="", date_added=""))
    assert record.director is None
    assert record.country is None
    assert record.date_added is None


@pytest.mark.parametrize(
    "field", ["show_id", "type", "title", "release_year", "rating"]
)
def test_missing_required_field(field: str):
    with pytest.raises(InvalidRecordError, match=f"Missing required field: {field}"):
        check_row(make_row(**{field: " "}))


def test_missing_duration():
    with pytest.raises(InvalidRecordError, match="Missing required field: duration"):
        check_row(make_row(duration=""))


def test_invalid_type():
    with pytest.raises(InvalidRecordError, match="Invalid type"):
        check_row(make_row(type="Series"))


def test_invalid_year():
    with pytest.raises(InvalidRecordError, match="Invalid release_year"):
        check_row(make_row(release_year="abc"))


def test_duration_typed_in_rating_column():
    with pytest.raises(InvalidRecordError, match="Invalid rating: '74 min'"):
        check_row(make_row(rating="74 min", duration=""))


@pytest.mark.parametrize(
    ("content_type", "duration"),
    [("Movie", "2 Seasons"), ("TV Show", "90 min")],
)
def test_duration_must_match_type(content_type: str, duration: str):
    with pytest.raises(InvalidRecordError, match="Invalid duration"):
        check_row(make_row(type=content_type, duration=duration))


# ---- the whole job ----


def test_read_rows_is_a_generator(tmp_path: Path):
    rows = read_rows(write_csv(tmp_path / "in.csv", [make_row()]))
    assert hasattr(rows, "__next__")
    assert next(rows)["show_id"] == "s1"


def test_clean_and_invalid_files_are_written(tmp_path: Path):
    source = write_csv(
        tmp_path / "in.csv",
        [make_row(), make_row(show_id="s2", rating="74 min", duration="")],
    )
    summary = process_file(source, tmp_path / "out")
    assert (summary["total"], summary["clean"], summary["invalid"]) == (2, 1, 1)
    assert [r["show_id"] for r in read_csv(tmp_path / "out" / "clean_titles.csv")] == [
        "s1"
    ]
    invalid = read_csv(tmp_path / "out" / "invalid_titles.csv")
    assert invalid[0]["show_id"] == "s2"
    assert "Invalid rating" in invalid[0]["reason"]


def test_duplicate_show_id_is_rejected(tmp_path: Path):
    source = write_csv(tmp_path / "in.csv", [make_row(), make_row()])
    summary = process_file(source, tmp_path / "out")
    assert (summary["clean"], summary["invalid"]) == (1, 1)
    assert summary["reasons"] == {"Duplicate show_id": 1}


def test_empty_file_gives_zero_rows(tmp_path: Path):
    empty = tmp_path / "empty.csv"
    empty.write_text("", encoding="utf-8")
    summary = process_file(empty, tmp_path / "out")
    assert summary["total"] == 0


def test_missing_column_makes_every_row_invalid(tmp_path: Path):
    columns = [name for name in COLUMNS if name != "title"]
    source = write_csv(
        tmp_path / "in.csv", [make_row(), make_row(show_id="s2")], columns
    )
    summary = process_file(source, tmp_path / "out")
    assert summary["invalid"] == 2
    assert summary["reasons"] == {"Missing required field": 2}


# ---- command line ----


def test_command_line_run(tmp_path: Path, monkeypatch, capsys):
    source = write_csv(tmp_path / "in.csv", [make_row()])
    monkeypatch.setattr(
        sys, "argv", ["main.py", str(source), "--output-dir", str(tmp_path / "out")]
    )
    main()
    assert "Clean rows   : 1" in capsys.readouterr().out
    assert (tmp_path / "out" / "report.txt").exists()


def test_command_line_missing_file(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["main.py", str(tmp_path / "nope.csv")])
    main()
    assert "file not found" in capsys.readouterr().out