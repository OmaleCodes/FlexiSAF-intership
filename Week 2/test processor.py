import pytest

from src.processor import InvalidRecord, parse_line, process_readings, running_average


def test_parse_line_valid():
    assert parse_line("08:00,21.5") == ("08:00", 21.5)


def test_parse_line_invalid_raises():
    with pytest.raises(InvalidRecord):
        parse_line("not,a,valid,line")


def test_parse_line_missing_timestamp_raises():
    with pytest.raises(InvalidRecord):
        parse_line(",21.5")


def test_process_readings_skips_invalid_lines():
    lines = ["08:00,21.5", "bad-line", "08:01,22.0", ",23.0"]
    result = list(process_readings(lines))
    assert result == [("08:00", 21.5), ("08:01", 22.0)]


def test_process_readings_is_lazy_generator():
    gen = process_readings(["08:00,21.5"])
    assert hasattr(gen, "__next__")
    assert next(gen) == ("08:00", 21.5)


def test_running_average():
    readings = [("a", 10.0), ("b", 20.0), ("c", 30.0)]
    averages = list(running_average(readings))
    assert averages == [10.0, 15.0, 20.0]