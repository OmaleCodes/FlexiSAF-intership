"""Reads the CSV, checks every row, and writes the clean and invalid files."""

import csv
from collections.abc import Iterator
from dataclasses import asdict
from pathlib import Path

from src.decorators import timed
from src.models import VALID_RATINGS, VALID_TYPES, InvalidRecordError, Record

REQUIRED_FIELDS = ["show_id", "type", "title", "release_year", "rating"]
CLEAN_COLUMNS = [
    "show_id", "content_type", "title", "release_year", "rating",
    "duration", "director", "country", "date_added",
]  # fmt: skip


def read_rows(path: Path) -> Iterator[dict[str, str]]:
    """Generator: gives back one row at a time instead of loading the whole file."""
    with open(path, newline="", encoding="utf-8-sig") as file:
        yield from csv.DictReader(file)


def check_row(row: dict[str, str]) -> Record:
    """Check one row against the rules. Return a Record, or raise InvalidRecordError."""
    for name in REQUIRED_FIELDS:
        if not (row.get(name) or "").strip():
            raise InvalidRecordError(f"Missing required field: {name}")

    content_type = row["type"].strip()
    if content_type not in VALID_TYPES:
        raise InvalidRecordError(f"Invalid type: {content_type!r}")

    try:
        release_year = int(row["release_year"])
    except ValueError:
        raise InvalidRecordError(f"Invalid release_year: {row['release_year']!r}")

    rating = row["rating"].strip()
    if rating not in VALID_RATINGS:
        raise InvalidRecordError(f"Invalid rating: {rating!r}")

    # Duration is checked last, after the rating, on purpose: in 3 rows the
    # duration was typed into the rating column, and "Invalid rating" explains
    # that problem better than "Missing duration".
    duration = (row.get("duration") or "").strip()
    if not duration:
        raise InvalidRecordError("Missing required field: duration")
    if content_type == "Movie" and not duration.endswith(" min"):
        raise InvalidRecordError(f"Invalid duration for a Movie: {duration!r}")
    if content_type == "TV Show" and "Season" not in duration:
        raise InvalidRecordError(f"Invalid duration for a TV Show: {duration!r}")

    return Record(
        show_id=row["show_id"].strip(),
        content_type=content_type,
        title=row["title"].strip(),
        release_year=release_year,
        rating=rating,
        duration=duration,
        director=(row.get("director") or "").strip() or None,
        country=(row.get("country") or "").strip() or None,
        date_added=(row.get("date_added") or "").strip() or None,
    )


@timed
def process_file(input_path: Path, output_dir: Path) -> dict[str, object]:
    """Run the whole job and return the numbers for the report."""
    clean_records: list[Record] = []
    invalid_rows: list[dict[str, str]] = []
    reasons: dict[str, int] = {}
    seen_ids: set[str] = set()  # a set makes the duplicate check fast

    for number, row in enumerate(read_rows(input_path), start=1):
        try:
            record = check_row(row)
            if record.show_id in seen_ids:
                raise InvalidRecordError(f"Duplicate show_id: {record.show_id!r}")
        except InvalidRecordError as error:
            reason = str(error)
            invalid_rows.append({"row_number": str(number), "reason": reason, **row})
            category = reason.split(":")[0]
            reasons[category] = reasons.get(category, 0) + 1
        else:
            seen_ids.add(record.show_id)
            clean_records.append(record)

    output_dir.mkdir(parents=True, exist_ok=True)
    write_clean(clean_records, output_dir / "clean_titles.csv")
    write_invalid(invalid_rows, output_dir / "invalid_titles.csv")

    return {
        "total": len(clean_records) + len(invalid_rows),
        "clean": len(clean_records),
        "invalid": len(invalid_rows),
        "reasons": reasons,
    }


def write_clean(records: list[Record], path: Path) -> None:
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=CLEAN_COLUMNS)
        writer.writeheader()
        for record in records:
            writer.writerow(asdict(record))


def write_invalid(rows: list[dict[str, str]], path: Path) -> None:
    columns = ["row_number", "reason"]
    for row in rows:
        for name in row:
            if name not in columns:
                columns.append(name)
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def format_report(summary: dict[str, object], input_path: Path) -> str:
    lines = [
        "Netflix Titles Toolkit - Report",
        f"Input file   : {input_path.name}",
        f"Rows read    : {summary['total']}",
        f"Clean rows   : {summary['clean']}",
        f"Invalid rows : {summary['invalid']}",
    ]
    reasons = summary["reasons"]
    if isinstance(reasons, dict) and reasons:
        lines.append("Why rows were rejected:")
        for reason, count in reasons.items():
            lines.append(f"  {reason}: {count}")
    return "\n".join(lines)