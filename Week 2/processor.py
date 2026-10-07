"""A generator-based processor for sensor-style 'timestamp,value' readings.

Everything here is lazy: nothing is loaded or computed until it's actually
asked for, which matters if the input were a huge file instead of a small
list of strings.
"""

from collections.abc import Iterable, Iterator


class InvalidRecord(Exception):
    """Raised when a line can't be parsed as a valid reading."""


def parse_line(line: str) -> tuple[str, float]:
    parts = line.split(",")
    if len(parts) != 2:
        raise InvalidRecord(f"Malformed line: {line!r}")
    timestamp, value_str = parts
    timestamp = timestamp.strip()
    if not timestamp:
        raise InvalidRecord(f"Missing timestamp in line: {line!r}")
    try:
        value = float(value_str)
    except ValueError as exc:
        raise InvalidRecord(f"Non-numeric value in line: {line!r}") from exc
    return timestamp, value


def process_readings(lines: Iterable[str]) -> Iterator[tuple[str, float]]:
    """Lazily parse lines into (timestamp, value) pairs, skipping invalid ones."""
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        try:
            yield parse_line(line)
        except InvalidRecord:
            continue


def running_average(readings: Iterable[tuple[str, float]]) -> Iterator[float]:
    """Lazily yield the running average of values as readings arrive."""
    total = 0.0
    for count, (_, value) in enumerate(readings, start=1):
        total += value
        yield total / count